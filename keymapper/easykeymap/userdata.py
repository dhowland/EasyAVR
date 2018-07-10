#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2018 David Howland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module contains code to load, save, and organize user save data."""

from pprint import pformat
from collections import namedtuple
import json

from .build import NUM_LAYERS, NUM_MACROS, NULL_SYMBOL, led_modes, led_assignments, num_led_layers


Map = namedtuple('Map', ['code', 'mode', 'tap', 'wmods'])
Opts = namedtuple('Opts', ['keyboard', 'media', 'nkro', 'mouse'])


class SaveFileException(Exception):
    """Raised when an error is encountered while working with an UserData object."""
    pass


class UserData:
    """UserData objects contain all the information that can be captured from the user
    in the keymapper GUI.  The open() and save() methods can be used to load/store the
    data to disk as JSON.
    """

    def __init__(self, configurations):
        self.configurations = configurations
        self.config = None
        self.path = None
        self.unique_id = None
        self.layout_mod = None
        self.keymap = None
        self.macros = None
        self.led_modes = None
        self.led_funcs = None
        self.led_layers = None
        self.usb_opts = None
        self.subscribers = {
            'keymap': [],
            'macros': [],
            'led_modes': [],
            'led_funcs': [],
            'led_layers': [],
            'usb_opts': [],
        }

    def new(self, unique_id, layout_mod):
        """Create a new set of keymap data with default values."""
        try:
            self.config = self.configurations[unique_id]
        except KeyError:
            raise SaveFileException("Invalid save file: unsupported unique_id " + unique_id) from None
        self.path = None
        self.unique_id = unique_id
        self.layout_mod = layout_mod
        unassigned = Map(NULL_SYMBOL, 0, NULL_SYMBOL, 0)
        self.keymap = [[[unassigned] * self.config.num_cols
                        for _ in range(self.config.num_rows)]
                       for _ in range(NUM_LAYERS)]
        self.macros = [''] * NUM_MACROS
        self.led_modes = [0] * self.config.num_ind
        self.led_funcs = [(255, 0)] * len(led_assignments)
        self.led_layers = [0] * num_led_layers
        if self.config.firmware.simple:
            self.usb_opts = Opts(True, True, False, False)
        else:
            self.usb_opts = Opts(True, True, True, True)
        self._default_map()
        return self

    def _default_map(self):
        # default key map
        for i, rowdef in enumerate(self.config.keyboard_definition):
            if isinstance(rowdef, list):
                for j, keydef in enumerate(rowdef):
                    keydim, matrix, defaults = keydef
                    if self.layout_mod:
                        mod_map = self.config.alt_layouts[self.layout_mod]
                        keydim = mod_map.get((i, j), keydim)
                    if isinstance(keydim, tuple) and isinstance(matrix, tuple):
                        if isinstance(defaults, str):
                            defaults = [defaults]
                        for layer, scancode in enumerate(defaults):
                            row, col = matrix
                            self.keymap[layer][row][col] = Map(scancode, 0, NULL_SYMBOL, 0)
        # default led map
        for i, led_def in enumerate(self.config.led_definition):
            _, assignment = led_def
            if assignment in led_modes:
                self.led_modes[i] = led_modes.index(assignment)
            if assignment in led_assignments:
                self.led_modes[i] = led_modes.index('Indicator')
                fn_id = led_assignments.index(assignment)
                self.led_funcs[fn_id] = (i, 0)

    def open(self, path):
        """Load keymap data from a JSON file located at `path`."""
        with open(path, 'r') as fdin:
            data = json.load(fdin)
        # first make sure this looks like a save file
        if not isinstance(data, dict):
            raise SaveFileException("Invalid save file: unexpected JSON data")
        # get unique_id and layout_mod, which are absolutely required
        try:
            self.unique_id = self.check_unique_id(data['unique_id'])
            self.layout_mod = self.check_layout_mod(data['layout_mod'])
        except KeyError as err:
            raise SaveFileException("Invalid save file: missing property " + err.args[0])
        # set default settings for everything
        self.new(self.unique_id, self.layout_mod)
        # replace default settings with data from the save file
        if 'keymap' in data:
            self.keymap = self.check_keymap(data['keymap'])
        if 'macros' in data:
            self.macros = self.check_macros(data['macros'])
        if 'led_modes' in data:
            self.led_modes = self.check_led_modes(data['led_modes'])
        if 'led_funcs' in data:
            self.led_funcs = self.check_led_funcs(data['led_funcs'])
        if 'led_layers' in data:
            self.led_layers = self.check_led_layers(data['led_layers'])
        if 'usb_opts' in data:
            self.usb_opts = self.check_usb_opts(data['usb_opts'])
        # successful load, store the path
        self.path = path

    def save(self, path=None):
        """Save keymap data to a JSON file.  If `path` is specified, it overrides the
        internal path, and the internal path is updated.
        """
        if path is None:
            if self.path is None:
                raise SaveFileException("No filename specified")
        else:
            self.path = path
        data = {
            'unique_id': self.unique_id,
            'layout_mod': self.layout_mod,
            'keymap': self.keymap,
            'macros': self.macros,
            'led_modes': self.led_modes,
            'led_funcs': self.led_funcs,
            'led_layers': self.led_layers,
            'usb_opts': self.usb_opts,
        }
        with open(self.path, 'w') as fdout:
            json.dump(data, fdout)
            # json.dump(data, fdout, indent=2)

    def subscribe(self, announcefn, config_items=None):
        """This method adds `announcefn` to the subscriber list of each item in the
        `config_items` list.  If `config_items` is None, `announcefn` is added to all.
        announcfn should be a function or method that takes two arguments.  The first
        will be this UserData object, and the second will be the config item that
        was updated.
        """
        for conf_item, sub_list in self.subscribers.items():
            if (config_items is None) or (conf_item in config_items):
                sub_list.append(announcefn)

    def announce(self, config_item):
        """This method is called to indicate that the caller has finished updating
        `config_item` in this UserData object and all subscribers should be notified of
        the changes.
        """
        for announcefn in self.subscribers[config_item]:
            announcefn(self, config_item)

    def check_unique_id(self, data):
        """make sure unique_id exists"""
        if data not in self.configurations:
            raise SaveFileException("Invalid save file: unsupported unique_id " + data)
        return data

    def check_layout_mod(self, data):
        """make sure layout_mod is known if set"""
        if (data is not None) and (data not in self.configurations[self.unique_id].alt_layouts):
            raise SaveFileException("Invalid save file: unknown layout_mod " + data)
        return data

    def check_keymap(self, data):
        """check length of keymaps and convert from list to tuple"""
        unassigned = Map(NULL_SYMBOL, 0, NULL_SYMBOL, 0)
        fixed = []
        if isinstance(data, list) and (len(data) == NUM_LAYERS):
            for li, layer in enumerate(data):
                fixedlayer = []
                fixed.append(fixedlayer)
                if isinstance(layer, list) and (len(layer) == self.config.num_rows):
                    for ri, row in enumerate(layer):
                        fixedrow = []
                        fixedlayer.append(fixedrow)
                        if isinstance(row, list) and (len(row) == self.config.num_cols):
                            for ki, key in enumerate(row):
                                if isinstance(key, list) and (len(key) == 4):
                                    if key[0] == NULL_SYMBOL:
                                        fixedrow.append(unassigned)
                                    else:
                                        fixedrow.append(Map._make(key))
                                else:
                                    msg = ("Invalid save file: incorrect keymap key "
                                           "(layer {0} row {1} key {2} is not array "
                                           "of length {3})")
                                    msg = msg.format(li, ri, ki, 4)
                                    raise SaveFileException(msg)
                        else:
                            msg = ("Invalid save file: incorrect keymap row "
                                   "(layer {0} row {1} is not array of length {2})")
                            msg = msg.format(li, ri, self.config.num_cols)
                            raise SaveFileException(msg)
                else:
                    msg = ("Invalid save file: incorrect keymap layer "
                           "(layer {0} is not array of length {1})")
                    msg = msg.format(li, self.config.num_rows)
                    raise SaveFileException(msg)
        else:
            raise SaveFileException("Invalid save file: incorrect keymap")
        return fixed

    def check_macros(self, data):
        """check length of macros and extend if necessary"""
        if isinstance(data, list) and (len(data) <= NUM_MACROS):
            for macro in data:
                if not isinstance(macro, str):
                    raise SaveFileException("Invalid save file: incorrect macro type")
            if len(data) < NUM_MACROS:
                tmp = [""] * (NUM_MACROS - len(data))
                data.extend(tmp)
            return data
        else:
            raise SaveFileException("Invalid save file: incorrect macros")

    def check_led_modes(self, data):
        """check length and values for led_modes"""
        if isinstance(data, list) and (len(data) == self.config.num_ind):
            for n in data:
                if n >= len(led_modes):
                    raise SaveFileException("Invalid save file: incorrect led_modes value")
            return data
        else:
            raise SaveFileException("Invalid save file: incorrect led_modes")

    def check_led_funcs(self, data):
        """check length and values for led_funcs and convert from list to tuple"""
        if isinstance(data, list) and (len(data) <= len(led_assignments)):
            fixed = []
            for kmap in data:
                if isinstance(kmap, list) and (len(kmap) == 2):
                    if (kmap[0] > 255) or (kmap[1] > 10):
                        raise SaveFileException("Invalid save file: incorrect leds value")
                    fixed.append(tuple(kmap))
                else:
                    raise SaveFileException("Invalid save file: incorrect leds value")
            while len(fixed) < len(led_assignments):
                fixed.append((255, 0))
            return fixed
        else:
            raise SaveFileException("Invalid save file: incorrect leds")

    def check_led_layers(self, data):
        """check length and values for led_layers"""
        if isinstance(data, list) and (len(data) == num_led_layers):
            for n in data:
                if n >= NUM_LAYERS:
                    raise SaveFileException("Invalid save file: incorrect led_layers value")
            return data
        else:
            raise SaveFileException("Invalid save file: incorrect led_layers")

    def check_usb_opts(self, data):
        """check length and convert from list to tuple"""
        if isinstance(data, list) and (len(data) == 4):
            return Opts._make([bool(x) for x in data])
        else:
            raise SaveFileException("Invalid save file: incorrect usb_opts")

    def __str__(self):
        return pformat(self.__dict__)

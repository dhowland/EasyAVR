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

"""This module contains code to load legacy user save data."""

import pickle
import re

from .build import NUM_MACROS, NULL_SYMBOL, key_mode_map, led_modes, led_assignments
from .scancodes import scancodes
from .userdata import Map


legacy_layers = ["Default", "Layer 1", "Layer 2", "Layer 3", "Layer 4",
                 "Layer 5", "Layer 6", "Layer 7", "Layer 8", "Layer 9"]


class LegacySaveFileException(Exception):
    """Raised when an error is encountered while loading a legacy layout file."""
    pass


def load_legacy(user_data, datfile):
    """Load the legacy .dat save file from the path given by `datfile` and populate
    the UserData object given by `user_data`.
    """
    legacy_data = open_legacy(datfile)
    convert_legacy(user_data, legacy_data)


def open_legacy(datfile):
    """Opens and decodes the pickled data in a legacy .dat save file.  `datfile`
    is a path to the file.  The function returns a dictionary with an item for each
    component of the legacy file.
    """
    with open(datfile, 'rb') as fdin:
        data = pickle.load(fdin)
        if len(data) < 12:
            raise LegacySaveFileException("The .dat file is either broken or too old.")
        unique_id = data[1]
        maps = data[2]
        macros = data[3]
        actions = data[4]
        modes = data[5]
        wmods = data[6]
        layout_mod = data[8]
        leds = data[9]
        if len(data) > 11:
            advancedleds = data[11]
            useadvancedleds = data[12]
        else:
            advancedleds = [(255, 0)] * len(led_assignments)
            useadvancedleds = False
        if len(data) > 13:
            ledlayers = data[13]
        else:
            ledlayers = [0, 0, 0, 0, 0]
    # fixes for older versions (renamed layers)
    for kmap in (maps, actions, modes, wmods):
        if 'Fn' in kmap:
            kmap['Layer 1'] = kmap['Fn']
            del kmap['Fn']
    # fixes for older versions (renamed/removed scancodes)
    for layer in maps:
        for row in maps[layer]:
            for i, k in enumerate(row):
                if k == "SCANCODE_DEBUG":
                    row[i] = "SCANCODE_CONFIG"
                elif k == "SCANCODE_LOCKINGCAPS":
                    row[i] = "HID_KEYBOARD_SC_LOCKING_CAPS_LOCK"
                elif k == "SCANCODE_FN":
                    row[i] = "SCANCODE_FN1"
                elif k not in scancodes:
                    row[i] = NULL_SYMBOL
    # fixes for older versions (renamed leds)
    leds = ['Any Fn Active' if (x == 'Fn Lock') else x for x in leds]
    leds = ['Fn1 Active' if (x == 'Fn Active') else x for x in leds]
    # fixes for older versions (added macros)
    extention = NUM_MACROS - len(macros)
    if extention > 0:
        macros.extend([''] * extention)

    return {
        'unique_id': unique_id,
        'layout_mod': layout_mod,
        'maps': maps,
        'actions': actions,
        'modes': modes,
        'wmods': wmods,
        'macros': macros,
        'leds': leds,
        'advancedleds': advancedleds,
        'useadvancedleds': useadvancedleds,
        'ledlayers': ledlayers,
    }


def convert_legacy(user_data, legacy_data):
    """Converts the data from a legacy save file into a `user_data` object.  `user_data`
    should be a fresh instance of UserData and `legacy_data` is the output from a
    successful call to open_legacy().
    """
    # can't save to legacy file
    user_data.path = None
    # get good defaults to start from
    user_data.new(legacy_data['unique_id'], legacy_data['layout_mod'])
    # transmogrify the keymap data
    for li, layer in enumerate(legacy_layers):
        for ri, rowdef in enumerate(user_data.config.keyboard_definition):
            if isinstance(rowdef, int):
                continue
            for ci, keydef in enumerate(rowdef):
                keydim, matrix, _ = keydef
                if user_data.layout_mod:
                        mod_map = user_data.config.alt_layouts[user_data.layout_mod]
                        keydim = mod_map.get((ri, ci), keydim)
                if isinstance(keydim, tuple) and isinstance(matrix, tuple):
                    row, col = matrix
                    map = Map(legacy_data['maps'][layer][ri][ci],
                              key_mode_map[legacy_data['modes'][layer][ri][ci]],
                              legacy_data['actions'][layer][ri][ci],
                              legacy_data['wmods'][layer][ri][ci])
                    user_data.keymap[li][row][col] = map
    # translate the macro data
    user_data.macros = [translate_macro(macro) for macro in legacy_data['macros']]
    # adapt the led data
    user_data.led_modes = []
    for old_assignment in legacy_data['leds']:
        if old_assignment == 'Backlight':
            user_data.led_modes.append(led_modes.index('Backlight'))
        elif old_assignment in led_assignments:
            user_data.led_modes.append(led_modes.index('Indicator'))
        else:
            user_data.led_modes.append(led_modes.index('Disabled'))
    if legacy_data['useadvancedleds']:
        for i, func in enumerate(legacy_data['advancedleds']):
            led_id, _ = func
            if led_id < len(user_data.led_modes):
                user_data.led_modes[led_id] = led_modes.index('Indicator')
            user_data.led_funcs[i] = func
    # copy the rest
    user_data.led_layers = legacy_data['ledlayers']


def translate_macro(input):
    """Translate the escape sequences in the original macro mini-language into
    the equivalent representations in the new macro mini-language.
    """
    # remove the special characters
    input = input.replace("\\\\,", "\\")
    input = input.replace("\\n,", "\n")
    input = input.replace("\\t,", "\t")
    # escape any $ symbols
    input = input.replace("$", "$$")
    # convert keyword format
    input = re.sub(r'\\([A-Z0-9_]+\()', r'$\1', input)
    # convert function/mod format
    input = re.sub(r'\\([A-Z0-9_]+),', r'${\1}', input)
    return input

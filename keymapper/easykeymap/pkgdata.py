#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2017 David Howland
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

"""Functions for locating associated program data.  The program may be run from
source, as a python package, or as a frozen executable.  This code is designed
to find auxiliary files in all three situations.
"""

from glob import glob
import importlib
import os.path
import pkgutil
import sys

from .templates import max_leds, max_indicators, max_bl_enables, matrix_dims, num_ports
import easykeymap.boards as boards
import easykeymap.cfgparse as cfgparse

if not hasattr(sys, 'frozen'):
    import pkg_resources


class BoardConfigException(Exception):
    pass


def get_pkg_path(path):
    """Get the real path to a file at the given `path` relative to the
    easykeymap package.
    """
    if hasattr(sys, 'frozen'):
        return os.path.join(os.path.dirname(sys.executable), path)
    else:
        return pkg_resources.resource_filename(__name__, path)


def check_user_dir(subdir):
    userdir = os.path.join(os.path.expanduser('~'), '.EasyAVR')
    usersubdir = os.path.join(userdir, subdir)
    for loc in [userdir, usersubdir]:
        if not os.path.exists(loc):
            os.mkdir(loc)
    return usersubdir


def get_user_boards_dir():
    return check_user_dir('boards')


def get_user_configs_dir():
    return check_user_dir('configs')


def import_pkg_boards(configurations, errors):
    """Finds all the keyboard configs in the easykeymap.boards package, imports
    them, and adds a mapping of unique ID to module references to the
    `configurations` dict.
    """
    for _, modpath, _ in pkgutil.iter_modules(boards.__path__):
        mod = importlib.import_module('.boards.' + modpath, 'easykeymap')
        try:
            verify_board_config(mod)
        except BoardConfigException as err:
            errors.append(err)
            continue
        configurations[mod.unique_id] = mod


def import_user_boards(configurations, errors):
    """Finds all the keyboard configs in the user's config directory, imports
    them, and adds a mapping of unique ID to module references to the
    `configurations` dict.
    """
    userboards = get_user_boards_dir()
    sys.path.append(userboards)
    for path in glob(os.path.join(userboards, '*.py')):
        board = os.path.splitext(os.path.basename(path))[0]
        mod = importlib.import_module(board)
        try:
            verify_board_config(mod)
        except BoardConfigException as err:
            errors.append(err)
            continue
        configurations[mod.unique_id] = mod


def load_layouts(configurations, errors):
    """Finds layout mod configs, if they exist, for each board config.  Looks
    in both the easykeymap package and the user's config directory.  If a match
    is found in both locations, the user's config directory takes precedence.
    It is not necessary for every board config to receive a layout mod.
    """
    userconfigs = get_user_configs_dir()
    for config in configurations.values():
        cfg_file = "%s.cfg" % config.cfg_name
        cfg_path = os.path.join(userconfigs, cfg_file)
        # allow user configs to override built-in configs
        if not os.path.exists(cfg_path):
            try:
                cfg_path = get_pkg_path('configs/' + cfg_file)
            except KeyError:
                continue
        # have to check again because above will always succeed if running from source
        config.alt_layouts = {}
        if os.path.exists(cfg_path):
            try:
                config.alt_layouts = cfgparse.parse(cfg_path)
            except Exception as err:
                msg = "Error loading layout config: " + str(err)
                tb = sys.exc_info()[2]
                new_err = BoardConfigException(msg).with_traceback(tb)
                errors.append(new_err)


def import_boards():
    """This function will collect all the keyboard configs from both the user's
    home directory and the easykeymap package, with all layout mods included.
    Returns a map of unique IDs to modules, and a list of all the errors
    encountered.
    """
    configurations = {}
    errors = []
    import_pkg_boards(configurations, errors)
    import_user_boards(configurations, errors)
    load_layouts(configurations, errors)
    return (configurations, errors)


def verify_board_config(mod):
    """Check an imported board config module for validity and internal
    consistency.  This function returns nothing.  Invalid boards will raise an
    exception.  This function also adds display_height and display_width to
    the module as a convenience.
    """
    pre_msg = ("Error loading keyboard definition '" + os.path.basename(mod.__file__) + "':  ")

    # first check that all the required attributes are present in the module
    required_board_attributes = [
        'firmware', 'description', 'unique_id', 'cfg_name', 'teensy', 'hw_boot_key', 'num_rows',
        'num_cols', 'strobe_cols', 'strobe_low', 'matrix_hardware', 'matrix_strobe', 'matrix_sense',
        'num_leds', 'num_ind', 'num_bl_enab', 'led_definition', 'led_hardware', 'backlighting',
        'bl_modes', 'KMAC_key', 'keyboard_definition'
    ]
    for attr in required_board_attributes:
        if attr not in dir(mod):
            msg = (pre_msg + "It is missing the '" + attr + "' attribute.")
            raise BoardConfigException(msg)

    # check that num_rows and num_cols fit in firmware
    max_rows, max_cols = matrix_dims[mod.firmware.size]
    if (mod.num_rows > max_rows) or (mod.num_cols > max_cols):
        msg = (pre_msg + "(num_rows, num_cols) must fit in " + repr((max_rows, max_cols)) +
               " for the " + mod.firmware.size + " firmware.")
        raise BoardConfigException(msg)

    # check that num_rows and num_cols are not zero
    if (mod.num_rows == 0) or (mod.num_cols == 0):
        msg = (pre_msg + "num_rows/num_cols must not be zero.")
        raise BoardConfigException(msg)

    # check that len(matrix_hardware) matches the firmware
    _num_ports = num_ports[mod.firmware.device]
    if len(mod.matrix_hardware) != _num_ports:
        msg = (pre_msg + "matrix_hardware should list " + repr(_num_ports) +
               " for the " + mod.firmware.device + " firmware.")
        raise BoardConfigException(msg)

    # check that len(matrix_strobe) equals num_rows or num_cols depending on strobe_cols
    num_strobe = mod.num_cols if mod.strobe_cols else mod.num_rows
    if len(mod.matrix_strobe) != num_strobe:
        if (len(mod.matrix_strobe) == 0) and (num_strobe == 1):
            pass  # we can ignore this special case
        else:
            msg = (pre_msg + "The length of matrix_strobe should be " + repr(num_strobe) +
                   " based on num_rows/num_cols and strobe_cols.")
            raise BoardConfigException(msg)

    # check that len(matrix_strobe[i]) equals firmware.num_ports
    for strobe in mod.matrix_strobe:
        if len(strobe) != _num_ports:
            msg = (pre_msg + "matrix_strobe should contain tuples of length " + repr(_num_ports) +
                   " for the " + mod.firmware.device + " firmware.")
            raise BoardConfigException(msg)

    # check that len(matrix_sense) equals num_rows or num_cols depending on strobe_cols
    num_sense = mod.num_rows if mod.strobe_cols else mod.num_cols
    if len(mod.matrix_sense) != num_sense:
        msg = (pre_msg + "The length of matrix_sense should be " + repr(num_sense) +
               " based on num_rows/num_cols and strobe_cols.")
        raise BoardConfigException(msg)

    # check that num_leds <= max_leds
    if mod.num_leds > max_leds:
        msg = (pre_msg + "num_leds must be at most " + repr(max_leds) + " .")
        raise BoardConfigException(msg)

    # check that num_ind <= max_indicators
    if mod.num_ind > max_indicators:
        msg = (pre_msg + "num_ind must be at most " + repr(max_indicators) + " .")
        raise BoardConfigException(msg)

    # check that num_ind <= num_leds
    if mod.num_ind > mod.num_leds:
        msg = (pre_msg + "num_ind must be less than or equal to num_leds.")
        raise BoardConfigException(msg)

    # check that num_bl_enab <= max_bl_enables
    if mod.num_bl_enab > max_bl_enables:
        msg = (pre_msg + "num_bl_enab must be at most " + repr(max_bl_enables) + " .")
        raise BoardConfigException(msg)

    # check that len(led_definition) equals num_ind
    if len(mod.led_definition) != mod.num_ind:
        msg = (pre_msg + "The length of led_definition must equal num_ind.")
        raise BoardConfigException(msg)

    # check that len(led_hardware) equals num_leds
    if len(mod.led_hardware) != mod.num_leds:
        msg = (pre_msg + "The length of led_hardware must equal num_leds.")
        raise BoardConfigException(msg)

    if mod.backlighting:
        # check that there are backlight LEDs (num_leds > num_ind)
        # if not (mod.num_leds > mod.num_ind):
            # msg = (pre_msg + "backlighting should only be True if num_leds is "
                   # "greater than num_ind.")
            # raise BoardConfigException(msg)

        # check that len(bl_modes) equals num_bl_enab
        if len(mod.bl_modes) != mod.num_bl_enab:
            msg = (pre_msg + "The length of bl_modes must equal num_bl_enab.")
            raise BoardConfigException(msg)

        # check that len(bl_modes[i]) equals num_leds
        for bl_mode in mod.bl_modes:
            if len(bl_mode) != mod.num_leds:
                msg = (pre_msg + "The length of each item in bl_modes must equal num_leds.")
                raise BoardConfigException(msg)

    # check that every (row,col) in keyboard_definition fit in num_rows and num_cols
    display_height = 0
    display_width = 0
    for rowdef in mod.keyboard_definition:
        if isinstance(rowdef, list):
            row_width = 0
            for keydef in rowdef:
                keydim, matrix, _ = keydef
                if isinstance(keydim, tuple) and isinstance(matrix, tuple):
                    width, height = keydim
                    row_width += width
                    row, col = matrix
                    if (row >= mod.num_rows) or (col >= mod.num_cols):
                        msg = (pre_msg + "keyboard_definition contains a key with matrix location " +
                               repr((row, col)) + " which does not fit into (num_rows, num_cols).")
                        raise BoardConfigException(msg)
                else:
                    row_width += keydim
            if row_width > display_width:
                display_width = row_width
            display_height += 4
        else:
            display_height += rowdef

    # save the calculated display width and height for easy access later
    mod.display_height = display_height
    mod.display_width = display_width

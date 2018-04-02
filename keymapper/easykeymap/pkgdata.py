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
import traceback

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


def import_pkg_boards():
    """Finds all the keyboard configs in the easykeymap.boards package, imports
    them, and returns a dict mapping unique ID to module references."""
    configurations = {}
    for _, modpath, _ in pkgutil.iter_modules(boards.__path__):
        mod = importlib.import_module('.boards.' + modpath, 'easykeymap')
        configurations[mod.unique_id] = mod
    return configurations


def import_user_boards():
    configurations = {}
    userboards = get_user_boards_dir()
    sys.path.append(userboards)
    for file in glob(os.path.join(userboards, '*.py')):
        board = os.path.splitext(os.path.basename(file))[0]
        mod = importlib.import_module(board)
        for attr in boards.required_board_attributes:
            if attr not in dir(mod):
                msg = ("Error loading user board definition '" +
                       board + "'.  It is missing the '" + attr +
                       "' attribute.")
                raise BoardConfigException(msg)
        else:
            configurations[mod.unique_id] = mod
    return configurations


def loadlayouts(configurations):
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
        if os.path.exists(cfg_path):
            try:
                config.alt_layouts = cfgparse.parse(cfg_path)
            except Exception as err:
                msg = 'Error: ' + traceback.format_exc()
                raise BoardConfigException(msg)


def import_boards():
    """This function will collect all the keyboard configs from both the user's
    home directory and the easykeymap package, with all layout mods included.
    Returns a map of unique IDs to modules.
    """
    configurations = {}
    configurations.update(import_pkg_boards())
    configurations.update(import_user_boards())
    loadlayouts(configurations)
    return configurations

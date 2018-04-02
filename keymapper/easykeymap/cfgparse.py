#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2013-2016 David Howland
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

"""This module contains code to parse EasyAVR layout modification .cfg files.
The .cfg files are similar to ini files, but contain a very restrictive syntax
consisting of only headers and three functions.
"""

import re


regex_header = re.compile(r"^\[(.+)\]$")
regex_command = re.compile(r"^(MAKE_[SPACERKYBLN]+)\(([ ,\d-]+)\)$")


def parse(cfg_path):
    """Parse the file at `cfg_path` as a layout mod .cfg file.  It returns
    a map of (row, col) coordinates to (width, height) or width attributes.
    """
    cfg = {}
    with open(cfg_path, 'r') as infd:
        mod_map = {}
        mod_name = None
        for i, line in enumerate(infd):
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            m = regex_header.match(line)
            if m:
                if mod_name:
                    cfg[mod_name] = mod_map
                mod_name = m.group(1)
                mod_map = {}
                continue
            m = regex_command.match(line)
            if m:
                try:
                    args = m.group(2).split(',')
                    if m.group(1) == "MAKE_KEY":
                        row = int(args[0].strip())
                        col = int(args[1].strip())
                        width = int(args[2].strip())
                        height = int(args[3].strip())
                        mod_map[(row, col)] = (width, height)
                    elif m.group(1) == "MAKE_SPACER":
                        row = int(args[0].strip())
                        col = int(args[1].strip())
                        width = int(args[2].strip())
                        mod_map[(row, col)] = width
                    elif m.group(1) == "MAKE_BLANK":
                        row = int(args[0].strip())
                        col = int(args[1].strip())
                        width = int(args[2].strip()) * -1
                        mod_map[(row, col)] = width
                    else:
                        raise Exception("%s:%d: invalid command %s" %
                                        (cfg_path, i, m.group(1)))
                except IndexError:
                    raise Exception("%s:%d: Not enough arguments" %
                                    (cfg_path, i))
                except ValueError:
                    raise Exception("%s:%d: Argument is not integer" %
                                    (cfg_path, i))
                continue
            raise Exception("%s:%d: Unrecognized: %s" %
                            (cfg_path, i, line))
        if mod_name:
            cfg[mod_name] = mod_map
    return cfg

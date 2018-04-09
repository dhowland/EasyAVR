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

"""The templates package holds information about different build configurations
of the firmware.
"""

max_leds = 16
max_indicators = 8
max_bl_enables = 16

matrix_dims = {
    'SQUARE': (12, 12),
    'JUMBO': (7, 24),
    'FULLSIZE': (6, 22),
    'COSTAR': (8, 18),
    'TKL': (6, 17),
    'SIXTY': (5, 15),
    'PAD': (6, 6),
    'CARD': (1, 6)
}

macro_lengths = {
    'AT90USB1286': (1024 * 4),
    'ATmega32U4': (1024 * 2),
    'ATmega32U2': (1024 * 2),
    'ATmega16U2': (512),
}

ram_macro_lengths = {
    'AT90USB1286': 160,
    'ATmega32U4': 80,
    'ATmega32U2': 40,
    'ATmega16U2': 0,
}

num_ports = {
    'AT90USB1286': 6,
    'ATmega32U4': 5,
    'ATmega32U2': 3,
    'ATmega16U2': 3,
}

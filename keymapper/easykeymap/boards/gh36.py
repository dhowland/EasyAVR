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

"""Keyboard definition for the GH36 custom keyboard."""

import easykeymap.templates.ATmega32U4_16MHz_TKL as firmware
from easykeymap.ioports import *

description = "GH36"
unique_id = "GH36_002"
cfg_name = "gh36"

teensy = True
hw_boot_key = False

num_rows = 6
num_cols = 12

strobe_cols = False
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b10001111 , 0b00000000 ),    # REF_PORTB
    ( 0b11000000 , 0b11000000 ),    # REF_PORTC
    ( 0b01001111 , 0b00001111 ),    # REF_PORTD
    ( 0b00000000 , 0b00000000 ),    # REF_PORTE
    ( 0b11110011 , 0b00000000 )     # REF_PORTF
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD    REF_PORTE   REF_PORTF
    ( 0b00000000 , 0b11000000 , 0b00001110 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b11000000 , 0b00001101 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b11000000 , 0b00001011 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b11000000 , 0b00000111 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b10000000 , 0b00001111 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b01000000 , 0b00001111 , 0b00000000, 0b00000000 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTF , (1 << 0) ),
    ( REF_PORTF , (1 << 1) ),
    ( REF_PORTF , (1 << 4) ),
    ( REF_PORTF , (1 << 5) ),
    ( REF_PORTF , (1 << 6) ),
    ( REF_PORTF , (1 << 7) ),
    ( REF_PORTB , (1 << 7) ),
    ( REF_PORTB , (1 << 3) ),
    ( REF_PORTB , (1 << 2) ),
    ( REF_PORTB , (1 << 1) ),
    ( REF_PORTB , (1 << 0) ),
    ( REF_PORTD , (1 << 6) )
]

num_leds = 4
num_ind = 3
num_bl_enab = 2

led_definition = [
    ('NUM Key', 'Num Lock'),
    ('CAPS Key', 'Backlight'),
    ('LED2', 'Backlight')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTB, 4, LED_DRIVER_PULLUP ),
    ( REF_PORTB, 5, LED_DRIVER_PULLUP ),
    ( REF_PORTB, 6, LED_DRIVER_PULLUP ),
    ( REF_PORTD, 7, LED_DRIVER_PULLUP )
]

backlighting = True

bl_modes = [
    ( 1, 1, 1, 1 ),
    ( 0, 0, 0, 0 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 11), '0'),
     ((4, 4), (0, 10), '0'),
     ((4, 4), (0, 9), '0'),
     ((4, 4), (0, 8), '0'),
     ((4, 4), (0, 7), '0'),
     ((4, 4), (0, 6), '0'),
     (2, None, '0'),
     ((4, 4), (0, 0), '0'),
     ((4, 4), (0, 1), '0'),
     ((4, 4), (0, 2), '0'),
     ((4, 4), (0, 3), '0'),
     ((4, 4), (0, 4), '0'),
     ((4, 4), (0, 5), '0')],

    [((4, 4), (1, 11), '0'),
     ((4, 4), (1, 10), '0'),
     ((4, 4), (1, 9), '0'),
     ((4, 4), (1, 8), '0'),
     ((4, 4), (1, 7), '0'),
     ((4, 4), (1, 6), '0'),
     (2, None, '0'),
     ((4, 4), (1, 0), '0'),
     ((4, 4), (1, 1), '0'),
     ((4, 4), (1, 2), '0'),
     ((4, 4), (1, 3), '0'),
     ((4, 4), (1, 4), '0'),
     ((4, 4), (1, 5), '0')],

    [((4, 4), (2, 11), '0'),
     ((4, 4), (2, 10), '0'),
     ((4, 4), (2, 9), '0'),
     ((4, 4), (2, 8), '0'),
     ((4, 4), (2, 7), '0'),
     ((4, 4), (2, 6), '0'),
     (2, None, '0'),
     ((4, 4), (2, 0), '0'),
     ((4, 4), (2, 1), '0'),
     ((4, 4), (2, 2), '0'),
     ((4, 4), (2, 3), '0'),
     ((4, 4), (2, 4), '0'),
     ((4, 4), (2, 5), '0')],

    [((4, 4), (3, 11), '0'),
     ((4, 4), (3, 10), '0'),
     ((4, 4), (3, 9), '0'),
     ((4, 4), (3, 8), '0'),
     ((4, 4), (3, 7), '0'),
     ((4, 4), (3, 6), '0'),
     (2, None, '0'),
     ((4, 4), (3, 0), '0'),
     ((4, 4), (3, 1), '0'),
     ((4, 4), (3, 2), '0'),
     ((4, 4), (3, 3), '0'),
     ((4, 4), (3, 4), '0'),
     ((4, 4), (3, 5), '0')],

    [((4, 4), (4, 11), '0'),
     ((4, 4), (4, 10), '0'),
     ((4, 4), (4, 9), '0'),
     ((4, 4), (4, 8), '0'),
     ((4, 4), (4, 7), '0'),
     ((4, 4), (4, 6), '0'),
     (2, None, '0'),
     ((4, 4), (4, 0), '0'),
     ((4, 4), (4, 1), '0'),
     ((4, 4), (4, 2), '0'),
     ((4, 4), (4, 3), '0'),
     ((4, 4), (4, 4), '0'),
     ((4, 4), (4, 5), '0')],

    [((4, 4), (5, 11), '0'),
     ((4, 4), (5, 10), '0'),
     ((4, 4), (5, 9), '0'),
     ((4, 4), (5, 8), '0'),
     ((4, 4), (5, 7), '0'),
     ((4, 4), (5, 6), '0'),
     (2, None, '0'),
     ((4, 4), (5, 0), '0'),
     ((4, 4), (5, 1), '0'),
     ((4, 4), (5, 2), '0'),
     ((4, 4), (5, 3), '0'),
     ((4, 4), (5, 4), '0'),
     ((4, 4), (5, 5), '0')]
]

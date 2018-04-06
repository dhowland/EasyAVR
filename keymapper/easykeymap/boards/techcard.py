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

"""Keyboard definition for the Techkeys card."""

import easykeymap.templates.ATmega16U2_16MHz_CARD as firmware
from easykeymap.ioports import *

description = "Techkeys Card"
unique_id = "TECHCARD_001"
cfg_name = "techcard"

teensy = False
hw_boot_key = True

num_rows = 1
num_cols = 3

strobe_cols = False
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b11100001 , 0b00000001 ),    # REF_PORTB
    ( 0b00000000 , 0b00000000 ),    # REF_PORTC
    ( 0b00000000 , 0b00000000 )     # REF_PORTD
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD
    ( 0b00000000 , 0b00000000 , 0b00000000 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTB , 0b10000000 ),
    ( REF_PORTB , 0b01000000 ),
    ( REF_PORTB , 0b00100000 )
]

num_leds = 4
num_ind = 1
num_bl_enab = 2

led_definition = [
    ('Corner LED', 'Any Fn Active')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTB, 1, LED_DRIVER_PULLDOWN ),
    ( REF_PORTB, 2, LED_DRIVER_PULLDOWN ),
    ( REF_PORTB, 3, LED_DRIVER_PULLDOWN ),
    ( REF_PORTB, 4, LED_DRIVER_PULLDOWN )
]

backlighting = True

bl_modes = [
    ( 1, 1, 1, 1 ),
    ( 0, 0, 0, 0 )
]

KMAC_key = None

keyboard_definition = [
    [(4, None, '0'),
     ((4, 4), (0, 0), 'SCANCODE_BROWSER'),
     ((4, 4), (0, 1), 'SCANCODE_MAIL'),
     ((4, 4), (0, 2), 'SCANCODE_CALC')],

    [(4, None, '0'),
     (4, None, '0'),
     (4, None, '0'),
     (4, None, '0')]
]

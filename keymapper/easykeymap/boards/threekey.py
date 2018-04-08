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

"""Keyboard definition for the Techkeys ThreeKeyBoard."""

import easykeymap.templates.ATmega16U2_16MHz_CARD as firmware
from easykeymap.ioports import *

description = "Techkeys ThreeKeyBoard"
unique_id = "THREEKEY_001"
cfg_name = "threekey"

teensy = False
hw_boot_key = True

num_rows = 1
num_cols = 3

strobe_cols = False
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b10001110 , 0b10000000 ),    # REF_PORTB
    ( 0b00000000 , 0b00000000 ),    # REF_PORTC
    ( 0b00000000 , 0b00000000 )     # REF_PORTD
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD
    ( 0b00000000 , 0b00000000 , 0b00000000 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTB , 0b00001000 ),
    ( REF_PORTB , 0b00000010 ),
    ( REF_PORTB , 0b00000100 )
]

num_leds = 2
num_ind = 2
num_bl_enab = 2

led_definition = [
    ('Center Switch', 'Any Fn Active'),
    ('Backside', 'USB Normal')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTD, 3, LED_DRIVER_PULLDOWN ),
    ( REF_PORTD, 4, LED_DRIVER_PULLDOWN )
]

backlighting = False

bl_modes = [
    ( 1, 1 ),
    ( 0, 0 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), 'SCANCODE_BROWSER'),
     ((4, 4), (0, 1), 'SCANCODE_MAIL'),
     ((4, 4), (0, 2), 'SCANCODE_CALC')],

    [(4, None, '0'),
     (4, None, '0'),
     (4, None, '0')]
]

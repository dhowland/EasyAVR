# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2013-2018 David Howland
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

"""Keyboard definition for the Techkeys OneKeyBoard."""

import easykeymap.templates.ATmega16U2_16MHz_CARD as firmware
from easykeymap.ioports import *

description = "Techkeys OneKeyBoard"
unique_id = "ONEKEY_001"
cfg_name = "onekey"

teensy = False
hw_boot_key = True

num_rows = 1
num_cols = 1

strobe_cols = False
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b10000010 , 0b10000000 ),    # REF_PORTB
    ( 0b00000000 , 0b00000000 ),    # REF_PORTC
    ( 0b00000000 , 0b00000000 )     # REF_PORTD
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD
    ( 0b00000000 , 0b00000000 , 0b00000000 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTB , 0b00000010 ),
]

num_leds = 2
num_ind = 2
num_bl_enab = 2

led_definition = [
    ('Switch', 'Backlight'),
    ('Corner', 'USB Normal')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTD, 3, LED_DRIVER_PULLDOWN ),
    ( REF_PORTD, 4, LED_DRIVER_PULLDOWN )
]

backlighting = True

bl_modes = [
    ( 1, 1 ),
    ( 0, 0 )
]

KMAC_key = None

keyboard_definition = [
    2,

    [(2, None, '0'),
     ((4, 4), (0, 0), 'SCANCODE_BROWSER'),
     (2, None, '0')],

    2
]

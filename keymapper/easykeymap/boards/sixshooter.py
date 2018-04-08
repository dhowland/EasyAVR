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

"""Keyboard definition for the CM Storm switch tester."""

import easykeymap.templates.ATmega32U4_16MHz_CARD as firmware
from easykeymap.ioports import *

description = "CM Tester (SixShooter)"
unique_id = "SIXSHOOTER_001"
cfg_name = "sixshooter"

teensy = True
hw_boot_key = True

num_rows = 1
num_cols = 6

strobe_cols = False
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b00000001 , 0b00000001 ),    # REF_PORTB
    ( 0b00000000 , 0b00000000 ),    # REF_PORTC
    ( 0b00000000 , 0b00000000 ),    # REF_PORTD
    ( 0b00000000 , 0b00000000 ),    # REF_PORTE
    ( 0b11110011 , 0b00000000 )     # REF_PORTF
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD   REF_PORTE   REF_PORTF
    ( 0b00000000 , 0b00000000 , 0b00000000, 0b00000000, 0b00000000 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTF , (1 << 1) ),
    ( REF_PORTF , (1 << 6) ),
    ( REF_PORTF , (1 << 7) ),
    ( REF_PORTF , (1 << 0) ),
    ( REF_PORTF , (1 << 4) ),
    ( REF_PORTF , (1 << 5) )
]

num_leds = 6
num_ind = 6
num_bl_enab = 2

led_definition = [
    ('Top Left', 'Backlight'),
    ('Top Middle', 'Backlight'),
    ('Top Right', 'Backlight'),
    ('Bottom Left', 'Backlight'),
    ('Bottom Middle', 'Backlight'),
    ('Bottom Right', 'Backlight')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTB, 6, LED_DRIVER_PULLUP ),
    ( REF_PORTC, 7, LED_DRIVER_PULLUP ),
    ( REF_PORTD, 0, LED_DRIVER_PULLUP ),
    ( REF_PORTB, 5, LED_DRIVER_PULLUP ),
    ( REF_PORTD, 7, LED_DRIVER_PULLUP ),
    ( REF_PORTB, 7, LED_DRIVER_PULLUP )
]

backlighting = True

bl_modes = [
    ( 1, 1, 1, 1, 1, 1 ),
    ( 0, 0, 0, 0, 0, 0 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 2), 'SCANCODE_MUTE'),
     ((4, 4), (0, 1), 'SCANCODE_VOL_DEC'),
     ((4, 4), (0, 0), 'SCANCODE_VOL_INC')],

    [((4, 4), (0, 5), 'SCANCODE_PREV_TRACK'),
     ((4, 4), (0, 4), 'SCANCODE_PLAY_PAUSE'),
     ((4, 4), (0, 3), 'SCANCODE_NEXT_TRACK')],
]

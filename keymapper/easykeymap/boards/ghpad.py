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

"""Keyboard definition for the GHpad custom numpad."""

import easykeymap.templates.ATmega32U4_16MHz_PAD as firmware
from easykeymap.ioports import *

description = "GHpad"
unique_id = "GHPAD_001"
cfg_name = "ghpad"

teensy = False
hw_boot_key = False

num_rows = 6
num_cols = 4

strobe_cols = False
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b00000000 , 0b00000000 ),    # REF_PORTB
    ( 0b10000000 , 0b00000000 ),    # REF_PORTC
    ( 0b00111111 , 0b00111111 ),    # REF_PORTD
    ( 0b01000000 , 0b00000000 ),    # REF_PORTE
    ( 0b00000011 , 0b00000000 )     # REF_PORTF
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD    REF_PORTE   REF_PORTF
    ( 0b00000000 , 0b00000000 , 0b00111110 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b00000000 , 0b00111101 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b00000000 , 0b00111011 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b00000000 , 0b00110111 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b00000000 , 0b00101111 , 0b00000000, 0b00000000 ),
    ( 0b00000000 , 0b00000000 , 0b00011111 , 0b00000000, 0b00000000 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTF , (1 << 0) ),
    ( REF_PORTF , (1 << 1) ),
    ( REF_PORTE , (1 << 6) ),
    ( REF_PORTC , (1 << 7) )
]

num_leds = 4
num_ind = 4
num_bl_enab = 2

led_definition = [
    ('Num Key', 'Num Lock'),
    ('Top 1', 'Any Fn Active'),
    ('Top 2', 'Unassigned'),
    ('Top 3', 'Unassigned')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTB, 2, LED_DRIVER_PULLDOWN ),
    ( REF_PORTF, 7, LED_DRIVER_PULLDOWN ),
    ( REF_PORTF, 6, LED_DRIVER_PULLDOWN ),
    ( REF_PORTF, 5, LED_DRIVER_PULLDOWN )
]

backlighting = False

bl_modes = [
    ( 0, 0, 0, 0 ),
    ( 1, 1, 1, 1 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), 'HID_KEYBOARD_SC_NUM_LOCK'),
     ((4, 4), (0, 1), 'HID_KEYBOARD_SC_KEYPAD_SLASH'),
     ((4, 4), (0, 2), 'HID_KEYBOARD_SC_KEYPAD_ASTERISK'),
     ((4, 4), (0, 3), 'HID_KEYBOARD_SC_KEYPAD_MINUS')],

    [((4, 4), (1, 0), 'HID_KEYBOARD_SC_KEYPAD_7_AND_HOME'),
     ((4, 4), (1, 1), 'HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW'),
     ((4, 4), (1, 2), 'HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP'),
     ((4, 4), (1, 3), 'HID_KEYBOARD_SC_KEYPAD_PLUS')],

    [((4, 4), (2, 0), 'HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW'),
     ((4, 4), (2, 1), 'HID_KEYBOARD_SC_KEYPAD_5'),
     ((4, 4), (2, 2), 'HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW'),
     ((4, 4), (2, 3), '0')],

    [((4, 4), (3, 0), 'HID_KEYBOARD_SC_KEYPAD_1_AND_END'),
     ((4, 4), (3, 1), 'HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW'),
     ((4, 4), (3, 2), 'HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN'),
     ((4, 4), (3, 3), 'HID_KEYBOARD_SC_KEYPAD_ENTER')],

    [((4, 4), (4, 0), 'HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT'),
     ((4, 4), (4, 1), 'HID_KEYBOARD_SC_UP_ARROW'),
     ((4, 4), (4, 2), 'HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE'),
     ((4, 4), (4, 3), '0')],

    [((4, 4), (5, 0), 'HID_KEYBOARD_SC_LEFT_ARROW'),
     ((4, 4), (5, 1), 'HID_KEYBOARD_SC_DOWN_ARROW'),
     ((4, 4), (5, 2), 'HID_KEYBOARD_SC_RIGHT_ARROW'),
     ((4, 4), (5, 3), 'SCANCODE_FN1')]
]

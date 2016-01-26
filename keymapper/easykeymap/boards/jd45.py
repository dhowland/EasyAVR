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

"""Keyboard definition for the JD45 custom keyboard."""

import easykeymap.templates.ATmega32U4_16MHz_SIXTY as firmware
from easykeymap.ioports import *

description = "JD45"
unique_id = "JD45_001"
cfg_name = "jd45"

teensy = True
hw_boot_key = False

display_height = int(4*4)
display_width = int(13*4)

num_rows = 4
num_cols = 12

strobe_cols = True
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b11111000 , 0b11111000 ),    # REF_PORTB
    ( 0b11000000 , 0b11000000 ),    # REF_PORTC
    ( 0b01001111 , 0b01001111 ),    # REF_PORTD
    ( 0b00000000 , 0b00000000 ),    # REF_PORTE
    ( 0b00110011 , 0b00000000 )     # REF_PORTF
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD    REF_PORTE    REF_PORTF
    ( 0b11110000 , 0b11000000 , 0b01001111 , 0b00000000 , 0b00000000 ),
    ( 0b01111000 , 0b11000000 , 0b01001111 , 0b00000000 , 0b00000000 ),
    ( 0b11111000 , 0b11000000 , 0b01001110 , 0b00000000 , 0b00000000 ),
    ( 0b11111000 , 0b11000000 , 0b01001101 , 0b00000000 , 0b00000000 ),
    ( 0b11111000 , 0b11000000 , 0b01001011 , 0b00000000 , 0b00000000 ),
    ( 0b11111000 , 0b11000000 , 0b01000111 , 0b00000000 , 0b00000000 ),
    ( 0b11111000 , 0b10000000 , 0b01001111 , 0b00000000 , 0b00000000 ),
    ( 0b11111000 , 0b01000000 , 0b01001111 , 0b00000000 , 0b00000000 ),
    ( 0b11011000 , 0b11000000 , 0b01001111 , 0b00000000 , 0b00000000 ),
    ( 0b11101000 , 0b11000000 , 0b01001111 , 0b00000000 , 0b00000000 ),
    ( 0b11111000 , 0b11000000 , 0b00001111 , 0b00000000 , 0b00000000 ),
    ( 0b10111000 , 0b11000000 , 0b01001111 , 0b00000000 , 0b00000000 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTF , (1 << 0) ),
    ( REF_PORTF , (1 << 1) ),
    ( REF_PORTF , (1 << 4) ),
    ( REF_PORTF , (1 << 5) )
]

num_leds = 1
num_ind = 1
num_bl_enab = 2

led_definition = [
    ('LED1', 'Backlight')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTD, 7, LED_DRIVER_PULLUP )
]

backlighting = False

bl_modes = [
    ( 0, ),
    ( 1, )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), 'HID_KEYBOARD_SC_TAB'),
     ((4, 4), (0, 1), 'HID_KEYBOARD_SC_Q'),
     ((4, 4), (0, 2), 'HID_KEYBOARD_SC_W'),
     ((4, 4), (0, 3), 'HID_KEYBOARD_SC_E'),
     ((4, 4), (0, 4), 'HID_KEYBOARD_SC_R'),
     ((4, 4), (0, 5), 'HID_KEYBOARD_SC_T'),
     ((4, 4), (0, 6), 'HID_KEYBOARD_SC_Y'),
     ((4, 4), (0, 7), 'HID_KEYBOARD_SC_U'),
     ((4, 4), (0, 8), 'HID_KEYBOARD_SC_I'),
     ((4, 4), (0, 9), 'HID_KEYBOARD_SC_O'),
     ((4, 4), (0, 10), 'HID_KEYBOARD_SC_P'),
     ((4, 4), (0, 11), 'HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE'),
     ((4, 4), (3, 11), 'HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE')],

    [((5, 4), (1, 0), 'HID_KEYBOARD_SC_CAPS_LOCK'),
     ((4, 4), (1, 1), 'HID_KEYBOARD_SC_A'),
     ((4, 4), (1, 2), 'HID_KEYBOARD_SC_S'),
     ((4, 4), (1, 3), 'HID_KEYBOARD_SC_D'),
     ((4, 4), (1, 4), 'HID_KEYBOARD_SC_F'),
     ((4, 4), (1, 5), 'HID_KEYBOARD_SC_G'),
     ((4, 4), (1, 6), 'HID_KEYBOARD_SC_H'),
     ((4, 4), (1, 7), 'HID_KEYBOARD_SC_J'),
     ((4, 4), (1, 8), 'HID_KEYBOARD_SC_K'),
     ((4, 4), (1, 9), 'HID_KEYBOARD_SC_L'),
     ((4, 4), (1, 10), 'HID_KEYBOARD_SC_SEMICOLON_AND_COLON'),
     ((7, 4), (1, 11), 'HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE')],

    [((7, 4), (2, 0), 'HID_KEYBOARD_SC_LEFT_SHIFT'),
     ((4, 4), (2, 1), 'HID_KEYBOARD_SC_Z'),
     ((4, 4), (2, 2), 'HID_KEYBOARD_SC_X'),
     ((4, 4), (2, 3), 'HID_KEYBOARD_SC_C'),
     ((4, 4), (2, 4), 'HID_KEYBOARD_SC_V'),
     ((4, 4), (2, 5), 'HID_KEYBOARD_SC_B'),
     ((4, 4), (2, 6), 'HID_KEYBOARD_SC_N'),
     ((4, 4), (2, 7), 'HID_KEYBOARD_SC_M'),
     ((4, 4), (2, 8), 'HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN'),
     ((4, 4), (2, 9), 'HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN'),
     ((4, 4), (2, 10), 'HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK'),
     ((5, 4), (2, 11), 'HID_KEYBOARD_SC_RIGHT_SHIFT')],

    [((5, 4), (3, 0), 'HID_KEYBOARD_SC_LEFT_CONTROL'),
     ((4, 4), (3, 1), 'SCANCODE_FN'),
     ((5, 4), (3, 2), 'HID_KEYBOARD_SC_LEFT_GUI'),
     ((5, 4), (3, 3), 'HID_KEYBOARD_SC_LEFT_ALT'),
     ((7, 4), (3, 4), 'HID_KEYBOARD_SC_SPACE'),
     ((7, 4), (3, 6), 'HID_KEYBOARD_SC_SPACE'),
     ((5, 4), (3, 7), 'HID_KEYBOARD_SC_RIGHT_ALT'),
     ((5, 4), (3, 8), 'HID_KEYBOARD_SC_APPLICATION'),
     ((4, 4), (3, 9), 'SCANCODE_FN2'),
     ((5, 4), (3, 10), 'HID_KEYBOARD_SC_RIGHT_CONTROL')]
]

alt_layouts = {}

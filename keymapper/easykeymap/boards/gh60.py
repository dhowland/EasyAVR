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

"""Keyboard definition for the GH60 custom keyboard."""

import easykeymap.templates.ATmega32U4_16MHz_SIXTY as firmware
from easykeymap.ioports import *

description = "GH60"
unique_id = "GH60_003"
cfg_name = "gh60revb"

teensy = False
hw_boot_key = False

display_height = int(5*4)
display_width = int(15*4)

num_rows = 5
num_cols = 14

strobe_cols = True
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b11111010 , 0b11111010 ),    # REF_PORTB
    ( 0b11000000 , 0b11000000 ),    # REF_PORTC
    ( 0b11111111 , 0b11010000 ),    # REF_PORTD
    ( 0b01000000 , 0b01000000 ),    # REF_PORTE
    ( 0b00000011 , 0b00000011 )     # REF_PORTF
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD    REF_PORTE   REF_PORTF
    ( 0b11111010 , 0b11000000 , 0b11010000 , 0b01000000 , 0b00000010 ),
    ( 0b11111010 , 0b11000000 , 0b11010000 , 0b01000000 , 0b00000001 ),
    ( 0b11111010 , 0b11000000 , 0b11010000 , 0b00000000 , 0b00000011 ),
    ( 0b11111010 , 0b01000000 , 0b11010000 , 0b01000000 , 0b00000011 ),
    ( 0b11111010 , 0b10000000 , 0b11010000 , 0b01000000 , 0b00000011 ),
    ( 0b10111010 , 0b11000000 , 0b11010000 , 0b01000000 , 0b00000011 ),
    ( 0b11111010 , 0b11000000 , 0b11000000 , 0b01000000 , 0b00000011 ),
    ( 0b11111000 , 0b11000000 , 0b11010000 , 0b01000000 , 0b00000011 ),
    ( 0b01111010 , 0b11000000 , 0b11010000 , 0b01000000 , 0b00000011 ),
    ( 0b11011010 , 0b11000000 , 0b11010000 , 0b01000000 , 0b00000011 ),
    ( 0b11101010 , 0b11000000 , 0b11010000 , 0b01000000 , 0b00000011 ),
    ( 0b11111010 , 0b11000000 , 0b01010000 , 0b01000000 , 0b00000011 ),
    ( 0b11111010 , 0b11000000 , 0b10010000 , 0b01000000 , 0b00000011 ),
    ( 0b11110010 , 0b11000000 , 0b11010000 , 0b01000000 , 0b00000011 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTD , (1 << 0) ),
    ( REF_PORTD , (1 << 1) ),
    ( REF_PORTD , (1 << 2) ),
    ( REF_PORTD , (1 << 3) ),
    ( REF_PORTD , (1 << 5) )
]

num_leds = 1
num_ind = 1
num_bl_enab = 2

led_definition = [
    ('Caps Key', 'Caps Lock')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTB, 2, LED_DRIVER_PULLDOWN )
]

backlighting = False

bl_modes = [
    ( 0 ),
    ( 1 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), 'HID_KEYBOARD_SC_ESCAPE'),
     ((4, 4), (0, 1), 'HID_KEYBOARD_SC_1_AND_EXCLAMATION'),
     ((4, 4), (0, 2), 'HID_KEYBOARD_SC_2_AND_AT'),
     ((4, 4), (0, 3), 'HID_KEYBOARD_SC_3_AND_HASHMARK'),
     ((4, 4), (0, 4), 'HID_KEYBOARD_SC_4_AND_DOLLAR'),
     ((4, 4), (0, 5), 'HID_KEYBOARD_SC_5_AND_PERCENTAGE'),
     ((4, 4), (0, 6), 'HID_KEYBOARD_SC_6_AND_CARET'),
     ((4, 4), (0, 7), 'HID_KEYBOARD_SC_7_AND_AND_AMPERSAND'),
     ((4, 4), (0, 8), 'HID_KEYBOARD_SC_8_AND_ASTERISK'),
     ((4, 4), (0, 9), 'HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS'),
     ((4, 4), (0, 10), 'HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS'),
     ((4, 4), (0, 11), 'HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE'),
     ((4, 4), (0, 12), 'HID_KEYBOARD_SC_EQUAL_AND_PLUS'),
     ((4, 4), (0, 13), 'HID_KEYBOARD_SC_BACKSPACE'),
     ((4, 4), (4, 9), '0')],

    [((6, 4), (1, 0), 'HID_KEYBOARD_SC_TAB'),
     ((4, 4), (1, 1), 'HID_KEYBOARD_SC_Q'),
     ((4, 4), (1, 2), 'HID_KEYBOARD_SC_W'),
     ((4, 4), (1, 3), 'HID_KEYBOARD_SC_E'),
     ((4, 4), (1, 4), 'HID_KEYBOARD_SC_R'),
     ((4, 4), (1, 5), 'HID_KEYBOARD_SC_T'),
     ((4, 4), (1, 6), 'HID_KEYBOARD_SC_Y'),
     ((4, 4), (1, 7), 'HID_KEYBOARD_SC_U'),
     ((4, 4), (1, 8), 'HID_KEYBOARD_SC_I'),
     ((4, 4), (1, 9), 'HID_KEYBOARD_SC_O'),
     ((4, 4), (1, 10), 'HID_KEYBOARD_SC_P'),
     ((4, 4), (1, 11), 'HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE'),
     ((4, 4), (1, 12), 'HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE'),
     ((6, 4), (1, 13), 'HID_KEYBOARD_SC_BACKSLASH_AND_PIPE')],

    [((7, 4), (2, 0), 'HID_KEYBOARD_SC_CAPS_LOCK'),
     ((4, 4), (2, 1), 'HID_KEYBOARD_SC_A'),
     ((4, 4), (2, 2), 'HID_KEYBOARD_SC_S'),
     ((4, 4), (2, 3), 'HID_KEYBOARD_SC_D'),
     ((4, 4), (2, 4), 'HID_KEYBOARD_SC_F'),
     ((4, 4), (2, 5), 'HID_KEYBOARD_SC_G'),
     ((4, 4), (2, 6), 'HID_KEYBOARD_SC_H'),
     ((4, 4), (2, 7), 'HID_KEYBOARD_SC_J'),
     ((4, 4), (2, 8), 'HID_KEYBOARD_SC_K'),
     ((4, 4), (2, 9), 'HID_KEYBOARD_SC_L'),
     ((4, 4), (2, 10), 'HID_KEYBOARD_SC_SEMICOLON_AND_COLON'),
     ((4, 4), (2, 11), 'HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE'),
     ((4, 4), (2, 12), '0'),
     ((5, 4), (2, 13), 'HID_KEYBOARD_SC_ENTER')],

    [((5, 4), (3, 0), 'HID_KEYBOARD_SC_LEFT_SHIFT'),
     ((4, 4), (3, 1), '0'),
     ((4, 4), (3, 2), 'HID_KEYBOARD_SC_Z'),
     ((4, 4), (3, 3), 'HID_KEYBOARD_SC_X'),
     ((4, 4), (3, 4), 'HID_KEYBOARD_SC_C'),
     ((4, 4), (3, 5), 'HID_KEYBOARD_SC_V'),
     ((4, 4), (3, 6), 'HID_KEYBOARD_SC_B'),
     ((4, 4), (3, 7), 'HID_KEYBOARD_SC_N'),
     ((4, 4), (3, 8), 'HID_KEYBOARD_SC_M'),
     ((4, 4), (3, 9), 'HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN'),
     ((4, 4), (3, 10), 'HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN'),
     ((4, 4), (3, 11), 'HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK'),
     ((7, 4), (3, 13), 'HID_KEYBOARD_SC_RIGHT_SHIFT'),
     ((4, 4), (3, 12), '0')],

    [((5, 4), (4, 0), 'HID_KEYBOARD_SC_LEFT_CONTROL'),
     ((5, 4), (4, 1), 'HID_KEYBOARD_SC_LEFT_GUI'),
     ((5, 4), (4, 2), 'HID_KEYBOARD_SC_LEFT_ALT'),
     ((25, 4), (4, 5), 'HID_KEYBOARD_SC_SPACE'),
     ((5, 4), (4, 10), 'HID_KEYBOARD_SC_RIGHT_ALT'),
     ((5, 4), (4, 11), 'HID_KEYBOARD_SC_RIGHT_GUI'),
     ((5, 4), (4, 12), 'HID_KEYBOARD_SC_APPLICATION'),
     ((5, 4), (4, 13), 'HID_KEYBOARD_SC_RIGHT_CONTROL')]
]

alt_layouts = {}

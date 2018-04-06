# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2017 David Howland
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

"""Keyboard definition for the XD60 custom keyboard."""

import easykeymap.templates.ATmega32U4_16MHz_SIXTY as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config

description = "XD60"
unique_id = "XD60_001"
cfg_name = "xd60"

teensy = False
hw_boot_key = False

num_rows = 5
num_cols = 14

strobe_cols = False
strobe_low = True

matrix_hardware, matrix_strobe, matrix_sense = make_matrix_config(
    strobe_cols=strobe_cols,
    strobe_low=strobe_low,
    rows=[D0, D1, D2, D3, D5],
    cols=[F0, F1, E6, C7, C6, B6, D4, B1, B7, B5, B4, D7, D6, B3],
    device=firmware.device
)

num_leds = 2
num_ind = 1
num_bl_enab = 2

led_definition = [
    ('Caps Key', 'Caps Lock'),
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTB, 2, LED_DRIVER_PULLDOWN ),
    ( REF_PORTF, 5, LED_DRIVER_PULLDOWN )
]

backlighting = True

bl_modes = [
    ( 1, 1 ),
    ( 0, 0 ),
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
     ((4, 4), (4, 9), 'HID_KEYBOARD_SC_DELETE')],

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
     ((4, 4), (2, 12), 'HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE'),
     ((5, 4), (2, 13), 'HID_KEYBOARD_SC_ENTER')],

    [((4, 4), (3, 0), 'HID_KEYBOARD_SC_LEFT_SHIFT'),
     ((4, 4), (3, 1), 'HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE'),
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
     ((4, 4), (4, 7), 'HID_KEYBOARD_SC_RIGHT_SHIFT'),
     ((4, 4), (3, 13), 'HID_KEYBOARD_SC_UP_ARROW'),
     ((4, 4), (3, 12), 'HID_KEYBOARD_SC_RIGHT_CONTROL')],

    [((5, 4), (4, 0), 'HID_KEYBOARD_SC_LEFT_CONTROL'),
     ((5, 4), (4, 1), 'HID_KEYBOARD_SC_LEFT_GUI'),
     ((5, 4), (4, 2), 'HID_KEYBOARD_SC_LEFT_ALT'),
     ((25, 4), (4, 5), 'HID_KEYBOARD_SC_SPACE'),
     ((4, 4), (4, 10), 'HID_KEYBOARD_SC_RIGHT_ALT'),
     ((4, 4), (4, 11), 'HID_KEYBOARD_SC_RIGHT_GUI'),
     ((4, 4), (4, 8), 'HID_KEYBOARD_SC_LEFT_ARROW'),
     ((4, 4), (4, 12), 'HID_KEYBOARD_SC_DOWN_ARROW'),
     ((4, 4), (4, 13), 'HID_KEYBOARD_SC_RIGHT_CONTROL')]
]

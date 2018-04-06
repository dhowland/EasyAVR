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

"""Keyboard definition for the Minorca custom keyboard."""

import easykeymap.templates.ATmega32U4_16MHz_SIXTY as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config

description = "Minorca (Switch Top)"
unique_id = "MINORCA_01"
cfg_name = "minorca"

teensy = True
hw_boot_key = True

num_rows = 4
num_cols = 12

strobe_cols = False
strobe_low = True

matrix_hardware, matrix_strobe, matrix_sense = make_matrix_config(
    strobe_cols=strobe_cols,
    strobe_low=strobe_low,
    rows=[F0, F1, F4, F5],
    cols=[B1, B2, B3, B7, D0, D1, D2, D3, C6, C7, F7, F6],
    device=firmware.device
)

num_leds = 0
num_ind = 0
num_bl_enab = 2

led_definition = []

led_hardware = []

backlighting = False

bl_modes = [
    ( 1, 1 ),
    ( 0, 0 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), ['HID_KEYBOARD_SC_ESCAPE', 'HID_KEYBOARD_SC_ESCAPE', 'HID_KEYBOARD_SC_ESCAPE']),
     ((4, 4), (0, 1), ['HID_KEYBOARD_SC_Q', 'HID_KEYBOARD_SC_1_AND_EXCLAMATION', 'HID_KEYBOARD_SC_Q']),
     ((4, 4), (0, 2), ['HID_KEYBOARD_SC_W', 'HID_KEYBOARD_SC_2_AND_AT', 'HID_KEYBOARD_SC_W']),
     ((4, 4), (0, 3), ['HID_KEYBOARD_SC_E', 'HID_KEYBOARD_SC_3_AND_HASHMARK', 'HID_KEYBOARD_SC_E']),
     ((4, 4), (0, 4), ['HID_KEYBOARD_SC_R', 'HID_KEYBOARD_SC_4_AND_DOLLAR', 'HID_KEYBOARD_SC_R']),
     ((4, 4), (0, 5), ['HID_KEYBOARD_SC_T', 'HID_KEYBOARD_SC_5_AND_PERCENTAGE', 'HID_KEYBOARD_SC_T']),
     ((4, 4), (0, 6), ['HID_KEYBOARD_SC_Y', 'HID_KEYBOARD_SC_6_AND_CARET', 'HID_KEYBOARD_SC_Y']),
     ((4, 4), (0, 7), ['HID_KEYBOARD_SC_U', 'HID_KEYBOARD_SC_7_AND_AND_AMPERSAND', 'HID_KEYBOARD_SC_U']),
     ((4, 4), (0, 8), ['HID_KEYBOARD_SC_I', 'HID_KEYBOARD_SC_8_AND_ASTERISK', 'HID_KEYBOARD_SC_I']),
     ((4, 4), (0, 9), ['HID_KEYBOARD_SC_O', 'HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS', 'HID_KEYBOARD_SC_O']),
     ((4, 4), (0, 10), ['HID_KEYBOARD_SC_P', 'HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE', 'HID_KEYBOARD_SC_P']),
     ((4, 4), (0, 11), ['HID_KEYBOARD_SC_BACKSPACE', 'HID_KEYBOARD_SC_DELETE', 'SCANCODE_BOOT'])],

    [((5, 4), (1, 0), ['HID_KEYBOARD_SC_TAB', 'HID_KEYBOARD_SC_TAB', 'HID_KEYBOARD_SC_TAB']),
     ((4, 4), (1, 1), ['HID_KEYBOARD_SC_A', 'HID_KEYBOARD_SC_4_AND_DOLLAR', 'HID_KEYBOARD_SC_A']),
     ((4, 4), (1, 2), ['HID_KEYBOARD_SC_S', 'HID_KEYBOARD_SC_5_AND_PERCENTAGE', 'HID_KEYBOARD_SC_S']),
     ((4, 4), (1, 3), ['HID_KEYBOARD_SC_D', 'HID_KEYBOARD_SC_6_AND_CARET', 'HID_KEYBOARD_SC_D']),
     ((4, 4), (1, 4), ['HID_KEYBOARD_SC_F', 'HID_KEYBOARD_SC_F', 'HID_KEYBOARD_SC_F']),
     ((4, 4), (1, 5), ['HID_KEYBOARD_SC_G', 'HID_KEYBOARD_SC_G', 'HID_KEYBOARD_SC_G']),
     ((4, 4), (1, 6), ['HID_KEYBOARD_SC_H', 'HID_KEYBOARD_SC_KEYPAD_MINUS', 'HID_KEYBOARD_SC_H']),
     ((4, 4), (1, 7), ['HID_KEYBOARD_SC_J', 'HID_KEYBOARD_SC_KEYPAD_PLUS', 'HID_KEYBOARD_SC_J']),
     ((4, 4), (1, 8), ['HID_KEYBOARD_SC_K', 'HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE', 'HID_KEYBOARD_SC_K']),
     ((4, 4), (1, 9), ['HID_KEYBOARD_SC_L', 'HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE', 'HID_KEYBOARD_SC_UP_ARROW']),
     ((7, 4), (1, 11), ['HID_KEYBOARD_SC_ENTER', 'HID_KEYBOARD_SC_ENTER', 'HID_KEYBOARD_SC_ENTER'])],

    [((7, 4), (2, 0), ['HID_KEYBOARD_SC_LEFT_SHIFT', 'HID_KEYBOARD_SC_LEFT_SHIFT', 'HID_KEYBOARD_SC_LEFT_SHIFT']),
     ((4, 4), (2, 2), ['HID_KEYBOARD_SC_Z', 'HID_KEYBOARD_SC_7_AND_AND_AMPERSAND', 'HID_KEYBOARD_SC_Z']),
     ((4, 4), (2, 3), ['HID_KEYBOARD_SC_X', 'HID_KEYBOARD_SC_8_AND_ASTERISK', 'HID_KEYBOARD_SC_X']),
     ((4, 4), (2, 4), ['HID_KEYBOARD_SC_C', 'HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS', 'HID_KEYBOARD_SC_C']),
     ((4, 4), (2, 5), ['HID_KEYBOARD_SC_V', 'HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS', 'HID_KEYBOARD_SC_V']),
     ((4, 4), (2, 6), ['HID_KEYBOARD_SC_B', 'HID_KEYBOARD_SC_B', 'HID_KEYBOARD_SC_B']),
     ((4, 4), (2, 7), ['HID_KEYBOARD_SC_N', 'HID_KEYBOARD_SC_SEMICOLON_AND_COLON', 'HID_KEYBOARD_SC_N']),
     ((4, 4), (2, 8), ['HID_KEYBOARD_SC_M', 'HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK', 'HID_KEYBOARD_SC_M']),
     ((4, 4), (2, 9), ['HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN', 'HID_KEYBOARD_SC_PAGE_UP', 'HID_KEYBOARD_SC_LEFT_ARROW']),
     ((5, 4), (2, 10), ['HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN', 'HID_KEYBOARD_SC_PAGE_DOWN', 'HID_KEYBOARD_SC_RIGHT_ARROW']),
     ((4, 4), (2, 11), ['HID_KEYBOARD_SC_RIGHT_SHIFT', 'HID_KEYBOARD_SC_RIGHT_SHIFT', 'HID_KEYBOARD_SC_RIGHT_SHIFT'])],

    [((5, 4), (3, 0), ['HID_KEYBOARD_SC_LEFT_CONTROL', 'HID_KEYBOARD_SC_LEFT_CONTROL', 'HID_KEYBOARD_SC_LEFT_CONTROL']),
     ((5, 4), (3, 2), ['HID_KEYBOARD_SC_LEFT_ALT', 'HID_KEYBOARD_SC_LEFT_ALT', 'HID_KEYBOARD_SC_LEFT_ALT']),
     ((5, 4), (3, 3), ['HID_KEYBOARD_SC_LEFT_GUI', 'HID_KEYBOARD_SC_LEFT_GUI', 'HID_KEYBOARD_SC_LEFT_GUI']),
     ((9, 4), (3, 4), ['HID_KEYBOARD_SC_BACKSPACE', 'HID_KEYBOARD_SC_BACKSPACE', 'HID_KEYBOARD_SC_BACKSPACE']),
     ((9, 4), (3, 7), ['HID_KEYBOARD_SC_SPACE', 'HID_KEYBOARD_SC_SPACE', 'HID_KEYBOARD_SC_SPACE']),
     ((5, 4), (3, 9), ['SCANCODE_FN2', 'SCANCODE_FN2', 'SCANCODE_FN2']),
     ((5, 4), (3, 10), ['HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE', 'HID_KEYBOARD_SC_END', 'HID_KEYBOARD_SC_DOWN_ARROW']),
     ((5, 4), (3, 11), ['SCANCODE_FN1', 'SCANCODE_FN1', 'SCANCODE_FN1'])]
]

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

"""Keyboard definition for the JD40 custom keyboard."""

import easykeymap.templates.ATmega32U4_16MHz_SIXTY as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config

description = "JD40 (Carpe keyboards)"
unique_id = "JD40_001"
cfg_name = "jd40"

teensy = False
hw_boot_key = True

num_rows = 4
num_cols = 12

strobe_cols = False
strobe_low = True

matrix_hardware, matrix_strobe, matrix_sense = make_matrix_config(
    strobe_cols=strobe_cols,
    strobe_low=strobe_low,
    rows=[F0, F1, F5, B4],
    cols=[F4, D7, B5, B6, C6, C7, D4, D6, D5, D0, D1, D2],
    device=firmware.device
)

num_leds = 2
num_ind = 1
num_bl_enab = 2

led_definition = [
    ('Underside', 'Backlight')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTE, 6, LED_DRIVER_PULLUP ),
    ( REF_PORTB, 7, LED_DRIVER_PULLUP )
]

backlighting = True

bl_modes = [
    ( 1, 1 ),
    ( 0, 0 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), ['HID_KEYBOARD_SC_ESCAPE', 'HID_KEYBOARD_SC_F1']),
     ((4, 4), (0, 1), ['HID_KEYBOARD_SC_Q', 'HID_KEYBOARD_SC_F2']),
     ((4, 4), (0, 2), ['HID_KEYBOARD_SC_W', 'HID_KEYBOARD_SC_F3']),
     ((4, 4), (0, 3), ['HID_KEYBOARD_SC_E', 'HID_KEYBOARD_SC_F4']),
     ((4, 4), (0, 4), ['HID_KEYBOARD_SC_R', 'HID_KEYBOARD_SC_F5']),
     ((4, 4), (0, 5), ['HID_KEYBOARD_SC_T', 'HID_KEYBOARD_SC_F6']),
     ((4, 4), (0, 6), ['HID_KEYBOARD_SC_Y', 'HID_KEYBOARD_SC_F7']),
     ((4, 4), (0, 7), ['HID_KEYBOARD_SC_U', 'HID_KEYBOARD_SC_F8']),
     ((4, 4), (0, 8), ['HID_KEYBOARD_SC_I', 'HID_KEYBOARD_SC_F9']),
     ((4, 4), (0, 9), ['HID_KEYBOARD_SC_O', 'HID_KEYBOARD_SC_F10']),
     ((4, 4), (0, 10), ['HID_KEYBOARD_SC_P', 'HID_KEYBOARD_SC_F11']),
     ((4, 4), (0, 11), ['HID_KEYBOARD_SC_BACKSPACE', 'HID_KEYBOARD_SC_F12'])],

    [((5, 4), (1, 0), ['HID_KEYBOARD_SC_TAB', 'HID_KEYBOARD_SC_CAPS_LOCK']),
     ((4, 4), (1, 1), ['HID_KEYBOARD_SC_A', 'HID_KEYBOARD_SC_1_AND_EXCLAMATION']),
     ((4, 4), (1, 2), ['HID_KEYBOARD_SC_S', 'HID_KEYBOARD_SC_2_AND_AT']),
     ((4, 4), (1, 3), ['HID_KEYBOARD_SC_D', 'HID_KEYBOARD_SC_3_AND_HASHMARK']),
     ((4, 4), (1, 4), ['HID_KEYBOARD_SC_F', 'HID_KEYBOARD_SC_4_AND_DOLLAR']),
     ((4, 4), (1, 5), ['HID_KEYBOARD_SC_G', 'HID_KEYBOARD_SC_5_AND_PERCENTAGE']),
     ((4, 4), (1, 6), ['HID_KEYBOARD_SC_H', 'HID_KEYBOARD_SC_6_AND_CARET']),
     ((4, 4), (1, 7), ['HID_KEYBOARD_SC_J', 'HID_KEYBOARD_SC_7_AND_AND_AMPERSAND']),
     ((4, 4), (1, 8), ['HID_KEYBOARD_SC_K', 'HID_KEYBOARD_SC_8_AND_ASTERISK']),
     ((4, 4), (1, 9), ['HID_KEYBOARD_SC_L', 'HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS']),
     ((7, 4), (1, 10), ['HID_KEYBOARD_SC_ENTER', 'HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS'])],

    [((7, 4), (2, 0), ['HID_KEYBOARD_SC_LEFT_SHIFT', 'HID_KEYBOARD_SC_UP_ARROW']),
     ((4, 4), (2, 1), ['HID_KEYBOARD_SC_Z', 'HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE']),
     ((4, 4), (2, 2), ['HID_KEYBOARD_SC_X', 'HID_KEYBOARD_SC_SEMICOLON_AND_COLON']),
     ((4, 4), (2, 3), ['HID_KEYBOARD_SC_C', 'HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE']),
     ((4, 4), (2, 4), ['HID_KEYBOARD_SC_V', 'HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE']),
     ((4, 4), (2, 5), ['HID_KEYBOARD_SC_B', 'HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE']),
     ((4, 4), (2, 6), ['HID_KEYBOARD_SC_N', 'HID_KEYBOARD_SC_BACKSLASH_AND_PIPE']),
     ((4, 4), (2, 7), ['HID_KEYBOARD_SC_M', 'HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE']),
     ((4, 4), (2, 8), ['HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN', 'HID_KEYBOARD_SC_EQUAL_AND_PLUS']),
     ((5, 4), (2, 9), ['HID_KEYBOARD_SC_RIGHT_SHIFT', 'HID_KEYBOARD_SC_RIGHT_SHIFT']),
     ((4, 4), (2, 10), ['SCANCODE_FN1', 'SCANCODE_FN1'])],

    [((5, 4), (3, 0), ['HID_KEYBOARD_SC_LEFT_CONTROL', 'HID_KEYBOARD_SC_LEFT_ARROW']),
     ((4, 4), (3, 1), ['HID_KEYBOARD_SC_DELETE', 'HID_KEYBOARD_SC_DOWN_ARROW']),
     ((4, 4), (3, 2), ['HID_KEYBOARD_SC_LEFT_ALT', 'HID_KEYBOARD_SC_UP_ARROW']),
     ((25, 4), (3, 5), ['HID_KEYBOARD_SC_SPACE', 'HID_KEYBOARD_SC_SPACE']),
     ((5, 4), (3, 9), ['HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN', 'HID_KEYBOARD_SC_RIGHT_ALT']),
     ((5, 4), (3, 10), ['HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK', 'HID_KEYBOARD_SC_RIGHT_CONTROL'])]
]

# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2013-2018 David Howland
# Copyright (C) 2018 TalkingTree
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

"""Keyboard definition for the GH80-3000 custom keyboard."""

import easykeymap.templates.ATmega32U4_16MHz_SQUARE as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config, make_led_config

description = "GH80-3000"
unique_id = "GH80_3000_001"
cfg_name = "gh80_3000"

teensy = False
hw_boot_key = False

num_rows = 11
num_cols = 11

strobe_cols = False
strobe_low = True

matrix_hardware, matrix_strobe, matrix_sense = make_matrix_config(
    strobe_cols=strobe_cols,
    strobe_low=strobe_low,
    rows=[F4, F1, F0, F5, F6, F7, D4, D5, D3, D2, D0],
    cols=[C7, C6, B4, D7, B3, B2, B0, E6, B1, D1, D6],
    device=firmware.device
)

num_leds, num_ind, led_hardware, backlighting, num_bl_enab, bl_modes = make_led_config(
    led_pins = [B5, B6, B7],
    led_dir=LED_DRIVER_PULLDOWN,
    backlight_pins = [],
    backlight_dir=LED_DRIVER_PULLDOWN
)

led_definition = [
    ('Num LED', 'Num Lock'),
    ('Caps LED', 'Caps Lock'),
    ('Scroll LED', 'Scroll Lock')
]

KMAC_key = None

# ((key width, key height), (matrix row, matrix column), 'default mapping')
keyboard_definition = [
 [((4, 4), (0, 0), 'HID_KEYBOARD_SC_ESCAPE'),
  (4, None, '0'),
  ((4, 4), (0, 1), 'HID_KEYBOARD_SC_F1'),
  ((4, 4), (0, 2), 'HID_KEYBOARD_SC_F2'),
  ((4, 4), (0, 3), 'HID_KEYBOARD_SC_F3'),
  ((4, 4), (3, 0), 'HID_KEYBOARD_SC_F4'),
  (2, None, '0'),
  ((4, 4), (3, 1), 'HID_KEYBOARD_SC_F5'),
  ((4, 4), (3, 2), 'HID_KEYBOARD_SC_F6'),
  ((4, 4), (3, 3), 'HID_KEYBOARD_SC_F7'),
  ((4, 4), (3, 6), 'HID_KEYBOARD_SC_F8'),
  (2, None, '0'),
  ((4, 4), (3, 7), 'HID_KEYBOARD_SC_F9'),
  ((4, 4), (3, 8), 'HID_KEYBOARD_SC_F10'),
  ((4, 4), (3, 9), 'HID_KEYBOARD_SC_F11'),
  ((4, 4), (3, 10), 'HID_KEYBOARD_SC_F12'),
  (1, None, '0'),
  ((4, 4), (0, 4), 'HID_KEYBOARD_SC_PRINT_SCREEN'),
  ((4, 4), (0, 5), 'HID_KEYBOARD_SC_SCROLL_LOCK'),
  ((4, 4), (0, 6), 'HID_KEYBOARD_SC_PAUSE')],
 2,
 [((4, 4), (1, 0), 'HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE'),
  ((4, 4), (1, 1), 'HID_KEYBOARD_SC_1_AND_EXCLAMATION'),
  ((4, 4), (1, 2), 'HID_KEYBOARD_SC_2_AND_AT'),
  ((4, 4), (1, 3), 'HID_KEYBOARD_SC_3_AND_HASHMARK'),
  ((4, 4), (4, 0), 'HID_KEYBOARD_SC_4_AND_DOLLAR'),
  ((4, 4), (4, 1), 'HID_KEYBOARD_SC_5_AND_PERCENTAGE'),
  ((4, 4), (4, 2), 'HID_KEYBOARD_SC_6_AND_CARET'),
  ((4, 4), (4, 3), 'HID_KEYBOARD_SC_7_AND_AND_AMPERSAND'),
  ((4, 4), (4, 4), 'HID_KEYBOARD_SC_8_AND_ASTERISK'),
  ((4, 4), (4, 5), 'HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS'),
  ((4, 4), (4, 6), 'HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS'),
  ((4, 4), (4, 7), 'HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE'),
  ((4, 4), (4, 8), 'HID_KEYBOARD_SC_EQUAL_AND_PLUS'),
  ((4, 4), (4, 9), 'HID_KEYBOARD_SC_BACKSPACE'),
  ((4, 4), (4, 10), 'HID_KEYBOARD_SC_BACKSPACE'),
  (1, None, '0'),
  ((4, 4), (1, 4), 'HID_KEYBOARD_SC_INSERT'),
  ((4, 4), (1, 5), 'HID_KEYBOARD_SC_HOME'),
  ((4, 4), (1, 6), 'HID_KEYBOARD_SC_PAGE_UP'),
  (1, None, '0'),
  ((4, 4), (1, 7), 'HID_KEYBOARD_SC_NUM_LOCK'),
  ((4, 4), (1, 8), 'HID_KEYBOARD_SC_KEYPAD_SLASH'),
  ((4, 4), (1, 9), 'HID_KEYBOARD_SC_KEYPAD_ASTERISK'),
  ((4, 4), (1, 10), 'HID_KEYBOARD_SC_KEYPAD_MINUS')],
 [((6, 4), (2, 0), 'HID_KEYBOARD_SC_TAB'),
  ((4, 4), (2, 1), 'HID_KEYBOARD_SC_Q'),
  ((4, 4), (2, 2), 'HID_KEYBOARD_SC_W'),
  ((4, 4), (2, 3), 'HID_KEYBOARD_SC_E'),
  ((4, 4), (5, 0), 'HID_KEYBOARD_SC_R'),
  ((4, 4), (5, 1), 'HID_KEYBOARD_SC_T'),
  ((4, 4), (5, 2), 'HID_KEYBOARD_SC_Y'),
  ((4, 4), (5, 3), 'HID_KEYBOARD_SC_U'),
  ((4, 4), (5, 5), 'HID_KEYBOARD_SC_I'),
  ((4, 4), (5, 6), 'HID_KEYBOARD_SC_O'),
  ((4, 4), (5, 7), 'HID_KEYBOARD_SC_P'),
  ((4, 4), (5, 8), 'HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE'),
  ((4, 4), (5, 9), 'HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE'),
  ((6, 4), (5, 10), 'HID_KEYBOARD_SC_BACKSLASH_AND_PIPE'),
  (1, None, '0'),
  ((4, 4), (2, 4), 'HID_KEYBOARD_SC_DELETE'),
  ((4, 4), (2, 5), 'HID_KEYBOARD_SC_END'),
  ((4, 4), (2, 6), 'HID_KEYBOARD_SC_PAGE_DOWN'),
  (1, None, '0'),
  ((4, 4), (2, 7), 'HID_KEYBOARD_SC_KEYPAD_7_AND_HOME'),
  ((4, 4), (2, 8), 'HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW'),
  ((4, 4), (2, 9), 'HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP'),
  ((4, 4), (2, 10), 'HID_KEYBOARD_SC_KEYPAD_PLUS')],
 [((7, 4), (8, 0), 'HID_KEYBOARD_SC_CAPS_LOCK'),
  ((4, 4), (8, 1), 'HID_KEYBOARD_SC_A'),
  ((4, 4), (8, 2), 'HID_KEYBOARD_SC_S'),
  ((4, 4), (8, 3), 'HID_KEYBOARD_SC_D'),
  ((4, 4), (6, 0), 'HID_KEYBOARD_SC_F'),
  ((4, 4), (6, 1), 'HID_KEYBOARD_SC_G'),
  ((4, 4), (6, 2), 'HID_KEYBOARD_SC_H'),
  ((4, 4), (6, 3), 'HID_KEYBOARD_SC_J'),
  ((4, 4), (6, 6), 'HID_KEYBOARD_SC_K'),
  ((4, 4), (6, 7), 'HID_KEYBOARD_SC_L'),
  ((4, 4), (6, 8), 'HID_KEYBOARD_SC_SEMICOLON_AND_COLON'),
  ((4, 4), (6, 9), 'HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE'),
  ((4, 4), (5, 10), 'HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE'),
  ((5, 4), (6, 10), 'HID_KEYBOARD_SC_ENTER'),
  (14, None, '0'),
  ((4, 4), (8, 7), 'HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW'),
  ((4, 4), (8, 8), 'HID_KEYBOARD_SC_KEYPAD_5'),
  ((4, 4), (8, 9), 'HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW'),
  ((4, 4), (8, 10), 'HID_KEYBOARD_SC_KEYPAD_PLUS')],
 [((5, 4), (9, 0), 'HID_KEYBOARD_SC_LEFT_SHIFT'),
  ((4, 4), (9, 1), 'HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE'),
  ((4, 4), (9, 2), 'HID_KEYBOARD_SC_Z'),
  ((4, 4), (9, 3), 'HID_KEYBOARD_SC_X'),
  ((4, 4), (7, 0), 'HID_KEYBOARD_SC_C'),
  ((4, 4), (7, 1), 'HID_KEYBOARD_SC_V'),
  ((4, 4), (7, 2), 'HID_KEYBOARD_SC_B'),
  ((4, 4), (7, 3), 'HID_KEYBOARD_SC_N'),
  ((4, 4), (7, 5), 'HID_KEYBOARD_SC_M'),
  ((4, 4), (7, 6), 'HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN'),
  ((4, 4), (7, 7), 'HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN'),
  ((4, 4), (7, 8), 'HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK'),
  ((7, 4), (7, 9), 'HID_KEYBOARD_SC_RIGHT_SHIFT'),
  ((4, 4), (7, 10), 'SCANCODE_FN1'),
  (5, None, '0'),
  ((4, 4), (9, 6), 'HID_KEYBOARD_SC_UP_ARROW'),
  (5, None, '0'),
  ((4, 4), (9, 7), 'HID_KEYBOARD_SC_KEYPAD_1_AND_END'),
  ((4, 4), (9, 8), 'HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW'),
  ((4, 4), (9, 9), 'HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN'),
  ((4, 4), (9, 10), 'HID_KEYBOARD_SC_KEYPAD_ENTER')],
 [((6, 4), (10, 0), 'HID_KEYBOARD_SC_LEFT_CONTROL'),
  ((4, 4), (10, 1), 'HID_KEYBOARD_SC_LEFT_GUI'),
  ((6, 4), (10, 2), 'HID_KEYBOARD_SC_LEFT_ALT'),
  ((4, 4), (10, 3), 'HID_KEYBOARD_SC_SPACE'),
  ((8, 4), (8, 4), 'HID_KEYBOARD_SC_SPACE'),
  ((4, 4), (8, 5), 'HID_KEYBOARD_SC_SPACE'),
  ((8, 4), (8, 6), 'HID_KEYBOARD_SC_SPACE'),
  ((4, 4), (6, 4), 'HID_KEYBOARD_SC_SPACE'),
  ((6, 4), (6, 5), 'HID_KEYBOARD_SC_RIGHT_ALT'),
  ((4, 4), (9, 4), 'HID_KEYBOARD_SC_APPLICATION'),
  ((6, 4), (9, 5), 'HID_KEYBOARD_SC_RIGHT_CONTROL'),
  (1, None, '0'),
  ((4, 4), (10, 4), 'HID_KEYBOARD_SC_LEFT_ARROW'),
  ((4, 4), (10, 5), 'HID_KEYBOARD_SC_DOWN_ARROW'),
  ((4, 4), (10, 6), 'HID_KEYBOARD_SC_RIGHT_ARROW'),
  (1, None, '0'),
  ((4, 4), (10, 7), 'HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT'),
  ((4, 4), (10, 8), 'HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT'),
  ((4, 4), (10, 9), 'HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE'),
  ((4, 4), (10, 10), 'HID_KEYBOARD_SC_KEYPAD_ENTER')]
]

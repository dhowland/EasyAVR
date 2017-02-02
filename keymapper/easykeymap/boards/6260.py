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

"""Keyboard definition for a hand-wired keyboard"""

# The first decision you have to make is to choose a hardware
# layout.  Assuming you are using a Teensy2.0, this is probably
# the best hardware layout for you.  ATmega32U4_16MHz_SIXTY might
# also work for you, though.  Leave the rest of the imports like
# they are here.
import easykeymap.templates.ATmega32U4_16MHz_TKL as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config, pin_to_binary

# The name of the board in the "New" dialog
description = "62/60 (Round 0)"
# Unique string to identify THIS exact hardware layout
unique_id = "6260_v01"
# The name of the .cfg file the system will try to find for altered
# layout options
cfg_name = "6260"

# Hand-wired boards usually use Teensy controllers.  Set this to
# True to make sure that the bootloader works.
teensy = False
# If your board has an exposed switch for going into boot mode, you
# can set this to True and the system won't prompt you to add a BOOT
# key to your layout.
hw_boot_key = True

# These two parameters define the size of the keyboard in the display.
# Must be whole numbers in units of quarter key lengths.  A TKL
# usually is 6 rows high with a 1/2 key length gutter under the Fn row.
# Therefore int(6.5*4).  Apply the same logic the width.  Remember
# we are talking visual width, not number of columns.
display_height = int(5*4)
display_width = int(15*4)

# The number of rows and columns in the matrix.  In a hand-wired board
# each of these will correspond to a single pin.
num_rows = 5
num_cols = 15

# Keyboards work by scanning a matrix to check each key.  The scan
# works by setting an active row/column (strobing) and then reading
# the status of every switch that crosses it (sensing).
# strobe_cols tells the firmware which direction you have your diodes
# installed.  If diodes go from column to row, then strobe_cols must
# be True.  If diodes go from row to column, then strobe_cols must be
# False.
strobe_cols = True
# strobe_low tells the firmware if a row/column should be activated
# by pulling the pin high or low.  Hand-wired boards will almost always
# use strobe_low = True
strobe_low = True

# The matrix_hardware, matrix_strobe, matrix_sense parameters tell
# the firmware how to initialize the ports, what pins must be set
# for each row/column, and what order to strobe/sense.  These are
# complicated and are explained fully elsewhere.  It is easiest to
# configure the matrix by using the make_matrix_config function as
# shown below.  Just customize 'rows' and 'cols' for your project.
matrix_hardware, matrix_strobe, matrix_sense = make_matrix_config(
    strobe_cols=strobe_cols,
    strobe_low=strobe_low,
    rows=[B3, B2, B1, B0, F0],
    cols=[F7, F6, F5, F4, F1, B7, D0, D1, D2, D3, D5, D4, D6, D7, B4],
    device=firmware.device
)

# The total number of LED outputs (indicators + backlights)
num_leds = 0
# The number of LED indicators (for example, caps lock)
num_ind = 0
# The number of backlight enable modes.  This counts the number of
# options available for the BL_ENABLE key
num_bl_enab = 0

# Define the default assignments of the indicator LEDs.  The length
# of this list must equal num_ind.  For each LED, the first string
# is the description of the key shown in the GUI.  The second string
# is the default function.  For valid function options, see
# led_assignments in gui.py
led_definition = [
]

# Definition of LED pins.  (indicators and backlights)  Indicators
# must come first.  LED_DRIVER_PULLUP is used when the pin is connected
# to the anode and the cathode is connected to ground.
# LED_DRIVER_PULLDOWN is used when the pin is connected to the cathode
# and the anode is connected to the power supply.
led_hardware = [
]

# True if the board supports backlight, otherwise False
backlighting = False

# This can be used to configure different backlighting zones.  Explained
# in more detail elsewhere.  Length of list must equal num_bl_enab.
# Length of each tuple must equal num_leds.  Uses the same ordering
# as led_hardware
bl_modes = [
]

# Just leave this here as-is.
KMAC_key = None

# Define your layout.  This is a list of rows.  Each row is a list
# of keys.  Each key is a tuple of three items.  First item is a tuple
# defining the width,height of the key.  If it is just a number, it
# will be a space instead of a key.  All units are in quarter key lengths,
# so a standard key would be (4,4).  Second item is a tuple defining the
# row,column in the matrix for that key.  Third item is the default scancode
# for that key, from scancodes.py.  If a row is a number instead of a list,
# it will just make a vertical spacer.
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
     ((4, 4), (0, 14), '0')],
    
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
     ((6, 4), (1, 14), 'HID_KEYBOARD_SC_BACKSLASH_AND_PIPE')],

    [((7, 4), (2, 0), 'HID_KEYBOARD_SC_LEFT_CONTROL'),
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
     ((9, 4), (2, 13), 'HID_KEYBOARD_SC_ENTER')],

    [((9, 4), (3, 0), 'HID_KEYBOARD_SC_LEFT_SHIFT'),
     ((4, 4), (3, 1), 'HID_KEYBOARD_SC_Z'),
     ((4, 4), (3, 2), 'HID_KEYBOARD_SC_X'),
     ((4, 4), (3, 3), 'HID_KEYBOARD_SC_C'),
     ((4, 4), (3, 5), 'HID_KEYBOARD_SC_V'),
     ((4, 4), (3, 6), 'HID_KEYBOARD_SC_B'),
     ((4, 4), (3, 7), 'HID_KEYBOARD_SC_N'),
     ((4, 4), (3, 8), 'HID_KEYBOARD_SC_M'),
     ((4, 4), (3, 9), 'HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN'),
     ((4, 4), (3, 10), 'HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN'),
     ((4, 4), (3, 11), 'HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK'),
     ((4, 4), (3, 12), 'HID_KEYBOARD_SC_UP_ARROW'),
     ((7, 4), (3, 14), 'HID_KEYBOARD_SC_RIGHT_SHIFT')],

    [(3, None, '0'),
     ((5, 4), (4, 0), 'HID_KEYBOARD_SC_LEFT_GUI'),
     ((5, 4), (4, 1), 'HID_KEYBOARD_SC_LEFT_ALT'),
     ((28, 4), (4, 6), 'HID_KEYBOARD_SC_SPACE'),
     ((4, 4), (4, 10), 'HID_KEYBOARD_SC_RIGHT_ALT'),
     ((4, 4), (4, 11), 'HID_KEYBOARD_SC_LEFT_ARROW'),
     ((4, 4), (4, 12), 'HID_KEYBOARD_SC_DOWN_ARROW'),
     ((4, 4), (4, 13), 'HID_KEYBOARD_SC_RIGHT_ARROW')]

]

use_rgb = True
rgb_pin = pin_to_binary(C7)
rgb_count = 72
rgb_max = 120
rgb_url = "http://www.keyboard-layout-editor.com/#/gists/437edbad91365c9ef7b2"
rgb_order = [71, 70, 69, 68, 67, 62, 63, 64, 65, 66, 61, 60,
             59, 58, 57, 56, 55, 54, 41, 42, 43, 44, 45, 46,
             47, 48, 49, 50, 51, 52, 53, 40, 39, 38, 37, 36,
             35, 34, 33, 32, 31, 30, 29, 28, 14, 15, 16, 17,
             18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 13, 12,
             11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        

# Just leave this here as-is.
alt_layouts = {}

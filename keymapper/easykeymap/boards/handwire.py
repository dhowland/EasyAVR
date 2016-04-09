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
# layout.  Assuming you are using a Teensy2.0, ATmega32U4_16MHz_TKL
# is probably the best hardware layout for you.  ATmega32U4_16MHz_SIXTY
# might also work for you, though.  The sizes are defined in the
# templates/__init__.py file of the keymapper.
# Leave the rest of the imports like they are here.
import easykeymap.templates.ATmega32U4_16MHz_TKL as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config

# The name of the board in the "New" dialog
description = "Hand-wire"
# Unique string to identify THIS exact hardware layout
unique_id = "HANDWIRE_001"
# The name of the .cfg file the system will try to find for altered
# layout options.  See the configs subdir of the keymapper.
cfg_name = "handwire"

# Hand-wired boards usually use Teensy controllers.  Set this to
# True to make sure that the bootloader works.
teensy = True
# If your board has an exposed switch for going into the bootloader,
# you can set this to True and the system won't prompt you to add a
# BOOT key to your layout.
hw_boot_key = False

# These two parameters define the size of the keyboard in the display.
# Must be whole numbers in units of quarter key lengths.  A TKL
# usually is 6 rows high with a 1/2 key length gutter under the Fn row.
# Therefore int(6.5*4).  Apply the same logic the width.  Remember
# we are talking visual width, not number of columns.
display_height = int(6.5*4)
display_width = int(18.25*4)

# The number of rows and columns in the matrix.  In a hand-wired board
# each of these will correspond to a single pin.
num_rows = 6
num_cols = 17

# Keyboards work by scanning a matrix to check each key.  The scan
# works by setting an active row/column (strobing) and then reading
# the status of every switch that crosses it (sensing).
# strobe_cols tells the firmware which direction you have your diodes
# installed.  If diodes go from column to row, then strobe_cols must
# be False.  If diodes go from row to column, then strobe_cols must be
# True.
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
    rows=[B5, B4, B3, B2, B1, B0],
    cols=[D5, C7, C6, D4, D0, E6, F0, F1, F4, F5, F6, F7, D7, D6, D1, D2, D3],
    device=firmware.device
)

# The total number of LED outputs (indicators + backlights)
num_leds = 2
# The number of LED indicators (for example, caps lock)
num_ind = 2
# The number of backlight enable modes.  This counts the number of
# options available for the BL_ENABLE key.  Boards without backlights
# should use the minimum value of 2.
num_bl_enab = 2

# Define the default assignments of the indicator LEDs.  The length
# of this list must equal num_ind.  For each LED, the first string
# is the description of the key shown in the GUI.  The second string
# is the default function assigned to that LED.  LED functions must
# be strings as defined in led_assignments of gui.py.  Common choices
# are 'Num Lock', 'Caps Lock', 'Scroll Lock', 'Win Lock', 'Fn Active',
# 'Recording', 'Backlight', and 'Unassigned'.
led_definition = [
    ('Caps Key', 'Caps Lock'),
    ('Scroll Key', 'Scroll Lock')
]

# Definition of LED pins.  (indicators and backlights)  Indicators
# must come first and be in the same order as defined in led_definition.
# LED_DRIVER_PULLUP is used when the pin is connected to the anode of
# the LED and the cathode is connected to ground.
# LED_DRIVER_PULLDOWN is used when the pin is connected to the cathode
# of the LED and the anode is connected to the power supply.
led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTB, 6, LED_DRIVER_PULLUP ),
    ( REF_PORTB, 7, LED_DRIVER_PULLUP )
]

# True if the board supports backlight, otherwise False
backlighting = False

# This can be used to configure different backlighting zones.  Explained
# in more detail elsewhere.  Length of list must equal num_bl_enab.
# Length of each tuple must equal num_leds.  Tuples use the same ordering
# as led_hardware.  Almost everyone should just use an all-on/all-off
# configuration.  That's a list of two tuples, one with all 1s for each
# LED, the other with all 0s for each LED.
bl_modes = [
    ( 0, 0 ),
    ( 1, 1 )
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
     (4, None, '0'),
     ((4, 4), (0, 2), 'HID_KEYBOARD_SC_F1'),
     ((4, 4), (0, 3), 'HID_KEYBOARD_SC_F2'),
     ((4, 4), (0, 4), 'HID_KEYBOARD_SC_F3'),
     ((4, 4), (0, 5), 'HID_KEYBOARD_SC_F4'),
     (2, None, '0'),
     ((4, 4), (0, 6), 'HID_KEYBOARD_SC_F5'),
     ((4, 4), (0, 7), 'HID_KEYBOARD_SC_F6'),
     ((4, 4), (0, 8), 'HID_KEYBOARD_SC_F7'),
     ((4, 4), (0, 9), 'HID_KEYBOARD_SC_F8'),
     (2, None, '0'),
     ((4, 4), (0, 10), 'HID_KEYBOARD_SC_F9'),
     ((4, 4), (0, 11), 'HID_KEYBOARD_SC_F10'),
     ((4, 4), (0, 12), 'HID_KEYBOARD_SC_F11'),
     ((4, 4), (0, 13), 'HID_KEYBOARD_SC_F12'),
     (1, None, '0'),
     ((4, 4), (0, 14), 'HID_KEYBOARD_SC_PRINT_SCREEN'),
     ((4, 4), (0, 15), 'HID_KEYBOARD_SC_SCROLL_LOCK'),
     ((4, 4), (0, 16), 'HID_KEYBOARD_SC_PAUSE')],

    2,

    [((4, 4), (1, 1), 'HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE'),
     ((4, 4), (1, 1), 'HID_KEYBOARD_SC_1_AND_EXCLAMATION'),
     ((4, 4), (1, 2), 'HID_KEYBOARD_SC_2_AND_AT'),
     ((4, 4), (1, 3), 'HID_KEYBOARD_SC_3_AND_HASHMARK'),
     ((4, 4), (1, 4), 'HID_KEYBOARD_SC_4_AND_DOLLAR'),
     ((4, 4), (1, 5), 'HID_KEYBOARD_SC_5_AND_PERCENTAGE'),
     ((4, 4), (1, 6), 'HID_KEYBOARD_SC_6_AND_CARET'),
     ((4, 4), (1, 7), 'HID_KEYBOARD_SC_7_AND_AND_AMPERSAND'),
     ((4, 4), (1, 8), 'HID_KEYBOARD_SC_8_AND_ASTERISK'),
     ((4, 4), (1, 9), 'HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS'),
     ((4, 4), (1, 10), 'HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS'),
     ((4, 4), (1, 11), 'HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE'),
     ((4, 4), (1, 12), 'HID_KEYBOARD_SC_EQUAL_AND_PLUS'),
     ((8, 4), (1, 13), 'HID_KEYBOARD_SC_BACKSPACE'),
     (1, None, '0'),
     ((4, 4), (1, 14), 'HID_KEYBOARD_SC_INSERT'),
     ((4, 4), (1, 15), 'HID_KEYBOARD_SC_HOME'),
     ((4, 4), (1, 16), 'HID_KEYBOARD_SC_PAGE_UP')],

    [((6, 4), (2, 0), 'HID_KEYBOARD_SC_TAB'),
     ((4, 4), (2, 1), 'HID_KEYBOARD_SC_Q'),
     ((4, 4), (2, 2), 'HID_KEYBOARD_SC_W'),
     ((4, 4), (2, 3), 'HID_KEYBOARD_SC_E'),
     ((4, 4), (2, 4), 'HID_KEYBOARD_SC_R'),
     ((4, 4), (2, 5), 'HID_KEYBOARD_SC_T'),
     ((4, 4), (2, 6), 'HID_KEYBOARD_SC_Y'),
     ((4, 4), (2, 7), 'HID_KEYBOARD_SC_U'),
     ((4, 4), (2, 8), 'HID_KEYBOARD_SC_I'),
     ((4, 4), (2, 9), 'HID_KEYBOARD_SC_O'),
     ((4, 4), (2, 10), 'HID_KEYBOARD_SC_P'),
     ((4, 4), (2, 11), 'HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE'),
     ((4, 4), (2, 12), 'HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE'),
     ((6, 4), (2, 13), 'HID_KEYBOARD_SC_BACKSLASH_AND_PIPE'),
     (1, None, '0'),
     ((4, 4), (2, 14), 'HID_KEYBOARD_SC_DELETE'),
     ((4, 4), (2, 15), 'HID_KEYBOARD_SC_END'),
     ((4, 4), (2, 16), 'HID_KEYBOARD_SC_PAGE_DOWN')],

    [((7, 4), (3, 0), 'HID_KEYBOARD_SC_CAPS_LOCK'),
     ((4, 4), (3, 1), 'HID_KEYBOARD_SC_A'),
     ((4, 4), (3, 2), 'HID_KEYBOARD_SC_S'),
     ((4, 4), (3, 3), 'HID_KEYBOARD_SC_D'),
     ((4, 4), (3, 4), 'HID_KEYBOARD_SC_F'),
     ((4, 4), (3, 5), 'HID_KEYBOARD_SC_G'),
     ((4, 4), (3, 6), 'HID_KEYBOARD_SC_H'),
     ((4, 4), (3, 7), 'HID_KEYBOARD_SC_J'),
     ((4, 4), (3, 8), 'HID_KEYBOARD_SC_K'),
     ((4, 4), (3, 9), 'HID_KEYBOARD_SC_L'),
     ((4, 4), (3, 10), 'HID_KEYBOARD_SC_SEMICOLON_AND_COLON'),
     ((4, 4), (3, 11), 'HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE'),
     ((9, 4), (3, 13), 'HID_KEYBOARD_SC_ENTER'),
     (13, None, '0')],

    [((9, 4), (4, 0), 'HID_KEYBOARD_SC_LEFT_SHIFT'),
     ((4, 4), (4, 2), 'HID_KEYBOARD_SC_Z'),
     ((4, 4), (4, 3), 'HID_KEYBOARD_SC_X'),
     ((4, 4), (4, 4), 'HID_KEYBOARD_SC_C'),
     ((4, 4), (4, 5), 'HID_KEYBOARD_SC_V'),
     ((4, 4), (4, 6), 'HID_KEYBOARD_SC_B'),
     ((4, 4), (4, 7), 'HID_KEYBOARD_SC_N'),
     ((4, 4), (4, 8), 'HID_KEYBOARD_SC_M'),
     ((4, 4), (4, 9), 'HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN'),
     ((4, 4), (4, 10), 'HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN'),
     ((4, 4), (4, 11), 'HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK'),
     ((11, 4), (4, 13), 'HID_KEYBOARD_SC_RIGHT_SHIFT'),
     (5, None, '0'),
     ((4, 4), (4, 15), 'HID_KEYBOARD_SC_UP_ARROW'),
     (4, None, '0')],

    [((5, 4), (5, 0), 'HID_KEYBOARD_SC_LEFT_CONTROL'),
     ((5, 4), (5, 1), 'HID_KEYBOARD_SC_LEFT_GUI'),
     ((5, 4), (5, 2), 'HID_KEYBOARD_SC_LEFT_ALT'),
     ((25, 4), (5, 6), 'HID_KEYBOARD_SC_SPACE'),
     ((5, 4), (5, 10), 'HID_KEYBOARD_SC_RIGHT_ALT'),
     ((5, 4), (5, 11), 'HID_KEYBOARD_SC_RIGHT_GUI'),
     ((5, 4), (5, 12), 'HID_KEYBOARD_SC_APPLICATION'),
     ((5, 4), (5, 13), 'HID_KEYBOARD_SC_RIGHT_CONTROL'),
     (1, None, '0'),
     ((4, 4), (5, 14), 'HID_KEYBOARD_SC_LEFT_ARROW'),
     ((4, 4), (5, 15), 'HID_KEYBOARD_SC_DOWN_ARROW'),
     ((4, 4), (5, 16), 'HID_KEYBOARD_SC_RIGHT_ARROW')]
]

# Just leave this here as-is.
alt_layouts = {}

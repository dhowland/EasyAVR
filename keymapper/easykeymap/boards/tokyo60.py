"""
Keyboard definition for the Tokyo60 custom keyboard.
Auto-generated from 'D:\\Users\\dave\\Desktop\\tokyo60.json'
"""

#
# READ THIS
#
# This file contains a description of the various parameters that
# must be defined in order to completely describe the new keyboard.
# This file must be correct for the firmware to work, however if
# if is incorrect reprogramming the board won't cause any damage.
#
# This tool that created this file did not have all the information
# needed to make a perfect config.  Check over all the data for
# correctness.  Definitely make sure to fix the matix rows/columns in
# keyboard_definition, which are almost certainly wrong.
#
# This file uses two helper functions to make the configuration
# easier.  For more complicated hardware, it may be necessary to
# set the parameters by hand.  Look at other configs, such as
# boards/sigma.py, for examples if you want to try it.
#

# The first decision you have to make is to choose a hardware
# build.  A handwire board using a Teensy2.0 will probably want
# ATmega32U4_16MHz_TKL or ATmega32U4_16MHz_SIXTY.  The sizes are
# defined in the templates/__init__.py file of the keymapper.
# Leave the rest of the imports like they are here.

import easykeymap.templates.ATmega32U4_16MHz_SIXTY as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config, make_led_config


# The name of the board in the "New" dialog

description = "Tokyo60"

# Unique string to identify THIS exact hardware layout.  If you change
# this file after saving layouts in the GUI, bump the unique_id to
# tell the tool that the old save files should not be used.  (prevents
# corrupted builds)

unique_id = "TOKYO60_001"

# The name of the .cfg file the system will try to find for altered
# layout options.  See the configs subdir of the keymapper.

cfg_name = "tokyo60"


# Hand-wired boards usually use Teensy controllers.  Set this to
# True to make sure that the bootloader works.

teensy = False

# If your board has an exposed switch for going into the bootloader,
# you can set this to True and the system won't prompt you to add a
# BOOT key to your layout.

hw_boot_key = False


# The number of rows and columns in the matrix.  In a hand-wired board
# each of these will correspond to a single pin.

num_rows = 5
num_cols = 14


# Keyboards work by scanning a matrix to check each key.  The scan
# works by setting an active row/column (strobing) and then reading
# the status of every switch that crosses it (sensing).
# strobe_cols tells the firmware which direction you have your diodes
# installed.  If diodes go from column to row, then strobe_cols must
# be False.  If diodes go from row to column, then strobe_cols must be
# True.

strobe_cols = False

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
    rows=[D0, D1, D2, D3, D5],
    cols=[F0, F1, E6, C7, C6, B6, D4, B1, B2, B5, B4, D7, D6, B3],
    device=firmware.device
)


# The num_leds, num_ind, led_hardware, backlighting, num_bl_enab,
# and bl_modes parameters tell the firmware how to operate the LEDs
# for indicators (for example, Caps Lock) and for backlighting.  In
# order to fine-tune the configs, these may have to be defined manually
# but it is easiest to use make_led_config.
# LED_DRIVER_PULLUP is used when the pin is connected to the anode of
# the LED and the cathode is connected to ground.
# LED_DRIVER_PULLDOWN is used when the pin is connected to the cathode
# of the LED and the anode is connected to the power supply.
# Hand-wired boards will usually want to use LED_DRIVER_PULLDOWN.
# If there are no backlights, just leave the list empty (ie. just []).

num_leds, num_ind, led_hardware, backlighting, num_bl_enab, bl_modes = make_led_config(
    led_pins = [],
    led_dir=LED_DRIVER_PULLDOWN,
    backlight_pins = [B7],
    backlight_dir=LED_DRIVER_PULLDOWN
)


# Define the default assignments of the indicator LEDs.  The length
# of this list must equal the length of led_pins.  For each LED, the
# first string is the description of the key shown in the GUI.  The
# second string is the default function assigned to that LED.  LED
# functions must be strings as defined in led_assignments of gui.py.
# Choices are 'Num Lock', 'Caps Lock', 'Scroll Lock', 'Compose', 'Kana',
# 'Win Lock', 'Fn1 Active', 'Fn2 Active', 'Fn3 Active', 'Fn4 Active',
# 'Fn5 Active', 'Fn6 Active', 'Fn7 Active', 'Fn8 Active', 'Fn9 Active',
# 'Any Fn Active', 'Recording', 'USB Init', 'USB Error', 'USB Suspend',
# 'USB Normal', 'Backlight', and 'Unassigned'.

led_definition = []


# Define your layout.  This is a list of rows.  Each row is a list
# of keys.  Each key is a tuple of three items.  First item is a tuple
# defining the width,height of the key.  If it is just a number, it
# will be a space instead of a key.  All units are in quarter key lengths,
# so a standard key would be (4,4).  Second item is a tuple defining the
# row,column in the matrix for that key.  Third item is the default scancode
# for that key, from scancodes.py.  If a row is a number instead of a list,
# it will just make a vertical spacer.
# ((key width, key height), (matrix row, matrix column), 'default mapping')

keyboard_definition = [[((4, 4), (0, 0), 'HID_KEYBOARD_SC_ESCAPE'),
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
  ((4, 4), (0, 13), 'HID_KEYBOARD_SC_BACKSLASH_AND_PIPE'),
  ((4, 4), (1, 13), 'HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE')],
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
  ((6, 4), (2, 13), 'HID_KEYBOARD_SC_BACKSPACE')],
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
  ((9, 4), (3, 13), 'HID_KEYBOARD_SC_ENTER')],
 [((9, 4), (3, 0), 'HID_KEYBOARD_SC_LEFT_SHIFT'),
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
  ((7, 4), (3, 12), 'HID_KEYBOARD_SC_RIGHT_SHIFT'),
  ((4, 4), (4, 13), 'SCANCODE_FN1')],
 [(6, None, '0'),
  ((4, 4), (4, 2), 'HID_KEYBOARD_SC_LEFT_ALT'),
  ((6, 4), (4, 3), 'HID_KEYBOARD_SC_LEFT_GUI'),
  ((28, 4), (4, 6), 'HID_KEYBOARD_SC_SPACE'),
  ((6, 4), (4, 11), 'HID_KEYBOARD_SC_RIGHT_GUI'),
  ((4, 4), (4, 12), 'HID_KEYBOARD_SC_RIGHT_ALT')]]


# Just leave this here as-is.
KMAC_key = None

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

"""Keyboard definition for the Tau custom numpad."""

import easykeymap.templates.ATmega32U4_16MHz_PAD as firmware
from easykeymap.ioports import *

description = "Tau (Qazpad)"
unique_id = "TAU_002"
cfg_name = "tau"

teensy = False
hw_boot_key = False

num_rows = 6
num_cols = 6

strobe_cols = True
strobe_low = True

matrix_hardware = [
#     Port mask     Dir mask
    ( 0b00000000 , 0b00000000 ),    # REF_PORTB
    ( 0b11000000 , 0b11000000 ),    # REF_PORTC
    ( 0b11111100 , 0b00000000 ),    # REF_PORTD
    ( 0b00000000 , 0b00000000 ),    # REF_PORTE
    ( 0b11110000 , 0b11110000 )     # REF_PORTF
]

matrix_strobe = [
#     REF_PORTB    REF_PORTC    REF_PORTD    REF_PORTE   REF_PORTF
    ( 0b00000000 , 0b11000000 , 0b00000000 , 0b00000000, 0b11100000 ),
    ( 0b00000000 , 0b11000000 , 0b00000000 , 0b00000000, 0b11010000 ),
    ( 0b00000000 , 0b11000000 , 0b00000000 , 0b00000000, 0b10110000 ),
    ( 0b00000000 , 0b11000000 , 0b00000000 , 0b00000000, 0b01110000 ),
    ( 0b00000000 , 0b10000000 , 0b00000000 , 0b00000000, 0b11110000 ),
    ( 0b00000000 , 0b01000000 , 0b00000000 , 0b00000000, 0b11110000 )
]

matrix_sense = [
#      Port        Pin mask
    ( REF_PORTD , 0b00000100 ),
    ( REF_PORTD , 0b00001000 ),
    ( REF_PORTD , 0b00010000 ),
    ( REF_PORTD , 0b00100000 ),
    ( REF_PORTD , 0b01000000 ),
    ( REF_PORTD , 0b10000000 )
]

num_leds = 5
num_ind = 2
num_bl_enab = 4

led_definition = [
    ('Esc Key', 'Any Fn Active'),
    ('Num Key', 'Num Lock')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTB, 3, LED_DRIVER_PULLDOWN ),
    ( REF_PORTB, 4, LED_DRIVER_PULLDOWN ),
    ( REF_PORTB, 5, LED_DRIVER_PULLUP ),
    ( REF_PORTB, 6, LED_DRIVER_PULLUP ),
    ( REF_PORTB, 7, LED_DRIVER_PULLUP )
]

backlighting = True

bl_modes = [
    ( 1, 1, 1, 1, 1 ),
    ( 0, 0, 0, 0, 0 ),
    ( 0, 0, 1, 0, 0 ),
    ( 0, 1, 1, 0, 1 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), 'HID_KEYBOARD_SC_ESCAPE'),
     ((4, 4), (0, 1), 'SCANCODE_FN1'),
     (1, None, '0'),
     ((4, 4), (0, 2), 'HID_KEYBOARD_SC_HOME'),
     ((4, 4), (0, 3), 'HID_KEYBOARD_SC_END'),
     ((4, 4), (0, 4), 'HID_KEYBOARD_SC_DELETE'),
     ((4, 4), (0, 5), 'HID_KEYBOARD_SC_BACKSPACE')],

    1,

    [((4, 4), (1, 0), 'HID_KEYBOARD_SC_A'),
     ((4, 4), (1, 1), 'HID_KEYBOARD_SC_B'),
     (1, None, '0'),
     ((4, 4), (1, 2), 'HID_KEYBOARD_SC_NUM_LOCK'),
     ((4, 4), (1, 3), 'HID_KEYBOARD_SC_KEYPAD_SLASH'),
     ((4, 4), (1, 4), 'HID_KEYBOARD_SC_KEYPAD_ASTERISK'),
     ((4, 4), (1, 5), 'HID_KEYBOARD_SC_KEYPAD_MINUS')],

    [((4, 4), (2, 0), 'HID_KEYBOARD_SC_C'),
     ((4, 4), (2, 1), 'HID_KEYBOARD_SC_D'),
     (1, None, '0'),
     ((4, 4), (2, 2), 'HID_KEYBOARD_SC_KEYPAD_7_AND_HOME'),
     ((4, 4), (2, 3), 'HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW'),
     ((4, 4), (2, 4), 'HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP'),
     ((4, 8), (3, 5), 'HID_KEYBOARD_SC_KEYPAD_PLUS')],

    [((4, 4), (3, 0), 'HID_KEYBOARD_SC_E'),
     ((4, 4), (3, 1), 'HID_KEYBOARD_SC_F'),
     (1, None, '0'),
     ((4, 4), (3, 2), 'HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW'),
     ((4, 4), (3, 3), 'HID_KEYBOARD_SC_KEYPAD_5'),
     ((4, 4), (3, 4), 'HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW'),
     (-4, None, '0')],

    [((4, 8), (4, 0), 'HID_KEYBOARD_SC_SPACE'),
     ((4, 8), (4, 1), 'HID_KEYBOARD_SC_TAB'),
     (1, None, '0'),
     ((4, 4), (4, 2), 'HID_KEYBOARD_SC_KEYPAD_1_AND_END'),
     ((4, 4), (4, 3), 'HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW'),
     ((4, 4), (4, 4), 'HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN'),
     ((4, 8), (5, 5), 'HID_KEYBOARD_SC_KEYPAD_ENTER')],

    [(-8, None, '0'),
     (1, None, '0'),
     ((8, 4), (5, 3), 'HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT'),
     ((4, 4), (5, 4), 'HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE'),
     (-4, None, '0')]
]

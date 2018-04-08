# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2013-2017 David Howland
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

"""Keyboard definition for Techkeys Sixkeyboard"""
# contributed by suicidal_orange

import easykeymap.templates.ATmega16U2_16MHz_CARD as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config

description = "Techkeys SixKeyBoard"
unique_id = "SIXKEYBOARD_001"
cfg_name = "sixkeyboard"

teensy = False
hw_boot_key = True

num_rows = 1
num_cols = 6

strobe_cols = False
strobe_low = True

matrix_hardware, matrix_strobe, matrix_sense = make_matrix_config(
    strobe_cols=strobe_cols,
    strobe_low=strobe_low,
    rows=[],
    cols=[C7, B7, B5, D6, D1, D4],
    device=firmware.device
)

num_leds = 7
num_ind = 7
num_bl_enab = 2

led_definition = [
    ('1', 'Unassigned'),
    ('2', 'Unassigned'),
    ('3', 'Unassigned'),
    ('4', 'Unassigned'),
    ('5', 'Unassigned'),
    ('6', 'Unassigned'),
    ('Underside', 'Unassigned')
]

led_hardware = [
#       Port    Pin    Direction
    ( REF_PORTC, 6, LED_DRIVER_PULLDOWN ),
    ( REF_PORTB, 6, LED_DRIVER_PULLDOWN ),
    ( REF_PORTB, 4, LED_DRIVER_PULLDOWN ),
    ( REF_PORTD, 5, LED_DRIVER_PULLDOWN ),
    ( REF_PORTD, 2, LED_DRIVER_PULLDOWN ),
    ( REF_PORTD, 3, LED_DRIVER_PULLDOWN ),
    ( REF_PORTC, 4, LED_DRIVER_PULLDOWN )
]

backlighting = False

bl_modes = [
    ( 0, 0, 0, 0, 0, 0, 0 ),
    ( 1, 1, 1, 1, 1, 1, 1 )
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), 'SCANCODE_MUTE'),
     ((4, 4), (0, 1), 'SCANCODE_VOL_DEC'),
     ((4, 4), (0, 2), 'SCANCODE_VOL_INC')],

    [((4, 4), (0, 3), 'SCANCODE_PREV_TRACK'),
     ((4, 4), (0, 4), 'SCANCODE_PLAY_PAUSE'),
     ((4, 4), (0, 5), 'SCANCODE_NEXT_TRACK')],
]

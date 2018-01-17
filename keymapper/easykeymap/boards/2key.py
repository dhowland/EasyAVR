# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2013-2018 David Howland
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

"""Keyboard definition for 2Key Macropad"""

import easykeymap.templates.ATmega16U2_16MHz_CARD as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config, make_led_config

description = "2key Macropad"
unique_id = "2KEY_001"
cfg_name = "2key"

teensy = False
hw_boot_key = True

display_height = int(1*4)
display_width = int(2*4)

num_rows = 1
num_cols = 2

strobe_cols = False
strobe_low = True

matrix_hardware, matrix_strobe, matrix_sense = make_matrix_config(
    strobe_cols=strobe_cols,
    strobe_low=strobe_low,
    rows=[],
    cols=[D1, D2],
    device=firmware.device
)

num_leds, num_ind, led_hardware, backlighting, num_bl_enab, bl_modes = make_led_config(
    led_pins = [B6, B5],
    led_dir=LED_DRIVER_PULLUP,
    backlight_pins = [],
    backlight_dir=LED_DRIVER_PULLDOWN
)

led_definition = [
    ('left', 'Unassigned'),
    ('right', 'Unassigned'),
]

KMAC_key = None

keyboard_definition = [
    [((4, 4), (0, 0), 'SCANCODE_VOL_DEC'),
     ((4, 4), (0, 1), 'SCANCODE_VOL_INC')],
]

alt_layouts = {}

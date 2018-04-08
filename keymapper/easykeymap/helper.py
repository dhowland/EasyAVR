#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
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

"""Helper functions for creating the more complex data structures in EasyAVR
board config files.  These functions are usually not perfect.  Some keyboard
configurations are too complex to represent with these functions, but it
many keyboards, especially hand-wired keyboards, these are sufficient.
"""

import copy

from .ioports import LED_DRIVER_PULLDOWN
from .templates import num_ports


def make_matrix_config(strobe_cols, strobe_low, rows, cols, device):
    """Utility function for use in keyboard config files.  The inputs
    specify the pin configuration of the matrix, and the return value
    is a tuple with the following required config parameters:
    matrix_hardware, matrix_strobe, and matrix_sense.
    """
    ports = num_ports[device]

    if strobe_cols:
        strobe_set = cols
        sense_set = rows
    else:
        strobe_set = rows
        sense_set = cols

    port_masks = [0] * ports
    dir_masks = [0] * ports
    for pin in strobe_set:
        port_masks[pin[0]] |= (1 << pin[1])
        dir_masks[pin[0]] |= (1 << pin[1])
    for pin in sense_set:
        port_masks[pin[0]] |= (1 << pin[1])
    matrix_hardware = [(p, d) for p, d in zip(port_masks, dir_masks)]

    matrix_strobe = []
    if strobe_low:
        default_state = copy.copy(dir_masks)
    else:
        default_state = [0] * ports
    for pin in strobe_set:
        strobe_state = copy.copy(default_state)
        if strobe_low:
            strobe_state[pin[0]] &= ~(1 << pin[1])
        else:
            strobe_state[pin[0]] |= (1 << pin[1])
        matrix_strobe.append(tuple(strobe_state))

    matrix_sense = []
    for pin in sense_set:
        matrix_sense.append((pin[0], (1 << pin[1])))

    return (matrix_hardware, matrix_strobe, matrix_sense)


def make_led_config(led_pins=[], led_dir=LED_DRIVER_PULLDOWN,
                    backlight_pins=[], backlight_dir=LED_DRIVER_PULLDOWN):
    """Utility function for use in keyboard config files.  The inputs
    specify the pin configuration of the LEDs and backlights, and the
    return value is a tuple with the following required config parameters:
    num_leds, num_ind, led_hardware, backlighting, num_bl_enab, bl_modes.
    """
    num_ind = len(led_pins)
    num_leds = num_ind + len(backlight_pins)

    led_hardware = []
    for port, pin in led_pins:
        led_hardware.append((port, pin, led_dir))
    for port, pin in backlight_pins:
        led_hardware.append((port, pin, backlight_dir))

    backlighting = (len(backlight_pins) > 0)
    num_bl_enab = 2
    bl_modes = [
        ((1,) * num_leds),
        ((0,) * num_leds)
    ]

    return (num_leds, num_ind, led_hardware, backlighting, num_bl_enab, bl_modes)

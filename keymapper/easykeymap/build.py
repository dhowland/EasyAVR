#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2018 David Howland
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

"""Functions for building keymap data into a binary overlay."""

from array import array

from .descriptors import confdesc_size, update_descriptor
from .macroparse import parse, MacroException
from .pkgdata import get_pkg_path
from .scancodes import scancodes
from .templates import matrix_dims, macro_lengths, max_leds
from .version import version_string
import easykeymap.intelhex as intelhex


NUM_LAYERS = 10

NUM_MACROS = 16

NULL_SYMBOL = '0'

TEENSY2_BOOT_PTR_HIGH_BYTE = 0x3F
TEENSY2PP_BOOT_PTR_HIGH_BYTE = 0xFE

FIRST_FN_CODE = 0xF0

key_modes = ['Normal', 'Toggle', 'Tap Key', 'Lockable', 'Rapid Fire']
key_mode_map = {'Normal': 0x00, 'Toggle': 0x01, 'Tap Key': 0x04,
                'Lockable': 0x02, 'Rapid Fire': 0x08}

with_mods = ['R_Shift', 'R_Ctrl', 'R_Alt', 'R_GUI']
with_mods_map = {'R_Shift': 0x20, 'R_Ctrl': 0x10, 'R_Alt': 0x40, 'R_GUI': 0x80}

# Poor man's bi-directional Enumerations
# string from int: list[int]
# int from string: list.index(string)
led_modes = ['Disabled', 'Indicator', 'Backlight']
led_assignments = ['Num Lock', 'Caps Lock', 'Scroll Lock',
                   'Compose', 'Kana', 'Win Lock', 'Fn1 Active',
                   'Fn2 Active', 'Fn3 Active', 'Fn4 Active',
                   'Fn5 Active', 'Fn6 Active', 'Fn7 Active',
                   'Fn8 Active', 'Fn9 Active', 'Any Fn Active',
                   'Recording', 'USB Init', 'USB Error',
                   'USB Suspend', 'USB Normal', 'KB Lock']

# USB HID keyboard spec defines 5 LED indicators
num_led_layers = 5


def check_for_boot(user_data):
    """Returns True if the layout in `user_data` contains a key bound to SCANCODE_BOOT
    or if the hardware has a boot key/button, otherwise returns False.
    """
    if user_data.config.hw_boot_key:
        return True
    for layer in user_data.keymap:
        for row in layer:
            for key in row:
                if key.code == 'SCANCODE_BOOT':
                    return True
    return False


def search_scancodes(user_data, low, high):
    """Returns True if the layout in `user_data` contains a key bound to a scancode in
    the range (low, high) inclusive, otherwise returns False.
    """
    for layer in user_data.keymap:
        for row in layer:
            for key in row:
                value = scancodes[key.code].value
                if (value >= low) and (value <= high):
                    return True
    return False


def unexpected_mouse(user_data):
    """Returns True if the layout in `user_data` contains a key bound to a mouse
    function while the mouse endpoint is disabled, otherwise returns False.
    """
    if user_data.usb_opts.mouse is True:
        return False
    low = scancodes['SCANCODE_MOUSE1'].value
    high = scancodes['SCANCODE_MOUSEYD'].value
    return search_scancodes(user_data, low, high)


def unexpected_media(user_data):
    """Returns True if the layout in `user_data` contains a key bound to a media or
    power function while the media endpoint is disabled, otherwise returns False.
    """
    if user_data.usb_opts.media is True:
        return False
    low = scancodes['SCANCODE_NEXT_TRACK'].value
    high = scancodes['SCANCODE_FAVES'].value
    if search_scancodes(user_data, low, high):
        return True
    low = scancodes['SCANCODE_POWER'].value
    high = scancodes['SCANCODE_WAKE'].value
    return search_scancodes(user_data, low, high)


def build_firmware(user_data, path, external_data):
    """Uses the layout and other settings from `user_data` to modify a firmware build,
    and saves the result to `path`.  The output will be in Intel Hex format unless the
    path ends with .bin, in which case it will be binary.  `external_data` contains
    a map with any data the build process might need that isn't stored in user_data.
    """
    hex_path = get_pkg_path('builds/' + user_data.config.firmware.hex_file_name)
    with open(hex_path, 'r') as fdin:
        hex_data = intelhex.read(fdin)
        overlay(user_data, hex_data, external_data)
    if path.lower().endswith('.bin'):
        with open(path, 'wb') as fdout:
            # shouldn't get more than one chunk per file
            start, byte_array = hex_data[0]
            byte_array.tofile(fdout)
    else:
        with open(path, 'w') as fdout:
            intelhex.write(fdout, hex_data)


def overlay(user_data, hex_data, external_data):
    overlay_keymap(user_data, hex_data)
    overlay_matrix(user_data, hex_data)
    overlay_macros(user_data, hex_data, external_data)
    overlay_leds(user_data, hex_data)
    overlay_backlight(user_data, hex_data)
    overlay_led_layers(user_data, hex_data)
    overlay_descriptor(user_data, hex_data)
    overlay_misc(user_data, hex_data)


def overlay_keymap(user_data, hex_data):
    config = user_data.config
    start, byte_array = hex_data[0]
    # overwrite data for key maps
    fw_rows, fw_cols = matrix_dims[config.firmware.size]
    col_diff = fw_cols - config.num_cols
    row_diff = (fw_rows - config.num_rows) * fw_cols
    l_offset = config.firmware.layers_map - start
    a_offset = config.firmware.actions_map - start
    t_offset = config.firmware.tapkeys_map - start
    for layer in user_data.keymap:
        for row in layer:
            for key in row:
                byte_array[l_offset] = scancodes[key.code].value
                byte_array[a_offset] = (key.mode | key.wmods)
                byte_array[t_offset] = scancodes[key.tap].value
                l_offset += 1
                a_offset += 1
                t_offset += 1
            l_offset += col_diff
            a_offset += col_diff
            t_offset += col_diff
        l_offset += row_diff
        a_offset += row_diff
        t_offset += row_diff


def overlay_matrix(user_data, hex_data):
    config = user_data.config
    start, byte_array = hex_data[0]
    # overwrite data for matrix style
    if config.strobe_cols:
        offset = config.firmware.strobe_cols_map - start
        byte_array[offset] = 1
    if config.strobe_low:
        offset = config.firmware.strobe_low_map - start
        byte_array[offset] = 1
    # overwrite data for matrix size
    if config.strobe_cols:
        num_strobe = config.num_cols
        num_sense = config.num_rows
    else:
        num_strobe = config.num_rows
        num_sense = config.num_cols
    offset = config.firmware.num_strobe_map - start
    byte_array[offset] = num_strobe
    offset = config.firmware.num_sense_map - start
    byte_array[offset] = num_sense
    # overwrite data for matrix definition
    offset = config.firmware.matrix_init_map - start
    for port_def in config.matrix_hardware:
        for mask in port_def:
            byte_array[offset] = mask
            offset += 1
    # overwrite data for matrix strobe list
    offset = config.firmware.matrix_strobe_map - start
    for strobe in config.matrix_strobe:
        for mask in strobe:
            byte_array[offset] = mask
            offset += 1
    # overwrite data for matrix sense list
    offset = config.firmware.matrix_sense_map - start
    for sense in config.matrix_sense:
        for mask in sense:
            byte_array[offset] = mask
            offset += 1
    # overwrite row/col for the weird "KMAC" key
    if config.KMAC_key is not None:
        offset = config.firmware.kmac_key_map - start
        for b in config.KMAC_key:
            byte_array[offset] = b
            offset += 1


def overlay_macros(user_data, hex_data, external_data):
    config = user_data.config
    start, byte_array = hex_data[0]
    macro_length = macro_lengths[config.firmware.device]
    # convert all the macros to byte arrays and get the length of each
    macro_data = [parse(m, external_data=external_data) for m in user_data.macros]
    mlens = [len(d) for d in macro_data]
    # figure out where the macros will fit inside the buffer
    index = NUM_MACROS
    index_list = []
    for mlen in mlens:
        if mlen <= 0:
            index_list.append(macro_length-1)
        else:
            index_list.append(index)
            index += ((mlen // 2) + 1)
            if index >= macro_length:
                raise MacroException("The macros have exceeded the allowable size.")
    if len(index_list) != NUM_MACROS:
        raise MacroException("The macro data is an inconsistent size.")
    # map the index table into the byte array
    offset = config.firmware.macro_map - start
    for index in index_list:
        short_array = array('H', [index])
        byte_array[offset:offset+2] = array('B', short_array.tostring())
        offset += 2
    # map the non-empty macros into the byte array
    for i in range(NUM_MACROS):
        if mlens[i] > 0:
            end = offset + mlens[i]
            byte_array[offset:end] = macro_data[i]
            byte_array[end:end+2] = array('B', [0, 0])
            offset += (mlens[i] + 2)
    # make sure the last spot of the byte array has a zero (terminator)
    last_spot = ((config.firmware.macro_map - start) + ((macro_length - 1) * 2))
    byte_array[last_spot:last_spot+2] = array('B', [0, 0])


def overlay_leds(user_data, hex_data):
    config = user_data.config
    start, byte_array = hex_data[0]
    # overwrite data for LED counts
    offset = config.firmware.num_leds_map - start
    byte_array[offset] = config.num_leds
    offset = config.firmware.num_ind_map - start
    byte_array[offset] = config.num_ind
    # overwrite data for LED IO list
    offset = config.firmware.led_hw_map - start
    for port, pin, direction in config.led_hardware:
        byte_array[offset] = port
        offset += 1
        byte_array[offset] = pin
        offset += 1
        byte_array[offset] = direction
        offset += 1
    # overwrite data for LED functions
    offset = config.firmware.led_map - start
    for tup in user_data.led_funcs:
        byte_array[offset] = tup[0]
        offset += 1
        byte_array[offset] = tup[1]
        offset += 1


def overlay_backlight(user_data, hex_data):
    config = user_data.config
    start, byte_array = hex_data[0]
    if config.firmware.num_bl_enab_map is not None:
        # overwrite data for backlight enables count
        offset = config.firmware.num_bl_enab_map - start
        byte_array[offset] = config.num_bl_enab
        # overwrite data for backlight mask
        offset = config.firmware.bl_mask_map - start
        for mode in user_data.led_modes:
            if mode == led_modes.index('Backlight'):
                byte_array[offset] = 1
            else:
                byte_array[offset] = 0
            offset += 1
        for i in range(config.num_leds - config.num_ind):
            byte_array[offset] = 1
            offset += 1
        # overwrite data for backlight enables
        led_diff = max_leds - config.num_leds
        offset = config.firmware.bl_mode_map - start
        for mode in config.bl_modes:
            for led in mode:
                byte_array[offset] = led
                offset += 1
            offset += led_diff


def overlay_led_layers(user_data, hex_data):
    config = user_data.config
    start, byte_array = hex_data[0]
    # overwrite data for led layers
    offset = config.firmware.led_layers_map - start
    for layer in user_data.led_layers:
        if layer:
            byte_array[offset] = FIRST_FN_CODE + layer
        else:
            byte_array[offset] = 0
        offset += 1


def overlay_descriptor(user_data, hex_data):
    config = user_data.config
    start, byte_array = hex_data[0]
    # overwrite data for USB endpoint enables
    offset = config.firmware.endpoint_opt_map - start
    opts = sum([(int(x) * (2**i)) for i, x in enumerate(user_data.usb_opts)])
    byte_array[offset] = opts
    # overwrite data for USB HID config descriptor
    offset = config.firmware.conf_desc_map - start
    default_desc = byte_array[offset:(offset+confdesc_size)]
    updated_desc = update_descriptor(default_desc, user_data.usb_opts)
    byte_array[offset:(offset+confdesc_size)] = array('B', updated_desc)


def overlay_misc(user_data, hex_data):
    config = user_data.config
    start, byte_array = hex_data[0]
    # overwrite data for teensy bootloader pointer
    if config.teensy:
        offset = config.firmware.boot_ptr_map - start + 1
        if config.firmware.device == "AT90USB1286":
            byte_array[offset] = TEENSY2PP_BOOT_PTR_HIGH_BYTE
        else:
            byte_array[offset] = TEENSY2_BOOT_PTR_HIGH_BYTE
    # overwrite data for version number
    offset = config.firmware.prod_str_map - start
    while byte_array[offset] != ord('#'):
        offset += 1
    for c in version_string:
        byte_array[offset] = ord(c)
        offset += 2

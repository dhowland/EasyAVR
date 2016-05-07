#!/usr/bin/env python
#
# Easy AVR USB Keyboard Firmware
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

"""Compile all hardware configurations and incorporate the binaries into
the keymapper application.
"""

from __future__ import print_function

import os
import os.path
import shutil
import re
import sys
import subprocess

proj_dir = "firmware"
hex_dir = "keymapper\\easykeymap\\builds"
templates_dir = "keymapper\\easykeymap\\templates"
output_dir = os.path.join(proj_dir, "Release")
hex_file_name = "autobuild.hex"
map_file_name = "autobuild.map"
hex_path = os.path.join(output_dir, hex_file_name)
map_path = os.path.join(output_dir, map_file_name)
in_proj_path = os.path.join(proj_dir, "firmware.cproj")
out_proj_path = os.path.join(proj_dir, "autobuild.cproj")
log_path = os.path.join(proj_dir, "log.txt")
componentinfo_path = os.path.join(proj_dir, "autobuild.componentinfo.xml")

hardware_table = [
    ("ATmega32U4", "16000000UL", "BOARD_SIZE_COSTAR"),
    ("ATmega32U4", "16000000UL", "BOARD_SIZE_TKL"),
    ("ATmega32U4", "16000000UL", "BOARD_SIZE_SIXTY"),
    ("ATmega32U4", "16000000UL", "BOARD_SIZE_PAD"),
    ("ATmega32U4", "16000000UL", "BOARD_SIZE_CARD"),
    ("ATmega32U2", "16000000UL", "BOARD_SIZE_COSTAR"),
    ("ATmega16U2", "16000000UL", "BOARD_SIZE_CARD"),
    ("AT90USB1286", "16000000UL", "BOARD_SIZE_COSTAR"),
    ("AT90USB1286", "16000000UL", "BOARD_SIZE_FULLSIZE"),
    ("AT90USB1286", "16000000UL", "BOARD_SIZE_JUMBO"),
    ("AT90USB1286", "8000000UL", "BOARD_SIZE_FULLSIZE"),
    ("ATmega32U4", "8000000UL", "BOARD_SIZE_TKL"),
]

translation_table = [
    r"ATmega\d+U\d",
    r"[168]+000000UL",
    r"BOARD_SIZE_[A-Z]+",
]

def write_symbol(outfile, symtable, symbol):
    try:
        outfile.write(symtable[symbol])
    except KeyError:
        outfile.write("None")

for hw in hardware_table:

    hardware_specs = (hw[0], hw[1].replace('000000UL','') + 'MHz', hw[2].replace('BOARD_SIZE_',''))
    hardware_name = "%s_%s_%s.hex" % hardware_specs
    print(hardware_name)

    with open(out_proj_path, 'w') as outfile:
        with open(in_proj_path, 'r') as infile:
            for line in infile:
                for subst,pattern in zip(hw, translation_table):
                    line = re.sub(pattern, subst, line, flags=re.I)
                outfile.write(line)

    subprocess.call("compile.bat")

    if os.path.exists(hex_path):
        os.remove(out_proj_path)
        os.remove(log_path)
        os.remove(componentinfo_path)
    else:
        print("Failed.")
        sys.exit(1)

    print("Copying in HEX file")
    target_path = os.path.join(hex_dir, hardware_name)
    if os.path.exists(target_path):
        os.remove(target_path)
    shutil.copy2(hex_path, target_path)

    print("Parsing MAP file")
    regex = re.compile(r"^\s+(0x[0-9a-f]{8})\s+(\w+)$")
    symbols = {}
    with open(map_path, 'r') as infile:
        for line in infile:
            match = regex.match(line)
            if match:
                symbols[match.group(2)] = match.group(1)

    print("Updating config source")
    template_name = "%s_%s_%s.py" % hardware_specs
    with open(os.path.join(templates_dir, template_name), 'w') as outfile:
        outfile.write("# This file is auto-generated.  Do not edit.\n\n")
        outfile.write("hex_file_name = '")
        outfile.write(hardware_name)
        outfile.write("'\ndevice = '")
        outfile.write(hardware_specs[0])
        outfile.write("'\nspeed = '")
        outfile.write(hardware_specs[1])
        outfile.write("'\nsize = '")
        outfile.write(hardware_specs[2])
        outfile.write("'\n\nlayers_map = ")
        write_symbol(outfile, symbols, 'LAYERS')
        outfile.write("\nactions_map = ")
        write_symbol(outfile, symbols, 'ACTIONS')
        outfile.write("\ntapkeys_map = ")
        write_symbol(outfile, symbols, 'TAPKEYS')
        outfile.write("\nmacro_map = ")
        write_symbol(outfile, symbols, 'MACRO_BUFFER')
        outfile.write("\nled_layers_map = ")
        write_symbol(outfile, symbols, 'LED_LAYERS')
        outfile.write("\nnum_leds_map = ")
        write_symbol(outfile, symbols, 'NUMBER_OF_LEDS')
        outfile.write("\nnum_ind_map = ")
        write_symbol(outfile, symbols, 'NUMBER_OF_INDICATORS')
        outfile.write("\nled_hw_map = ")
        write_symbol(outfile, symbols, 'LEDS_LIST')
        outfile.write("\nled_map = ")
        write_symbol(outfile, symbols, 'LED_FN')
        outfile.write("\nnum_bl_enab_map = ")
        write_symbol(outfile, symbols, 'NUMBER_OF_BACKLIGHT_ENABLES')
        outfile.write("\nbl_mask_map = ")
        write_symbol(outfile, symbols, 'BACKLIGHT_MASK')
        outfile.write("\nbl_mode_map = ")
        write_symbol(outfile, symbols, 'BLMODE_LIST')
        outfile.write("\nstrobe_cols_map = ")
        write_symbol(outfile, symbols, 'STROBE_COLS')
        outfile.write("\nstrobe_low_map = ")
        write_symbol(outfile, symbols, 'STROBE_LOW')
        outfile.write("\nnum_strobe_map = ")
        write_symbol(outfile, symbols, 'NUMBER_OF_STROBE')
        outfile.write("\nnum_sense_map = ")
        write_symbol(outfile, symbols, 'NUMBER_OF_SENSE')
        outfile.write("\nmatrix_init_map = ")
        write_symbol(outfile, symbols, 'MATRIX_INIT_LIST')
        outfile.write("\nmatrix_strobe_map = ")
        write_symbol(outfile, symbols, 'MATRIX_STROBE_LIST')
        outfile.write("\nmatrix_sense_map = ")
        write_symbol(outfile, symbols, 'MATRIX_SENSE_LIST')
        outfile.write("\nkmac_key_map = ")
        write_symbol(outfile, symbols, 'KMAC_KEY')
        outfile.write("\npw_defs_map = ")
        write_symbol(outfile, symbols, 'PWDEFS')
        outfile.write("\nboot_ptr_map = ")
        write_symbol(outfile, symbols, 'BOOTLOADER')
        outfile.write("\nprod_str_map = ")
        write_symbol(outfile, symbols, 'ProductString')
        outfile.write("\n")

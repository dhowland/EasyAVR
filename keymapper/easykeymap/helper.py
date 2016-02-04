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

import copy

from easykeymap.templates import num_ports

def make_matrix_config(strobe_cols, strobe_low, rows, cols, device):
    ports = num_ports[device]
    
    if strobe_cols:
        strobe_set = cols
        sense_set = rows
    else:
        strobe_set = rows
        sense_set = cols
    
    port_masks = [ 0 ] * ports
    dir_masks = [ 0 ] * ports
    for pin in strobe_set:
        port_masks[pin[0]] |= (1 << pin[1])
        dir_masks[pin[0]] |= (1 << pin[1])
    for pin in sense_set:
        port_masks[pin[0]] |= (1 << pin[1])
    matrix_hardware = [ (p, d) for p, d in zip(port_masks, dir_masks)]
    
    matrix_strobe = []
    if strobe_low:
        default_state = copy.copy(dir_masks)
    else:
        default_state = [ 0 ] * ports
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

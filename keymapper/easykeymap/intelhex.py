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

"""Intel HEX file parser/emitter.

Data object format is a list of tuples, each with a start address and an array
object containing the data bytes:
[(address1, array1), (address2, array2) ...]

Description of the Intel HEX format:

:ccaaaarrddss
:     Start-of-line colon
cc    The byte-count, 2 digits, counting the actual data bytes in the record
aaaa  The address field, 4 digits, the first address to be used by this record
rr    Record type, 2 digits, indicates the record type
dd    The actual data of this record
ss    Checksum, 2 digits, cc+aaH+aaL+rr+sum(dd)+ss=0

Record types
00 = Data Record
01 = End Of File Record
02 = Extended Segment Address Record
03 = Start Segment Address Record
04 = Extended Linear Address Record
05 = Start Linear Address Record.

"""

from array import array


def read(hex_file):
    """Read `hex_file` and return an array of bytes.  `hex_file` should be an
    opened text file (or file-like object).
    """
    if not ((hasattr(hex_file, '__iter__')) and (hasattr(hex_file, 'read'))):
        raise Exception("Not a valid file-like object")
    data = []
    prev_addr = -1
    block = None
    for i, line in enumerate(hex_file):
        line = line.strip()
        if line[0] != ':':
            continue
        if checksum(parse(line[1:])) != 0:
            raise Exception("HEX data has invalid checksum at line %d" % i)
        num_chars = int(line[1:3], 16) * 2
        address = int(line[3:7], 16)
        if line[7:9] == '00':
            div_data = line[9:(9+num_chars)]
            byte_array = array('B', parse(div_data))
            if address != prev_addr:
                block = array('B')
                data.append((address, block))
                block.extend(byte_array)
                prev_addr = address + len(byte_array)
            else:
                block.extend(byte_array)
                prev_addr += len(byte_array)
        elif line[7:9] == '01':
            pass
        else:
            raise Exception("Record type not supported at line %d" % i)
    return data


def write(hex_file, data):
    """Write the array of bytes in data to `hex_file`.  `hex_file` should be
    an opened text file (or file-like object).
    """
    if not (hasattr(hex_file, 'write')):
        raise Exception("Not a valid file-like object")
    for address, byte_array in data:
        for chunk in [byte_array[x:x+16] for x in range(0, len(byte_array), 16)]:
            bstr = ''.join([("%02X" % x) for x in chunk])
            line = "%02X%04X00%s" % (len(chunk), address, bstr)
            chks = antichecksum(parse(line))
            hex_file.write(":%s%s\n" % (line, chks))
            address += len(chunk)
    hex_file.write(":00000001FF\n")


def parse(string):
    return [int(string[x:x+2], 16) for x in range(0, len(string), 2)]


def checksum(lst):
    chksum = sum(lst)
    return (chksum & 0xFF)


def antichecksum(lst):
    return "%02X" % ((0x100 - checksum(lst)) & 0xFF)

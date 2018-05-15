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

"""This module contains code for parsing the macro mini-language and converting strings to
a sequence of scancodes as required by the EasyAVR firmware.
"""

from array import array
import re

from .scancodes import scancodes, char_map


class MacroException(Exception):
    """Raised when an error is encountered while parsing a macro string."""
    pass


modmap = {
    "CTRL": 1,
    "LCTRL": 1,
    "SHIFT": 2,
    "LSHIFT": 2,
    "ALT": 4,
    "OPTION": 4,
    "LALT": 4,
    "GUI": 8,
    "WIN": 8,
    "COMMAND": 8,
    "META": 8,
    "LGUI": 8,
    "LWIN": 8,
    "RCTRL": 16,
    "RSHIFT": 32,
    "ALTGR": 64,
    "RALT": 64,
    "RGUI": 128,
    "RWIN": 128,
}

kpmap = {
    '/': "KPSLA",
    '*': "KPAST",
    '-': "KPMIN",
    '+': "KPPLS",
    '\n': "KPENT",
    '1': "KP1",
    '2': "KP2",
    '3': "KP3",
    '4': "KP4",
    '5': "KP5",
    '6': "KP6",
    '7': "KP7",
    '8': "KP8",
    '9': "KP9",
    '0': "KP0",
    '.': "KPDOT"
}


def waitparse(input_string, external_data):
    try:
        n = int(input_string)
        assert(n >= 0)
        assert(n <= 255)
    except Exception:
        raise MacroException("The WAIT function requires an integer between "
                             "0 and 255.")
    # use HID_KEYBOARD_SC_ERROR_ROLLOVER as the scancode for WAIT
    return (1, n)


def hintparse(input_string, external_data):
    try:
        n = int(input_string)
        assert(n >= 0)
        assert(n <= 9)
    except Exception:
        raise MacroException("The HINT function requires an integer between "
                             "0 and 9.")
    try:
        layermap = external_data['hints'][n]
    except Exception:
        raise MacroException("The HINT function requires a list of strings in "
                             "the external_data map.")
    return parse(layermap.replace('$', '$$'))


funcs = {
    "WAIT": waitparse,
    "HINT": hintparse
}


def parse(macro_string, modval=0, external_data=None):
    """Take the string from `macro_string` and convert it to a sequence of scancodes.  The string
    is interpreted using the macro mini-language.  This is a recursive function, so macro
    functions that contain substrings will cause another call to this function with the bit
    packed modifier word in `modval`.  Layer hints are expected in `external_data['hints']`.
    """
    data = array('B')
    escaping = False
    esc_string = ""
    subbing = False
    sub_string = ""
    sub_modval = modval
    nested = 0
    func_input = None
    is_alt_code = isaltcode(macro_string, modval)
    for c in macro_string:
        if escaping:
            if c == '{':
                continue
            elif c == '(':
                if esc_string in modmap:
                    sub_modval = modval | modmap[esc_string]
                elif esc_string in funcs:
                    func_input = esc_string
                else:
                    raise MacroException("Substrings must be preceded by "
                                         "a mod key or function.")
                escaping = False
                subbing = True
                sub_string = ""
                nested += 1
            elif c == '$':
                escaping = False
                data.extend(emit(modval, '$'))
            elif re.match(r"[A-Za-z0-9_]", c):
                esc_string = esc_string + c.upper()
            else:
                # c is } or any other character besides { and ( that can't be a keyword
                escaping = False
                if esc_string in modmap:
                    raise MacroException("Mod keys must be followed by a '('.")
                elif esc_string in funcs:
                    raise MacroException("Functions must be followed by a '('.")
                else:
                    data.extend(emit(modval, esc_string))
        elif subbing:
            if c == '(':
                nested += 1
                sub_string = sub_string + c
            elif c == ')':
                nested -= 1
                if nested == 0:
                    subbing = False
                    if func_input:
                        data.extend(funcs[func_input](sub_string, external_data))
                        func_input = None
                    else:
                        data.extend(parse(sub_string, sub_modval))
                else:
                    sub_string = sub_string + c
            else:
                sub_string = sub_string + c
        else:
            if c == '$':
                escaping = True
                esc_string = ""
            else:
                if is_alt_code:
                    try:
                        c = kpmap[c]
                    except KeyError:
                        pass
                data.extend(emit(modval, c))
    if escaping:
        raise MacroException("Unclosed escape character.")
    if subbing:
        raise MacroException("Unclosed substring.")
    if (modval != 0) and (len(data) == 0):
        data.extend(emit(modval, 0))
    return data


def isaltcode(macro_string, modval):
    """This function attempts to recognize 'Alt codes', which have to be entered
    with the keypad instead of the number row.  Windows recognizes several types
    of codes, so the trick is to catch them without modifying a combination that
    the user intended for the number row.
    """
    # '+' followed by a hex number
    if re.match(r"^\+[0-9a-fA-F]{1,4}$", macro_string):
        # if either of the ALT keys is pressed and no other mods
        if (modval == modmap['LALT']) or (modval == modmap['RALT']):
            return True
    # two to three digit decimal number, possibly preceded by zero
    elif re.match(r"^0?[0-9]{2,3}$", macro_string):
        # if either of the ALT keys is pressed and no other mods
        if (modval == modmap['LALT']) or (modval == modmap['RALT']):
            return True
    # single decimal digit, larger than zero
    elif re.match(r"^[1-9]$", macro_string):
        # if the Left ALT keys is pressed and no other mods
        if modval == modmap['LALT']:
            return True
        # Right ALT plus a single number is assumed to be a AltGr usage
    return False


def emit(modval, macro_char):
    shift_is_pressed = ((modval & (modmap['LSHIFT'] | modmap['RSHIFT'])) != 0)
    try:
        scancode = char_map[macro_char][0]
        shift_needed = char_map[macro_char][1]
    except KeyError:
        raise MacroException("Unrecognized escape sequence '%s'." % macro_char)
    if (shift_needed) and (not shift_is_pressed):
        effective_modval = modval | modmap['SHIFT']
    else:
        effective_modval = modval
    return (scancodes[scancode][1], effective_modval)

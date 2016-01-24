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

from __future__ import print_function

import re
from array import array

from easykeymap.scancodes import scancodes, char_map

modmap = {
    "CTRL": 1,
    "SHIFT": 2,
    "ALT": 4,
    "WIN": 8,
    "LCTRL": 1,
    "LSHIFT": 2,
    "LALT": 4,
    "LWIN": 8,
    "RCTRL": 16,
    "RSHIFT": 32,
    "RALT": 64,
    "RWIN": 128
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

DEBUG = False


def waitparse(input_string, externaldata):
    try:
        n = int(input_string)
        assert(n >= 0)
        assert(n <= 255)
    except:
        raise Exception("The WAIT function requires an integer between "
                        "0 and 255.")
    # use HID_KEYBOARD_SC_ERROR_ROLLOVER as the scancode for WAIT
    return (1, n)


def hintparse(input_string, externaldata):
    try:
        n = int(input_string)
        assert(n >= 0)
        assert(n <= 9)
    except:
        raise Exception("The HINT function requires an integer between "
                        "0 and 9.")
    layermap = externaldata['hints'][n]
    return parse(layermap.replace('\\','\\\\,'))

funcs = {
    "WAIT": waitparse,
    "HINT": hintparse
}


def parse(macro_string, modval=0, externaldata={}):
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
            if c == ',':
                escaping = False
                if esc_string in modmap:
                    raise Exception("Mod keys must be followed by a '('.")
                elif esc_string in funcs:
                    raise Exception("Functions must be followed by a '('.")
                else:
                    if esc_string == 'n':
                        esc_string = '\n'
                    if esc_string == 't':
                        esc_string = '\t'
                    data.extend(emit(modval, esc_string))
            elif c == '(':
                if esc_string in modmap:
                    sub_modval = modval | modmap[esc_string]
                elif esc_string in funcs:
                    func_input = esc_string
                else:
                    raise Exception("Substrings must be preceded by "
                                    "a mod key or function.")
                escaping = False
                subbing = True
                sub_string = ""
                nested += 1
            else:
                esc_string = esc_string + c
        elif subbing:
            if c == '(':
                nested += 1
                sub_string = sub_string + c
            elif c == ')':
                nested -= 1
                if nested == 0:
                    subbing = False
                    if func_input:
                        data.extend(funcs[func_input](sub_string, externaldata))
                        func_input = None
                    else:
                        data.extend(parse(sub_string, sub_modval))
                else:
                    sub_string = sub_string + c
            else:
                sub_string = sub_string + c
        else:
            if c == '\\':
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
        raise Exception("Unclosed escape character.")
    if subbing:
        raise Exception("Unclosed substring.")
    if (modval != 0) and (len(data) == 0):
        data.extend(emit(modval, 0))
    return data


def isaltcode(macro_string, modval):
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
        raise Exception("Unrecognized escape sequence '%s'." % macro_char)
    if (shift_needed) and (not shift_is_pressed):
        effective_modval = modval | modmap['SHIFT']
    else:
        effective_modval = modval
    if DEBUG:
        if effective_modval == 0:
            print("%s," % (scancode,))
        elif scancode == '0':
            print("%#04x00," % (effective_modval,))
        else:
            print("(%#04x00 | %s)," % (effective_modval, scancode))
    return (scancodes[scancode][1], effective_modval)

if __name__ == '__main__':
    DEBUG = True
    s = "the quick brown fox jumps over the lazy dog.,/;'[]"
    parse(s)
    s = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG><?:\"{}"
    parse(s)
    s = "\\ENTER,\MUTE,\F4,\BKSP,\ESC,\CAPSLK,\DOWN,"
    parse(s)
    s = "\\n,\\t,\\\\,"
    parse(s)
    s = "\\SHIFT(test)"
    parse(s)
    s = "\\CTRL(\\ALT(\\DEL,))"
    parse(s)
    s = "\\RSHIFT(nocaps CAPS)"
    parse(s)
    s = "\\ALT(one \\WIN(two) \\CTRL(three))"
    parse(s)
    s = "\\RSHIFT()\\RWIN(\\LWIN())"
    parse(s)
    s = "\\ALT(62)"
    parse(s)
    s = "\\ALT(0162)"
    parse(s)
    s = "\\ALT(+11b)"
    parse(s)
    s = "\\RALT(2)"
    parse(s)

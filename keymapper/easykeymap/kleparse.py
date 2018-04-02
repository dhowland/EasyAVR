#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
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

"""Parse JSON files from http://www.keyboard-layout-editor.com and convert
to an EasyAVR layout data structure.  The conversion is not complete, because
layouts from KLE don't contain enough information to completely define a board.
This whole thing is a total hack-job.  It is not meant to be a perfect solution,
it is only meant to be a quick way to start adding support for a new board.
"""

import json

from .build import NULL_SYMBOL


# All default legends from the ANSI104 and ISO105 predefined layouts.
conversion_table = {
    "A": "HID_KEYBOARD_SC_A",
    "B": "HID_KEYBOARD_SC_B",
    "C": "HID_KEYBOARD_SC_C",
    "D": "HID_KEYBOARD_SC_D",
    "E": "HID_KEYBOARD_SC_E",
    "F": "HID_KEYBOARD_SC_F",
    "G": "HID_KEYBOARD_SC_G",
    "H": "HID_KEYBOARD_SC_H",
    "I": "HID_KEYBOARD_SC_I",
    "J": "HID_KEYBOARD_SC_J",
    "K": "HID_KEYBOARD_SC_K",
    "L": "HID_KEYBOARD_SC_L",
    "M": "HID_KEYBOARD_SC_M",
    "N": "HID_KEYBOARD_SC_N",
    "O": "HID_KEYBOARD_SC_O",
    "P": "HID_KEYBOARD_SC_P",
    "Q": "HID_KEYBOARD_SC_Q",
    "R": "HID_KEYBOARD_SC_R",
    "S": "HID_KEYBOARD_SC_S",
    "T": "HID_KEYBOARD_SC_T",
    "U": "HID_KEYBOARD_SC_U",
    "V": "HID_KEYBOARD_SC_V",
    "W": "HID_KEYBOARD_SC_W",
    "X": "HID_KEYBOARD_SC_X",
    "Y": "HID_KEYBOARD_SC_Y",
    "Z": "HID_KEYBOARD_SC_Z",
    "!\n1": "HID_KEYBOARD_SC_1_AND_EXCLAMATION",
    "@\n2": "HID_KEYBOARD_SC_2_AND_AT",
    "\"\n2": "HID_KEYBOARD_SC_2_AND_AT",
    "#\n3": "HID_KEYBOARD_SC_3_AND_HASHMARK",
    "£\n3": "HID_KEYBOARD_SC_3_AND_HASHMARK",
    "$\n4": "HID_KEYBOARD_SC_4_AND_DOLLAR",
    "%\n5": "HID_KEYBOARD_SC_5_AND_PERCENTAGE",
    "^\n6": "HID_KEYBOARD_SC_6_AND_CARET",
    "&\n7": "HID_KEYBOARD_SC_7_AND_AND_AMPERSAND",
    "*\n8": "HID_KEYBOARD_SC_8_AND_ASTERISK",
    "(\n9": "HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS",
    ")\n0": "HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS",
    "Enter": "HID_KEYBOARD_SC_ENTER",
    "Esc": "HID_KEYBOARD_SC_ESCAPE",
    "Backspace": "HID_KEYBOARD_SC_BACKSPACE",
    "Tab": "HID_KEYBOARD_SC_TAB",
    " ": "HID_KEYBOARD_SC_SPACE",
    "_\n-": "HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE",
    "+\n=": "HID_KEYBOARD_SC_EQUAL_AND_PLUS",
    "{\n[": "HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE",
    "}\n]": "HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE",
    "|\n\\": "HID_KEYBOARD_SC_BACKSLASH_AND_PIPE",
    "~\n#": "HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE",
    ":\n;": "HID_KEYBOARD_SC_SEMICOLON_AND_COLON",
    "\"\n'": "HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE",
    "@\n'": "HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE",
    "~\n`": "HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE",
    "¬\n`": "HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE",
    "<\n,": "HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN",
    ">\n.": "HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN",
    "?\n/": "HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK",
    "Caps Lock": "HID_KEYBOARD_SC_CAPS_LOCK",
    "F1": "HID_KEYBOARD_SC_F1",
    "F2": "HID_KEYBOARD_SC_F2",
    "F3": "HID_KEYBOARD_SC_F3",
    "F4": "HID_KEYBOARD_SC_F4",
    "F5": "HID_KEYBOARD_SC_F5",
    "F6": "HID_KEYBOARD_SC_F6",
    "F7": "HID_KEYBOARD_SC_F7",
    "F8": "HID_KEYBOARD_SC_F8",
    "F9": "HID_KEYBOARD_SC_F9",
    "F10": "HID_KEYBOARD_SC_F10",
    "F11": "HID_KEYBOARD_SC_F11",
    "F12": "HID_KEYBOARD_SC_F12",
    "PrtSc": "HID_KEYBOARD_SC_PRINT_SCREEN",
    "Scroll Lock": "HID_KEYBOARD_SC_SCROLL_LOCK",
    "Pause\nBreak": "HID_KEYBOARD_SC_PAUSE",
    "Insert": "HID_KEYBOARD_SC_INSERT",
    "Home": "HID_KEYBOARD_SC_HOME",
    "PgUp": "HID_KEYBOARD_SC_PAGE_UP",
    "Delete": "HID_KEYBOARD_SC_DELETE",
    "End": "HID_KEYBOARD_SC_END",
    "PgDn": "HID_KEYBOARD_SC_PAGE_DOWN",
    "→": "HID_KEYBOARD_SC_RIGHT_ARROW",
    "←": "HID_KEYBOARD_SC_LEFT_ARROW",
    "↓": "HID_KEYBOARD_SC_DOWN_ARROW",
    "↑": "HID_KEYBOARD_SC_UP_ARROW",
    "Num Lock": "HID_KEYBOARD_SC_NUM_LOCK",
    "/": "HID_KEYBOARD_SC_KEYPAD_SLASH",
    "*": "HID_KEYBOARD_SC_KEYPAD_ASTERISK",
    "-": "HID_KEYBOARD_SC_KEYPAD_MINUS",
    "+": "HID_KEYBOARD_SC_KEYPAD_PLUS",
    "kpEnter": "HID_KEYBOARD_SC_KEYPAD_ENTER",
    "1\nEnd": "HID_KEYBOARD_SC_KEYPAD_1_AND_END",
    "2\n↓": "HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW",
    "3\nPgDn": "HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN",
    "4\n←": "HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW",
    "5": "HID_KEYBOARD_SC_KEYPAD_5",
    "6\n→": "HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW",
    "7\nHome": "HID_KEYBOARD_SC_KEYPAD_7_AND_HOME",
    "8\n↑": "HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW",
    "9\nPgUp": "HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP",
    "0\nIns": "HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT",
    ".\nDel": "HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE",
    # "|\n\\": "HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE",
    "Menu": "HID_KEYBOARD_SC_APPLICATION",
    "=": "HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN",
    "Ctrl": "HID_KEYBOARD_SC_LEFT_CONTROL",
    "Shift": "HID_KEYBOARD_SC_LEFT_SHIFT",
    "Alt": "HID_KEYBOARD_SC_LEFT_ALT",
    "Win": "HID_KEYBOARD_SC_LEFT_GUI",
    "rCtrl": "HID_KEYBOARD_SC_RIGHT_CONTROL",
    "rShift": "HID_KEYBOARD_SC_RIGHT_SHIFT",
    "AltGr": "HID_KEYBOARD_SC_RIGHT_ALT",
    "rWin": "HID_KEYBOARD_SC_RIGHT_GUI",
}


def convert(s, legend, width=4, height=4):
    """Utility function to make legends less ambiguous."""
    if legend == 'Enter' and width == 4 and height == 8:
        legend = 'kpEnter'
    elif legend == '' and width > 8:
        legend = ' '
    elif legend == 'Ctrl':
        if s['ctrl']:
            legend = 'rCtrl'
        else:
            s['ctrl'] = True
    elif legend == 'Shift':
        if s['shift']:
            legend = 'rShift'
        else:
            s['shift'] = True
    elif legend == 'Alt':
        if s['alt']:
            legend = 'AltGr'
        else:
            s['alt'] = True
    elif legend == 'Win':
        if s['win']:
            legend = 'rWin'
        else:
            s['win'] = True
    try:
        return conversion_table[legend]
    except KeyError:
        return NULL_SYMBOL


def parse(path):
    """Open the JSON file at `path` and return a structure of the layout for
    use in EasyAVR board config files.
    """
    with open(path, encoding="utf8") as fp:
        jslayout = json.load(fp)

    state = {
        'ctrl': False,
        'shift': False,
        'alt': False,
        'win': False,
    }

    width = 4
    height = 4
    maxwidth = 0
    totalwidth = 0
    totalheight = 0
    rownum = 0
    colnum = 0
    maxcols = 0
    overhang = False
    lastoverhang = False
    layout = []

    for row in jslayout:
        newrow = []
        if totalwidth > maxwidth:
            maxwidth = totalwidth
        totalwidth = 0
        if colnum > maxcols:
            maxcols = colnum
        colnum = 0
        overhang = False
        for item in row:
            if isinstance(item, str):
                scancode = convert(state, item, width, height)
                newrow.append(((width, height), (rownum, colnum), scancode))
                totalwidth += width
                width = 4
                height = 4
                colnum += 1
            elif isinstance(item, dict):
                for param, val in item.items():
                    if param == 'w':
                        width = int(val * 4)
                    elif param == 'h':
                        height = int(val * 4)
                        if height != 8:
                            raise Exception("Only heights of 1u or 2u are supported.")
                        overhang = True
                    elif param == 'x':
                        if lastoverhang:
                            # total hack to prevent overlaps in ISO enter
                            newrow.append((int(val * -4), None, NULL_SYMBOL))
                        else:
                            newrow.append((int(val * 4), None, NULL_SYMBOL))
                        totalwidth += int(val * 4)
                    elif param == 'y':
                        layout.append(int(val * 4))
                        totalheight += int(val * 4)
                    else:
                        continue
            else:
                raise TypeError("Unrecognized object in row array.")
        layout.append(newrow)
        totalheight += 4
        rownum += 1
        lastoverhang = overhang

    return {
        'display_height': totalheight,
        'display_width': maxwidth,
        'num_rows': rownum,
        'num_cols': maxcols,
        'layout': layout,
    }

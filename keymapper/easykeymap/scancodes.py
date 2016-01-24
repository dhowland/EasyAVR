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

"""This module contains the list of scan codes and their associations to
bytes, ASCII characters, and Tk symbols.
"""

scancodes = {
    "0": (" ", 0x00, " "),
    #"HID_KEYBOARD_SC_ERROR_ROLLOVER": ("", 0x01, ""),
    #"HID_KEYBOARD_SC_POST_FAIL": ("", 0x02, ""),
    #"HID_KEYBOARD_SC_ERROR_UNDEFINED": ("", 0x03, ""),
    "HID_KEYBOARD_SC_A": ("A", 0x04, "A"),
    "HID_KEYBOARD_SC_B": ("B", 0x05, "B"),
    "HID_KEYBOARD_SC_C": ("C", 0x06, "C"),
    "HID_KEYBOARD_SC_D": ("D", 0x07, "D"),
    "HID_KEYBOARD_SC_E": ("E", 0x08, "E"),
    "HID_KEYBOARD_SC_F": ("F", 0x09, "F"),
    "HID_KEYBOARD_SC_G": ("G", 0x0A, "G"),
    "HID_KEYBOARD_SC_H": ("H", 0x0B, "H"),
    "HID_KEYBOARD_SC_I": ("I", 0x0C, "I"),
    "HID_KEYBOARD_SC_J": ("J", 0x0D, "J"),
    "HID_KEYBOARD_SC_K": ("K", 0x0E, "K"),
    "HID_KEYBOARD_SC_L": ("L", 0x0F, "L"),
    "HID_KEYBOARD_SC_M": ("M", 0x10, "M"),
    "HID_KEYBOARD_SC_N": ("N", 0x11, "N"),
    "HID_KEYBOARD_SC_O": ("O", 0x12, "O"),
    "HID_KEYBOARD_SC_P": ("P", 0x13, "P"),
    "HID_KEYBOARD_SC_Q": ("Q", 0x14, "Q"),
    "HID_KEYBOARD_SC_R": ("R", 0x15, "R"),
    "HID_KEYBOARD_SC_S": ("S", 0x16, "S"),
    "HID_KEYBOARD_SC_T": ("T", 0x17, "T"),
    "HID_KEYBOARD_SC_U": ("U", 0x18, "U"),
    "HID_KEYBOARD_SC_V": ("V", 0x19, "V"),
    "HID_KEYBOARD_SC_W": ("W", 0x1A, "W"),
    "HID_KEYBOARD_SC_X": ("X", 0x1B, "X"),
    "HID_KEYBOARD_SC_Y": ("Y", 0x1C, "Y"),
    "HID_KEYBOARD_SC_Z": ("Z", 0x1D, "Z"),
    "HID_KEYBOARD_SC_1_AND_EXCLAMATION": ("!\n1", 0x1E, "1!"),
    "HID_KEYBOARD_SC_2_AND_AT": ("@\n2", 0x1F, "2@"),
    "HID_KEYBOARD_SC_3_AND_HASHMARK": ("#\n3", 0x20, "3#"),
    "HID_KEYBOARD_SC_4_AND_DOLLAR": ("$\n4", 0x21, "4$"),
    "HID_KEYBOARD_SC_5_AND_PERCENTAGE": ("%\n5", 0x22, "5%"),
    "HID_KEYBOARD_SC_6_AND_CARET": ("^\n6", 0x23, "6^"),
    "HID_KEYBOARD_SC_7_AND_AND_AMPERSAND": ("&\n7", 0x24, "7&"),
    "HID_KEYBOARD_SC_8_AND_ASTERISK": ("*\n8", 0x25, "8*"),
    "HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS": ("(\n9", 0x26, "9("),
    "HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS": (")\n0", 0x27, "0)"),
    "HID_KEYBOARD_SC_ENTER": ("Enter", 0x28, "Enter"),
    "HID_KEYBOARD_SC_ESCAPE": ("Esc", 0x29, "Esc"),
    "HID_KEYBOARD_SC_BACKSPACE": ("Backspace", 0x2A, "Bksp"),
    "HID_KEYBOARD_SC_TAB": ("Tab", 0x2B, "Tab"),
    "HID_KEYBOARD_SC_SPACE": ("Space", 0x2C, "Space"),
    "HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE": ("_\n-", 0x2D, "-_"),
    "HID_KEYBOARD_SC_EQUAL_AND_PLUS": ("+\n=", 0x2E, "=+"),
    "HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE": ("{\n[", 0x2F, "[{"),
    "HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE": ("}\n]", 0x30, "]}"),
    "HID_KEYBOARD_SC_BACKSLASH_AND_PIPE": ("|\n\\", 0x31, "\\|"),
    "HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE": ("~\n#", 0x32, "#~"),
    "HID_KEYBOARD_SC_SEMICOLON_AND_COLON": (":\n;", 0x33, ";:"),
    "HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE": ("\"\n'", 0x34, "'\""),
    "HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE": ("~\n`", 0x35, "`~"),
    "HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN": ("<\n,", 0x36, ",<"),
    "HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN": (">\n.", 0x37, ".>"),
    "HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK": ("?\n/", 0x38, "/?"),
    "HID_KEYBOARD_SC_CAPS_LOCK": ("Caps\nLock", 0x39, "Caps"),
    "HID_KEYBOARD_SC_F1": ("F1", 0x3A, "F1"),
    "HID_KEYBOARD_SC_F2": ("F2", 0x3B, "F2"),
    "HID_KEYBOARD_SC_F3": ("F3", 0x3C, "F3"),
    "HID_KEYBOARD_SC_F4": ("F4", 0x3D, "F4"),
    "HID_KEYBOARD_SC_F5": ("F5", 0x3E, "F5"),
    "HID_KEYBOARD_SC_F6": ("F6", 0x3F, "F6"),
    "HID_KEYBOARD_SC_F7": ("F7", 0x40, "F7"),
    "HID_KEYBOARD_SC_F8": ("F8", 0x41, "F8"),
    "HID_KEYBOARD_SC_F9": ("F9", 0x42, "F9"),
    "HID_KEYBOARD_SC_F10": ("F10", 0x43, "F10"),
    "HID_KEYBOARD_SC_F11": ("F11", 0x44, "F11"),
    "HID_KEYBOARD_SC_F12": ("F12", 0x45, "F12"),
    "HID_KEYBOARD_SC_PRINT_SCREEN": ("Print\nScreen", 0x46, "PtSc"),
    "HID_KEYBOARD_SC_SCROLL_LOCK": ("Scroll\nLock", 0x47, "ScLk"),
    "HID_KEYBOARD_SC_PAUSE": ("Pause", 0x48, "Paus"),
    "HID_KEYBOARD_SC_INSERT": ("Insert", 0x49, "Ins"),
    "HID_KEYBOARD_SC_HOME": ("Home", 0x4A, "Home"),
    "HID_KEYBOARD_SC_PAGE_UP": ("Page\nUp", 0x4B, "PgUp"),
    "HID_KEYBOARD_SC_DELETE": ("Delete", 0x4C, "Del"),
    "HID_KEYBOARD_SC_END": ("End", 0x4D, "End"),
    "HID_KEYBOARD_SC_PAGE_DOWN": ("Page\nDown", 0x4E, "PgDn"),
    "HID_KEYBOARD_SC_RIGHT_ARROW": ("Right", 0x4F, "Rt"),
    "HID_KEYBOARD_SC_LEFT_ARROW": ("Left", 0x50, "Lf"),
    "HID_KEYBOARD_SC_DOWN_ARROW": ("Down", 0x51, "Dn"),
    "HID_KEYBOARD_SC_UP_ARROW": ("Up", 0x52, "Up"),
    "HID_KEYBOARD_SC_NUM_LOCK": ("Num\nLock", 0x53, "NmLk"),
    "HID_KEYBOARD_SC_KEYPAD_SLASH": ("/", 0x54, "/"),
    "HID_KEYBOARD_SC_KEYPAD_ASTERISK": ("*", 0x55, "*"),
    "HID_KEYBOARD_SC_KEYPAD_MINUS": ("-", 0x56, "-"),
    "HID_KEYBOARD_SC_KEYPAD_PLUS": ("+", 0x57, "+"),
    "HID_KEYBOARD_SC_KEYPAD_ENTER": ("Enter", 0x58, "Ent"),
    "HID_KEYBOARD_SC_KEYPAD_1_AND_END": ("1\nEnd", 0x59, "1"),
    "HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW": ("2\nDown", 0x5A, "2"),
    "HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN": ("3\nPgDn", 0x5B, "3"),
    "HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW": ("4\nLeft", 0x5C, "4"),
    "HID_KEYBOARD_SC_KEYPAD_5": ("5", 0x5D, "5"),
    "HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW": ("6\nRight", 0x5E, "6"),
    "HID_KEYBOARD_SC_KEYPAD_7_AND_HOME": ("7\nHome", 0x5F, "7"),
    "HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW": ("8\nUp", 0x60, "8"),
    "HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP": ("9\nPgUp", 0x61, "9"),
    "HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT": ("0\nIns", 0x62, "0"),
    "HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE": (".\nDel", 0x63, "."),
    "HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE": ("|\n\\", 0x64, "\\|"),
    "HID_KEYBOARD_SC_APPLICATION": ("App", 0x65, "App"),
    "HID_KEYBOARD_SC_POWER": ("Power\n(Mac)", 0x66, "Pwr"),
    "HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN": ("=\n(Mac)", 0x67, "="),
    "HID_KEYBOARD_SC_F13": ("F13", 0x68, "F13"),
    "HID_KEYBOARD_SC_F14": ("F14", 0x69, "F14"),
    "HID_KEYBOARD_SC_F15": ("F15", 0x6A, "F15"),
    "HID_KEYBOARD_SC_F16": ("F16", 0x6B, "F16"),
    "HID_KEYBOARD_SC_F17": ("F17", 0x6C, "F17"),
    "HID_KEYBOARD_SC_F18": ("F18", 0x6D, "F18"),
    "HID_KEYBOARD_SC_F19": ("F19", 0x6E, "F19"),
    "HID_KEYBOARD_SC_F20": ("F20", 0x6F, "F20"),
    "HID_KEYBOARD_SC_F21": ("F21", 0x70, "F21"),
    "HID_KEYBOARD_SC_F22": ("F22", 0x71, "F22"),
    "HID_KEYBOARD_SC_F23": ("F23", 0x72, "F23"),
    "HID_KEYBOARD_SC_F24": ("F24", 0x73, "F24"),
    #"HID_KEYBOARD_SC_EXECUTE": ("Execute\n(Unix)", 0x74, ""),
    #"HID_KEYBOARD_SC_HELP": ("Help\n(Unix)", 0x75, ""),
    #"HID_KEYBOARD_SC_MANU": ("Menu\n(Unix)", 0x76, ""),
    #"HID_KEYBOARD_SC_SELECT": ("Select\n(Unix)", 0x77, ""),
    #"HID_KEYBOARD_SC_STOP": ("Stop\n(Unix)", 0x78, ""),
    #"HID_KEYBOARD_SC_AGAIN": ("Again\n(Unix)", 0x79, ""),
    #"HID_KEYBOARD_SC_UNDO": ("Undo\n(Unix)", 0x7A, ""),
    #"HID_KEYBOARD_SC_CUT": ("Cut\n(Unix)", 0x7B, ""),
    #"HID_KEYBOARD_SC_COPY": ("Copy\n(Unix)", 0x7C, ""),
    #"HID_KEYBOARD_SC_PASTE": ("Paste\n(Unix)", 0x7D, ""),
    #"HID_KEYBOARD_SC_FIND": ("Find\n(Unix)", 0x7E, ""),
    #"HID_KEYBOARD_SC_MUTE": ("Mute\n(Mac)", 0x7F, ""),
    #"HID_KEYBOARD_SC_VOLUME_UP": ("Vol+\n(Mac)", 0x80, ""),
    #"HID_KEYBOARD_SC_VOLUME_DOWN": ("Vol-\n(Mac)", 0x81, ""),
    "HID_KEYBOARD_SC_LOCKING_CAPS_LOCK": ("Locking\nCaps", 0x82, "Caps"),
    "HID_KEYBOARD_SC_LOCKING_NUM_LOCK": ("Locking\nNum", 0x83, "NmLk"),
    "HID_KEYBOARD_SC_LOCKING_SCROLL_LOCK": ("Locking\nScroll", 0x84, "ScLk"),
    #"HID_KEYBOARD_SC_KEYPAD_COMMA": ("", 0x85, ""),
    #"HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN_AS400": ("", 0x86, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL1": ("", 0x87, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL2": ("", 0x88, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL3": ("", 0x89, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL4": ("", 0x8A, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL5": ("", 0x8B, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL6": ("", 0x8C, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL7": ("", 0x8D, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL8": ("", 0x8E, ""),
    #"HID_KEYBOARD_SC_INTERNATIONAL9": ("", 0x8F, ""),
    #"HID_KEYBOARD_SC_LANG1": ("", 0x90, ""),
    #"HID_KEYBOARD_SC_LANG2": ("", 0x91, ""),
    #"HID_KEYBOARD_SC_LANG3": ("", 0x92, ""),
    #"HID_KEYBOARD_SC_LANG4": ("", 0x93, ""),
    #"HID_KEYBOARD_SC_LANG5": ("", 0x94, ""),
    #"HID_KEYBOARD_SC_LANG6": ("", 0x95, ""),
    #"HID_KEYBOARD_SC_LANG7": ("", 0x96, ""),
    #"HID_KEYBOARD_SC_LANG8": ("", 0x97, ""),
    #"HID_KEYBOARD_SC_LANG9": ("", 0x98, ""),
    #"HID_KEYBOARD_SC_ALTERNATE_ERASE": ("", 0x99, ""),
    #"HID_KEYBOARD_SC_SISREQ": ("", 0x9A, ""),
    #"HID_KEYBOARD_SC_CANCEL": ("", 0x9B, ""),
    #"HID_KEYBOARD_SC_CLEAR": ("", 0x9C, ""),
    #"HID_KEYBOARD_SC_PRIOR": ("", 0x9D, ""),
    #"HID_KEYBOARD_SC_RETURN": ("", 0x9E, ""),
    #"HID_KEYBOARD_SC_SEPARATOR": ("", 0x9F, ""),
    #"HID_KEYBOARD_SC_OUT": ("", 0xA0, ""),
    #"HID_KEYBOARD_SC_OPER": ("", 0xA1, ""),
    #"HID_KEYBOARD_SC_CLEAR_AND_AGAIN": ("", 0xA2, ""),
    #"HID_KEYBOARD_SC_CRSEL_ANDPROPS": ("", 0xA3, ""),
    #"HID_KEYBOARD_SC_EXSEL": ("", 0xA4, ""),
    #"HID_KEYBOARD_SC_KEYPAD_00": ("", 0xB0, ""),
    #"HID_KEYBOARD_SC_KEYPAD_000": ("", 0xB1, ""),
    #"HID_KEYBOARD_SC_THOUSANDS_SEPARATOR": ("", 0xB2, ""),
    #"HID_KEYBOARD_SC_DECIMAL_SEPARATOR": ("", 0xB3, ""),
    #"HID_KEYBOARD_SC_CURRENCY_UNIT": ("", 0xB4, ""),
    #"HID_KEYBOARD_SC_CURRENCY_SUB_UNIT": ("", 0xB5, ""),
    #"HID_KEYBOARD_SC_KEYPAD_OPENING_PARENTHESIS": ("", 0xB6, ""),
    #"HID_KEYBOARD_SC_KEYPAD_CLOSING_PARENTHESIS": ("", 0xB7, ""),
    #"HID_KEYBOARD_SC_KEYPAD_OPENING_BRACE": ("", 0xB8, ""),
    #"HID_KEYBOARD_SC_KEYPAD_CLOSING_BRACE": ("", 0xB9, ""),
    #"HID_KEYBOARD_SC_KEYPAD_TAB": ("", 0xBA, ""),
    #"HID_KEYBOARD_SC_KEYPAD_BACKSPACE": ("", 0xBB, ""),
    #"HID_KEYBOARD_SC_KEYPAD_A": ("", 0xBC, ""),
    #"HID_KEYBOARD_SC_KEYPAD_B": ("", 0xBD, ""),
    #"HID_KEYBOARD_SC_KEYPAD_C": ("", 0xBE, ""),
    #"HID_KEYBOARD_SC_KEYPAD_D": ("", 0xBF, ""),
    #"HID_KEYBOARD_SC_KEYPAD_E": ("", 0xC0, ""),
    #"HID_KEYBOARD_SC_KEYPAD_F": ("", 0xC1, ""),
    #"HID_KEYBOARD_SC_KEYPAD_XOR": ("", 0xC2, ""),
    #"HID_KEYBOARD_SC_KEYPAD_CARET": ("", 0xC3, ""),
    #"HID_KEYBOARD_SC_KEYPAD_PERCENTAGE": ("", 0xC4, ""),
    #"HID_KEYBOARD_SC_KEYPAD_LESS_THAN_SIGN": ("", 0xC5, ""),
    #"HID_KEYBOARD_SC_KEYPAD_GREATER_THAN_SIGN": ("", 0xC6, ""),
    #"HID_KEYBOARD_SC_KEYPAD_AMP": ("", 0xC7, ""),
    #"HID_KEYBOARD_SC_KEYPAD_AMP_AMP": ("", 0xC8, ""),
    #"HID_KEYBOARD_SC_KEYPAD_PIPE": ("", 0xC9, ""),
    #"HID_KEYBOARD_SC_KEYPAD_PIPE_PIPE": ("", 0xCA, ""),
    #"HID_KEYBOARD_SC_KEYPAD_COLON": ("", 0xCB, ""),
    #"HID_KEYBOARD_SC_KEYPAD_HASHMARK": ("", 0xCC, ""),
    #"HID_KEYBOARD_SC_KEYPAD_SPACE": ("", 0xCD, ""),
    #"HID_KEYBOARD_SC_KEYPAD_AT": ("", 0xCE, ""),
    #"HID_KEYBOARD_SC_KEYPAD_EXCLAMATION_SIGN": ("", 0xCF, ""),
    #"HID_KEYBOARD_SC_KEYPAD_MEMORY_STORE": ("", 0xD0, ""),
    #"HID_KEYBOARD_SC_KEYPAD_MEMORY_RECALL": ("", 0xD1, ""),
    #"HID_KEYBOARD_SC_KEYPAD_MEMORY_CLEAR": ("", 0xD2, ""),
    #"HID_KEYBOARD_SC_KEYPAD_MEMORY_ADD": ("", 0xD3, ""),
    #"HID_KEYBOARD_SC_KEYPAD_MEMORY_SUBTRACT": ("", 0xD4, ""),
    #"HID_KEYBOARD_SC_KEYPAD_MEMORY_MULTIPLY": ("", 0xD5, ""),
    #"HID_KEYBOARD_SC_KEYPAD_MEMORY_DIVIDE": ("", 0xD6, ""),
    #"HID_KEYBOARD_SC_KEYPAD_PLUS_AND_MINUS": ("", 0xD7, ""),
    #"HID_KEYBOARD_SC_KEYPAD_CLEAR": ("", 0xD8, ""),
    #"HID_KEYBOARD_SC_KEYPAD_CLEAR_ENTRY": ("", 0xD9, ""),
    #"HID_KEYBOARD_SC_KEYPAD_BINARY": ("", 0xDA, ""),
    #"HID_KEYBOARD_SC_KEYPAD_OCTAL": ("", 0xDB, ""),
    #"HID_KEYBOARD_SC_KEYPAD_DECIMAL": ("", 0xDC, ""),
    #"HID_KEYBOARD_SC_KEYPAD_HEXADECIMAL": ("", 0xDD, ""),
    "HID_KEYBOARD_SC_LEFT_CONTROL": ("L_Ctrl", 0xE0, "Ctrl"),
    "HID_KEYBOARD_SC_LEFT_SHIFT": ("L_Shift", 0xE1, "Shift"),
    "HID_KEYBOARD_SC_LEFT_ALT": ("L_Alt", 0xE2, "Alt"),
    "HID_KEYBOARD_SC_LEFT_GUI": ("L_Win", 0xE3, "GUI"),
    "HID_KEYBOARD_SC_RIGHT_CONTROL": ("R_Ctrl", 0xE4, "Ctrl"),
    "HID_KEYBOARD_SC_RIGHT_SHIFT": ("R_Shift", 0xE5, "Shift"),
    "HID_KEYBOARD_SC_RIGHT_ALT": ("R_Alt", 0xE6, "Alt"),
    "HID_KEYBOARD_SC_RIGHT_GUI": ("R_Win", 0xE7, "GUI"),
    "SCANCODE_M1": ("M1", 0xD0, "M1"),
    "SCANCODE_M2": ("M2", 0xD1, "M2"),
    "SCANCODE_M3": ("M3", 0xD2, "M3"),
    "SCANCODE_M4": ("M4", 0xD3, "M4"),
    "SCANCODE_M5": ("M5", 0xD4, "M5"),
    "SCANCODE_M6": ("M6", 0xD5, "M6"),
    "SCANCODE_M7": ("M7", 0xD6, "M7"),
    "SCANCODE_M8": ("M8", 0xD7, "M8"),
    "SCANCODE_M9": ("M9", 0xD8, "M9"),
    "SCANCODE_M10": ("M10", 0xD9, "M10"),
    "SCANCODE_M11": ("M11", 0xDA, "M11"),
    "SCANCODE_M12": ("M12", 0xDB, "M12"),
    "SCANCODE_M13": ("M13", 0xDC, "M13"),
    "SCANCODE_M14": ("M14", 0xDD, "M14"),
    "SCANCODE_MRAM_RECORD": ("Macro\nRec", 0xDE, "Mrec"),
    "SCANCODE_MRAM_PLAY": ("Macro\nPlay", 0xDF, "Mply"),
    "SCANCODE_FN": ("Fn", 0xF1, "FN"),
    "SCANCODE_FN2": ("Fn 2", 0xF2, "FN2"),
    "SCANCODE_FN3": ("Fn 3", 0xF3, "FN3"),
    "SCANCODE_FN4": ("Fn 4", 0xF4, "FN4"),
    "SCANCODE_FN5": ("Fn 5", 0xF5, "FN5"),
    "SCANCODE_FN6": ("Fn 6", 0xF6, "FN6"),
    "SCANCODE_FN7": ("Fn 7", 0xF7, "FN7"),
    "SCANCODE_FN8": ("Fn 8", 0xF8, "FN8"),
    "SCANCODE_FN9": ("Fn 9", 0xF9, "FN9"),
    "SCANCODE_MOUSE1": ("Mouse\nBtn 1", 0xC1, "MB1"),
    "SCANCODE_MOUSE2": ("Mouse\nBtn 2", 0xC2, "MB2"),
    "SCANCODE_MOUSE3": ("Mouse\nBtn 3", 0xC3, "MB3"),
    "SCANCODE_MOUSEXR": ("Mouse\nRight", 0xC6, "Mrt"),
    "SCANCODE_MOUSEXL": ("Mouse\nLeft", 0xC7, "Mlf"),
    "SCANCODE_MOUSEYU": ("Mouse\nUp", 0xC8, "Mup"),
    "SCANCODE_MOUSEYD": ("Mouse\nDown", 0xC9, "Mdn"),
    "SCANCODE_MUTE": ("Mute", 0xB0, "Mute"),
    "SCANCODE_VOL_INC": ("Vol\nUp", 0xB1, "Vol+"),
    "SCANCODE_VOL_DEC": ("Vol\nDown", 0xB2, "Vol-"),
    "SCANCODE_BASS_BOOST": ("Bass\nBoost", 0xB3, "Bass"),
    "SCANCODE_NEXT_TRACK": ("Next\nTrack", 0xB4, "Next"),
    "SCANCODE_PREV_TRACK": ("Prev\nTrack", 0xB5, "Prev"),
    "SCANCODE_STOP": ("Stop", 0xB6, "Stop"),
    "SCANCODE_PLAY_PAUSE": ("Play\nPause", 0xB7, "Play"),
    "SCANCODE_BACK": ("Nav\nBack", 0xB8, "Back"),
    "SCANCODE_FORWARD": ("Nav\nForward", 0xB9, "Forw"),
    "SCANCODE_MEDIA": ("Media\nPlayer", 0xBA, "Medi"),
    "SCANCODE_MAIL": ("Mail", 0xBB, "Mail"),
    "SCANCODE_CALC": ("Calc", 0xBC, "Calc"),
    "SCANCODE_MYCOMP": ("My\nComp", 0xBD, "Comp"),
    "SCANCODE_SEARCH": ("Search", 0xBE, "Srch"),
    "SCANCODE_BROWSER": ("Web\nBrowser", 0xBF, "Web"),
    "SCANCODE_BL_DIMMER": ("BL\nDimmer", 0xA1, "BLdm"),
    "SCANCODE_BL_MODE": ("BL\nMode", 0xA2, "BLmd"),
    "SCANCODE_BL_ENABLE": ("BL\nEnable", 0xA3, "BLen"),
    "SCANCODE_PASSWORD1": ("PW1", 0xA4, "PW1"),
    "SCANCODE_PASSWORD2": ("PW2", 0xA5, "PW2"),
    "SCANCODE_PASSWORD3": ("PW3", 0xA6, "PW3"),
    "SCANCODE_PASSWORD4": ("PW4", 0xA7, "PW4"),
    "SCANCODE_KEYLOCK": ("KB\nLock", 0xA8, "KbLk"),
    "SCANCODE_WINLOCK": ("Win\nLock", 0xA9, "WnLk"),
    "SCANCODE_ESCGRAVE": ("~\nEsc", 0xAA, "~Esc"),
    "SCANCODE_BOOT": ("Boot\nMode", 0xAE, "BOOT"),
    "SCANCODE_CONFIG": ("Config\nConsole", 0xAF, "Conf")
}

# parse_text:(scancode,needs_shift)
char_map = {
    0: ("0", False),
    "MUTE": ("SCANCODE_MUTE", False),
    "VOLUP": ("SCANCODE_VOL_INC", False),
    "VOLDN": ("SCANCODE_VOL_DEC", False),
    "BASS": ("SCANCODE_BASS_BOOST", False),
    "NEXT": ("SCANCODE_NEXT_TRACK", False),
    "PREV": ("SCANCODE_PREV_TRACK", False),
    "STOP": ("SCANCODE_STOP", False),
    "PLAY": ("SCANCODE_PLAY_PAUSE", False),
    "ESC": ("HID_KEYBOARD_SC_ESCAPE", False),
    "F1": ("HID_KEYBOARD_SC_F1", False),
    "F2": ("HID_KEYBOARD_SC_F2", False),
    "F3": ("HID_KEYBOARD_SC_F3", False),
    "F4": ("HID_KEYBOARD_SC_F4", False),
    "F5": ("HID_KEYBOARD_SC_F5", False),
    "F6": ("HID_KEYBOARD_SC_F6", False),
    "F7": ("HID_KEYBOARD_SC_F7", False),
    "F8": ("HID_KEYBOARD_SC_F8", False),
    "F9": ("HID_KEYBOARD_SC_F9", False),
    "F10": ("HID_KEYBOARD_SC_F10", False),
    "F11": ("HID_KEYBOARD_SC_F11", False),
    "F12": ("HID_KEYBOARD_SC_F12", False),
    "F13": ("HID_KEYBOARD_SC_F13", False),
    "F14": ("HID_KEYBOARD_SC_F14", False),
    "F15": ("HID_KEYBOARD_SC_F15", False),
    "F16": ("HID_KEYBOARD_SC_F16", False),
    "F17": ("HID_KEYBOARD_SC_F17", False),
    "F18": ("HID_KEYBOARD_SC_F18", False),
    "F19": ("HID_KEYBOARD_SC_F19", False),
    "F20": ("HID_KEYBOARD_SC_F20", False),
    "F21": ("HID_KEYBOARD_SC_F21", False),
    "F22": ("HID_KEYBOARD_SC_F22", False),
    "F23": ("HID_KEYBOARD_SC_F23", False),
    "F24": ("HID_KEYBOARD_SC_F24", False),
    "PRINT": ("HID_KEYBOARD_SC_PRINT_SCREEN", False),
    "SCRLK": ("HID_KEYBOARD_SC_SCROLL_LOCK", False),
    "PAUSE": ("HID_KEYBOARD_SC_PAUSE", False),
    "KPSLA": ("HID_KEYBOARD_SC_KEYPAD_SLASH", False),
    "KPAST": ("HID_KEYBOARD_SC_KEYPAD_ASTERISK", False),
    "KPMIN": ("HID_KEYBOARD_SC_KEYPAD_MINUS", False),
    "KPPLS": ("HID_KEYBOARD_SC_KEYPAD_PLUS", False),
    "KPENT": ("HID_KEYBOARD_SC_KEYPAD_ENTER", False),
    "KP1": ("HID_KEYBOARD_SC_KEYPAD_1_AND_END", False),
    "KP2": ("HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW", False),
    "KP3": ("HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN", False),
    "KP4": ("HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW", False),
    "KP5": ("HID_KEYBOARD_SC_KEYPAD_5", False),
    "KP6": ("HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW", False),
    "KP7": ("HID_KEYBOARD_SC_KEYPAD_7_AND_HOME", False),
    "KP8": ("HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW", False),
    "KP9": ("HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP", False),
    "KP0": ("HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT", False),
    "KPDOT": ("HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE", False),
    "KPEQ": ("HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN", False),
    "`": ("HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE", False),
    "1": ("HID_KEYBOARD_SC_1_AND_EXCLAMATION", False),
    "2": ("HID_KEYBOARD_SC_2_AND_AT", False),
    "3": ("HID_KEYBOARD_SC_3_AND_HASHMARK", False),
    "4": ("HID_KEYBOARD_SC_4_AND_DOLLAR", False),
    "5": ("HID_KEYBOARD_SC_5_AND_PERCENTAGE", False),
    "6": ("HID_KEYBOARD_SC_6_AND_CARET", False),
    "7": ("HID_KEYBOARD_SC_7_AND_AND_AMPERSAND", False),
    "8": ("HID_KEYBOARD_SC_8_AND_ASTERISK", False),
    "9": ("HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS", False),
    "0": ("HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS", False),
    "-": ("HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE", False),
    "=": ("HID_KEYBOARD_SC_EQUAL_AND_PLUS", False),
    "~": ("HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE", True),
    "!": ("HID_KEYBOARD_SC_1_AND_EXCLAMATION", True),
    "@": ("HID_KEYBOARD_SC_2_AND_AT", True),
    "#": ("HID_KEYBOARD_SC_3_AND_HASHMARK", True),
    "$": ("HID_KEYBOARD_SC_4_AND_DOLLAR", True),
    "%": ("HID_KEYBOARD_SC_5_AND_PERCENTAGE", True),
    "^": ("HID_KEYBOARD_SC_6_AND_CARET", True),
    "&": ("HID_KEYBOARD_SC_7_AND_AND_AMPERSAND", True),
    "*": ("HID_KEYBOARD_SC_8_AND_ASTERISK", True),
    "(": ("HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS", True),
    ")": ("HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS", True),
    "_": ("HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE", True),
    "+": ("HID_KEYBOARD_SC_EQUAL_AND_PLUS", True),
    "BKSP": ("HID_KEYBOARD_SC_BACKSPACE", False),
    "INS": ("HID_KEYBOARD_SC_INSERT", False),
    "HOME": ("HID_KEYBOARD_SC_HOME", False),
    "PGUP": ("HID_KEYBOARD_SC_PAGE_UP", False),
    "TAB": ("HID_KEYBOARD_SC_TAB", False),
    "\t": ("HID_KEYBOARD_SC_TAB", False),
    "q": ("HID_KEYBOARD_SC_Q", False),
    "w": ("HID_KEYBOARD_SC_W", False),
    "e": ("HID_KEYBOARD_SC_E", False),
    "r": ("HID_KEYBOARD_SC_R", False),
    "t": ("HID_KEYBOARD_SC_T", False),
    "y": ("HID_KEYBOARD_SC_Y", False),
    "u": ("HID_KEYBOARD_SC_U", False),
    "i": ("HID_KEYBOARD_SC_I", False),
    "o": ("HID_KEYBOARD_SC_O", False),
    "p": ("HID_KEYBOARD_SC_P", False),
    "[": ("HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE", False),
    "]": ("HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE", False),
    "\\": ("HID_KEYBOARD_SC_BACKSLASH_AND_PIPE", False),
    "Q": ("HID_KEYBOARD_SC_Q", True),
    "W": ("HID_KEYBOARD_SC_W", True),
    "E": ("HID_KEYBOARD_SC_E", True),
    "R": ("HID_KEYBOARD_SC_R", True),
    "T": ("HID_KEYBOARD_SC_T", True),
    "Y": ("HID_KEYBOARD_SC_Y", True),
    "U": ("HID_KEYBOARD_SC_U", True),
    "I": ("HID_KEYBOARD_SC_I", True),
    "O": ("HID_KEYBOARD_SC_O", True),
    "P": ("HID_KEYBOARD_SC_P", True),
    "{": ("HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE", True),
    "}": ("HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE", True),
    "|": ("HID_KEYBOARD_SC_BACKSLASH_AND_PIPE", True),
    "DEL": ("HID_KEYBOARD_SC_DELETE", False),
    "END": ("HID_KEYBOARD_SC_END", False),
    "PGDN": ("HID_KEYBOARD_SC_PAGE_DOWN", False),
    "CAPSLK": ("HID_KEYBOARD_SC_CAPS_LOCK", False),
    "a": ("HID_KEYBOARD_SC_A", False),
    "s": ("HID_KEYBOARD_SC_S", False),
    "d": ("HID_KEYBOARD_SC_D", False),
    "f": ("HID_KEYBOARD_SC_F", False),
    "g": ("HID_KEYBOARD_SC_G", False),
    "h": ("HID_KEYBOARD_SC_H", False),
    "j": ("HID_KEYBOARD_SC_J", False),
    "k": ("HID_KEYBOARD_SC_K", False),
    "l": ("HID_KEYBOARD_SC_L", False),
    ";": ("HID_KEYBOARD_SC_SEMICOLON_AND_COLON", False),
    "'": ("HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE", False),
    "A": ("HID_KEYBOARD_SC_A", True),
    "S": ("HID_KEYBOARD_SC_S", True),
    "D": ("HID_KEYBOARD_SC_D", True),
    "F": ("HID_KEYBOARD_SC_F", True),
    "G": ("HID_KEYBOARD_SC_G", True),
    "H": ("HID_KEYBOARD_SC_H", True),
    "J": ("HID_KEYBOARD_SC_J", True),
    "K": ("HID_KEYBOARD_SC_K", True),
    "L": ("HID_KEYBOARD_SC_L", True),
    ":": ("HID_KEYBOARD_SC_SEMICOLON_AND_COLON", True),
    "\"": ("HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE", True),
    "ENTER": ("HID_KEYBOARD_SC_ENTER", False),
    "\n": ("HID_KEYBOARD_SC_ENTER", False),
    "\r": ("HID_KEYBOARD_SC_ENTER", False),
    "z": ("HID_KEYBOARD_SC_Z", False),
    "x": ("HID_KEYBOARD_SC_X", False),
    "c": ("HID_KEYBOARD_SC_C", False),
    "v": ("HID_KEYBOARD_SC_V", False),
    "b": ("HID_KEYBOARD_SC_B", False),
    "n": ("HID_KEYBOARD_SC_N", False),
    "m": ("HID_KEYBOARD_SC_M", False),
    ",": ("HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN", False),
    ".": ("HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN", False),
    "/": ("HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK", False),
    "Z": ("HID_KEYBOARD_SC_Z", True),
    "X": ("HID_KEYBOARD_SC_X", True),
    "C": ("HID_KEYBOARD_SC_C", True),
    "V": ("HID_KEYBOARD_SC_V", True),
    "B": ("HID_KEYBOARD_SC_B", True),
    "N": ("HID_KEYBOARD_SC_N", True),
    "M": ("HID_KEYBOARD_SC_M", True),
    "<": ("HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN", True),
    ">": ("HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN", True),
    "?": ("HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK", True),
    "UP": ("HID_KEYBOARD_SC_UP_ARROW", False),
    "LEFT": ("HID_KEYBOARD_SC_LEFT_ARROW", False),
    "DOWN": ("HID_KEYBOARD_SC_DOWN_ARROW", False),
    "RIGHT": ("HID_KEYBOARD_SC_RIGHT_ARROW", False),
    "SPACE": ("HID_KEYBOARD_SC_SPACE", False),
    " ": ("HID_KEYBOARD_SC_SPACE", False),
    "APP": ("HID_KEYBOARD_SC_APPLICATION", False)
}

keysyms = {
    0x0020: "HID_KEYBOARD_SC_SPACE",    # space
    0x0021: "HID_KEYBOARD_SC_1_AND_EXCLAMATION",    # exclam
    0x0022: "HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE",    # quotedbl
    0x0023: "HID_KEYBOARD_SC_3_AND_HASHMARK",    # numbersign
    0x0024: "HID_KEYBOARD_SC_4_AND_DOLLAR",    # dollar
    0x0025: "HID_KEYBOARD_SC_5_AND_PERCENTAGE",    # percent
    0x0026: "HID_KEYBOARD_SC_7_AND_AND_AMPERSAND",    # ampersand
    0x0027: "HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE",    # quoteright
    0x0028: "HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS",    # parenleft
    0x0029: "HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS",    # parenright
    0x002a: "HID_KEYBOARD_SC_8_AND_ASTERISK",    # asterisk
    0x002b: "HID_KEYBOARD_SC_EQUAL_AND_PLUS",    # plus
    0x002c: "HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN",    # comma
    0x002d: "HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE",    # minus
    0x002e: "HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN",    # period
    0x002f: "HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK",    # slash
    0x0030: "HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS",    # 0
    0x0031: "HID_KEYBOARD_SC_1_AND_EXCLAMATION",    # 1
    0x0032: "HID_KEYBOARD_SC_2_AND_AT",    # 2
    0x0033: "HID_KEYBOARD_SC_3_AND_HASHMARK",    # 3
    0x0034: "HID_KEYBOARD_SC_4_AND_DOLLAR",    # 4
    0x0035: "HID_KEYBOARD_SC_5_AND_PERCENTAGE",    # 5
    0x0036: "HID_KEYBOARD_SC_6_AND_CARET",    # 6
    0x0037: "HID_KEYBOARD_SC_7_AND_AND_AMPERSAND",    # 7
    0x0038: "HID_KEYBOARD_SC_8_AND_ASTERISK",    # 8
    0x0039: "HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS",    # 9
    0x003a: "HID_KEYBOARD_SC_SEMICOLON_AND_COLON",    # colon
    0x003b: "HID_KEYBOARD_SC_SEMICOLON_AND_COLON",    # semicolon
    0x003c: "HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN",    # less
    0x003d: "HID_KEYBOARD_SC_EQUAL_AND_PLUS",    # equal
    0x003e: "HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN",    # greater
    0x003f: "HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK",    # question
    0x0040: "HID_KEYBOARD_SC_2_AND_AT",    # at
    0x0041: "HID_KEYBOARD_SC_A",    # A
    0x0042: "HID_KEYBOARD_SC_B",    # B
    0x0043: "HID_KEYBOARD_SC_C",    # C
    0x0044: "HID_KEYBOARD_SC_D",    # D
    0x0045: "HID_KEYBOARD_SC_E",    # E
    0x0046: "HID_KEYBOARD_SC_F",    # F
    0x0047: "HID_KEYBOARD_SC_G",    # G
    0x0048: "HID_KEYBOARD_SC_H",    # H
    0x0049: "HID_KEYBOARD_SC_I",    # I
    0x004a: "HID_KEYBOARD_SC_J",    # J
    0x004b: "HID_KEYBOARD_SC_K",    # K
    0x004c: "HID_KEYBOARD_SC_L",    # L
    0x004d: "HID_KEYBOARD_SC_M",    # M
    0x004e: "HID_KEYBOARD_SC_N",    # N
    0x004f: "HID_KEYBOARD_SC_O",    # O
    0x0050: "HID_KEYBOARD_SC_P",    # P
    0x0051: "HID_KEYBOARD_SC_Q",    # Q
    0x0052: "HID_KEYBOARD_SC_R",    # R
    0x0053: "HID_KEYBOARD_SC_S",    # S
    0x0054: "HID_KEYBOARD_SC_T",    # T
    0x0055: "HID_KEYBOARD_SC_U",    # U
    0x0056: "HID_KEYBOARD_SC_V",    # V
    0x0057: "HID_KEYBOARD_SC_W",    # W
    0x0058: "HID_KEYBOARD_SC_X",    # X
    0x0059: "HID_KEYBOARD_SC_Y",    # Y
    0x005a: "HID_KEYBOARD_SC_Z",    # Z
    0x005b: "HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE",  # bracketleft
    0x005c: "HID_KEYBOARD_SC_BACKSLASH_AND_PIPE",    # backslash
    0x005d: "HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE",  # bracketright
    0x005e: "HID_KEYBOARD_SC_6_AND_CARET",    # asciicircum
    0x005f: "HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE",    # underscore
    0x0060: "HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE",    # quoteleft
    0x0061: "HID_KEYBOARD_SC_A",    # a
    0x0062: "HID_KEYBOARD_SC_B",    # b
    0x0063: "HID_KEYBOARD_SC_C",    # c
    0x0064: "HID_KEYBOARD_SC_D",    # d
    0x0065: "HID_KEYBOARD_SC_E",    # e
    0x0066: "HID_KEYBOARD_SC_F",    # f
    0x0067: "HID_KEYBOARD_SC_G",    # g
    0x0068: "HID_KEYBOARD_SC_H",    # h
    0x0069: "HID_KEYBOARD_SC_I",    # i
    0x006a: "HID_KEYBOARD_SC_J",    # j
    0x006b: "HID_KEYBOARD_SC_K",    # k
    0x006c: "HID_KEYBOARD_SC_L",    # l
    0x006d: "HID_KEYBOARD_SC_M",    # m
    0x006e: "HID_KEYBOARD_SC_N",    # n
    0x006f: "HID_KEYBOARD_SC_O",    # o
    0x0070: "HID_KEYBOARD_SC_P",    # p
    0x0071: "HID_KEYBOARD_SC_Q",    # q
    0x0072: "HID_KEYBOARD_SC_R",    # r
    0x0073: "HID_KEYBOARD_SC_S",    # s
    0x0074: "HID_KEYBOARD_SC_T",    # t
    0x0075: "HID_KEYBOARD_SC_U",    # u
    0x0076: "HID_KEYBOARD_SC_V",    # v
    0x0077: "HID_KEYBOARD_SC_W",    # w
    0x0078: "HID_KEYBOARD_SC_X",    # x
    0x0079: "HID_KEYBOARD_SC_Y",    # y
    0x007a: "HID_KEYBOARD_SC_Z",    # z
    0x007b: "HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE",    # braceleft
    0x007c: "HID_KEYBOARD_SC_BACKSLASH_AND_PIPE",    # bar
    0x007d: "HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE",   # braceright
    0x007e: "HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE",    # asciitilde
    0xff08: "HID_KEYBOARD_SC_BACKSPACE",    # BackSpace
    0xff09: "HID_KEYBOARD_SC_TAB",    # Tab
    0xff0d: "HID_KEYBOARD_SC_ENTER",    # Return
    0xff13: "HID_KEYBOARD_SC_PAUSE",    # Pause
    0xff14: "HID_KEYBOARD_SC_SCROLL_LOCK",    # Scroll_Lock
    0xff15: "HID_KEYBOARD_SC_PRINT_SCREEN",    # Sys_Req
    0xff1b: "HID_KEYBOARD_SC_ESCAPE",    # Escape
    0xff50: "HID_KEYBOARD_SC_HOME",    # Home
    0xff51: "HID_KEYBOARD_SC_LEFT_ARROW",    # Left
    0xff52: "HID_KEYBOARD_SC_UP_ARROW",    # Up
    0xff53: "HID_KEYBOARD_SC_RIGHT_ARROW",    # Right
    0xff54: "HID_KEYBOARD_SC_DOWN_ARROW",    # Down
    0xff55: "HID_KEYBOARD_SC_PAGE_UP",    # Prior
    0xff56: "HID_KEYBOARD_SC_PAGE_DOWN",    # Next
    0xff57: "HID_KEYBOARD_SC_END",    # End
    0xff5b: "HID_KEYBOARD_SC_LEFT_GUI",    # Win_L
    0xff5c: "HID_KEYBOARD_SC_RIGHT_GUI",    # Win_R
    0xff5d: "HID_KEYBOARD_SC_APPLICATION",    # App
    0xff61: "HID_KEYBOARD_SC_PRINT_SCREEN",    # Print
    0xff63: "HID_KEYBOARD_SC_INSERT",    # Insert
    0xff69: "HID_KEYBOARD_SC_PAUSE",    # Cancel
    0xff7f: "HID_KEYBOARD_SC_NUM_LOCK",    # Num_Lock
    0xff8d: "HID_KEYBOARD_SC_KEYPAD_ENTER",    # KP_Enter
    0xffaa: "HID_KEYBOARD_SC_KEYPAD_ASTERISK",    # KP_Multiply
    0xffab: "HID_KEYBOARD_SC_KEYPAD_PLUS",    # KP_Add
    0xffad: "HID_KEYBOARD_SC_KEYPAD_MINUS",    # KP_Subtract
    0xffae: "HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE",    # KP_Decimal
    0xffaf: "HID_KEYBOARD_SC_KEYPAD_SLASH",    # KP_Divide
    0xffb0: "HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT",    # KP_0
    0xffb1: "HID_KEYBOARD_SC_KEYPAD_1_AND_END",    # KP_1
    0xffb2: "HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW",    # KP_2
    0xffb3: "HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN",    # KP_3
    0xffb4: "HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW",    # KP_4
    0xffb5: "HID_KEYBOARD_SC_KEYPAD_5",    # KP_5
    0xffb6: "HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW",    # KP_6
    0xffb7: "HID_KEYBOARD_SC_KEYPAD_7_AND_HOME",    # KP_7
    0xffb8: "HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW",    # KP_8
    0xffb9: "HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP",    # KP_9
    0xffbe: "HID_KEYBOARD_SC_F1",    # F1
    0xffbf: "HID_KEYBOARD_SC_F2",    # F2
    0xffc0: "HID_KEYBOARD_SC_F3",    # F3
    0xffc1: "HID_KEYBOARD_SC_F4",    # F4
    0xffc2: "HID_KEYBOARD_SC_F5",    # F5
    0xffc3: "HID_KEYBOARD_SC_F6",    # F6
    0xffc4: "HID_KEYBOARD_SC_F7",    # F7
    0xffc5: "HID_KEYBOARD_SC_F8",    # F8
    0xffc6: "HID_KEYBOARD_SC_F9",    # F9
    0xffc7: "HID_KEYBOARD_SC_F10",    # F10
    0xffc8: "HID_KEYBOARD_SC_F11",    # F11
    0xffc9: "HID_KEYBOARD_SC_F12",    # F12
    0xffe1: "HID_KEYBOARD_SC_LEFT_SHIFT",    # Shift_L
    0xffe2: "HID_KEYBOARD_SC_RIGHT_SHIFT",    # Shift_R
    0xffe3: "HID_KEYBOARD_SC_LEFT_CONTROL",    # Control_L
    0xffe4: "HID_KEYBOARD_SC_RIGHT_CONTROL",    # Control_R
    0xffe5: "HID_KEYBOARD_SC_CAPS_LOCK",    # Caps_Lock
    # 0xffe7: ,    # Meta_L
    # 0xffe8: ,    # Meta_R
    0xffe9: "HID_KEYBOARD_SC_LEFT_ALT",    # Alt_L
    0xffea: "HID_KEYBOARD_SC_RIGHT_ALT",    # Alt_R
    # 0xffeb: ,    # Super_L
    # 0xffec: ,    # Super_R
    # 0xffed: ,    # Hyper_L
    # 0xffee: ,    # Hyper_R
    0xffff: "HID_KEYBOARD_SC_DELETE",    # Delete
}

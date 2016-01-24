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

"""This file defines a window that displays all possible scancodes that
can be assigned to keys.
"""

from __future__ import print_function

try:
    from Tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
    
from easykeymap.scancodes import scancodes


UNIT = 12


class Selector(object):

    def __init__(self, parent, main, width, scancode):
        self.main = main
        self.scancode = scancode
        btn_frame = Frame(parent, width=(width*UNIT), height=(4*UNIT))
        btn_frame.pack_propagate(0)
        btn = Button(btn_frame,
                     text=scancodes[scancode][0],
                     command=self.on_press)
        btn.pack(fill=BOTH, expand=1)
        btn_frame.pack(side=LEFT, fill=BOTH, expand=1)

    def on_press(self):
        self.main.pickerselect(self.scancode)


class Spacer(object):

    def __init__(self, parent, width, height):
        btn_frame = Frame(parent, width=(width*UNIT), height=(height*UNIT))
        btn_frame.pack_propagate(0)
        btn_frame.pack(side=LEFT, fill=BOTH, expand=1)


class Picker(object):

    def __init__(self, main):
        self.main = main
        self.root = main.root
        self.createwindow()
        self.toplevel.withdraw()

    def show(self):
        self.toplevel.update()
        self.toplevel.deiconify()

    def lift(self):
        self.toplevel.lift()

    def userclosing(self):
        self.toplevel.withdraw()

    def createwindow(self):
        self.toplevel = Toplevel(self.root)
        self.toplevel.title("Scancode Picker")
        self.toplevel.resizable(0,0)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.userclosing)

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(1*UNIT))
        rowframe.pack(side=TOP)

        Spacer(rowframe, 8, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F13")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F14")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F15")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F16")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F17")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F18")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F19")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F20")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F21")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F22")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F23")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F24")
        Spacer(rowframe, 1, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_LOCKING_CAPS_LOCK")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_LOCKING_SCROLL_LOCK")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_LOCKING_NUM_LOCK")
        Spacer(rowframe, 17, 4)

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_ESCAPE")
        Spacer(rowframe, 4, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F1")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F2")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F3")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F4")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F5")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F6")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F7")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F8")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F9")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F10")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F11")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F12")
        Spacer(rowframe, 1, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_PRINT_SCREEN")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_SCROLL_LOCK")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_PAUSE")
        Spacer(rowframe, 13, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_POWER")

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(1*UNIT))
        rowframe.pack(side=TOP)

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_1_AND_EXCLAMATION")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_2_AND_AT")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_3_AND_HASHMARK")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_4_AND_DOLLAR")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_5_AND_PERCENTAGE")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_6_AND_CARET")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_7_AND_AND_AMPERSAND")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_8_AND_ASTERISK")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_EQUAL_AND_PLUS")
        Selector(rowframe, self.main, 8, "HID_KEYBOARD_SC_BACKSPACE")
        Spacer(rowframe, 1, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_INSERT")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_HOME")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_PAGE_UP")
        Spacer(rowframe, 1, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_NUM_LOCK")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_SLASH")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_ASTERISK")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_MINUS")

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 6, "HID_KEYBOARD_SC_TAB")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_Q")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_W")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_E")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_R")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_T")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_Y")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_U")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_I")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_O")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_P")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE")
        Selector(rowframe, self.main, 6, "HID_KEYBOARD_SC_BACKSLASH_AND_PIPE")
        Spacer(rowframe, 1, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_DELETE")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_END")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_PAGE_DOWN")
        Spacer(rowframe, 1, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_7_AND_HOME")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN")

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 7, "HID_KEYBOARD_SC_CAPS_LOCK")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_A")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_S")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_D")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_F")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_G")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_H")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_J")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_K")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_L")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_SEMICOLON_AND_COLON")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE")
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_ENTER")
        Spacer(rowframe, 14, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_5")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_PLUS")

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_LEFT_SHIFT")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_Z")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_X")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_C")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_V")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_B")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_N")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_M")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK")
        Selector(rowframe, self.main, 11, "HID_KEYBOARD_SC_RIGHT_SHIFT")
        Spacer(rowframe, 5, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_UP_ARROW")
        Spacer(rowframe, 5, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_1_AND_END")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_ENTER")

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_LEFT_CONTROL")
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_LEFT_GUI")
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_LEFT_ALT")
        Selector(rowframe, self.main, 25, "HID_KEYBOARD_SC_SPACE")
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_RIGHT_ALT")
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_RIGHT_GUI")
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_APPLICATION")
        Selector(rowframe, self.main, 5, "HID_KEYBOARD_SC_RIGHT_CONTROL")
        Spacer(rowframe, 1, 4)
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_LEFT_ARROW")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_DOWN_ARROW")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_RIGHT_ARROW")
        Spacer(rowframe, 1, 4)
        Selector(rowframe, self.main, 8, "HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE")
        Selector(rowframe, self.main, 4, "HID_KEYBOARD_SC_KEYPAD_ENTER")

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(1*UNIT))
        rowframe.pack(side=TOP)

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 4, "SCANCODE_FN")
        Selector(rowframe, self.main, 4, "SCANCODE_FN2")
        Selector(rowframe, self.main, 4, "SCANCODE_FN3")
        Selector(rowframe, self.main, 4, "SCANCODE_FN4")
        Selector(rowframe, self.main, 4, "SCANCODE_FN5")
        Selector(rowframe, self.main, 4, "SCANCODE_FN6")
        Selector(rowframe, self.main, 4, "SCANCODE_FN7")
        Selector(rowframe, self.main, 4, "SCANCODE_FN8")
        Selector(rowframe, self.main, 4, "SCANCODE_FN9")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "SCANCODE_MOUSE1")
        Selector(rowframe, self.main, 4, "SCANCODE_MOUSE2")
        Selector(rowframe, self.main, 4, "SCANCODE_MOUSE3")
        Selector(rowframe, self.main, 4, "SCANCODE_MOUSEXL")
        Selector(rowframe, self.main, 4, "SCANCODE_MOUSEYD")
        Selector(rowframe, self.main, 4, "SCANCODE_MOUSEYU")
        Selector(rowframe, self.main, 4, "SCANCODE_MOUSEXR")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "SCANCODE_KEYLOCK")
        Selector(rowframe, self.main, 4, "SCANCODE_WINLOCK")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "SCANCODE_ESCGRAVE")
        Spacer(rowframe, 8, 4)

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(1*UNIT))
        rowframe.pack(side=TOP)

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 4, "SCANCODE_M1")
        Selector(rowframe, self.main, 4, "SCANCODE_M2")
        Selector(rowframe, self.main, 4, "SCANCODE_M3")
        Selector(rowframe, self.main, 4, "SCANCODE_M4")
        Selector(rowframe, self.main, 4, "SCANCODE_M5")
        Selector(rowframe, self.main, 4, "SCANCODE_M6")
        Selector(rowframe, self.main, 4, "SCANCODE_M7")
        Selector(rowframe, self.main, 4, "SCANCODE_M8")
        Selector(rowframe, self.main, 4, "SCANCODE_M9")
        Selector(rowframe, self.main, 4, "SCANCODE_M10")
        Selector(rowframe, self.main, 4, "SCANCODE_M11")
        Selector(rowframe, self.main, 4, "SCANCODE_M12")
        Selector(rowframe, self.main, 4, "SCANCODE_M13")
        Selector(rowframe, self.main, 4, "SCANCODE_M14")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "SCANCODE_MRAM_RECORD")
        Selector(rowframe, self.main, 4, "SCANCODE_MRAM_PLAY")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "SCANCODE_PASSWORD1")
        Selector(rowframe, self.main, 4, "SCANCODE_PASSWORD2")
        Selector(rowframe, self.main, 4, "SCANCODE_PASSWORD3")
        Selector(rowframe, self.main, 4, "SCANCODE_PASSWORD4")
        Spacer(rowframe, 6, 4)

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(1*UNIT))
        rowframe.pack(side=TOP)

        rowframe = Frame(self.toplevel,
                         width=(int(22.5*4)*UNIT),
                         height=(4*UNIT))
        rowframe.pack(side=TOP)
        Selector(rowframe, self.main, 4, "SCANCODE_MUTE")
        Selector(rowframe, self.main, 4, "SCANCODE_VOL_INC")
        Selector(rowframe, self.main, 4, "SCANCODE_VOL_DEC")
        Selector(rowframe, self.main, 4, "SCANCODE_BASS_BOOST")
        Selector(rowframe, self.main, 4, "SCANCODE_NEXT_TRACK")
        Selector(rowframe, self.main, 4, "SCANCODE_PREV_TRACK")
        Selector(rowframe, self.main, 4, "SCANCODE_STOP")
        Selector(rowframe, self.main, 4, "SCANCODE_PLAY_PAUSE")
        Selector(rowframe, self.main, 4, "SCANCODE_BACK")
        Selector(rowframe, self.main, 4, "SCANCODE_FORWARD")
        Selector(rowframe, self.main, 4, "SCANCODE_MEDIA")
        Selector(rowframe, self.main, 4, "SCANCODE_MAIL")
        Selector(rowframe, self.main, 4, "SCANCODE_CALC")
        Selector(rowframe, self.main, 4, "SCANCODE_MYCOMP")
        Selector(rowframe, self.main, 4, "SCANCODE_SEARCH")
        Selector(rowframe, self.main, 4, "SCANCODE_BROWSER")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "SCANCODE_BL_DIMMER")
        Selector(rowframe, self.main, 4, "SCANCODE_BL_MODE")
        Selector(rowframe, self.main, 4, "SCANCODE_BL_ENABLE")
        Spacer(rowframe, 2, 4)
        Selector(rowframe, self.main, 4, "SCANCODE_BOOT")
        Selector(rowframe, self.main, 4, "SCANCODE_CONFIG")
        Spacer(rowframe, 2, 4)

if __name__ == '__main__':
    print("Picker must be run from the main GUI.")

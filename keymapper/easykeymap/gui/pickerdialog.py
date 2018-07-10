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

"""A dialog for selecting a scancode from a graphical layout of options."""

from collections import namedtuple

import wx

from ..scancodes import scancodes
from .scale import GRID_SIZE


# Anything above HID_KEYBOARD_SC_APPLICATION (mods and special functions)
SPECIAL_BOUNDARY = 0x65

Loc = namedtuple('Loc', ['row', 'col'])
Dim = namedtuple('Dim', ['height', 'width'])


class PickerLayout:
    """This class encapsulates the entire picker layout as a list of rows.  It
    enables the layout to be created with a minimum of boilerplate code.
    """

    def __init__(self, parent):
        self.parent = parent
        self.rows = []
        self.rowcount = 0

    def append(self):
        row = PickerRow(self.parent, self.rowcount)
        self.rowcount += 4
        self.rows.append(row)
        return row

    def spacer(self, count):
        self.rowcount += count

    def add_all(self):
        for row in self.rows:
            row.add_all()

    def enable_special(self, enable=True):
        for row in self.rows:
            row.enable_special(enable)


class PickerRow:
    """This class encapsulates one row of the picker layout as a list of keys.
    It enables the layout to be created with a minimum of boilerplate code.
    """

    def __init__(self, parent, rowcount):
        self.parent = parent
        self.rowcount = rowcount
        self.keys = []
        self.colcount = 0

    def append(self, scancode, dim):
        loc = Loc(self.rowcount, self.colcount)
        key = PickerKey(self.parent, loc, scancode, dim)
        self.colcount += dim.width
        self.keys.append(key)
        return key

    def spacer(self, count):
        self.colcount += count

    def add_all(self):
        for key in self.keys:
            key.add()

    def enable_special(self, enable=True):
        for key in self.keys:
            key.enable_special(enable)


class PickerKey:
    """This class encapsulates one key in the picker layout.  Each key is
    represented as a button, and clicking the button will end the dialog.
    It enables the layout to be created with a minimum of boilerplate code.
    """

    def __init__(self, parent, loc, scancode, dim):
        self.parent = parent
        self.loc = loc
        self.scancode = scancode
        self.dim = dim
        label = scancodes[scancode].display
        size = wx.Size(GRID_SIZE.width * dim.width, GRID_SIZE.height * dim.height)
        self.btn = wx.Button(self.parent, wx.ID_ANY, label, size=size)
        self.btn.SetToolTip(scancode)
        self.btn.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.special = scancodes[scancode].value > SPECIAL_BOUNDARY

    def add(self):
        self.parent.main_sizer.Add(self.btn, tuple(self.loc), tuple(self.dim), wx.EXPAND|wx.ALL, 0)

    def OnClicked(self, event):
        self.parent.selected_scancode = self.scancode
        self.parent.EndModal(wx.ID_OK)

    def enable_special(self, enable=True):
        if self.special:
            self.btn.Enable(enable=enable)


class PickerDialog(wx.Dialog):
    """A dialog for selecting a scancode from a graphical layout of options."""

    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Scancode Picker'
        wx.Dialog.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_CHAR_HOOK, self.OnCharHook)

        self.main_sizer = main_sizer = wx.GridBagSizer(0, 0)
        main_sizer.SetEmptyCellSize(GRID_SIZE)
        self.__create_layout()
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

        self.selected_scancode = "0"

    def OnCharHook(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def enable_special(self, enable=True):
        """If called with `enable` == False, all modifiers and non-standard keys
        are disabled so the user can't select them.
        """
        self.layout.enable_special(enable)

    def __create_layout(self):
        self.layout = layout = PickerLayout(self)
        row = layout.append()
        row.append("SCANCODE_ESCGRAVE", Dim(4, 4))
        row.spacer(4)
        row.append("HID_KEYBOARD_SC_F13", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F14", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F15", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F16", Dim(4, 4))
        row.spacer(2)
        row.append("HID_KEYBOARD_SC_F17", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F18", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F19", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F20", Dim(4, 4))
        row.spacer(2)
        row.append("HID_KEYBOARD_SC_F21", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F22", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F23", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F24", Dim(4, 4))
        row.spacer(1)
        row.append("HID_KEYBOARD_SC_LOCKING_CAPS_LOCK", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_LOCKING_SCROLL_LOCK", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_LOCKING_NUM_LOCK", Dim(4, 4))
        row.spacer(1)
        row.append("SCANCODE_POWER", Dim(4, 4))
        row.append("SCANCODE_SLEEP", Dim(4, 4))
        row.append("SCANCODE_WAKE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_POWER", Dim(4, 4))
        row = layout.append()
        row.append("HID_KEYBOARD_SC_ESCAPE", Dim(4, 4))
        row.spacer(4)
        row.append("HID_KEYBOARD_SC_F1", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F2", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F3", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F4", Dim(4, 4))
        row.spacer(2)
        row.append("HID_KEYBOARD_SC_F5", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F6", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F7", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F8", Dim(4, 4))
        row.spacer(2)
        row.append("HID_KEYBOARD_SC_F9", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F10", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F11", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F12", Dim(4, 4))
        row.spacer(1)
        row.append("HID_KEYBOARD_SC_PRINT_SCREEN", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_SCROLL_LOCK", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_PAUSE", Dim(4, 4))
        row.spacer(1)
        row.append("SCANCODE_KEYLOCK", Dim(4, 4))
        row.append("SCANCODE_WINLOCK", Dim(4, 4))
        row.append("0", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN", Dim(4, 4))
        layout.spacer(1)
        row = layout.append()
        row.append("HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_1_AND_EXCLAMATION", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_2_AND_AT", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_3_AND_HASHMARK", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_4_AND_DOLLAR", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_5_AND_PERCENTAGE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_6_AND_CARET", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_7_AND_AND_AMPERSAND", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_8_AND_ASTERISK", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_EQUAL_AND_PLUS", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_BACKSPACE", Dim(4, 8))
        row.spacer(1)
        row.append("HID_KEYBOARD_SC_INSERT", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_HOME", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_PAGE_UP", Dim(4, 4))
        row.spacer(1)
        row.append("HID_KEYBOARD_SC_NUM_LOCK", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_SLASH", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_ASTERISK", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_MINUS", Dim(4, 4))
        row = layout.append()
        row.append("HID_KEYBOARD_SC_TAB", Dim(4, 6))
        row.append("HID_KEYBOARD_SC_Q", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_W", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_E", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_R", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_T", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_Y", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_U", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_I", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_O", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_P", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_BACKSLASH_AND_PIPE", Dim(4, 6))
        row.spacer(1)
        row.append("HID_KEYBOARD_SC_DELETE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_END", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_PAGE_DOWN", Dim(4, 4))
        row.spacer(1)
        row.append("HID_KEYBOARD_SC_KEYPAD_7_AND_HOME", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_PLUS", Dim(8, 4))
        row = layout.append()
        row.append("HID_KEYBOARD_SC_CAPS_LOCK", Dim(4, 7))
        row.append("HID_KEYBOARD_SC_A", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_S", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_D", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_F", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_G", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_H", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_J", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_K", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_L", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_SEMICOLON_AND_COLON", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_ENTER", Dim(4, 5))
        row.spacer(14)
        row.append("HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_5", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW", Dim(4, 4))
        row = layout.append()
        row.append("HID_KEYBOARD_SC_LEFT_SHIFT", Dim(4, 5))
        row.append("HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_Z", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_X", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_C", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_V", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_B", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_N", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_M", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_RIGHT_SHIFT", Dim(4, 11))
        row.spacer(5)
        row.append("HID_KEYBOARD_SC_UP_ARROW", Dim(4, 4))
        row.spacer(5)
        row.append("HID_KEYBOARD_SC_KEYPAD_1_AND_END", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_KEYPAD_ENTER", Dim(8, 4))
        row = layout.append()
        row.append("HID_KEYBOARD_SC_LEFT_CONTROL", Dim(4, 5))
        row.append("HID_KEYBOARD_SC_LEFT_GUI", Dim(4, 5))
        row.append("HID_KEYBOARD_SC_LEFT_ALT", Dim(4, 5))
        row.append("HID_KEYBOARD_SC_SPACE", Dim(4, 25))
        row.append("HID_KEYBOARD_SC_RIGHT_ALT", Dim(4, 5))
        row.append("HID_KEYBOARD_SC_RIGHT_GUI", Dim(4, 5))
        row.append("HID_KEYBOARD_SC_APPLICATION", Dim(4, 5))
        row.append("HID_KEYBOARD_SC_RIGHT_CONTROL", Dim(4, 5))
        row.spacer(1)
        row.append("HID_KEYBOARD_SC_LEFT_ARROW", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_DOWN_ARROW", Dim(4, 4))
        row.append("HID_KEYBOARD_SC_RIGHT_ARROW", Dim(4, 4))
        row.spacer(1)
        row.append("HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT", Dim(4, 8))
        row.append("HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE", Dim(4, 4))
        layout.spacer(1)
        row = layout.append()
        row.append("SCANCODE_BOOT", Dim(4, 4))
        row.append("SCANCODE_CONFIG", Dim(4, 4))
        row.append("SCANCODE_FN0", Dim(4, 4))
        row.append("SCANCODE_FN1", Dim(4, 4))
        row.spacer(1)
        row.append("SCANCODE_M1", Dim(4, 4))
        row.append("SCANCODE_M2", Dim(4, 4))
        row.append("SCANCODE_M3", Dim(4, 4))
        row.append("SCANCODE_M4", Dim(4, 4))
        row.append("SCANCODE_M5", Dim(4, 4))
        row.append("SCANCODE_M6", Dim(4, 4))
        row.append("SCANCODE_MOUSE1", Dim(4, 4))
        row.append("SCANCODE_MOUSE2", Dim(4, 4))
        row.append("SCANCODE_MOUSE3", Dim(4, 4))
        row.append("SCANCODE_NEXT_TRACK", Dim(4, 4))
        row.append("SCANCODE_PREV_TRACK", Dim(4, 4))
        row.append("SCANCODE_STOP", Dim(4, 4))
        row.append("SCANCODE_PLAY_PAUSE", Dim(4, 4))
        row.append("SCANCODE_BRIGHT_INC", Dim(4, 4))
        row.append("SCANCODE_BRIGHT_DEC", Dim(4, 4))
        row.append("SCANCODE_MUTE", Dim(4, 4))
        row.append("SCANCODE_BASS_BOOST", Dim(4, 4))
        row.spacer(1)
        row.append("SCANCODE_BL_ENABLE", Dim(4, 4))
        row = layout.append()
        row.append("SCANCODE_FN2", Dim(4, 4))
        row.append("SCANCODE_FN3", Dim(4, 4))
        row.append("SCANCODE_FN4", Dim(4, 4))
        row.append("SCANCODE_FN5", Dim(4, 4))
        row.spacer(1)
        row.append("SCANCODE_M7", Dim(4, 4))
        row.append("SCANCODE_M8", Dim(4, 4))
        row.append("SCANCODE_M9", Dim(4, 4))
        row.append("SCANCODE_M10", Dim(4, 4))
        row.append("SCANCODE_M11", Dim(4, 4))
        row.append("SCANCODE_M12", Dim(4, 4))
        row.append("0", Dim(4, 4))
        row.append("SCANCODE_MOUSEYU", Dim(4, 4))
        row.append("0", Dim(4, 4))
        row.append("SCANCODE_VOL_INC", Dim(4, 4))
        row.append("SCANCODE_VOL_DEC", Dim(4, 4))
        row.append("SCANCODE_BASS_INC", Dim(4, 4))
        row.append("SCANCODE_BASS_DEC", Dim(4, 4))
        row.append("SCANCODE_TREB_INC", Dim(4, 4))
        row.append("SCANCODE_TREB_DEC", Dim(4, 4))
        row.append("SCANCODE_BACK", Dim(4, 4))
        row.append("SCANCODE_FORWARD", Dim(4, 4))
        row.spacer(1)
        row.append("SCANCODE_BL_DIMMER", Dim(4, 4))
        row = layout.append()
        row.append("SCANCODE_FN6", Dim(4, 4))
        row.append("SCANCODE_FN7", Dim(4, 4))
        row.append("SCANCODE_FN8", Dim(4, 4))
        row.append("SCANCODE_FN9", Dim(4, 4))
        row.spacer(1)
        row.append("SCANCODE_M13", Dim(4, 4))
        row.append("SCANCODE_M14", Dim(4, 4))
        row.append("SCANCODE_M15", Dim(4, 4))
        row.append("SCANCODE_M16", Dim(4, 4))
        row.append("SCANCODE_MRAM_RECORD", Dim(4, 4))
        row.append("SCANCODE_MRAM_PLAY", Dim(4, 4))
        row.append("SCANCODE_MOUSEXL", Dim(4, 4))
        row.append("SCANCODE_MOUSEYD", Dim(4, 4))
        row.append("SCANCODE_MOUSEXR", Dim(4, 4))
        row.append("SCANCODE_MAIL", Dim(4, 4))
        row.append("SCANCODE_CALC", Dim(4, 4))
        row.append("SCANCODE_MYCOMP", Dim(4, 4))
        row.append("SCANCODE_SEARCH", Dim(4, 4))
        row.append("SCANCODE_BROWSER", Dim(4, 4))
        row.append("SCANCODE_WWWSTOP", Dim(4, 4))
        row.append("SCANCODE_REFRESH", Dim(4, 4))
        row.append("SCANCODE_FAVES", Dim(4, 4))
        row.spacer(1)
        row.append("SCANCODE_BL_MODE", Dim(4, 4))
        layout.add_all()

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

"""A configuration panel for capturing macro assignments."""

import wx

from ..build import NUM_MACROS
from .scale import MARGIN


labels = [("M%d" % (i+1)) for i in range(NUM_MACROS)]

# Must sync with ..scancodes.char_map and ..macroparse.modmap
macro_hints = [
    "$$",
    "",
    "Modifier Functions:",
    "$LCTRL()",
    "$LSHIFT()",
    "$LALT()",
    "$LGUI()",
    "$RCTRL()",
    "$RSHIFT()",
    "$RALT()",
    "$RGUI()",
    "",
    "Modifier Aliases:",
    "$CTRL()",
    "$SHIFT()",
    "$ALT()",
    "$ALTGR()",
    "$OPTION()",
    "$GUI()",
    "$WIN()",
    "$COMMAND()",
    "$META()",
    "",
    "Special Functions:",
    "$WAIT()",
    "$HINT()",
    "",
    "Non-printable keys:",
    "${ESC}",
    "${F1}",
    "${F2}",
    "${F3}",
    "${F4}",
    "${F5}",
    "${F6}",
    "${F7}",
    "${F8}",
    "${F9}",
    "${F10}",
    "${F11}",
    "${F12}",
    "${F13}",
    "${F14}",
    "${F15}",
    "${F16}",
    "${F17}",
    "${F18}",
    "${F19}",
    "${F20}",
    "${F21}",
    "${F22}",
    "${F23}",
    "${F24}",
    "${PRINT}",
    "${PAUSE}",
    "${SCRLK}",
    "${NUMLK}",
    "${CAPSLK}",
    "${INS}",
    "${DEL}",
    "${HOME}",
    "${END}",
    "${PGUP}",
    "${PGDN}",
    "${TAB}",
    "${BKSP}",
    "${ENTER}",
    "${UP}",
    "${DOWN}",
    "${LEFT}",
    "${RIGHT}",
    "${SPACE}",
    "${APP}",
    "${NON_US_BACKSLASH}",
    "",
    "Keypad keys:",
    "${KPSLA}",
    "${KPAST}",
    "${KPMIN}",
    "${KPPLS}",
    "${KPENT}",
    "${KP1}",
    "${KP2}",
    "${KP3}",
    "${KP4}",
    "${KP5}",
    "${KP6}",
    "${KP7}",
    "${KP8}",
    "${KP9}",
    "${KP0}",
    "${KPDOT}",
    "${KPEQ}",
    "",
    "Media keys:",
    "${MUTE}",
    "${VOLUP}",
    "${VOLDN}",
    "${BASS}",
    "${NEXT}",
    "${PREV}",
    "${STOP}",
    "${PLAY}",
    "${MAIL}",
    "${CALC}",
    "${MYCOMP}",
    "${SEARCH}",
    "${BROWSER}",
    "${BACK}",
    "${FORWARD}",
    "${WWWSTOP}",
    "${REFRESH}",
    "${FAVES}",
]


class MacroPanel(wx.Panel):
    """A configuration panel for capturing macro assignments."""

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.user_data = None

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        font = wx.Font(wx.FontInfo().FaceName("Consolas"))
        if not font.IsOk():
            font = wx.Font(wx.FontInfo().Family(wx.FONTFAMILY_TELETYPE))

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.main_rb = wx.RadioBox(self, label="Macro Selection", choices=labels)
        self.Bind(wx.EVT_RADIOBOX, self.OnMacroChanged, self.main_rb)
        main_sizer.Add(self.main_rb, flag=wx.ALL, border=MARGIN)

        edit_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.main_tc = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB|wx.TE_NOHIDESEL)
        self.main_tc.SetOwnFont(font)
        self.Bind(wx.EVT_TEXT, self.OnMainText, self.main_tc)
        edit_sizer.Add(self.main_tc, proportion=1, flag=wx.EXPAND|wx.ALL, border=MARGIN)

        list_sizer = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(self, label="Keyword List:")
        st.SetToolTip("Double-click a keyword to enter it into the current macro.")
        list_sizer.Add(st, flag=wx.TOP|wx.LEFT|wx.RIGHT, border=MARGIN)
        snippet_lb = wx.ListBox(self, choices=macro_hints)
        snippet_lb.SetOwnFont(font)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSnippetDclick, snippet_lb)
        list_sizer.Add(snippet_lb, proportion=1, flag=wx.EXPAND|wx.ALL, border=MARGIN)

        edit_sizer.Add(list_sizer, flag=wx.EXPAND)
        main_sizer.Add(edit_sizer, proportion=1, flag=wx.EXPAND)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

    def load_macros(self, user_data):
        """Dump the existing macros and repopulate using a new `user_data` object."""
        self.user_data = user_data
        self.main_rb.SetSelection(0)
        self.main_tc.ChangeValue(self.user_data.macros[0])
        self.main_tc.DiscardEdits()

    def OnMacroChanged(self, event):
        if self.user_data is not None:
            self.main_tc.ChangeValue(self.user_data.macros[event.GetInt()])
            self.main_tc.DiscardEdits()

    def OnSnippetDclick(self, event):
        snippet = macro_hints[event.GetInt()]
        if snippet.startswith('$'):
            self.main_tc.WriteText(snippet)
            self.timer.Start(1000)
            if snippet.endswith(')'):
                pos = self.main_tc.GetInsertionPoint()
                self.main_tc.SetInsertionPoint(pos - 1)

    def OnMainText(self, event):
        """Don't save for every keystroke, that would cause excessive announcements."""
        self.timer.Start(1000)

    def OnTimer(self, event):
        if (self.user_data is not None) and (self.main_tc.IsModified()):
            self.user_data.macros[self.main_rb.GetSelection()] = self.main_tc.GetValue()
            self.user_data.announce('macros')
            self.main_tc.DiscardEdits()

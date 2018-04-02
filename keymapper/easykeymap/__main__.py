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

"""This is the main entry point for the keymapper application."""

import wx

from .gui.mainframe import MainFrame


class EasyApp(wx.App):
    """Launches the EasyAVR keymapper application."""

    def OnInit(self):
        self.SetVendorName("dhowland")
        self.SetAppName("easykeymap")
        self.SetClassName("easykeymap")
        main_frame = MainFrame(None)
        self.SetTopWindow(main_frame)
        main_frame.Show(True)
        # self.RedirectStdio()
        return True


app = EasyApp()
app.MainLoop()

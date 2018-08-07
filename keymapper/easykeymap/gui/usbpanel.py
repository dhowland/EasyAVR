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

"""A configuration panel for capturing USB endpoint enables."""

import wx

from ..userdata import Opts
from .scale import MARGIN


class UsbPanel(wx.Panel):
    """A configuration panel for capturing USB endpoint enables."""

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.user_data = None

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        usb_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, "USB Endpoint Enables")
        label = "Standard USB HID keyboard, Boot compatible, 6KRO"
        self.keyboard_cb = wx.CheckBox(usb_sizer.GetStaticBox(), label=label)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckbox, self.keyboard_cb)
        self.keyboard_cb.Enable(False)
        self.keyboard_cb.SetValue(True)
        usb_sizer.Add(self.keyboard_cb, flag=wx.ALL, border=MARGIN)
        label = "Microsoft Windows compatible media and power controls"
        self.media_cb = wx.CheckBox(usb_sizer.GetStaticBox(), label=label)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckbox, self.media_cb)
        usb_sizer.Add(self.media_cb, flag=wx.ALL, border=MARGIN)
        label = "NKRO, Enables simultaneous activation of all keys"
        self.nkro_cb = wx.CheckBox(usb_sizer.GetStaticBox(), label=label)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckbox, self.nkro_cb)
        usb_sizer.Add(self.nkro_cb, flag=wx.ALL, border=MARGIN)
        label = "Standard USB HID mouse, Boot compatible, 3-button"
        self.mouse_cb = wx.CheckBox(usb_sizer.GetStaticBox(), label=label)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckbox, self.mouse_cb)
        usb_sizer.Add(self.mouse_cb, flag=wx.ALL, border=MARGIN)

        main_sizer.Add(usb_sizer, flag=wx.ALL, border=MARGIN)

        win_warn = wx.StaticText(self, label="Note for Windows users:\n\nWindows is known to become "
                                             "confused when the USB endpoints are changed.\nIf your "
                                             "keyboard stops working, try uninstalling the keyboard "
                                             "from the Devices\ncontrol panel or simply moving it "
                                             "to a different USB port.")
        main_sizer.Add(win_warn, flag=wx.ALL, border=MARGIN*2)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

    def load_opts(self, user_data):
        """Load USB endpoint options from a new `user_data` object."""
        self.user_data = user_data
        self.keyboard_cb.SetValue(user_data.usb_opts.keyboard)
        self.media_cb.SetValue(user_data.usb_opts.media)
        self.nkro_cb.SetValue(user_data.usb_opts.nkro)
        self.mouse_cb.SetValue(user_data.usb_opts.mouse)
        if user_data.config.firmware.simple:
            self.nkro_cb.Enable(False)
            self.mouse_cb.Enable(False)
        else:
            self.nkro_cb.Enable(True)
            self.mouse_cb.Enable(True)

    def OnCheckbox(self, event):
        self.user_data.usb_opts = Opts(self.keyboard_cb.GetValue(), self.media_cb.GetValue(),
                                       self.nkro_cb.GetValue(), self.mouse_cb.GetValue())
        self.user_data.announce('usb_opts')

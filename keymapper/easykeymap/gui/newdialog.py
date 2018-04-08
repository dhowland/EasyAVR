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

"""A dialog for selecting a keyboard for a new layout."""

import wx

from .scale import MARGIN


class NewDialog(wx.Dialog):
    """A dialog for selecting a keyboard for a new layout."""

    def __init__(self, *args, **kwargs):
        """The `conf` argument must be supplied as the configurations map."""
        self.configurations = kwargs['conf']
        del kwargs['conf']
        kwargs['title'] = 'New Keyboard Layout'
        wx.Dialog.__init__(self, *args, **kwargs)

        self.selected_id = None
        self.selected_layout = None

        # Establish a canonical order for the options in alphabetical order
        self.conflist = sorted(
            [(k, self.configurations[k].description) for k in self.configurations.keys()],
            key=lambda x: x[1]
        )
        names = list([x[1] for x in self.conflist])

        SPLIT = 16
        n = len(names) % SPLIT
        while (n > 0) and (n < 8):
            SPLIT += 1
            n = len(names) % SPLIT

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_rb = wx.RadioBox(self, wx.ID_ANY, "Hardware Selection", choices=names,
                              majorDimension=SPLIT, style=wx.RA_SPECIFY_ROWS)
        self.Bind(wx.EVT_RADIOBOX, self.OnSelectionChanged, main_rb)
        main_sizer.Add(main_rb, flag=wx.EXPAND|wx.ALL, border=MARGIN)

        conf_sizer = wx.BoxSizer(wx.HORIZONTAL)

        st = wx.StaticText(self, label="Layout Customization:")
        conf_sizer.Add(st, flag=wx.ALIGN_CENTER)
        conf_sizer.AddSpacer(MARGIN)
        self.layout_ch = wx.Choice(self, wx.ID_ANY)
        self.Bind(wx.EVT_CHOICE, self.OnLayoutChanged, self.layout_ch)
        conf_sizer.Add(self.layout_ch, proportion=1, flag=wx.EXPAND)
        conf_sizer.AddStretchSpacer(2)

        main_sizer.Add(conf_sizer, flag=wx.ALL|wx.EXPAND, border=MARGIN)

        dlgbtn_sizer = wx.StdDialogButtonSizer()
        dlgbtn_sizer.AddButton(wx.Button(self, wx.ID_OK))
        dlgbtn_sizer.AddButton(wx.Button(self, wx.ID_CANCEL))
        dlgbtn_sizer.Realize()
        main_sizer.Add(dlgbtn_sizer, flag=wx.EXPAND|wx.ALL, border=MARGIN)

        self.FindWindow(wx.ID_OK).SetDefault()
        self.SetSizerAndFit(main_sizer)
        self.Layout()

        self._selected(main_rb.GetSelection())

    def OnSelectionChanged(self, event):
        self._selected(event.GetInt())

    def _selected(self, i):
        self.selected_id = self.conflist[i][0]
        config = self.configurations[self.selected_id]
        layouts = ["<All Keys>"]
        layouts.extend(sorted(config.alt_layouts.keys()))
        self.layout_ch.Clear()
        self.layout_ch.Set(layouts)
        self.layout_ch.SetSelection(0)
        self.selected_layout = None

    def OnLayoutChanged(self, event):
        if event.GetInt() == 0:
            self.selected_layout = None
        else:
            self.selected_layout = event.GetString()

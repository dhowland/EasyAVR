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

"""A configuration panel for capturing LED assignments."""

import wx

from ..build import led_modes, led_assignments
from .layoutpanel import labels as layers
from .scale import MARGIN


layer_select = ['No Action']
layer_select.extend(layers[1:])
hid_leds = ['Num Lock', 'Caps Lock', 'Scroll Lock', 'Compose', 'Kana']
led_blips = ['Solid', '1 Blip', '2 Blips', '3 Blips', '4 Blips',
             '5 Blips', '6 Blips', '7 Blips', '8 Blips', '9 Blips']
# view_order items must match led_assignments!
view_order = ['Num Lock',    'Recording',      # noqa: E241
              'Caps Lock',   'Fn1 Active',     # noqa: E241
              'Scroll Lock', 'Fn2 Active',     # noqa: E241
              'Compose',     'Fn3 Active',     # noqa: E241
              'Kana',        'Fn4 Active',     # noqa: E241
              'Win Lock',    'Fn5 Active',     # noqa: E241
              'KB Lock',     'Fn6 Active',     # noqa: E241
              'USB Init',    'Fn7 Active',     # noqa: E241
              'USB Error',   'Fn8 Active',     # noqa: E241
              'USB Suspend', 'Fn9 Active',     # noqa: E241
              'USB Normal',  'Any Fn Active']  # noqa: E241


class LedPanel(wx.Panel):
    """A configuration panel for capturing LED assignments."""

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.main_sizer = main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.modes_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, "LED Mode Configuration")
        self.modes_panel = wx.Panel(self.modes_sizer.GetStaticBox(), size=(2*MARGIN, 2*MARGIN))
        self.modes_sizer.Add(self.modes_panel)
        main_sizer.Add(self.modes_sizer, flag=wx.ALL, border=MARGIN)

        self.assign_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, "LED Function Assignments")
        self.assign_panel = wx.Panel(self.assign_sizer.GetStaticBox(), size=(2*MARGIN, 2*MARGIN))
        self.assign_sizer.Add(self.assign_panel)
        main_sizer.Add(self.assign_sizer, flag=wx.ALL, border=MARGIN)

        self.autofn_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, "LED Auto Layer Select")
        self.autofn_panel = wx.Panel(self.autofn_sizer.GetStaticBox(), size=(2*MARGIN, 2*MARGIN))
        self.autofn_sizer.Add(self.autofn_panel)
        main_sizer.Add(self.autofn_sizer, flag=wx.ALL, border=MARGIN)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

    def load_leds(self, user_data):
        """Dump the existing selectors and recreate using a new `user_data` object."""
        self.user_data = user_data

        old_modes_panel = self.modes_panel
        sb = self.modes_sizer.GetStaticBox()
        self.modes_panel = ModePanel(sb, user_data=self.user_data)
        self.modes_sizer.Replace(old_modes_panel, self.modes_panel)
        old_modes_panel.Destroy()
        del old_modes_panel

        old_assign_panel = self.assign_panel
        sb = self.assign_sizer.GetStaticBox()
        self.assign_panel = AssignPanel(sb, user_data=self.user_data)
        self.assign_sizer.Replace(old_assign_panel, self.assign_panel)
        old_assign_panel.Destroy()
        del old_assign_panel

        old_autofn_panel = self.autofn_panel
        sb = self.autofn_sizer.GetStaticBox()
        self.autofn_panel = AutoFnPanel(sb, user_data=self.user_data)
        self.autofn_sizer.Replace(old_autofn_panel, self.autofn_panel)
        old_autofn_panel.Destroy()
        del old_autofn_panel

        self.main_sizer.Fit(self)


class ModePanel(wx.Panel):
    """A sub panel for LED mode configuration."""

    def __init__(self, *args, **kwargs):
        """The `user_data` argument must be supplied as the current user save data."""
        self.user_data = kwargs['user_data']
        del kwargs['user_data']
        wx.Panel.__init__(self, *args, **kwargs)

        self.choices = []

        main_sizer = wx.FlexGridSizer(2, MARGIN, MARGIN)
        for led_id, mode in enumerate(self.user_data.led_modes):
            name, _ = self.user_data.config.led_definition[led_id]
            st = wx.StaticText(self, label=name)
            main_sizer.Add(st, flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            ch = wx.Choice(self, choices=led_modes)
            ch.SetToolTip("Disabled: always off\n"
                          "Indicator: can be assigned to a function\n"
                          "Backlight: blend in with backlighting")
            ch.led_id = led_id
            # selection order is the same as led_modes enumeration
            ch.SetSelection(mode)
            self.Bind(wx.EVT_CHOICE, self.OnChoice, ch)
            main_sizer.Add(ch, flag=wx.ALIGN_CENTER_VERTICAL)
            self.choices.append(ch)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()
        self.user_data.subscribe(self.assign_changed, ['led_funcs'])

    def OnChoice(self, event):
        ch = event.GetEventObject()
        # selection order is the same as led_modes enumeration
        self.user_data.led_modes[ch.led_id] = ch.GetSelection()
        self.user_data.announce('led_modes')

    def assign_changed(self, user_data, config_item):
        """Find any led functions that have been assigned to LEDs, and make sure those LEDs
        are set to 'Indicator'.
        """
        for assign, _ in self.user_data.led_funcs:
            if assign != 255:
                ch = self.choices[assign]
                ind_val = led_modes.index('Indicator')
                ch.SetSelection(ind_val)
                self.user_data.led_modes[assign] = ind_val


class AssignPanel(wx.Panel):
    """A sub panel for LED function assignments."""

    def __init__(self, *args, **kwargs):
        """The `user_data` argument must be supplied as the current user save data."""
        self.user_data = kwargs['user_data']
        del kwargs['user_data']
        wx.Panel.__init__(self, *args, **kwargs)

        self.choices = {}

        leds = ['Unassigned']
        leds.extend([name for name, _ in self.user_data.config.led_definition])

        main_sizer = wx.FlexGridSizer(6, MARGIN, MARGIN)
        for led_fn in view_order:
            conf_index = led_assignments.index(led_fn)
            assign, blips = self.user_data.led_funcs[conf_index]
            st = wx.StaticText(self, label=led_fn)
            main_sizer.Add(st, flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            assign_ch = wx.Choice(self, choices=leds)
            assign_ch.SetToolTip("Selected LED indicates when the\n"
                                 "corresponding function is active")
            assign_ch.conf_index = conf_index
            sel_index = 0 if (assign == 255) else (assign + 1)
            assign_ch.SetSelection(sel_index)
            self.Bind(wx.EVT_CHOICE, self.OnChoice, assign_ch)
            main_sizer.Add(assign_ch, flag=wx.ALIGN_CENTER_VERTICAL)
            blip_ch = wx.Choice(self, choices=led_blips)
            blip_ch.SetToolTip("LED will blink with selected pattern when\n"
                               "the corresponding function is active")
            blip_ch.conf_index = conf_index
            blip_ch.SetSelection(blips)
            self.Bind(wx.EVT_CHOICE, self.OnChoice, blip_ch)
            main_sizer.Add(blip_ch, flag=wx.ALIGN_CENTER_VERTICAL)
            self.choices[conf_index] = (assign_ch, blip_ch)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()
        self.user_data.subscribe(self.mode_changed, ['led_modes'])

    def OnChoice(self, event):
        ch = event.GetEventObject()
        conf_index = ch.conf_index
        assign_ch, blip_ch = self.choices[conf_index]
        assign_sel = assign_ch.GetSelection()
        assign = 255 if (assign_sel == 0) else (assign_sel - 1)
        blips = blip_ch.GetSelection()
        self.user_data.led_funcs[conf_index] = (assign, blips)
        self.user_data.announce('led_funcs')

    def mode_changed(self, user_data, config_item):
        """Find any LEDs that are set to 'Backlight' or 'Disabled' and make sure those LEDs
        are not assigned to LED functions.
        """
        for led_id, mode in enumerate(self.user_data.led_modes):
            if mode != led_modes.index('Indicator'):
                for conf_index, led_func in enumerate(self.user_data.led_funcs):
                    assign, blips = led_func
                    if assign == led_id:
                        assign_ch, blip_ch = self.choices[conf_index]
                        assign_ch.SetSelection(0)
                        blip_ch.SetSelection(0)
                        self.user_data.led_funcs[conf_index] = (255, 0)


class AutoFnPanel(wx.Panel):
    """A sub panel for LED auto layer configuration."""

    def __init__(self, *args, **kwargs):
        """The `user_data` argument must be supplied as the current user save data."""
        self.user_data = kwargs['user_data']
        del kwargs['user_data']
        wx.Panel.__init__(self, *args, **kwargs)

        main_sizer = wx.FlexGridSizer(2, MARGIN, MARGIN)
        for i, led in enumerate(hid_leds):
            st = wx.StaticText(self, label=led)
            main_sizer.Add(st, flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            ch = wx.Choice(self, choices=layer_select)
            ch.SetToolTip("Selected layer becomes default when the\n"
                          "PC activates the corresponding indicator")
            ch.hid_id = i
            # selection order is the same as led_layers enumeration
            ch.SetSelection(self.user_data.led_layers[i])
            self.Bind(wx.EVT_CHOICE, self.OnChoice, ch)
            main_sizer.Add(ch, flag=wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

    def OnChoice(self, event):
        ch = event.GetEventObject()
        # selection order is the same as led_layers enumeration
        self.user_data.led_layers[ch.hid_id] = ch.GetSelection()
        self.user_data.announce('led_layers')

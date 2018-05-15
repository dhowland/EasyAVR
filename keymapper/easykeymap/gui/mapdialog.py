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

"""A dialog for updating the mapping of a single key."""

import wx
import wx.propgrid as wxpg

from ..build import key_mode_map, with_mods_map, NULL_SYMBOL
from ..scancodes import char_map, keycode_map


class MapDialog(wx.Dialog):
    """A dialog for updating the mapping of a single key."""

    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Key Config'
        wx.Dialog.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_CHAR_HOOK, self.OnCharHook)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.pg = pg = wxpg.PropertyGrid(self)

        pg.Bind(wxpg.EVT_PG_CHANGED, self.OnPropGridChange)

        pg.Append(wxpg.PropertyCategory("Key Parameters"))

        prop = wxpg.StringProperty("Layout Coordinates", "layout", value="Row 0, Col 0")
        prop.ChangeFlag(wxpg.PG_PROP_READONLY, True)
        pg.Append(prop)
        prop = wxpg.StringProperty("Matrix Coordinates", "matrix", value="Row 0, Col 0")
        prop.ChangeFlag(wxpg.PG_PROP_READONLY, True)
        pg.Append(prop)
        prop = wxpg.StringProperty("Key Geometry", "geom", value="Height 0, Width 0")
        prop.ChangeFlag(wxpg.PG_PROP_READONLY, True)
        pg.Append(prop)

        pg.Append(wxpg.PropertyCategory("Key Assignment"))

        pg.Append(ScancodeProperty("Scancode", "code"))
        pg.LimitPropertyEditing("code", limit=True)

        labels = list(key_mode_map.keys())
        values = list(key_mode_map.values())
        pg.Append(wxpg.EnumProperty("Mode", "mode", labels=labels, values=values))

        pg.Append(ScancodeProperty("Tap Code", "tap"))
        pg.LimitPropertyEditing("tap", limit=True)
        pg.EnableProperty("tap", enable=False)

        labels = list(with_mods_map.keys())
        values = list(with_mods_map.values())
        prop = wxpg.FlagsProperty("Automods", "wmods", labels=labels, values=values)
        prop.SetAttribute(wxpg.PG_BOOL_USE_CHECKBOX, True)
        pg.Append(prop)
        pg.LimitPropertyEditing(prop, limit=True)

        pg.ExpandAll()
        minHeight = (13 * pg.GetRowHeight()) + 4
        minWidth = int(minHeight * 1.25)
        pg.SetMinSize((minWidth, minHeight))
        pg.FitColumns()

        main_sizer.Add(pg, proportion=1, flag=wx.EXPAND)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()

    def OnCharHook(self, event):
        """Called when the user presses a keyboard key while the dialog is focused.
        This allows the user to take a shortcut to assigning keycodes without using
        the picker tool, but it can't handle all keycodes.  Navigation keys are
        not intercepted so the user can still use the keyboard to operate the
        property grid.
        """
        keycode = event.GetKeyCode()
        if (keycode > 32) and (keycode < 127):
            # printable ASCII characters
            scancode = char_map[chr(keycode)].scancode
        elif keycode in keycode_map:
            # non-printable keys, except PropertyGrid navigation
            scancode = keycode_map[keycode]
        else:
            # PropertyGrid navigation
            event.Skip()
            return
        self.pg.SetPropertyValueString('code', scancode)
        self.key_btn.update_map('code', scancode)
        self._update_title()

    def OnPropGridChange(self, event):
        prop = event.GetPropertyName()
        if prop == 'mode':
            self._enable_tap()
        if prop == 'code':
            self._update_title()
        self.key_btn.update_map(prop, event.GetPropertyValue())

    def _enable_tap(self):
        if self.pg.GetPropertyValue('mode') == key_mode_map['Tap Key']:
            self.pg.EnableProperty("tap", enable=True)
        else:
            self.pg.EnableProperty("tap", enable=False)

    def _update_title(self):
        self.SetTitle(self.key_btn.GetLabel().replace('\n', ' '))

    def switch_key(self, key_btn):
        self.key_btn = key_btn
        self.pg.SetPropertyValues(key_btn.props)
        self._enable_tap()
        self._update_title()


class PickerDialogAdapter(wxpg.PGEditorDialogAdapter):
    """Adapt the picker dialog for use with a PGproperty."""

    def __init__(self, with_specials=True):
        wxpg.PGEditorDialogAdapter.__init__(self)
        self.with_specials = with_specials

    def DoShowDialog(self, propGrid, prop):
        # propGrid -> MapDialog -> KeyPanel -> picker_dialog
        picker_dialog = propGrid.GetParent().GetParent().picker_dialog
        picker_dialog.enable_special(self.with_specials)
        if picker_dialog.ShowModal() == wx.ID_OK:
            self.SetValue(picker_dialog.selected_scancode)
            return True
        else:
            return False


class ScancodeProperty(wxpg.StringProperty):
    """A StringProperty that is edited using the picker dialog."""

    def __init__(self, label, name=wxpg.PG_LABEL, value=NULL_SYMBOL):
        wxpg.StringProperty.__init__(self, label, name, value)
        self.with_specials = (name != "tap")

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrlAndButton")

    def GetEditorDialog(self):
        return PickerDialogAdapter(self.with_specials)

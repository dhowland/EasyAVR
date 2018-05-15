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

"""A configuration panel for capturing key map assignments."""

import copy

import wx

from ..scancodes import scancodes
from ..userdata import Map
from .mapdialog import MapDialog
from .pickerdialog import PickerDialog
from .scale import UNIT_SIZE, GRID_SIZE, MARGIN


labels = ["Default", "Layer 1", "Layer 2", "Layer 3", "Layer 4",
          "Layer 5", "Layer 6", "Layer 7", "Layer 8", "Layer 9"]


class LayoutPanel(wx.Panel):
    """A configuration panel for capturing key map assignments."""

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.user_data = None
        self.clipboard = None

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.main_rb = wx.RadioBox(self, label="Layer Selection", choices=labels)
        self.Bind(wx.EVT_RADIOBOX, self.OnLayerChanged, self.main_rb)
        self.main_sizer.Add(self.main_rb, flag=wx.ALL, border=MARGIN)

        # Force initial size to be 6x6 grid, to keep the window from collapsing
        self.key_panel = wx.Panel(self, size=GRID_SIZE*24)
        self.key_si = self.main_sizer.Add(self.key_panel, flag=wx.EXPAND|wx.ALL, border=MARGIN)

        self.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)
        self.Layout()

    def OnLayerChanged(self, event):
        if self.user_data is not None:
            self.hide_popup()
            self.key_panel.change_layer(event.GetInt())

    def load_layout(self, user_data):
        """Dump the existing layout and recreate using a new `user_data` object."""
        self._clear_clipboard(user_data)
        self.user_data = user_data
        old_panel = self.key_panel
        self.key_panel = KeyPanel(self, user_data=self.user_data)
        self.main_sizer.Replace(old_panel, self.key_panel)
        # self.main_sizer.Fit(self)
        self.Layout()
        old_panel.Destroy()
        del old_panel
        self.main_rb.SetSelection(0)
        self.key_panel.change_layer(self.main_rb.GetSelection())

    def get_hint_strings(self):
        """Convert the layout into strings for $HINT() commands in macros."""
        if self.user_data is not None:
            return self.key_panel.get_hint_strings()

    def hide_popup(self):
        if self.user_data is not None:
            self.key_panel.map_dialog.Close()

    def copy_layer(self):
        """Copy the currently selected layer to an internal clipboard."""
        if self.user_data is None:
            return None
        layer = self.main_rb.GetSelection()
        self.clipboard = copy.deepcopy(self.user_data.keymap[layer])
        return layer

    def paste_layer(self):
        """Paste the layer in an internal clipboard, if there is one, to the
        currently selected layer.
        """
        if self.user_data is None:
            return None
        if self.clipboard is None:
            return None
        layer = self.main_rb.GetSelection()
        self.user_data.keymap[layer] = self.clipboard
        self.user_data.announce('keymap')
        self.key_panel.change_layer(layer)
        return layer

    def _clear_clipboard(self, new_user_data):
        if self.user_data is None:
            return
        if self.user_data.config.unique_id != new_user_data.config.unique_id:
            self.clipboard = None


class KeyPanel(wx.Panel):
    """A sub panel to display the actual layout grid."""

    def __init__(self, *args, **kwargs):
        self.user_data = kwargs['user_data']
        del kwargs['user_data']
        wx.Panel.__init__(self, *args, **kwargs)

        self.map_dialog = MapDialog(self)
        self.picker_dialog = PickerDialog(self)

        self.SetSize(self.user_data.config.display_width * UNIT_SIZE,
                     self.user_data.config.display_height * UNIT_SIZE)

        self.main_sizer = wx.GridBagSizer(0, 0)
        self.main_sizer.SetEmptyCellSize(GRID_SIZE)

        self.keylist = []
        self.hint_map = []
        self._build_layout()

        self.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)
        self.Layout()

    def _build_layout(self):
        x = y = 0
        for i, rowdef in enumerate(self.user_data.config.keyboard_definition):
            if isinstance(rowdef, list):
                hint_row = []
                for j, keydef in enumerate(rowdef):
                    keydim, matrix, _ = keydef
                    if self.user_data.layout_mod:
                        mod_map = self.user_data.config.alt_layouts[self.user_data.layout_mod]
                        keydim = mod_map.get((i, j), keydim)
                    if isinstance(keydim, tuple):
                        w, h = keydim
                        if (w > 0) and (h > 0):
                            size = wx.Size(GRID_SIZE.width * w, GRID_SIZE.height * h)
                            kb = KeyButton(self, size=size, user_data=self.user_data,
                                           layout=(i, j), matrix=matrix, geom=(h, w))
                            # wx takes (row, col)
                            self.main_sizer.Add(kb, pos=(y, x), span=(h, w))
                            self.keylist.append(kb)
                        elif (w > 0) and (h < 0):
                            h = (-1 * h)
                            tmpy = y - (h - 4)
                            size = wx.Size(GRID_SIZE.width * w, GRID_SIZE.height * h)
                            kb = KeyButton(self, size=size, user_data=self.user_data,
                                           layout=(i, j), matrix=matrix, geom=(h, w))
                            self.main_sizer.Add(kb, pos=(tmpy, x), span=(h, w))
                            self.keylist.append(kb)
                        else:
                            wx.MessageBox("Error: invalid keyboard_definition",
                                          caption="Can't load config",
                                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
                            return
                        x += w
                        hint_row.append((w, matrix))
                    elif isinstance(keydim, int):
                        if keydim > 0:
                            w = keydim
                        else:
                            # legacy could have -1 for a 'blank' instead of 'spacer'
                            w = (-1 * keydim)
                        x += w
                        hint_row.append((w, None))
                    else:
                        wx.MessageBox("Error: invalid keyboard_definition",
                                      caption="Can't load config",
                                      style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
                        return
                y += 4
                x = 0
                self.hint_map.append(hint_row)
            elif isinstance(rowdef, int):
                y += rowdef
            else:
                wx.MessageBox("Error: invalid keyboard_definition", caption="Can't load config",
                              style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
                return

    def change_layer(self, layer):
        for kb in self.keylist:
            kb.change_layer(layer)

    def get_hint_strings(self):
        """Print the keymap to a list of huge strings."""
        macro_list = []
        for layer in self.user_data.keymap:
            string_list = []
            for row in self.hint_map:
                for w, matrix in row:
                    if matrix is None:
                        string_list.append(' ' * w)
                    else:
                        row, col = matrix
                        code = layer[row][col].code
                        hint = scancodes[code].hint
                        pad = w - len(hint)
                        lf = pad // 2
                        rt = pad - lf
                        string_list.append(' ' * lf)
                        string_list.append(hint)
                        string_list.append(' ' * rt)
                string_list.append('\n')
            macro_list.append(''.join(string_list))
        return macro_list


class KeyButton(wx.Button):
    """A button representing a key on the keyboard layout."""

    def __init__(self, *args, **kwargs):
        """The `layout`, `matrix`, and `geom` arguments must be supplied as
        tuples describing the properties of this particular key.  The formats are
        (row, col) and (height, width).
        """
        self.user_data = kwargs['user_data']
        del kwargs['user_data']
        self.layout = kwargs['layout']
        del kwargs['layout']
        self.matrix = kwargs['matrix']
        del kwargs['matrix']
        self.geom = kwargs['geom']
        del kwargs['geom']
        wx.Button.__init__(self, *args, **kwargs)

        h, w = self.geom
        h = h/4
        w = w/4
        self.props = {
            'layout': "Row %d, Col %d" % self.layout,
            'matrix': "Row %d, Col %d" % self.matrix,
            'geom': "Height %du, Width %gu" % (h, w),
        }

        self.Bind(wx.EVT_BUTTON, self.OnClicked)

    def OnClicked(self, event):
        map_dialog = self.GetParent().map_dialog

        map_dialog.switch_key(self)

        key_panel_pos = self.GetParent().GetScreenPosition()
        key_panel_sz = self.GetParent().GetSize()
        key_button_pos = self.GetScreenPosition()
        key_button_sz = self.GetSize()
        map_dialog_sz = map_dialog.GetSize()

        right_border = key_panel_pos.x + key_panel_sz.x
        right_side_x = key_button_pos.x + key_button_sz.x - 8
        right_margin = right_border - (right_side_x + map_dialog_sz.x)
        left_border = key_panel_pos.x
        left_side_x = key_button_pos.x - map_dialog_sz.x + 8
        left_margin = left_side_x - left_border

        both_sides_y = key_button_pos.y + (2 * UNIT_SIZE)

        if left_margin <= 0:
            # always avoid left-side overhang
            target = (right_side_x, both_sides_y)
        elif right_margin < 0:
            # try to avoid right-side overhang
            target = (left_side_x, both_sides_y)
        else:
            # default to the right
            target = (right_side_x, both_sides_y)

        map_dialog.Move(target)
        map_dialog.Show()
        map_dialog.SetFocus()
        # self.SetBackgroundColour((255,255,192))
        # self.SetOwnBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        # self.Refresh()

    def update_map(self, prop, value):
        row, col = self.matrix
        map_dict = self.user_data.keymap[self.layer][row][col]._asdict()
        map_dict[prop] = value
        self._refresh_state(map_dict)
        self.user_data.keymap[self.layer][row][col] = Map._make(map_dict.values())
        self.user_data.announce('keymap')

    def change_layer(self, layer):
        self.layer = layer
        row, col = self.matrix
        map = self.user_data.keymap[layer][row][col]
        self._refresh_state(map._asdict())

    def _refresh_state(self, map_dict):
        self.props.update(map_dict)
        scancode = map_dict['code']
        display = scancodes[scancode].display
        self.SetLabelText(display)

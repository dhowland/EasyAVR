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

"""This is top level interface window for the EasyAVR keymapper.  With this
application, a user can create and edit key maps for the various keyboards
supported by the Easy AVR USB Keyboard Firmware.  User keymaps can be compiled
directly into functional HEX files for programming.
"""

import os.path
import traceback

import wx
import wx.adv

from ..build import check_for_boot, unexpected_media, unexpected_mouse, build_firmware
from ..legacy import load_legacy, LegacySaveFileException
from ..macroparse import MacroException
from ..pkgdata import get_pkg_path, import_boards
from ..userdata import UserData, SaveFileException
from ..version import version_string
from .layoutpanel import LayoutPanel
from .ledpanel import LedPanel
from .macropanel import MacroPanel
from .newboardwizard import nbwizard
from .newdialog import NewDialog
from .programdialog import ProgramDialog
from .scale import MIN_STATUS_WIDTH
from .usbpanel import UsbPanel


NUM_STATUS_FIELDS = 4
SF_MSG, SF_BLDP, SF_DESC, SF_MOD = range(NUM_STATUS_FIELDS)


class MainFrame(wx.Frame):
    """The top level GUI window"""

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)
        self.make_data()
        self.make_gui()

    def make_data(self):
        self.configurations, self.config_errors = import_boards()
        wx.CallAfter(self.show_config_errors)
        self.user_data = None
        self.unsaved_changes = False
        self.build_path = None
        self.op_msg = None

    def show_config_errors(self):
        for err in self.config_errors:
            wx.MessageBox(str(err), caption="Error loading board config",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)

    def make_gui(self):
        iconpath = get_pkg_path('res/keyboard.ico')
        self.SetIcon(wx.Icon(iconpath, wx.BITMAP_TYPE_ICO))
        self.make_menubar()
        self.make_statusbar()
        self.make_main()
        self.set_title()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def make_menubar(self):
        self.disabled_items = []
        # File menu
        file_menu = wx.Menu()
        new_item = file_menu.Append(wx.ID_NEW, "&New...\tCtrl+N",
                                    "Create a new keymap")
        self.Bind(wx.EVT_MENU, self.OnFileNew, new_item)
        open_item = file_menu.Append(wx.ID_OPEN, "&Open...\tCtrl+O",
                                     "Open a saved keymap")
        self.Bind(wx.EVT_MENU, self.OnFileOpen, open_item)
        save_item = file_menu.Append(wx.ID_SAVE, "&Save\tCtrl+S",
                                     "Save the current keymap")
        self.disabled_items.append(save_item)
        self.Bind(wx.EVT_MENU, self.OnFileSave, save_item)
        saveas_item = file_menu.Append(wx.ID_SAVEAS, "Save &As...",
                                       "Save the current keymap with a new file name")
        self.disabled_items.append(saveas_item)
        self.Bind(wx.EVT_MENU, self.OnFileSaveAs, saveas_item)
        file_menu.AppendSeparator()
        newboard_item = file_menu.Append(wx.ID_ANY, "&Define Keyboard...",
                                         "Add support for new hardware")
        self.Bind(wx.EVT_MENU, self.OnNewboard, newboard_item)
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnFileExit, exit_item)
        # Edit menu
        edit_menu = wx.Menu()
        copy_item = edit_menu.Append(wx.ID_COPY, "Copy Layer\tCtrl+C",
                                     "Copy from the selected layer to the clipboard")
        self.disabled_items.append(copy_item)
        self.Bind(wx.EVT_MENU, self.OnCopy, copy_item)
        paste_item = edit_menu.Append(wx.ID_PASTE, "Paste Layer\tCtrl+V",
                                      "Paste to the selected layer from the clipboard")
        self.disabled_items.append(paste_item)
        self.Bind(wx.EVT_MENU, self.OnPaste, paste_item)
        # Build menu
        build_menu = wx.Menu()
        build_item = build_menu.Append(wx.ID_ANY, "&Build\tF7",
                                       "Build a loadable file using the current keymap")
        self.disabled_items.append(build_item)
        self.Bind(wx.EVT_MENU, self.OnBuild, build_item)
        buildas_item = build_menu.Append(wx.ID_ANY, "Build As...\tShift+F7",
                                         "Build a loadable file with a new file name")
        self.disabled_items.append(buildas_item)
        self.Bind(wx.EVT_MENU, self.OnBuildAs, buildas_item)
        reprog_item = build_menu.Append(wx.ID_ANY, "Build and &Reprogram...\tF5",
                                        "Build a loadable file and open the reprogramming tool")
        self.disabled_items.append(reprog_item)
        self.Bind(wx.EVT_MENU, self.OnBuildAndReprogram, reprog_item)
        # Help menu
        help_menu = wx.Menu()
        help_item = help_menu.Append(wx.ID_ANY, "View Help\tF1",
                                     "View the built-in help documents")
        self.Bind(wx.EVT_MENU, self.OnHelpView, help_item)
        help_menu.AppendSeparator()
        about_item = help_menu.Append(wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, about_item)
        # Menu bar
        menubar = wx.MenuBar()
        menubar.Append(file_menu, "&File")
        menubar.Append(edit_menu, "&Edit")
        menubar.Append(build_menu, "&Build")
        menubar.Append(help_menu, "&Help")
        self.SetMenuBar(menubar)
        # Disable menu items that can't be used until a file is loaded
        self.enable_menus(False)

    def enable_menus(self, enable=True):
        for menu_item in self.disabled_items:
            menu_item.Enable(enable=enable)

    def make_statusbar(self):
        self.statusbar = self.CreateStatusBar(NUM_STATUS_FIELDS)
        # hard-coded pixels are only temporary
        self.SetStatusWidths([-1, MIN_STATUS_WIDTH, MIN_STATUS_WIDTH, MIN_STATUS_WIDTH])

    def make_main(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.main_nb = wx.Notebook(self)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnNbChange, self.main_nb)
        self.main_sizer.Add(self.main_nb, proportion=1, flag=wx.EXPAND)

        self.layout_panel = LayoutPanel(self.main_nb)
        self.main_nb.AddPage(self.layout_panel, "Layout")

        self.macro_panel = MacroPanel(self.main_nb)
        self.main_nb.AddPage(self.macro_panel, "Macros")

        self.led_panel = LedPanel(self.main_nb)
        self.main_nb.AddPage(self.led_panel, "LEDs")

        self.usb_panel = UsbPanel(self.main_nb)
        self.main_nb.AddPage(self.usb_panel, "USB")

        self.SetSizerAndFit(self.main_sizer)
        self.Layout()

    def set_title(self):
        title = "EasyAVR"
        if self.user_data is not None:
            if self.user_data.path is None:
                path = "New"
            else:
                path = self.user_data.path
            title = path + " - " + title
            if self.unsaved_changes:
                title = "*" + title
        self.Title = title

    def set_status(self):
        if self.user_data is None:
            return

        sb = self.GetStatusBar()

        text = "" if (self.op_msg is None) else self.op_msg
        self.SetStatusText(text)

        text = "" if (self.build_path is None) else os.path.basename(self.build_path)
        bldp_width = sb.GetTextExtent(text).x
        bldp_width = max(bldp_width, MIN_STATUS_WIDTH)
        self.SetStatusText(text, number=SF_BLDP)

        text = self.user_data.config.description
        desc_width = sb.GetTextExtent(text).x
        desc_width = max(desc_width, MIN_STATUS_WIDTH)
        self.SetStatusText(text, number=SF_DESC)

        text = "" if (self.user_data.layout_mod is None) else self.user_data.layout_mod
        mod_width = sb.GetTextExtent(text).x
        mod_width = max(mod_width, MIN_STATUS_WIDTH)
        self.SetStatusText(text, number=SF_MOD)

        widths = [-1, bldp_width, desc_width, mod_width]
        self.SetStatusWidths(widths)
        del widths  # suggested by the wxPython docs for SetStatusWidths

    def OnNbChange(self, event):
        # layout_panel is the first tab
        if event.GetSelection() == 0:
            self.layout_panel.hide_popup()

    def OnClose(self, event):
        if event.CanVeto():
            if not self.check_modified():
                return
        self.Destroy()

    #
    # File methods
    #

    def OnFileNew(self, event):
        if not self.check_modified():
            return
        with NewDialog(self, conf=self.configurations) as dlg:
            ret = dlg.ShowModal()
            if ret == wx.ID_OK:
                self.user_data = UserData(self.configurations)
                self.user_data.new(dlg.selected_id, dlg.selected_layout)
                self.user_data.subscribe(self.changes_made)
                self.load_config()

    def OnFileOpen(self, event):
        if not self.check_modified():
            return
        wildcard = "EasyAVR keymaps (*.json)|*.json|Legacy EasyAVR keymaps (*.dat)|*.dat"
        with wx.FileDialog(self, message="Open", wildcard=wildcard,
                           style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = file_dialog.GetPath()
        new_ud = UserData(self.configurations)
        _, ext = os.path.splitext(path)
        try:
            if ext == '.dat':
                load_legacy(new_ud, path)
            else:
                new_ud.open(path)
        except (SaveFileException, LegacySaveFileException) as err:
            wx.MessageBox(str(err), caption="Error opening file",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
            return
        except Exception as err:
            msg = traceback.format_exc()
            wx.MessageBox(msg, caption="Error opening file",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
            return
        self.user_data = new_ud
        self.user_data.subscribe(self.changes_made)
        self.load_config()

    def OnFileSave(self, event):
        if self.user_data.path is None:
            return self.OnFileSaveAs(event)
        try:
            self.user_data.save()
        except OSError as err:
            wx.MessageBox(str(err), caption="Error opening file",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
            return
        self.unsaved_changes = False
        self.op_msg = "Keymap saved successfully."
        self.set_title()
        self.set_status()

    def OnFileSaveAs(self, event):
        wildcard = "EasyAVR keymaps (*.json)|*.json"
        with wx.FileDialog(self, message="Save", wildcard=wildcard,
                           style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = file_dialog.GetPath()
        if path.endswith(".dat"):
            path = path + ".json"
            msg = "Saving with new file format, renamed to {0}.".format(os.path.basename(path))
            wx.MessageBox(msg, caption="Save file rename",
                          style=wx.OK|wx.CENTRE, parent=self)
        try:
            self.user_data.save(path)
        except OSError as err:
            wx.MessageBox(str(err), caption="Error opening file",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
            return
        self.build_path = None
        self.unsaved_changes = False
        self.op_msg = "Keymap saved successfully."
        self.set_title()
        self.set_status()

    def OnNewboard(self, event):
        nbwizard(self)

    def OnFileExit(self, event):
        self.Close()

    def check_modified(self):
        if ((self.unsaved_changes) and
            (wx.MessageBox("There are unsaved changes.  Proceed?", caption="Discard changes",
                           style=wx.ICON_QUESTION|wx.YES_NO|wx.CENTRE, parent=self) == wx.NO)):
            return False
        return True

    def changes_made(self, user_data, config_item):
        if self.unsaved_changes:
            return
        self.unsaved_changes = True
        self.op_msg = None
        self.set_title()
        self.set_status()

    def load_config(self):
        self.Freeze()
        self.layout_panel.load_layout(self.user_data)
        self.macro_panel.load_macros(self.user_data)
        self.led_panel.load_leds(self.user_data)
        self.usb_panel.load_opts(self.user_data)
        self.Thaw()

        self.main_nb.Fit()
        self.main_sizer.SetSizeHints(self)

        self.enable_menus()
        self.unsaved_changes = False
        self.build_path = None
        self.op_msg = "Keymap loaded successfully."
        self.set_title()
        self.set_status()

    #
    # Edit methods
    #

    def OnCopy(self, event):
        layer = self.layout_panel.copy_layer()
        if layer is not None:
            self.op_msg = "Copied layer {0} to the clipboard".format(layer)
            self.set_status()

    def OnPaste(self, event):
        layer = self.layout_panel.paste_layer()
        if layer is not None:
            self.op_msg = "Pasted layer {0} from the clipboard".format(layer)
            self.set_status()

    #
    # Build methods
    #

    def OnBuild(self, event):
        self.do_build()

    def OnBuildAs(self, event):
        self.do_build(override=True)

    def OnBuildAndReprogram(self, event):
        self.do_build(reprogram=True)

    def boot_check(self):
        if not check_for_boot(self.user_data):
            if (wx.MessageBox("You do not have a key bound to BOOT mode.  "
                              "Without it you can't easily reprogram your keyboard."
                              "  Are you sure this is what you want?",
                              caption="BOOT key not found",
                              style=wx.ICON_QUESTION|wx.YES_NO|wx.CENTRE,
                              parent=self) == wx.NO):
                return False
        if unexpected_media(self.user_data):
            if (wx.MessageBox("You have a key bound to a MEDIA or POWER function, but you don't "
                              "have the Media/Power USB endpoint enabled."
                              "  Are you sure this is what you want?",
                              caption="Useless mapping found",
                              style=wx.ICON_QUESTION|wx.YES_NO|wx.CENTRE,
                              parent=self) == wx.NO):
                return False
        if unexpected_mouse(self.user_data):
            if (wx.MessageBox("You have a key bound to a MOUSE function, but you don't "
                              "have the Mouse USB endpoint enabled."
                              "  Are you sure this is what you want?",
                              caption="Useless mapping found",
                              style=wx.ICON_QUESTION|wx.YES_NO|wx.CENTRE,
                              parent=self) == wx.NO):
                return False
        return True

    def get_build_path(self, override=False):
        if (self.build_path is None) or (override is True):
            wildcard = "Intel Hex Files (*.hex)|*.hex|Binary Files (*.bin)|*.bin"
            if self.build_path is None:
                default = ''
            else:
                default = os.path.splitext(os.path.basename(self.user_data.path))[0] + '.hex'
            with wx.FileDialog(self, message="Save", wildcard=wildcard, defaultFile=default,
                               style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as file_dialog:
                if file_dialog.ShowModal() == wx.ID_CANCEL:
                    return
                self.build_path = file_dialog.GetPath()
                self.set_status()

    def do_build(self, override=False, reprogram=False):
        if not self.boot_check():
            return
        self.get_build_path(override=override)
        if self.build_path is None:
            return
        try:
            hint_strings = self.layout_panel.get_hint_strings()
            external_data = {'hints': hint_strings}
            build_firmware(self.user_data, self.build_path, external_data)
        except MacroException as err:
            wx.MessageBox(str(err), caption="Error building firmware",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
        except Exception as err:
            msg = traceback.format_exc()
            wx.MessageBox(msg, caption="Error building firmware",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
        else:
            self.op_msg = "Build complete.  Firmware saved successfully."
            self.set_status()
            if reprogram:
                with ProgramDialog(self, user_data=self.user_data, path=self.build_path) as dlg:
                    dlg.ShowModal()
            else:
                wx.MessageBox("Firmware saved successfully.", caption="Build complete",
                              style=wx.OK|wx.CENTRE, parent=self)

    #
    # Help methods
    #

    def OnHelpView(self, event):
        wx.LaunchDefaultBrowser("http://dhowland.github.io/EasyAVR/")

    def OnHelpAbout(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetName("EasyAVR")
        info.SetVersion(version_string)
        info.SetDescription("Keymapper for the Easy AVR USB Keyboard Firmware")
        info.SetCopyright("Copyright (C) 2013-2018 David Howland")
        info.SetWebSite("https://github.com/dhowland/EasyAVR")
        iconpath = get_pkg_path('res/keycap.ico')
        info.SetIcon(wx.Icon(iconpath, type=wx.BITMAP_TYPE_ICO))
        info.SetLicence("GPLv2.0\n\n"
                        "This program comes with ABSOLUTELY NO WARRANTY.\n"
                        "This is free software, and you are welcome to redistribute it under\n"
                        "certain conditions.  See <http://www.gnu.org/licenses/> for details.")
        wx.adv.AboutBox(info)

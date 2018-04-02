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

"""A wizard for creating a new keyboard definition."""

import os.path
import re
from pprint import pformat
from string import Template

import wx
import wx.adv as wxa

from ..pkgdata import get_pkg_path, get_user_boards_dir
from .scale import MARGIN, WIZ_WIDTH
import easykeymap.kleparse as kleparse


def nbwizard(parent):
    """Create a wx wizard with pages and run it.  Then use the collected information
    to populate the newboard_template and save it to the user's config directory.
    `parent` is the wx.Window that will own the wizard.
    """
    inputs = {}

    bmp = wx.Bitmap(get_pkg_path("res/wizard.png"), wx.BITMAP_TYPE_PNG)
    wizard = wxa.Wizard(parent, title="New Keyboard Definition", bitmap=bmp)

    page1 = IntroWizardPage(wizard, inputs)
    page2 = DescIdWizardPage(wizard, inputs)
    page3 = AvrWizardPage(wizard, inputs)
    page4 = MatrixWizardPage(wizard, inputs)
    page5 = LedWizardPage(wizard, inputs)
    page6 = KleWizardPage(wizard, inputs)
    page7 = OutroWizardPage(wizard, inputs)

    page1.Chain(page2).Chain(page3).Chain(page4).Chain(page5).Chain(page6).Chain(page7)

    wizard.FitToPage(page1)
    wizard.GetPageAreaSizer().Add(page1)

    wizard.Bind(wx.adv.EVT_WIZARD_BEFORE_PAGE_CHANGED, OnPageChange)

    if wizard.RunWizard(page1):
        try:
            parsed = kleparse.parse(inputs['path'])
            mapping = create_mapping(inputs, parsed)
            output_file = inputs['id'].lower() + '.py'
            output_path = os.path.join(get_user_boards_dir(), output_file)
            create_config(output_path, mapping)
        except Exception as err:
            wx.MessageBox(str(err), caption="Error creating config",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=parent)
            return
        msg = ("Config file for '{0}' successfully created.  Edit the following file then "
               "restart EasyAVR.\n\n{1}").format(inputs['description'], output_path)
        wx.MessageBox(msg, caption="Success", parent=parent)


def OnPageChange(event):
    if event.GetDirection():
        page = event.GetPage()
        if not page.validate():
            event.Veto()


def create_mapping(inputs, parsed):
    """Convert wizard data in `inputs` and the KLE data in `parsed` to the mapping
    needed for Template string and returns the mapping.
    """
    if inputs['teensy++']:
        avr = 'AT90USB1286'
        matrix = 'FULLSIZE'
    else:
        avr = 'ATmega32U4'
        if parsed['num_rows'] <= 5:
            matrix = 'SIXTY'
        else:
            matrix = 'TKL'
    led_def = [('led%d' % i, 'Unassigned') for i in range(len(inputs['led_list']))]
    mapping = {
        'description': inputs['description'],
        'path': repr(inputs['path']),
        'avr': avr,
        'matrix': matrix,
        'unique': inputs['id'].upper()+"_001",
        'cfg': inputs['id'].lower(),
        'teensy': inputs['teensy'],
        'display_height': parsed['display_height'],
        'display_width': parsed['display_width'],
        'num_rows': parsed['num_rows'],
        'num_cols': parsed['num_cols'],
        'row_pins': ', '.join(inputs['row_list']),
        'col_pins': ', '.join(inputs['col_list']),
        'led_pins': ', '.join(inputs['led_list']),
        'backlight_pins': ', '.join(inputs['bl_list']),
        'led_definition': pformat(led_def),
        'keyboard_definition': pformat(parsed['layout']),
    }
    return mapping


def create_config(output_path, mapping):
    """Populates the newboard_template with the data from `mapping` and saves
    the result to `output_path`.
    """
    template_path = get_pkg_path('res/newboard_template.txt')
    with open(template_path, encoding="utf8") as fp:
        config_template = fp.read()
    with open(output_path, 'w') as fp:
        fp.write(Template(config_template).substitute(mapping))


class BaseWizardPage(wxa.WizardPageSimple):
    """This is the base class for all wizard pages.  It must be extended.  Subclasses
    should override `create_page()` and `validate()`.
    """

    def __init__(self, parent, inputs):
        """The `inputs` argument is a dictionary that is shared between all pages
        in the wizard and is used to store data collected from the user.
        """
        wxa.WizardPageSimple.__init__(self, parent)
        self.inputs = inputs
        self.create_page()

    def create_page(self):
        pass  # override

    def validate(self):
        return True  # override


class TitleWizardPage(BaseWizardPage):
    """This is the base class for a title page.  It implements `create_page()`
    to create a large title and a paragraph of text.  Subclasses should define
    `self.title` and `self.text`.
    """

    title = ""  # override
    text = ""  # override

    def create_page(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        st = wx.StaticText(self, label=self.title)
        st.SetFont(wx.Font(wx.FontInfo(16).Bold()))
        st.Wrap(WIZ_WIDTH)
        main_sizer.Add(st, flag=wx.ALL, border=MARGIN)
        main_sizer.AddSpacer(2*MARGIN)

        st = wx.StaticText(self, label=self.text)
        st.Wrap(WIZ_WIDTH)
        main_sizer.Add(st, flag=wx.ALL, border=MARGIN)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()


class InputWizardPage(BaseWizardPage):
    """This is the base class for wizard pages that take inputs from the user.
    There is a discussion paragraph followed by several input sections.  Each
    section consists of a paragraph of text to explain the input, a label, and
    a control.  Subclasses should define `self.discussion` and `self.packages`
    where `packages` is a list of classes derived from `BaseInputPkg`.
    """

    discussion = ""  # override
    packages = []  # override

    def create_page(self):
        grid_sizer = wx.FlexGridSizer(2, gap=(MARGIN, MARGIN))
        grid_sizer.AddGrowableCol(1)
        self.SetSizer(grid_sizer)

        grid_sizer.AddSpacer(MARGIN)
        st = wx.StaticText(self, label=self.discussion)
        st.Wrap(WIZ_WIDTH)
        grid_sizer.Add(st)

        self.pkg_obj = [pkg(self) for pkg in self.packages]
        for pkg in self.pkg_obj:
            grid_sizer.AddSpacer(2*MARGIN)
            grid_sizer.AddSpacer(2*MARGIN)
            pkg.create_widgets()

        grid_sizer.Fit(self)
        self.Layout()

    def validate(self):
        for pkg in self.pkg_obj:
            if not pkg.validate():
                return False
        return True

    def error(self, msg):
        wx.MessageBox(("Error: " + msg), caption="Invalid inputs",
                      style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
        return False


class BaseInputPkg:
    """This is the base class for input packages.  These classes are helpers
    for use with `InputWizardPage`.  Each package creates the user interface
    by populating the grid sizer of it's parent wizard page.  It also validates
    the user data.  Subclasses should override `_create_input` and `validate`
    and define `self.help` and `self.label`.
    """

    help = ""  # override
    label = ""  # override

    def __init__(self, parent):
        """The `parent` argument is a InputWizardPage object."""
        self.parent = parent

    def create_widgets(self):
        grid_sizer = self.parent.GetSizer()
        grid_sizer.AddSpacer(MARGIN)
        st = wx.StaticText(self.parent, label=self.help)
        st.Wrap(WIZ_WIDTH)
        grid_sizer.Add(st)
        st = wx.StaticText(self.parent, label=self.label)
        grid_sizer.Add(st, flag=wx.ALIGN_CENTER_VERTICAL)
        widget = self._create_input()
        grid_sizer.Add(widget, flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

    def _create_input(self):
        pass  # override

    def validate(self):
        pass  # override


class TextInputPkg(BaseInputPkg):
    """This is a base class for text inputs.  It creates the text control as `self.tc`,
    but subclasses are responsible for implementing the rest.
    """

    def _create_input(self):
        self.tc = wx.TextCtrl(self.parent)
        return self.tc


class PinListInputPkg(TextInputPkg):
    """This is the base class for a special case of TextInput, where the text is
    assumed to be a list of input pins.  It implements `validate()` but subclasses
    are still responsible for implementing `self.help` and `self.label`.  Subclasses
    must also define `self.input_key` and `self.list_name`.
    """

    input_key = ''  # override
    list_name = ''  # override

    def splitpins(self, input):
        if len(input.strip()) == 0:
            return []
        return [s.strip().upper() for s in input.split(',')]

    def validate(self):
        inputs = self.parent.inputs
        inputs[self.input_key] = self.splitpins(self.tc.GetValue())
        if not inputs[self.input_key] and self.required:
            return self.parent.error("Missing {0} pins.".format(self.list_name))
        for pin in inputs[self.input_key]:
            if not re.match(r"^[A-F][0-7]$", pin):
                return self.parent.error("Invalid pins in {0} list.".format(self.list_name))
        return True


class RadioInputPkg(BaseInputPkg):
    """This is the base class for radio button inputs.  It creates the radio button
    controls from a list of strings in `self.options`, which must be defined by
    subclasses.  The label of the selected radio button will be stored in
    `self.selected`.
    """

    options = ['Default']

    def _create_input(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        rb = wx.RadioButton(self.parent, label=self.options[0], style=wx.RB_GROUP)
        self.parent.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton, rb)
        rb.SetValue(True)
        self.selected = self.options[0]
        sizer.Add(rb)
        for label in self.options[1:]:
            rb = wx.RadioButton(self.parent, label=label)
            self.parent.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton, rb)
            sizer.Add(rb, flag=wx.LEFT, border=MARGIN)
        return sizer

    def OnRadioButton(self, event):
        self.selected = event.GetEventObject().GetLabel()


class FileInputPkg(BaseInputPkg):
    """This is the base class for file inputs.  The user will be able to select a
    file from disk.  The path is stored in a TextCtrl as `self.tc`.
    """

    def _create_input(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tc = wx.TextCtrl(self.parent)
        sizer.Add(self.tc, proportion=1, flag=wx.EXPAND)
        btn = wx.Button(self.parent, label="Open...")
        self.parent.Bind(wx.EVT_BUTTON, self.OnButton, btn)
        sizer.Add(btn, flag=wx.LEFT, border=MARGIN)
        return sizer

    def OnButton(self, event):
        wildcard = "KLE Downloads (*.json)|*.json"
        with wx.FileDialog(self.parent, message="Open", wildcard=wildcard,
                           style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = file_dialog.GetPath()
            self.tc.SetValue(path)


# Page 1
class IntroWizardPage(TitleWizardPage):

    title = "Welcome to the New Keyboard Definition Wizard"
    text = ("This wizard will guide you through the process of adding support for new hardware."
            "  The wizard will take a keyboard layout downloaded from keyboard-layout-editor.com "
            "and create a baseline config file for EasyAVR.  It will then be up to you to fill in "
            "the details with a text editor.  Click Next to get started.")


# Page 2
class DescInputPkg(TextInputPkg):

    help = ("The description will be used to refer to this layout in the New Layout dialog and "
            "other parts of the GUI.  Make it specific but not too long.\n"
            "Examples: GH60 Satan, KMAC, QuickFire Rapid.")
    label = "Description: "

    def validate(self):
        inputs = self.parent.inputs
        inputs['description'] = self.tc.GetValue()
        if not inputs['description']:
            return self.parent.error("Missing description.")
        if len(inputs['description']) > 35:
            return self.parent.error("Description should be shorter")
        return True


class IdInputPkg(TextInputPkg):

    help = ("The hardware ID is used to refer to this layout in save files and is used for config "
            " file names.  It can be up to 10 characters.\n"
            "Examples: gh60satan, kmac, qfr.")
    label = "Hardware ID: "

    def validate(self):
        inputs = self.parent.inputs
        inputs['id'] = self.tc.GetValue()
        if not inputs['id']:
            return self.parent.error("Missing ID.")
        if not re.match(r"^[a-zA-Z0-9_]{2,10}$", inputs['id']):
            return self.parent.error("ID should be one short alphanumeric word.")
        return True


class DescIdWizardPage(InputWizardPage):

    discussion = "Let's being by entering some descriptive information for your new layout."
    packages = [DescInputPkg, IdInputPkg]


# Page 3
class TeensyInputPkg(RadioInputPkg):

    help = ("If your board uses a Teensy controller, select it below.  If you aren't sure just "
            "select 'Generic AVR'.")
    label = "AVR type: "

    options = ['Generic AVR', 'Teensy 2.0', 'Teensy++ 2.0']

    def validate(self):
        inputs = self.parent.inputs
        inputs['teensy'] = ('Teensy' in self.selected)
        inputs['teensy++'] = ('++' in self.selected)
        return True


class AvrWizardPage(InputWizardPage):

    discussion = ("Next, it is important to specify what kind of AVR is built into the new "
                  "keyboard.  This will be used to determine how the bootloader works.")
    packages = [TeensyInputPkg]


# Page 4
class RowInputPkg(PinListInputPkg):

    help = ("Enter the pins used for the rows as a comma-separated list.\n"
            "For example: D0, D1, D2, D3, D5")
    label = "Row pins: "

    input_key = 'row_list'
    list_name = 'row'
    required = True


class ColInputPkg(PinListInputPkg):

    help = ("Enter the pins used for the columns as a comma-separated list.\n"
            "For example: F0, F1, E6, C7, C6, B6, D4, B1, B7, B5, B4, D7, D6, B3")
    label = "Column pins: "

    input_key = 'col_list'
    list_name = 'column'
    required = True


class MatrixWizardPage(InputWizardPage):

    discussion = ("This is where you will tell the firmware how the AVR is connected to the matrix."
                  "  The firmware needs to know which pins access the rows and columns.  Later, "
                  "each key is assigned a position in the matrix as (row, col) where 'row' and "
                  "'col' are indexes into the following lists.  The indexes start at 0, so the key "
                  "at the first column of the first row is (0, 0).")
    packages = [RowInputPkg, ColInputPkg]


# Page 5
class LedInputPkg(PinListInputPkg):

    help = ("Enter the pins used for the LED indicators (like Caps Lock).\n"
            "For example: B2")
    label = "LED pins: "

    input_key = 'led_list'
    list_name = 'LED'
    required = False


class BacklightInputPkg(PinListInputPkg):

    help = ("Enter the pins used for the backlights.\n"
            "For example: F6, F7, F4, F5")
    label = "Backlight pins: "

    input_key = 'bl_list'
    list_name = 'backlight'
    required = False


class LedWizardPage(InputWizardPage):

    discussion = ("This is where you will tell the firmware how the AVR is connected to any LEDs.  "
                  "If the new keyboard does not have any LED indicators or backlights, just leave "
                  "the input empty.")
    packages = [LedInputPkg, BacklightInputPkg]


# Page 6
class JsonInputPkg(FileInputPkg):

    help = "Select the JSON layout file from keyboard-layout-editor.com"
    label = "JSON file: "

    def validate(self):
        inputs = self.parent.inputs
        inputs['path'] = self.tc.GetValue()
        return True


class KleWizardPage(InputWizardPage):

    discussion = ("We are ready to load the layout information from keyboard-layout-editor.com.  "
                  "It is recommended to start your layout using the ANSI 104 or ISO 105 presets, "
                  "because those legends will be recognized and translated.  When you are ready, "
                  "use the 'Download' button and select 'Download JSON'.  Do not copy/paste the "
                  "data out of the 'Raw data' window, it isn't valid JSON.")
    packages = [JsonInputPkg]


# Page 7
class OutroWizardPage(TitleWizardPage):

    title = "Wizard complete"
    text = ("Your new keyboard config is ready to be created but YOU ARE NOT DONE.  This tool has "
            "made some guesses that likely must be changed by hand.  At a minimum, you must check "
            "and correct the matrix (row, col) for each key because that information was not "
            "included in the data from keyboard-layout-editor.com.  Additional instructions will "
            "be included in the config file.")

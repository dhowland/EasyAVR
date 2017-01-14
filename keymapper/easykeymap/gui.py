# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2013-2016 David Howland
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

"""This is a stand-alone tool for creating and editing key maps for the
various keyboards supported by the Easy AVR USB Keyboard Firmware.  User
keymaps can be compiled directly into functional HEX files for programming.
"""

from __future__ import print_function

import sys

try:
    from Tkinter import *
    from ttk import *
    import tkFileDialog as filedialog
    import tkSimpleDialog as simpledialog
    import tkMessageBox as messagebox
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import filedialog
    from tkinter import simpledialog
    from tkinter import messagebox

import pickle
import copy
from array import array
import os
import os.path
import importlib
from glob import glob
import traceback

if not hasattr(sys, 'frozen'):
    import pkg_resources

from easykeymap import __version__
from easykeymap.scancodes import scancodes, keysyms
from easykeymap.picker import Picker
from easykeymap.password import Password
import easykeymap.intelhex as intelhex
import easykeymap.macroparse as macroparse
import easykeymap.cfgparse as cfgparse
import easykeymap.templates as templates
import easykeymap.boards as boards
import easykeymap.programming as programming

ABOUT = """Easy AVR USB Keyboard Firmware Keymapper  (Version %s)

To ask questions contact me on geekhack.org, username 'metalliqaz'.

Copyright (C) 2013-2016 David Howland.

This program comes with ABSOLUTELY NO WARRANTY.  This is free software,
and you are welcome to redistribute it under certain conditions.  See
<http://www.gnu.org/licenses/> for details.
""" % __version__

configurations = {}
for board in boards.__all__:
    mod = importlib.import_module('easykeymap.boards.' + board)
    configurations[mod.unique_id] = mod

# save file layout revision
SAVE_VERSION = 14

#pixels for 1/4x key size
UNIT = 12

MACRO_NUM = 14

NULL_SYMBOL = '0'
# DEBUG_NULL_SYMBOL = 'HID_KEYBOARD_SC_KEYPAD_ASTERISK'
DEBUG_NULL_SYMBOL = NULL_SYMBOL     # disabled

TEENSY2_BOOT_PTR_HIGH_BYTE = 0x3F
TEENSY2PP_BOOT_PTR_HIGH_BYTE = 0xFE

FIRST_FN_CODE = 0xF0

master_layers = ["Default", "Fn", "Layer 2", "Layer 3", "Layer 4",
                 "Layer 5", "Layer 6", "Layer 7", "Layer 8", "Layer 9"]
default_layer = "Default"

key_modes = ['Normal', 'Toggle', 'Tap Key', 'Lockable', 'Rapid Fire']
key_mode_map = {'Normal': 0x00, 'Toggle': 0x01, 'Tap Key': 0x04,
                'Lockable': 0x02, 'Rapid Fire': 0x08}
default_mode = 'Normal'

with_mods = ['Shift', 'Ctrl', 'Alt', 'Win']
with_mods_map = {'Shift': 0x20, 'Ctrl': 0x10, 'Alt': 0x40, 'Win': 0x80}

led_assignments = {'Num Lock': 0, 'Caps Lock': 1, 'Scroll Lock': 2,
                   'Compose': 3, 'Kana': 4, 'Win Lock': 5, 'Fn Active': 6,
                   'Fn2 Active': 7, 'Fn3 Active': 8, 'Fn4 Active': 9,
                   'Fn5 Active': 10, 'Fn6 Active': 11, 'Fn7 Active': 12,
                   'Fn8 Active': 13, 'Fn9 Active': 14, 'Any Fn Active':15,
                   'Recording': 16, 'USB Init': 17, 'USB Error': 18,
                   'USB Suspend': 19, 'USB Normal': 20,
                   'Backlight': None, 'Unassigned': None}
unassigned_string = 'Unassigned'
backlight_string = 'Backlight'
num_led_assignments = len(led_assignments)-2

required_board_attributes = [
    'firmware', 'description', 'unique_id', 'cfg_name', 'teensy', 'hw_boot_key',
    'display_height', 'display_width', 'num_rows', 'num_cols', 'strobe_cols',
    'strobe_low', 'matrix_hardware', 'matrix_strobe', 'matrix_sense', 'num_leds',
    'num_ind', 'num_bl_enab', 'led_definition', 'led_hardware', 'backlighting',
    'bl_modes', 'KMAC_key', 'keyboard_definition', 'alt_layouts'
]


class GUI(object):

    """The main window object.

    Displays the main window and contains most of the functions.

    """

    def __init__(self):
        self.root = Tk()
        self.layers = []
        self.layers.extend(master_layers)
        self.leds = []
        self.advancedleds = []
        self.useadvancedleds = False
        self.ledlayers = []
        self.macros = [''] * MACRO_NUM
        self.selectedconfig = None
        self.selectedlayoutmod = None
        self.keys = None
        self.ignorelist = None
        self.maps = None
        self.modes = None
        self.actions = None
        self.wmods = None
        self.namevar = StringVar()
        self.namevar.set('None')
        self.altvar = StringVar()
        self.altvar.set('None')
        self.layoutrowvar = StringVar()
        self.matrixrowvar = StringVar()
        self.layoutcolvar = StringVar()
        self.matrixcolvar = StringVar()
        self.bindvar = StringVar()
        self.actionvar = StringVar()
        self.actionwidget = None
        self.modevar = StringVar()
        self.modewidget = None
        self.wmodvars = [StringVar() for x in with_mods]
        self.layervar = StringVar()
        self.macrovar = StringVar()
        self.currentmacro = None
        self.activekey = None
        self.unsaved_changes = False
        self.clipboard = None
        self.checkuserdir()
        self.pickerwindow = Picker(self)
        self.password = Password()
        self.filename = None
        self.creategui()
        self.loadlayouts()

    def go(self):
        self.root.mainloop()

    def get_pkg_path(self, path):
        if hasattr(sys, 'frozen'):
            return os.path.join(os.path.dirname(sys.executable), path)
        else:
            return pkg_resources.resource_filename(__name__, path)

    def checkuserdir(self):
        self.userdir = os.path.join(os.path.expanduser('~'), '.EasyAVR')
        self.userboards = os.path.join(self.userdir, 'boards')
        self.userconfigs = os.path.join(self.userdir, 'configs')
        for loc in [self.userdir, self.userboards, self.userconfigs]:
            if not os.path.exists(loc):
                os.mkdir(loc)
        sys.path.append(self.userboards)
        for file in glob(os.path.join(self.userboards, '*.py')):
            board = os.path.splitext(os.path.basename(file))[0]
            mod = importlib.import_module(board)
            for attr in required_board_attributes:
                if attr not in dir(mod):
                    msg = ("Can't load user board definition '" +
                        board + "'.  It is missing the '" + attr +
                        "' attribute.")
                    messagebox.showerror(title="Can't read board definition",
                                         message=msg,
                                         parent=self.root)
                    break
            else:
                configurations[mod.unique_id] = mod

    def loadlayouts(self):
        for config in configurations.values():
            cfg_file = "%s.cfg" % config.cfg_name
            cfg_path = os.path.join(self.userconfigs, cfg_file)
            # allow user configs to override built-in configs
            if not os.path.exists(cfg_path):
                try:
                    cfg_path = self.get_pkg_path('configs/' + cfg_file)
                except KeyError:
                    continue
            # have to check again because above will always succeed if running from source
            if os.path.exists(cfg_path):
                try:
                    config.alt_layouts = cfgparse.parse(cfg_path)
                except Exception as err:
                    msg = traceback.format_exc()
                    messagebox.showerror(title="Can't read config file",
                                         message='Error: ' + msg,
                                         parent=self.root)

    def creategui(self):
        # top level window
        self.root.title("Easy AVR USB Keyboard Firmware Keymapper")
        self.root.option_add('*tearOff', FALSE)
        self.root.resizable(0, 0)
        iconpath = self.get_pkg_path('icons/keyboard.ico')
        try:
            self.root.iconbitmap(default=iconpath)
        except:
            pass
        self.root.protocol("WM_DELETE_WINDOW", self.checksave)
        # menu bar
        menubar = Menu(self.root)
        menu_file = Menu(menubar)
        menu_file.add_command(label='New Layout...',
                              command=self.newfile)
        menu_file.add_command(label='Open Layout...',
                              command=self.openfile)
        menu_file.add_command(label='Save Layout', command=self.savefile)
        menu_file.add_command(label='Save Layout As...', command=self.savefileAs)
        menu_file.add_separator()
        menu_file.add_command(label='Build Firmware', command=self.build)
        menu_file.add_command(label='Build Firmware As...', command=self.buildAs)
        menu_file.add_command(label='Build and Reprogram...', command=self.buildandupload)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=self.checksave)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_edit = Menu(menubar)
        menu_edit.add_command(label='Copy Layer', command=self.copylayer)
        menu_edit.add_command(label='Paste Layer', command=self.pastelayer)
        menubar.add_cascade(menu=menu_edit, label='Edit')
        menu_view = Menu(menubar)
        menu_view.add_command(label='Scancode Picker', command=self.showpicker)
        menu_view.add_command(label='Password Generator',
                              command=self.showpassword)
        menu_view.add_command(label='LED Configuration', command=self.showled)
        menu_view.add_command(label='LED Auto-Fn Configuration', command=self.showledlayers)
        menubar.add_cascade(menu=menu_view, label='View')
        menu_help = Menu(menubar)
        menu_help.add_command(label="Beginner's Guide",
                              command=self.helpreadme)
        menu_help.add_command(label='Help on Functions and Layers',
                              command=self.helplayers)
        menu_help.add_command(label='Help on Writing Macros',
                              command=self.helpmacros)
        menu_help.add_command(label='Help on Special Config Settings',
                              command=self.helpconsole)
        menu_help.add_command(label='Help on the Password Generator',
                              command=self.helppasswords)
        menu_help.add_separator()
        menu_help.add_command(label='About',
                              command=self.about)
        menubar.add_cascade(menu=menu_help, label='Help')
        self.root['menu'] = menubar
        # frame to hold info labels
        infoframe = Frame(self.root)
        Label(infoframe, text="Hardware: ").pack(side=LEFT)
        Label(infoframe, textvariable=self.namevar).pack(side=LEFT)
        Label(infoframe, text="      Layout: ").pack(side=LEFT)
        Label(infoframe, textvariable=self.altvar).pack(side=LEFT)
        Label(infoframe, text="      Layout Row: ").pack(side=LEFT)
        Entry(infoframe, textvariable=self.layoutrowvar, state='readonly',
              width=2).pack(side=LEFT)
        Label(infoframe, text=" Col: ").pack(side=LEFT)
        Entry(infoframe, textvariable=self.layoutcolvar, state='readonly',
              width=2).pack(side=LEFT)
        Label(infoframe, text="      Matrix Row: ").pack(side=LEFT)
        Entry(infoframe, textvariable=self.matrixrowvar, state='readonly',
              width=2).pack(side=LEFT)
        Label(infoframe, text=" Col: ").pack(side=LEFT)
        Entry(infoframe, textvariable=self.matrixcolvar, state='readonly',
              width=2).pack(side=LEFT)
        infoframe.pack()
        Separator(self.root, orient=HORIZONTAL).pack(fill=X, pady=2)
        # frame to hold the editing controls
        modframe = Frame(self.root)
        Label(modframe, text="Set: ").pack(side=LEFT)
        temp = sorted(scancodes.keys())
        temp2 = [x for x in temp if not x.startswith("SCANCODE_")]
        setbox = Combobox(modframe, width=40, height=40)
        setbox['values'] = temp
        setbox['textvariable'] = self.bindvar
        setbox.state(['readonly'])
        setbox.bind('<<ComboboxSelected>>', self.updatekey)
        setbox.pack(side=LEFT)
        Label(modframe, text="      Mode: ").pack(side=LEFT)
        setbox = Combobox(modframe, width=10)
        setbox['values'] = key_modes
        setbox['textvariable'] = self.modevar
        setbox.state(['readonly', 'disabled'])
        setbox.bind('<<ComboboxSelected>>', self.updatelockmode)
        setbox.pack(side=LEFT)
        self.modewidget = setbox
        setbox = Combobox(modframe, width=40, height=40)
        setbox['values'] = temp2
        setbox['textvariable'] = self.actionvar
        setbox.state(['readonly', 'disabled'])
        setbox.bind('<<ComboboxSelected>>', self.updateaction)
        setbox.pack(side=LEFT)
        self.actionwidget = setbox
        modframe.pack()
        modframe2 = Frame(self.root)
        Label(modframe2, text="With mods:   ").pack(side=LEFT)
        for modifier, modvar in zip(with_mods, self.wmodvars):
            modvar.set('False')
            cb = Checkbutton(modframe2, text=modifier, variable=modvar,
                onvalue='True', offvalue='False', command=self.updatewmods)
            cb.pack(side=LEFT, padx=8)
        modframe2.pack()
        Separator(self.root, orient=HORIZONTAL).pack(fill=X, pady=2)
        #frame to hold the layer selectors
        layerframe = Frame(self.root)
        Label(layerframe, text="Layer: ").pack(side=LEFT)
        for layer in self.layers:
            Radiobutton(layerframe, text=layer,
                        variable=self.layervar, value=layer,
                        command=self.selectlayer).pack(side=LEFT, padx=5)
        layerframe.pack()
        Separator(self.root, orient=HORIZONTAL).pack(fill=X, pady=2)
        # frame for the layout
        self.layoutframe = Frame(self.root)
        self.layoutframe.pack(fill=BOTH, expand=1)
        self.subframe = None
        Separator(self.root, orient=HORIZONTAL).pack(fill=X, pady=2)
        # macros frame
        macroframe = Frame(self.root)
        macrosubframe = Frame(macroframe)
        Label(macrosubframe, text="Macro: ").pack(side=LEFT)
        for i in range(MACRO_NUM):
            Radiobutton(macrosubframe, text="M%d" % (i+1),
                        variable=self.macrovar, value=str(i),
                        command=self.selectmacro).pack(side=LEFT, padx=3)
        macrosubframe.pack()
        macrosubframe = Frame(macroframe)
        macrosubframe.rowconfigure(0, weight=1)
        macrosubframe.columnconfigure(0, weight=1)
        self.macrotext = Text(macrosubframe, height=5)
        self.macrotext.bind('<<Modified>>', self.macrochange)
        self.macrotext.grid(row=0, column=0, sticky=(N, W, E, S))
        scroll = Scrollbar(macrosubframe, orient=VERTICAL,
                           command=self.macrotext.yview)
        scroll.grid(row=0, column=1, sticky=(N, S))
        self.macrotext['yscrollcommand'] = scroll.set
        macrosubframe.pack(fill=X)
        self.resetmacros()
        macroframe.pack(fill=X)
        # set up some styles
        style = Style()
        style.configure("Gold.TButton", background="Gold")

    def showpicker(self):
        self.pickerwindow.show()

    def showpassword(self):
        limit = 0
        if self.selectedconfig:
            config = configurations[self.selectedconfig]
            limit = templates.ram_macro_lengths[config.firmware.device]
        self.password.popup(self.root, limit)

    def showled(self):
        if self.selectedconfig:
            LEDWindow(self.root, self)
        else:
            messagebox.showerror(title="Can't Configure LEDs",
                                 message='Create a keyboard first!',
                                 parent=self.root)

    def showledlayers(self):
        if self.selectedconfig:
            LEDLayersWindow(self.root, self)
        else:
            messagebox.showerror(title="Can't Configure LEDs",
                                 message='Create a keyboard first!',
                                 parent=self.root)

    def checksave(self):
        if self.askchanges():
            self.root.destroy()

    def askchanges(self):
        if self.unsaved_changes:
            return messagebox.askokcancel(
                title="Discard changes",
                message="There are unsaved changes.  Continue?",
                parent=self.root)
        return True

    def resetmacros(self):
        self.macrotext.delete('1.0', 'end')
        self.macrovar.set('0')
        self.currentmacro = 0
        self.macros = [''] * MACRO_NUM

    def macrochange(self, event):
        if self.selectedconfig:
            self.unsaved_changes = True

    def selectmacro(self, withsave=True):
        if withsave:
            macro_string = self.macrotext.get('1.0', 'end')
            # the text widget always seems to add a newline to every string
            if macro_string[-1] == '\n':
                macro_string = macro_string[:-1]
            self.macros[self.currentmacro] = macro_string
        self.currentmacro = int(self.macrovar.get())
        self.macrotext.delete('1.0', 'end')
        if self.macros[self.currentmacro]:
            self.macrotext.insert('1.0', self.macros[self.currentmacro])
        self.macrotext.focus_set()

    def selectlayer(self):
        if self.maps:
            selectedmap = self.maps[self.layervar.get()]
            if self.keys:
                for row in self.keys:
                    for kb in row:
                        kb.set(selectedmap[kb.row][kb.col])
                self.setactivekey(self.keys[0][0])

    def updatekey(self, event):
        if self.maps and self.activekey:
            selectedmap = self.maps[self.layervar.get()]
            selectedmap[self.activekey.row][self.activekey.col] = (
                self.bindvar.get())
            self.activekey.set(self.bindvar.get())
            self.managefnchange(self.activekey)
            self.unsaved_changes = True

    def updateaction(self, event):
        if self.actions and self.activekey:
            selectedactions = self.actions[self.layervar.get()]
            selectedactions[self.activekey.row][self.activekey.col] = (
                self.actionvar.get())
            self.unsaved_changes = True

    def updatelockmode(self, event):
        if self.modes and self.activekey:
            selectedmodes = self.modes[self.layervar.get()]
            selectedmodes[self.activekey.row][self.activekey.col] = (
                self.modevar.get())
            if self.modevar.get() == 'Tap Key':
                selectedactions = self.actions[self.layervar.get()]
                self.actionvar.set(
                    selectedactions[self.activekey.row][self.activekey.col])
                self.actionwidget.state(['readonly', '!disabled'])
            else:
                self.actionvar.set('')
                self.actionwidget.state(['readonly', 'disabled'])
            self.unsaved_changes = True

    def updatewmods(self):
        if self.wmods and self.activekey:
            selectedwmods = self.wmods[self.layervar.get()]
            wmodval = 0
            for modifier, wmodvar in zip(with_mods, self.wmodvars):
                if wmodvar.get() == 'True':
                    wmodval |= with_mods_map[modifier]
            selectedwmods[self.activekey.row][self.activekey.col] = wmodval
            self.unsaved_changes = True

    def managefnchange(self, kb):
        kbwmod = self.wmods[self.layervar.get()][kb.row][kb.col]
        for modifier, wmodvar in zip(with_mods, self.wmodvars):
            if ((kbwmod & with_mods_map[modifier]) > 0):
                wmodvar.set('True')
            else:
                wmodvar.set('False')
        if kb.fnbound:
            kbmode = self.modes[self.layervar.get()][kb.row][kb.col]
            self.modevar.set(kbmode)
            self.modewidget.state(['!disabled'])
            if kbmode == 'Tap Key':
                kbaction = self.actions[self.layervar.get()][kb.row][kb.col]
                self.actionvar.set(kbaction)
                self.actionwidget.state(['readonly', '!disabled'])
            else:
                self.actionvar.set('')
                self.actionwidget.state(['readonly', 'disabled'])
        else:
            self.actionvar.set('')
            self.actionwidget.state(['readonly', 'disabled'])
            self.modevar.set('')
            self.modewidget.state(['disabled'])

    def setactivekey(self, kb):
        if self.activekey:
            self.activekey.normal()
        self.activekey = kb
        self.activekey.highlight()
        config = configurations[self.selectedconfig]
        self.layoutrowvar.set(str(kb.row))
        self.layoutcolvar.set(str(kb.col))
        r, c = config.keyboard_definition[kb.row][kb.col][1]
        self.matrixrowvar.set(str(r))
        self.matrixcolvar.set(str(c))
        selectedmap = self.maps[self.layervar.get()]
        self.bindvar.set(selectedmap[kb.row][kb.col])
        self.managefnchange(kb)

    def keypress(self, evt):
        if (evt.keysym_num in keysyms):
            self.bindvar.set(keysyms[evt.keysym_num])
            self.updatekey(None)

    def pickerselect(self, scancode):
        self.bindvar.set(scancode)
        self.updatekey(None)
        self.root.lift()

    def getlayoutmod(self, layoutmod, row, col, default):
        for mod in layoutmod:
            if mod[0] == (row, col):
                return mod[1]
        return default

    def loadconfig(self, unique_id, layoutmod=None):
        #remove the old layout graphic
        if self.subframe:
            self.subframe.destroy()
        self.keys = []
        self.ignorelist = []
        self.activekey = None
        #lookup the new configuration
        config = configurations[unique_id]
        self.selectedconfig = unique_id
        self.selectedlayoutmod = layoutmod
        #check to see if layout is changing
        if self.namevar.get() != config.description:
            self.clipboard = None
        #create the new layout graphic
        self.namevar.set(config.description)
        if layoutmod:
            if layoutmod not in config.alt_layouts:
                messagebox.showerror(
                    title="Can't load config",
                    message='Error: can not find layout %s' % layoutmod,
                    parent=self.root)
                return
            self.altvar.set(layoutmod)
        else:
            self.altvar.set(config.description)
        self.subframe = Frame(self.layoutframe,
                              width=(config.display_width*UNIT),
                              height=(config.display_height*UNIT))
        x = y = 0
        for i, rowdef in enumerate(config.keyboard_definition):
            if isinstance(rowdef, list):
                keylist = []
                for j, keydef in enumerate(rowdef):
                    if layoutmod:
                        keydef = self.getlayoutmod(
                            config.alt_layouts[layoutmod],
                            i, j, keydef[0])
                    else:
                        keydef = keydef[0]
                    if isinstance(keydef, tuple):
                        w, h = keydef
                        if (w > 0) and (h > 0):
                            btn_frame = Frame(self.subframe, width=(w*UNIT),
                                              height=(h*UNIT))
                            btn_frame.pack_propagate(0)
                            kb = KeyButton(i, j, btn_frame, self)
                            kb.btn.pack(fill=BOTH, expand=1)
                            keylist.append(kb)
                            btn_frame.grid(row=y, column=x, rowspan=h,
                                           columnspan=w)
                        elif (w > 0) and (h < 0):
                            h = (-1 * h)
                            tmpy = y - (h - 4)
                            btn_frame = Frame(self.subframe, width=(w*UNIT),
                                              height=(h*UNIT))
                            btn_frame.pack_propagate(0)
                            kb = KeyButton(i, j, btn_frame, self)
                            kb.btn.pack(fill=BOTH, expand=1)
                            keylist.append(kb)
                            btn_frame.grid(row=tmpy, column=x, rowspan=h,
                                           columnspan=w)
                        else:
                            messagebox.showerror(
                                title="Can't load config",
                                message='Error: invalid keyboard_definition',
                                parent=self.root)
                            return
                        x += w
                    elif isinstance(keydef, int):
                        self.ignorelist.append((i, j))
                        if keydef > 0:
                            space_frame = Frame(self.subframe,
                                                width=(keydef*UNIT),
                                                height=(4*UNIT))
                            space_frame.grid(row=y, column=x, rowspan=4,
                                             columnspan=keydef)
                            x += keydef
                        else:
                            x += (-1 * keydef)
                    else:
                        messagebox.showerror(
                            title="Can't load config",
                            message='Error: invalid keyboard_definition',
                            parent=self.root)
                        return
                self.keys.append(keylist)
                y += 4
                x = 0
            elif isinstance(rowdef, int):
                w = config.display_width
                space_frame = Frame(self.subframe, width=(w*UNIT),
                                    height=(rowdef*UNIT))
                space_frame.grid(row=y, column=x, rowspan=rowdef, columnspan=w)
                y += rowdef
            else:
                messagebox.showerror(
                    title="Can't load config",
                    message='Error: invalid keyboard_definition',
                    parent=self.root)
                return
        self.subframe.pack()

    def copylayer(self):
        if self.selectedconfig:
            if self.maps:
                layer = self.layervar.get()
                self.clipboard = (copy.deepcopy(self.maps[layer]),
                        copy.deepcopy(self.modes[layer]),
                        copy.deepcopy(self.actions[layer]),
                        copy.deepcopy(self.wmods[layer]))
        else:
            messagebox.showerror(title="Can't Copy",
                                 message='Create a keyboard first!',
                                 parent=self.root)

    def pastelayer(self):
        if self.clipboard is None:
            messagebox.showerror(title="Can't Paste",
                                 message='Clipboard is empty!',
                                 parent=self.root)
        else:
            if self.maps:
                layer = self.layervar.get()
                self.maps[layer] = copy.deepcopy(self.clipboard[0])
                self.modes[layer] = copy.deepcopy(self.clipboard[1])
                self.actions[layer] = copy.deepcopy(self.clipboard[2])
                self.wmods[layer] = copy.deepcopy(self.clipboard[3])
                self.unsaved_changes = True
                self.selectlayer()

    def getkeymap(self, keyboard_definition):
        all_maps = {}
        for i,layer in enumerate(self.layers):
            key_map = []
            for rowdef in keyboard_definition:
                if isinstance(rowdef, list):
                    rowlist = []
                    for keydef in rowdef:
                        def_asmt = keydef[2]
                        if isinstance(def_asmt, list):
                            try:
                                rowlist.append(def_asmt[i])
                            except IndexError:
                                rowlist.append('0')
                        else:
                            # old, single-string format (default layer only)
                            if i == 0:
                                rowlist.append(def_asmt)
                            else:
                                rowlist.append('0')
                    key_map.append(rowlist)
                elif isinstance(rowdef, int):
                    key_map.append([])
                else:
                    raise Exception('Error: invalid keyboard_definition')
            all_maps[layer] = key_map
        return all_maps

    def initadvancedleds(self):
        self.advancedleds = [(255, 0)] * num_led_assignments
        self.useadvancedleds = False
        for i, ledfn in enumerate(self.leds):
            n = led_assignments[ledfn]
            if n is not None:
                self.advancedleds[n] = (i, 0)

    def newfile(self):
        if self.askchanges():
            new_win = NewWindow(self.root, "Select type for new layout")
            if new_win.result:
                self.loadconfig(new_win.result, new_win.layout)
                config = configurations[new_win.result]
                #get the default keymap to start with
                self.maps = {}
                self.modes = {}
                self.actions = {}
                self.wmods = {}
                default_keymaps = self.getkeymap(config.keyboard_definition)
                empty_keymap = [['0'] * len(x) for x in default_keymaps[default_layer]]
                init_modes = [[default_mode] * len(x) for x in default_keymaps[default_layer]]
                init_wmods = [[0] * len(x) for x in default_keymaps[default_layer]]
                for layer in self.layers:
                    self.maps[layer] = copy.deepcopy(default_keymaps[layer])
                    self.modes[layer] = copy.deepcopy(init_modes)
                    self.actions[layer] = copy.deepcopy(empty_keymap)
                    self.wmods[layer] = copy.deepcopy(init_wmods)
                self.layervar.set(default_layer)
                self.leds = [x[1] for x in config.led_definition]
                self.initadvancedleds()
                self.ledlayers = [0, 0, 0, 0, 0]
                del self.password
                self.password = Password()
                self.selectlayer()
                self.resetmacros()
                self.unsaved_changes = False
                self.filename = None

    def openfile(self):
        if self.askchanges():
            filename = filedialog.askopenfilename(
                filetypes=[('Saved Layouts', '.dat')],
                parent=self.root)
            if not filename:
                return
            try:
                with open(filename, 'rb') as fdin:
                    data = pickle.load(fdin)
                    version = data[0]
                    if version < 12:
                        answer = messagebox.askokcancel(
                            title="Save file is incompatible",
                            message="The save file you have selected was saved"
                            " by an older version and will probably not work."
                            "  Are you sure this is what you want?",
                            parent=self.root)
                        if not answer:
                            return
                    unique_id = data[1]
                    if unique_id not in configurations:
                        messagebox.showerror(
                            title="Can't load save file",
                            message="This save file describes a configuration "
                            "that cannot be loaded.",
                            parent=self.root)
                        return
                    maps = data[2]
                    if len(data) > 8:
                        layoutmod = data[8]
                    else:
                        layoutmod = None
                    self.loadconfig(unique_id, layoutmod)
                    self.maps = maps
                    if version == 1:
                        self.adapt_v1()
                    if version <= 2:
                        self.adapt_v2()
                    if len(data) > 3:
                        self.resetmacros()
                        self.macros = data[3]
                        self.selectmacro(withsave=False)
                    if version >= 12:
                        if len(data) > 4:
                            self.actions = data[4]
                        if len(data) > 5:
                            self.modes = data[5]
                        if len(data) > 6:
                            self.wmods = data[6]
                        if len(data) > 7:
                            pass    # unused
                    else:
                        self.actions = {}
                        self.modes = {}
                        self.wmods = {}
                        config = configurations[self.selectedconfig]
                        default_keymaps = self.getkeymap(config.keyboard_definition)
                        empty_keymap = [['0'] * len(x) for x in default_keymaps[default_layer]]
                        init_modes = [[default_mode] * len(x) for x in default_keymaps[default_layer]]
                        init_wmods = [[0] * len(x) for x in default_keymaps[default_layer]]
                        for layer in self.layers:
                            self.modes[layer] = copy.deepcopy(init_modes)
                            self.actions[layer] = copy.deepcopy(empty_keymap)
                            self.wmods[layer] = copy.deepcopy(init_wmods)
                    self.layervar.set(default_layer)
                    self.selectlayer()
                    if len(data) > 9:
                        self.leds = data[9]
                    else:
                        self.leds = [x[1] for x in config.led_definition]
                    if len(data) > 10:
                        del self.password
                        self.password = Password(data[10])
                    if len(data) > 11:
                        self.advancedleds = data[11]
                        self.useadvancedleds = data[12]
                    else:
                        self.initadvancedleds()
                    if len(data) > 13:
                        self.ledlayers = data[13]
                    else:
                        self.ledlayers = [0, 0, 0, 0, 0]
                    if version <= 3:
                        self.adapt_v3()
                    if version <= 4:
                        self.adapt_v4()
                    if version <= 5:
                        self.adapt_v5()
                    if version <= 6:
                        self.adapt_v6()
                    if version <= 7:
                        self.adapt_v7()
                    if version <= 8:
                        self.adapt_v8()
                    if version <= 9:
                        self.adapt_v9()
                    if version <= 10:
                        self.adapt_v10()
                    if version <= 11:
                        self.adapt_v11()
                    if version <= 12:
                        self.adapt_v12()
                    if version <= 13:
                        self.adapt_v13()
                    self.scrub_scancodes()
                self.unsaved_changes = False
                self.filename = filename
            except Exception as err:
                msg = traceback.format_exc()
                messagebox.showerror(title="Can't open layout",
                                     message='Error: ' + msg,
                                     parent=self.root)

    def adapt_v1(self):
        print("Adapting save file v1->v2")
        newmaps = {}
        for layer in self.maps:
            newmaps[layer] = []
            for row in self.maps[layer]:
                newmaps[layer].append([x for x in row if x is not None])
        self.maps = newmaps

    def adapt_v2(self):
        print("Adapting save file v2->v3")
        remap = {'Top': 'Default', 'Fn': 'Fn', 'Special': 'Layer 2',
                 'Alt': 'Layer 3'}
        newmaps = {}
        for layer in self.maps:
            newname = remap[layer]
            newmaps[newname] = self.maps[layer]
        newmaps['Layer 4'] = copy.deepcopy(self.maps['Alt'])
        self.maps = newmaps

    def adapt_v3(self):
        print("Adapting save file v3->v4")
        for layer in master_layers:
            if layer not in self.maps:
                self.maps[layer] = \
                    copy.deepcopy(self.maps['Default'])
        extention = MACRO_NUM - len(self.macros)
        if extention > 0:
            self.macros.extend([''] * extention)

    def adapt_v4(self):
        print("Adapting save file v4->v5")

    def adapt_v5(self):
        print("Adapting save file v5->v6")

    def adapt_v6(self):
        print("Adapting save file v6->v7")

    def adapt_v7(self):
        print("Adapting save file v7->v8")

    def adapt_v8(self):
        print("Adapting save file v8->v9")
        del self.password
        self.password = Password()

    def adapt_v9(self):
        print("Adapting save file v9->v10")
        extention = MACRO_NUM - len(self.macros)
        if extention > 0:
            self.macros.extend([''] * extention)

    def adapt_v10(self):
        print("Adapting save file v10->v11")
        self.leds = ['Any Fn Active' if (x == 'Fn Lock') else x
                        for x in self.leds]

    def adapt_v11(self):
        print("Adapting save file v11->v12")

    def adapt_v12(self):
        print("Adapting save file v12->v13")

    def adapt_v13(self):
        print("Adapting save file v13->v14")

    def scrub_scancodes(self):
        for layer in self.maps:
            for row in self.maps[layer]:
                for i, k in enumerate(row):
                    if k == "SCANCODE_DEBUG":
                        row[i] = "SCANCODE_CONFIG"
                    elif k == "SCANCODE_LOCKINGCAPS":
                        row[i] = "HID_KEYBOARD_SC_LOCKING_CAPS_LOCK"
                    elif k not in scancodes:
                        row[i] = '0'

    def savefileReal(self, filename):
        self.selectmacro()
        package = (SAVE_VERSION, self.selectedconfig, self.maps,
                   self.macros, self.actions, self.modes,
                   self.wmods, None,
                   self.selectedlayoutmod, self.leds,
                   self.password.getstruct(),
                   self.advancedleds, self.useadvancedleds,
                   self.ledlayers)
        try:
            with open(filename, 'wb') as fdout:
                pickle.dump(package, fdout, protocol=2)
            self.unsaved_changes = False
            self.filename = filename
        except Exception as err:
            msg = traceback.format_exc()
            messagebox.showerror(title="Can't save layout",
                                 message='Error: ' + msg,
                                 parent=self.root)

    def savefile(self):
        if self.selectedconfig:
            if self.filename == None:
                self.savefileAs()
            else:
                self.savefileReal(self.filename)
        else:
            messagebox.showerror(title="Can't save layout",
                                 message='Create a keyboard first!',
                                 parent=self.root)
    def savefileAs(self):
        if self.selectedconfig:
            filename = filedialog.asksaveasfilename(
                defaultextension=".dat",
                filetypes=[('Saved Layouts', '.dat')],
                parent=self.root)
            if not filename:
                return
            self.savefileReal(filename)
        else:
            messagebox.showerror(title="Can't save layout",
                                 message='Create a keyboard first!',
                                 parent=self.root)

    def checkforscancode(self, scancode):
        if self.maps:
            for keymap in self.maps.values():
                for row in keymap:
                    if scancode in row:
                        return True
        return False

    def translate(self, keymap, default='0'):
        config = configurations[self.selectedconfig]
        output = []
        for i in range(config.num_rows):
            output.append([default]*config.num_cols)
        for r, row in enumerate(keymap):
            for c, value in enumerate(row):
                if (r, c) in self.ignorelist:
                    continue
                if value is not None:
                    target = config.keyboard_definition[r][c][1]
                    if target is not None:
                        y, x = target
                        output[y][x] = value
        return output

    def gethintstrings(self):
        # print the keymap to a list of huge strings
        macro_list = []
        config = configurations[self.selectedconfig]
        layout = config.keyboard_definition
        layoutmod = self.selectedlayoutmod
        for layer in self.layers:
            string_list = []
            for i, rowdef in enumerate(config.keyboard_definition):
                if isinstance(rowdef, list):
                    for j, keydef in enumerate(rowdef):
                        if layoutmod:
                            keydef = self.getlayoutmod(
                                config.alt_layouts[layoutmod],
                                i, j, keydef[0])
                        else:
                            keydef = keydef[0]
                        if isinstance(keydef, tuple):
                            width = keydef[0]
                            assign = self.maps[layer][i][j]
                            text = scancodes[assign][2]
                            pad = width - len(text)
                            lf = pad // 2
                            rt = pad - lf
                            string_list.append(' ' * lf)
                            string_list.append(text)
                            string_list.append(' ' * rt)
                        elif isinstance(keydef, int):
                            string_list.append(' ' * abs(keydef))
                        # string_list.append('|')
                    string_list.append('\n')
            macro_list.append(''.join(string_list))
        return macro_list

    def buildandupload(self):
        filename = self.build(sub=True)
        if filename is None:
            return
        config = configurations[self.selectedconfig]
        programming.popup(self.root, filename, config)

    def buildReal(self, filename, config, sub=False):
        try:
            hex_path = self.get_pkg_path('builds/' + config.firmware.hex_file_name)
            with open(hex_path, 'r') as fdin:
                hexdata = self.overlay(intelhex.read(fdin))
            if filename.lower().endswith('.bin'):
                with open(filename, 'wb') as fdout:
                    hexdata[0][1].tofile(fdout)
            else:
                with open(filename, 'w') as fdout:
                    intelhex.write(fdout, hexdata)
            if sub:
                return filename
            else:
                messagebox.showinfo(
                    title="Build complete",
                    message="Firmware saved successfully.",
                    parent=self.root)
        except Exception as err:
            msg = traceback.format_exc()
            messagebox.showerror(title="Can't build binary",
                                 message='Error: ' + msg,
                                 parent=self.root)

    def build(self, sub=False):
        if self.filename == None:
            self.buildAs(sub)
            return

        if self.selectedconfig:
            config = configurations[self.selectedconfig]
            if ((not self.checkforscancode('SCANCODE_BOOT')) and
                    (config.hw_boot_key == False)):
                answer = messagebox.askokcancel(
                    title="BOOT key not found",
                    message="You do not have a key bound to BOOT mode.  "
                    "Without it you can't easily reprogram your keyboard."
                    "  Are you sure this is what you want?",
                    parent=self.root)
                if not answer:
                    return
            filename = os.path.splitext(self.filename)[0] + '.hex'
            self.buildReal(filename, config, sub)

    def buildAs(self, sub=False):
        if self.selectedconfig:
            config = configurations[self.selectedconfig]
            if ((not self.checkforscancode('SCANCODE_BOOT')) and
                    (config.hw_boot_key == False)):
                answer = messagebox.askokcancel(
                    title="BOOT key not found",
                    message="You do not have a key bound to BOOT mode.  "
                    "Without it you can't easily reprogram your keyboard."
                    "  Are you sure this is what you want?",
                    parent=self.root)
                if not answer:
                    return
            defaultFilename = 'Untitled.hex'
            if self.filename != None:
                defaultFilename = os.path.splitext(os.path.basename(self.filename))[0] + '.hex'
            filename = filedialog.asksaveasfilename(
                defaultextension=".hex", initialfile=defaultFilename,
                filetypes=[('Intel Hex Files', '.hex'), ('Binary Files', '.bin')],
                parent=self.root)
            if not filename:
                return
            self.buildReal(filename, config, sub)
        else:
            messagebox.showerror(title="Can't build binary",
                                 message='Create a keyboard first!',
                                 parent=self.root)

    def overlay(self, hexdata):
        config = configurations[self.selectedconfig]
        # shouldn't get more than one chunk per file
        start, bytes = hexdata[0]
        # overwrite data for key maps
        fw_rows,fw_cols = templates.matrix_dims[config.firmware.size]
        col_diff = fw_cols - config.num_cols
        row_diff = (fw_rows - config.num_rows) * fw_cols
        address = config.firmware.layers_map
        offset = address - start
        for layer in self.layers:
            mapdata = self.translate(self.maps[layer])
            for row in mapdata:
                for value in row:
                    if value == NULL_SYMBOL:
                        value = DEBUG_NULL_SYMBOL
                    bytes[offset] = scancodes[value][1]
                    offset += 1
                offset += col_diff
            offset += row_diff
        # overwrite data for key actions
        address = config.firmware.actions_map
        offset = address - start
        for layer in self.layers:
            mapdata = self.translate(self.modes[layer], default=default_mode)
            mapdata2 = self.translate(self.wmods[layer], default=0)
            for row, row2 in zip(mapdata, mapdata2):
                for value, value2 in zip(row, row2):
                    bytes[offset] = (key_mode_map[value] | value2)
                    offset += 1
                offset += col_diff
            offset += row_diff
        # overwrite data for tap keys
        address = config.firmware.tapkeys_map
        offset = address - start
        for layer in self.layers:
            mapdata = self.translate(self.actions[layer])
            for row in mapdata:
                for value in row:
                    bytes[offset] = scancodes[value][1]
                    offset += 1
                offset += col_diff
            offset += row_diff
        # overwrite data for led layers
        address = config.firmware.led_layers_map
        offset = address - start
        for layer in self.ledlayers:
            if layer:
                bytes[offset] = FIRST_FN_CODE + layer
            else:
                bytes[offset] = 0
            offset += 1
        # overwrite data for macros
        self.selectmacro()
        self.assemblemacrodata(config, bytes, start)
        # overwrite data for matrix style
        if config.strobe_cols:
            address = config.firmware.strobe_cols_map
            offset = address - start
            bytes[offset] = 1
        if config.strobe_low:
            address = config.firmware.strobe_low_map
            offset = address - start
            bytes[offset] = 1
        # overwrite data for matrix size
        if config.strobe_cols:
            num_strobe = config.num_cols
            num_sense = config.num_rows
        else:
            num_strobe = config.num_rows
            num_sense = config.num_cols
        address = config.firmware.num_strobe_map
        offset = address - start
        bytes[offset] = num_strobe
        address = config.firmware.num_sense_map
        offset = address - start
        bytes[offset] = num_sense
        # overwrite data for matrix definition
        address = config.firmware.matrix_init_map
        offset = address - start
        for port_def in config.matrix_hardware:
            for mask in port_def:
                bytes[offset] = mask
                offset += 1
        # overwrite data for matrix strobe list
        address = config.firmware.matrix_strobe_map
        offset = address - start
        for strobe in config.matrix_strobe:
            for mask in strobe:
                bytes[offset] = mask
                offset += 1
        # overwrite data for matrix sense list
        address = config.firmware.matrix_sense_map
        offset = address - start
        for sense in config.matrix_sense:
            for mask in sense:
                bytes[offset] = mask
                offset += 1
        # overwrite row/col for the weird "KMAC" key
        if config.KMAC_key is not None:
            address = config.firmware.kmac_key_map
            offset = address - start
            for b in config.KMAC_key:
                bytes[offset] = b
                offset += 1
        # overwrite data for LED counts
        address = config.firmware.num_leds_map
        offset = address - start
        bytes[offset] = config.num_leds
        address = config.firmware.num_ind_map
        offset = address - start
        bytes[offset] = config.num_ind
        # overwtite data for LED IO list
        address = config.firmware.led_hw_map
        offset = address - start
        for port,pin,direction in config.led_hardware:
            bytes[offset] = port
            offset += 1
            bytes[offset] = pin
            offset += 1
            bytes[offset] = direction
            offset += 1
        # overwrite data for LED functions
        address = config.firmware.led_map
        offset = address - start
        for tup in self.advancedleds:
            bytes[offset] = tup[0]
            offset += 1
            bytes[offset] = tup[1]
            offset += 1
        if config.firmware.num_bl_enab_map is not None:
            # overwrite data for backlight enables count
            address = config.firmware.num_bl_enab_map
            offset = address - start
            bytes[offset] = config.num_bl_enab
            # overwrite data for backlight mask
            address = config.firmware.bl_mask_map
            offset = address - start
            for led_id, ledfn in enumerate(self.leds):
                if ledfn == backlight_string:
                    bytes[offset] = 1
                else:
                    bytes[offset] = 0
                offset += 1
            for i in range(config.num_leds - config.num_ind):
                bytes[offset] = 1
                offset += 1
            # overwrite data for backlight enables
            led_diff = templates.max_leds - config.num_leds
            address = config.firmware.bl_mode_map
            offset = address - start
            for mode in config.bl_modes:
                for led in mode:
                    bytes[offset] = led
                    offset += 1
                offset += led_diff
        # overwrite data for password generators
        if config.firmware.pw_defs_map is not None:
            address = config.firmware.pw_defs_map
            offset = address - start
            s = self.password.getstring()
            if s is not None:
                end = offset + len(s)
                bytes[offset:end] = array('B', s)
        # overwrite data for teensy bootloader pointer
        if config.teensy:
            address = config.firmware.boot_ptr_map
            offset = address - start + 1
            if config.firmware.device == "AT90USB1286":
                bytes[offset] = TEENSY2PP_BOOT_PTR_HIGH_BYTE
            else:
                bytes[offset] = TEENSY2_BOOT_PTR_HIGH_BYTE
        # overwrite data for version number
        address = config.firmware.prod_str_map
        offset = address - start
        while bytes[offset] != ord('#'):
            offset += 1
        for c in __version__:
            bytes[offset] = ord(c)
            offset += 2
        # finish up
        return hexdata

    def assemblemacrodata(self, config, bytes, start):
        macro_length = templates.macro_lengths[config.firmware.device]
        # convert all the macros to byte arrays and get the length of each
        extd = {'hints': self.gethintstrings()}
        macrodata = [macroparse.parse(m, externaldata=extd)
                        for m in self.macros]
        macrolen = [len(d) for d in macrodata]
        # figure out where the macros will fit inside the buffer
        index = MACRO_NUM
        macroindex = []
        for mlen in macrolen:
            if mlen <= 0:
                macroindex.append(macro_length-1)
            else:
                macroindex.append(index)
                index += ((mlen // 2) + 1)
                if index >= macro_length:
                    raise Exception("The macros have exceeded "
                                    "the allowable size.")
        if len(macroindex) != MACRO_NUM:
            raise Exception("The macro data is an inconsistent size.")
        # map the index table into the byte array
        offset = config.firmware.macro_map - start
        for index in macroindex:
            short_array = array('H', [index])
            byte_array = array('B', short_array.tostring())
            bytes[offset:offset+2] = byte_array[:]
            offset += 2
        # map the non-empty macros into the byte array
        for i in range(MACRO_NUM):
            if macrolen[i] > 0:
                end = offset+macrolen[i]
                bytes[offset:end] = macrodata[i][:]
                bytes[end:end+2] = array('B', [0, 0])[:]
                offset += (macrolen[i] + 2)
        # make sure the last spot of the byte array has a zero (terminator)
        last_spot = ((config.firmware.macro_map - start) + ((macro_length - 1) * 2))
        bytes[last_spot:last_spot+2] = array('B', [0, 0])[:]

    def showtext(self, textfile):
        path = self.get_pkg_path('manuals/' + textfile)
        if os.path.exists(path):
            filename = os.path.basename(path)
            with open(path, 'r') as fd:
                TextWindow(self.root, filename, fd.read())
        else:
            messagebox.showerror(title="Can't display document",
                                 message='File not found: ' + path,
                                 parent=self.root)

    def helpreadme(self):
        self.showtext('readme.txt')

    def helplayers(self):
        self.showtext('functions.txt')

    def helpmacros(self):
        self.showtext('macros.txt')

    def helpconsole(self):
        self.showtext('console.txt')

    def helppasswords(self):
        self.showtext('passwords.txt')

    def about(self):
        AboutWindow(self.root, 'About', ABOUT)


class KeyButton(object):

    """Represents one button on the keyboard."""

    def __init__(self, row, col, parent, gui):
        self.row = row
        self.col = col
        self.gui = gui
        self.display = StringVar()
        self.btn = Button(parent, textvariable=self.display,
                          command=self.on_press)
        self.btn.bind('<KeyPress>', gui.keypress)
        self.fnbound = False

    def on_press(self):
        self.gui.setactivekey(self)
        self.gui.pickerwindow.lift()

    def highlight(self):
        self.btn['style'] = "Gold.TButton"

    def normal(self):
        self.btn['style'] = "TButton"

    def set(self, scancode):
        self.display.set(scancodes[scancode][0])
        self.fnbound = False
        if scancode.startswith('SCANCODE_FN'):
            self.fnbound = True
        if scancode.startswith('HID_KEYBOARD_SC'):
            self.fnbound = True


class NewWindow(simpledialog.Dialog):

    """A dialog window to select from a list of available layouts."""

    def body(self, master):
        self.resizable(0, 0)
        Label(master, text="Available keyboard types: ").pack(side=TOP)
        self.selectionvar = StringVar()
        keyboards = sorted(configurations.keys())
        subframe = Frame(master)
        subsubframe = Frame(subframe)
        split = len(keyboards) - (len(keyboards)//2)
        for i,kb in enumerate(keyboards):
            if i == split:
                subsubframe.pack(side=LEFT)
                subsubframe = Frame(subframe)
            Radiobutton(subsubframe, text=configurations[kb].description,
                        command=self.selectionchanged,
                        variable=self.selectionvar,
                        value=kb).pack(side=TOP, fill=X)
        subsubframe.pack(side=LEFT)
        subframe.pack(side=TOP)
        Label(master, text="Available layouts: ").pack(side=TOP)
        self.layoutvar = StringVar()
        self.layoutbox = Combobox(master)
        self.layoutbox['values'] = []
        self.layoutbox['textvariable'] = self.layoutvar
        self.layoutbox.state(['readonly'])
        self.layoutbox.pack(side=TOP)

    def selectionchanged(self):
        config = configurations[self.selectionvar.get()]
        layouts = ["<All Keys>"]
        layouts.extend(sorted(config.alt_layouts.keys()))
        self.layoutbox['values'] = layouts
        self.layoutvar.set("<All Keys>")

    def validate(self):
        if self.selectionvar.get():
            return True
        return False

    def apply(self):
        self.result = self.selectionvar.get()
        self.layout = self.layoutvar.get()
        if self.layout == "<All Keys>":
            self.layout = None
        if self.layout == "":
            self.layout = None


class LEDLayersWindow(simpledialog.Dialog):

    """A dialog window to configure LED layers settings"""

    def __init__(self, parent, gui=None):
        self.gui = gui
        self.textvars = []
        self.selections = ['No Action']
        for i in range(1, len(master_layers)):
            self.selections.append('Layer %d' % (i,))
        simpledialog.Dialog.__init__(self, parent, "LED Auto-Fn Configuration")

    def body(self, master):
        self.resizable(0, 0)
        for i,name in [(0,'Num Lock'), (1,'Caps Lock'), (2,'Scroll Lock'), (3,'Compose'), (4,'Kana')]:
            Label(master, text="%s LED Auto-Fn:  " % (name,)).grid(row=i, column=0, sticky=(E))
            s = StringVar()
            self.textvars.append(s)
            Combobox(master, values=self.selections, textvariable=s, state='readonly').grid(row=i, column=1, sticky=(E,W))
            s.set(self.selections[self.gui.ledlayers[i]])

    def apply(self):
        for i,s in enumerate(self.textvars):
            self.gui.ledlayers[i] = self.selections.index(s.get())


class LEDWindow(simpledialog.Dialog):

    """A dialog window to configure LED settings"""

    def __init__(self, parent, gui=None):
        self.gui = gui
        self.config = configurations[self.gui.selectedconfig]
        self.assignments = [x[0] for x in self.config.led_definition]
        self.assignments.append(unassigned_string)
        self.actions = ['Solid', '1 Blip', '2 Blips', '3 Blips', '4 Blips',
                        '5 Blips', '6 Blips', '7 Blips', '8 Blips', '9 Blips']
        simpledialog.Dialog.__init__(self, parent, "LED Configuration")

    def reverse_led_assign(self, n):
        for fn, assign in led_assignments.items():
            if assign == n:
                return fn

    def assignment_to_num(self, assign):
        if assign == unassigned_string:
            return 255
        else:
            return self.assignments.index(assign)

    def num_to_assignment(self, n):
        if n == 255:
            return unassigned_string
        else:
            return self.assignments[n]

    def action_to_num(self, action):
        return self.actions.index(action)

    def num_to_action(self, n):
        return self.actions[n]

    def body(self, master):
        self.resizable(0, 0)
        self.advancedvar = StringVar()
        self.advancedvar.set(str(self.gui.useadvancedleds))
        self.advancedvar.trace('w', self.swap)
        Checkbutton(master,
            text="Use Advanced Settings",
            variable=self.advancedvar, onvalue='True', offvalue='False').pack()

        self.basicframe = Frame(master)
        Label(self.basicframe, text='Function').grid(row=0, column=1, sticky=W)
        self.basicvars = []
        for i, led_def in enumerate(self.config.led_definition):
            ledname, default = led_def
            try:
                ledfn = self.gui.leds[i]
            except:
                ledfn = default
            setvar = StringVar()
            setvar.set(ledfn)
            setvar.trace('w', self.updateled)
            self.basicvars.append(setvar)
            Label(self.basicframe, text=ledname).grid(row=i+1, column=0, sticky=W)
            setbox = Combobox(self.basicframe, width=12)
            setbox['values'] = sorted(led_assignments.keys())
            setbox['textvariable'] = setvar
            setbox.state(['readonly'])
            setbox.grid(row=i+1, column=1, sticky=W)

        self.advancedframe = Frame(master)
        Label(self.advancedframe, text='LED Location').grid(row=0, column=1, sticky=W)
        Label(self.advancedframe, text='Active Action').grid(row=0, column=2, sticky=W)
        self.advancedvars = []
        for i in range(num_led_assignments):
            fntext = self.reverse_led_assign(i)
            try:
                assign, action = self.gui.advancedleds[i]
            except:
                assign, action = (255, 0)
            assignvar = StringVar()
            assignvar.set(self.num_to_assignment(assign))
            assignvar.trace('w', self.updateadvanced)
            actionvar = StringVar()
            actionvar.set(self.num_to_action(action))
            actionvar.trace('w', self.updateadvanced)
            Label(self.advancedframe, text=fntext).grid(row=i+1, column=0, sticky=W)
            cb = Combobox(self.advancedframe, width=12)
            cb['values'] = self.assignments
            cb['textvariable'] = assignvar
            cb.state(['readonly'])
            cb.grid(row=i+1, column=1, sticky=W)
            cb = Combobox(self.advancedframe, width=12)
            cb['values'] = self.actions
            cb['textvariable'] = actionvar
            cb.state(['readonly'])
            cb.grid(row=i+1, column=2, sticky=W)
            self.advancedvars.append((i, assignvar, actionvar))

        self.swap(None, None, None)

    def swap(self, name, index, mode):
        if (self.advancedvar.get() == 'True'):
            self.basicframe.pack_forget()
            self.advancedframe.pack()
        else:
            self.advancedframe.pack_forget()
            self.basicframe.pack()

    def updateled(self, name, index, mode):
        # find out which LED it is and what the new setting is
        for var in self.basicvars:
            if name == var._name:
                setting = var.get()
                break
        # see if we have a conflict and resolve it
        if (setting != unassigned_string) and (setting != backlight_string):
            for var in self.basicvars:
                if (var._name != name) and (var.get() == setting):
                    var.set(unassigned_string)
        self.gui.unsaved_changes = True

    def updateadvanced(self, name, index, mode):
        self.gui.unsaved_changes = True

    def apply(self):
        self.gui.advancedleds = [(255, 0)] * num_led_assignments
        self.gui.useadvancedleds = (self.advancedvar.get() == 'True')
        if self.gui.useadvancedleds:
            if self.config.backlighting:
                self.gui.leds = [backlight_string] * len(self.basicvars)
            for i, assignvar, actionvar in self.advancedvars:
                assign = self.assignment_to_num(assignvar.get())
                action = self.action_to_num(actionvar.get())
                self.gui.advancedleds[i] = (assign, action)
                if (self.config.backlighting) and (assign != 255):
                    self.gui.leds[assign] = unassigned_string
        else:
            for i, var in enumerate(self.basicvars):
                ledfn = var.get()
                self.gui.leds[i] = ledfn
                n = led_assignments[ledfn]
                if n is not None:
                    self.gui.advancedleds[n] = (i, 0)

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        box.pack()


class MultiSelectWindow(simpledialog.Dialog):

    """A dialog window to select from a list of options"""

    def __init__(self, parent, title=None, message="", options=[]):
        self.message = message
        self.options = options
        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        if self.message:
            Label(master, text=self.message).pack(padx=5, pady=5)
        self.selectionvar = StringVar(master, )
        c = Combobox(master, textvariable=self.selectionvar)
        c['values'] = self.options
        c.pack(padx=5, pady=5)
        self.selectionvar.set(self.options[0])
        return c

    def apply(self):
        self.result = self.selectionvar.get()

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        box.pack()


class TextWindow(simpledialog.Dialog):

    """A dialog window to simply display text to the user."""

    def __init__(self, parent, title=None, text_data=None):
        self.text_data = text_data
        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.text = Text(master, height=40, width=80, wrap='none')
        self.text.grid(row=0, column=0, sticky=(N, E, W, S))
        scroll = Scrollbar(master, orient=VERTICAL, command=self.text.yview)
        scroll.grid(row=0, column=1, sticky=(N, S))
        self.text['yscrollcommand'] = scroll.set
        scroll = Scrollbar(master, orient=HORIZONTAL, command=self.text.xview)
        scroll.grid(row=1, column=0, sticky=(E, W))
        self.text['xscrollcommand'] = scroll.set
        self.text.insert('1.0', self.text_data)
        self.text['state'] = 'disabled'

    def buttonbox(self):
        #no buttons needed
        self.bind("<Escape>", self.cancel)


class AboutWindow(simpledialog.Dialog):

    """A dialog window to simply display a message to the user."""

    def __init__(self, parent, title=None, text_data=None):
        self.text_data = text_data
        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        Label(master, text=self.text_data).pack()

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

def main():
    GUI().go()

if __name__ == '__main__':
    main()

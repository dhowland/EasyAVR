# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2013-2017 David Howland
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

"""This file defines a window that generates a new keyboard definition using
data from http://www.keyboard-layout-editor.com and addtitional user input.
"""

from __future__ import print_function

import re
import sys
import os.path
import traceback
from pprint import pformat
from string import Template

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

import easykeymap.kleparse as kleparse


config_template = '''
"""
Keyboard definition for the ${description} custom keyboard.
Auto-generated from ${path}
"""

# Look at handwire.py in the EasyAVR source code for definitions of these
# configuration options.  Make sure to fix the matix rows/columns in
# keyboard_definition, which are not known by the program that created
# this file.

import easykeymap.templates.ATmega32U4_16MHz_${matrix} as firmware
from easykeymap.ioports import *
from easykeymap.helper import make_matrix_config, make_led_config

description = "${description}"
unique_id = "${unique}"
cfg_name = "${cfg}"

teensy = ${teensy}
hw_boot_key = ${teensy}

display_height = ${display_height}
display_width = ${display_width}

num_rows = ${num_rows}
num_cols = ${num_cols}

strobe_cols = False
strobe_low = True

matrix_hardware, matrix_strobe, matrix_sense = make_matrix_config(
    strobe_cols=strobe_cols,
    strobe_low=strobe_low,
    rows=[${row_pins}],
    cols=[${col_pins}],
    device=firmware.device
)

num_leds, num_ind, led_hardware, backlighting, num_bl_enab, bl_modes = make_led_config(
    led_pins = [${led_pins}],
    led_dir=LED_DRIVER_PULLDOWN,
    backlight_pins = [${backlight_pins}],
    backlight_dir=LED_DRIVER_PULLDOWN
)

led_definition = ${led_definition}

KMAC_key = None

# ((key width, key height), (matrix row, matrix column), 'default mapping')
keyboard_definition = ${keyboard_definition}

alt_layouts = {}

'''

def popup(root, userpath):
    new_win = NewBoardWindow(root, "New Keyboard Wizard")
    inputs = new_win.result
    while inputs is not None:
        try:
            parsed = kleparse.parse(inputs['path'])
            if parsed['num_rows'] <= 5:
                matrix = 'SIXTY'
            else:
                matrix = 'TKL'
            if (parsed['num_rows'] > 6):
                messagebox.showinfo(title="Heads up",
                    message="Your layout appears to have more than six rows.  "
                    "That will not fit into the default firmware as configured.  "
                    "This will have to be remedied by hand.",
                    parent=root)
            mapping = {
                'description': inputs['description'],
                'path': inputs['path'],
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
                'led_definition': pformat(tuple( (('led%d' % i, 'Unassigned') for i in range(len(inputs['led_list']))) )),
                'keyboard_definition': pformat(parsed['layout']),
            }
            filename = inputs['id'].lower() + '.py'
            fullpath = os.path.join(userpath, filename)
            with open(fullpath, 'w') as fp:
                fp.write(Template(config_template).substitute(mapping))
            messagebox.showinfo(title="New Board Configuration Created",
                message="Your new config has been created but YOU ARE NOT DONE.  "
                "This tool has made some guesses that likely must be changed by "
                "hand.  At a minimum, you must correct the matrix rows/columns "
                "because that information was not included in the data from "
                "keyboard-layout-editor.com.  Edit the following file then "
                "restart EasyAVR.\n\n%s" % fullpath,
                parent=root)
            inputs = None
        except Exception as err:
            msg = traceback.format_exc()
            messagebox.showerror(title="Error creating config file",
                                 message='Error: ' + msg,
                                 parent=root)
            new_win = NewBoardWindow(root, "New Keyboard Wizard", inputs)
            inputs = new_win.result

desc_hint = '''Begin by entering descriptive name for the New Layout dialog.
Examples: GH60 Satan, KMAC, QuickFire Rapid.'''
id_hint = '''Next, enter a short name for IDs and filenames.
Examples: gh60satan, kmac, qfr.'''
file_hint = '''Select the JSON layout from keyboard-layout-editor.com
You must use the Download button, NOT Raw Data.'''
matrix_hint = '''Enter the pins used for the rows and columns as a comma-separated list.
For example: F0, F1, E6, C7, C6, B6, D4, B1, B7, B5, B4, D7, D6, B3'''
led_hint = '''Enter the pins used for the LED indicators (like Caps Lock) and backlights.
For example: B2, B6'''
teensy_hint = '''Check this box if the keyboard uses a Teensy controller.'''

wrap_units = 500

class NewBoardWindow(simpledialog.Dialog):

    def __init__(self, root, title, inputs=None):
        self.inputs = inputs
        simpledialog.Dialog.__init__(self, root, title)

    def body(self, master):
        self.resizable(0, 0)
        rowcount = 0
        
        Label(master, text=desc_hint, wraplength=wrap_units).grid(column=1, row=rowcount, sticky=(W), padx=2, pady=2)
        rowcount += 1
        Label(master, text="Description: ").grid(column=0, row=rowcount, sticky=(W), padx=2, pady=2)
        self.desc_var = StringVar()
        Entry(master, width=20, textvariable=self.desc_var).grid(column=1, row=rowcount, sticky=(W), padx=2, pady=2)
        rowcount += 1
        
        Label(master, text=id_hint, wraplength=wrap_units).grid(column=1, row=rowcount, sticky=(W), padx=2, pady=(8,2))
        rowcount += 1
        Label(master, text="ID: ").grid(column=0, row=rowcount, sticky=(W), padx=2, pady=2)
        self.id_var = StringVar()
        Entry(master, width=10, textvariable=self.id_var).grid(column=1, row=rowcount, sticky=(W), padx=2, pady=2)
        rowcount += 1
        
        Label(master, text=file_hint, wraplength=wrap_units).grid(column=1, row=rowcount, sticky=(W), padx=2, pady=(8,2))
        rowcount += 1
        Label(master, text="JSON file: ").grid(column=0, row=rowcount, sticky=(W), padx=2, pady=2)
        self.file_var = StringVar()
        Entry(master, width=50, textvariable=self.file_var).grid(column=1, row=rowcount, sticky=(E,W), padx=2, pady=2)
        Button(master, text="Open...", command=self.openfile).grid(column=2, row=rowcount, sticky=(W), padx=2, pady=2)
        rowcount += 1
        
        Label(master, text=matrix_hint, wraplength=wrap_units).grid(column=1, row=rowcount, sticky=(W), padx=2, pady=(8,2))
        rowcount += 1
        self.row_var = StringVar()
        Label(master, text="Row pins: ").grid(column=0, row=rowcount, sticky=(W), padx=2, pady=2)
        Entry(master, width=65, textvariable=self.row_var).grid(column=1, row=rowcount, columnspan=2, sticky=(E,W), padx=2, pady=2)
        rowcount += 1
        self.col_var = StringVar()
        Label(master, text="Column pins: ").grid(column=0, row=rowcount, sticky=(W), padx=2, pady=2)
        Entry(master, width=65, textvariable=self.col_var).grid(column=1, row=rowcount, columnspan=2, sticky=(E,W), padx=2, pady=2)
        rowcount += 1
        
        Label(master, text=led_hint, wraplength=wrap_units).grid(column=1, row=rowcount, sticky=(W), padx=2, pady=(8,2))
        rowcount += 1
        self.led_var = StringVar()
        Label(master, text="LED pins: ").grid(column=0, row=rowcount, sticky=(W), padx=2, pady=2)
        Entry(master, width=65, textvariable=self.led_var).grid(column=1, row=rowcount, columnspan=2, sticky=(E,W), padx=2, pady=2)
        rowcount += 1
        self.bl_var = StringVar()
        Label(master, text="Backlight pins: ").grid(column=0, row=rowcount, sticky=(W), padx=2, pady=2)
        Entry(master, width=65, textvariable=self.bl_var).grid(column=1, row=rowcount, columnspan=2, sticky=(E,W), padx=2, pady=2)
        rowcount += 1
        
        Label(master, text=teensy_hint, wraplength=wrap_units).grid(column=1, row=rowcount, sticky=(W), padx=2, pady=(8,2))
        rowcount += 1
        self.teensy_var = StringVar()
        self.teensy_var.set('False')
        Checkbutton(master, text='Teensy', variable=self.teensy_var, onvalue='True', offvalue='False').grid(column=1, row=rowcount, sticky=(W), padx=2, pady=2)
        
        self.setinputs()

    def openfile(self):
        filename = filedialog.askopenfilename(
            filetypes=[('KLE layouts', '.json')],
            parent=self)
        if not filename:
            return
        self.file_var.set(filename)

    def setinputs(self):
        if self.inputs is None:
            return
        self.desc_var.set(self.inputs['description'])
        self.id_var.set(self.inputs['id'])
        self.file_var.set(self.inputs['path'])
        self.row_var.set(', '.join(self.inputs['row_list']))
        self.col_var.set(', '.join(self.inputs['col_list']))
        self.led_var.set(', '.join(self.inputs['led_list']))
        self.bl_var.set(', '.join(self.inputs['bl_list']))
        self.teensy_var.set('True' if self.inputs['teensy'] else 'False')

    def getinputs(self):
        self.inputs = {}
        self.inputs['description'] = self.desc_var.get()
        self.inputs['id'] = self.id_var.get()
        self.inputs['path'] = self.file_var.get()
        self.inputs['row_list'] = self.splitpins(self.row_var.get())
        self.inputs['col_list'] = self.splitpins(self.col_var.get())
        self.inputs['led_list'] = self.splitpins(self.led_var.get())
        self.inputs['bl_list'] = self.splitpins(self.bl_var.get())
        self.inputs['teensy'] = (self.teensy_var.get() == 'True')

    def splitpins(self, input):
        if len(input.strip()) == 0:
            return []
        return [s.strip().upper() for s in input.split(',')]

    def validate(self):
        self.getinputs()
        
        if not self.inputs['description']:
            return self.error("Missing description.")
        if len(self.inputs['description']) > 35:
            return self.error("Description should be shorter")
        
        if not self.inputs['id']:
            return self.error("Missing ID.")
        if not re.match(r"^[a-zA-Z0-9_]{2,10}$", self.inputs['id']):
            return self.error("ID should be one alphanumeric word.")
        
        if not self.inputs['path']:
            return self.error("Missing JSON file.")
        if not os.path.isfile(self.inputs['path']):
            return self.error("JSON file not found.")
        
        if not self.inputs['row_list']:
            return self.error("Missing row pins.")
        for pin in self.inputs['row_list']:
            if not re.match(r"^[A-F][0-7]$", pin):
                return self.error("Invalid pins in row list.")
        
        if not self.inputs['col_list']:
            return self.error("Missing column pins.")
        for pin in self.inputs['col_list']:
            if not re.match(r"^[A-F][0-7]$", pin):
                return self.error("Invalid pins in column list.")
        
        return True

    def error(self, msg):
        messagebox.showerror(title="Invalid inputs",
                             message='Error: ' + msg,
                             parent=self)
        return False

    def apply(self):
        self.result = self.inputs


if __name__ == '__main__':
    print("Newboard must be run from the main GUI.")

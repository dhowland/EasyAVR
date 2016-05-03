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

"""A collection of utility functions and a GUI for programming builds to
various AVRs.
"""

from __future__ import print_function

import sys
import subprocess
import traceback
try:
    import queue
except:
    import Queue as queue

try:
    from Tkinter import *
    from ttk import *
    import tkSimpleDialog as simpledialog
    import tkMessageBox as messagebox
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import simpledialog
    from tkinter import messagebox


def popup(root, filename, config):
    info = ProgrammingInfo()
    info.filename = filename
    info.binformat = filename.endswith('bin')
    info.description = config.description
    info.device = config.firmware.device
    info.teensy = config.teensy
    info.windows = sys.platform.startswith('win32')
    new_win = ProgrammingWindow(root, "AVR Programming", info)
    return new_win.result

def execute(args, logger):
    p = subprocess.Popen(args,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, ''):
        logger(line.rstrip())
    return p.wait()


class ProgrammingTask(object):

    def __init__(self, logger, info):
        self.logger = logger
        self.info = info

    def run(self):
        # override this method
        pass


class TeensyWindows(ProgrammingTask):

    description = "Upload to Teensy"
    windows = True
    posix = False
    teensy = True

    def run(self):
        if self.info.binformat:
            raise ProgrammingException("Teensy Loader requires a build in HEX format.")
        cmd = "teensy_loader_cli -mmcu=%s -w -v %s" % (
                self.info.device.lower(), self.info.filename)
        execute(cmd, self.logger)


class FlipWindows(ProgrammingTask):

    description = "Upload to USB AVR with Flip"
    windows = True
    posix = False
    teensy = False

    def run(self):
        pass


class AvrdudePosix(ProgrammingTask):

    description = "Upload to USB AVR with AVRdude"
    windows = False
    posix = True
    teensy = False

    def run(self):
        pass


class ProgrammingException(Exception):
    pass

class ProgrammingInfo(object):
    pass


class ProgrammingWindow(simpledialog.Dialog):

    def __init__(self, root, title, info):
        # in the future this should be automatically scanned from a directory
        taskclasses = [
            TeensyWindows,
            FlipWindows,
            AvrdudePosix
        ]
        self.tasks = [t for t in taskclasses if t.windows]
        self.info = info
        self.queue = queue.Queue()
        simpledialog.Dialog.__init__(self, root, title)

    def body(self, master):
        self.taskvar = StringVar()
        Label(master, text="Task:  ").grid(column=0, row=0, sticky=(E))
        self.combo = Combobox(master, textvariable=self.taskvar, state='readonly')
        self.combo['values'] = [t.description for t in self.tasks]
        self.combo.bind('<<ComboboxSelected>>', self.taskselect)
        self.combo.grid(column=1, row=0, sticky=(E,W))
        self.button = Button(master, text="Run", command=self.run)
        self.button.state(['disabled'])
        self.button.grid(column=2, row=0, columnspan=2, sticky=(W))
        master.columnconfigure(1, weight=1)
        
        self.text = Text(master, width=80, height=20, wrap=WORD)
        self.text.grid(column=0, row=1, columnspan=3, sticky=(N, W, E, S))
        self.scroll = Scrollbar(master, orient=VERTICAL, command=self.text.yview)
        self.scroll.grid(column=3, row=1, sticky=(N, W, E, S))
        self.text["yscrollcommand"] = self.scroll.set
        
        self.bodyframe = master
        self.bodyframe.after(250, self.showtext)

    def taskselect(self, event):
        taskdesc = self.taskvar.get()
        for t in self.tasks:
            if t.description == taskdesc:
                self.selectedtask = t
                self.button.state(['!disabled'])
                break
        
    def run(self):
        self.combo.state(['disabled'])
        self.button.state(['disabled'])
        msg = 'Running task "%s"\n\n' % (self.taskvar.get(),)
        self.logtext(msg)
        try:
            self.selectedtask(self.logtext, self.info).run()
        except ProgrammingException as err:
            msg = str(err)
            messagebox.showerror(title="Can't complete programming",
                                 message='Error: ' + msg,
                                 parent=self.parent)
        except Exception as err:
            msg = traceback.format_exc()
            messagebox.showerror(title="Can't complete programming",
                                 message='Error: ' + msg,
                                 parent=self.parent)

    def logtext(self, text):
        self.queue.put(text)
        self.queue.put('\n')

    def showtext(self):
        if self.queue.qsize != 0:
            try:
                while True:
                    line = self.queue.get_nowait()
                    self.text.insert('end', line)
            except queue.Empty:
                pass
            self.text.see('end')
            self.text.update_idletasks()
        self.bodyframe.after(250, self.showtext)

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

import os
import os.path
import subprocess
import sys
import threading
import time
import traceback
try:
    import queue
except:
    import Queue as queue
if not hasattr(sys, 'frozen'):
    import pkg_resources

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
    info.filename = os.path.normpath(filename)
    info.binformat = filename.endswith('bin')
    info.description = config.description
    info.device = config.firmware.device
    info.teensy = config.teensy
    info.windows = sys.platform.startswith('win32')
    new_win = ProgrammingWindow(root, "AVR Programming", info)
    return new_win.result

def get_pkg_path(path):
    if hasattr(sys, 'frozen'):
        return os.path.join(os.path.dirname(sys.executable), path)
    else:
        return pkg_resources.resource_filename(__name__, path)


class ProgrammingTask(object):

    def __init__(self, logger, info):
        self.logger = logger
        self.info = info
        self.tool_path = self.findallpaths(self.loader_tools)
        self.die = False
        self.busy = False

    def run(self):
        # override this method
        pass

    def watchproc(self, p):
        while True:
            time.sleep(0.5)
            if self.die:
                if p.poll() is None:
                    p.terminate()
                return
            if not self.busy:
                return

    def execute(self, args):
        if self.die:
            return
        self.busy = True
        p = subprocess.Popen(args,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        th = threading.Thread(target=self.watchproc, args=(p,))
        th.start()
        for line in iter(p.stdout.readline, b''):
            self.logger(line.rstrip())
        self.busy = False
        th.join()
        return p.wait()

    def findpath(self, name):
        # check for absolute path
        path = os.path.expandvars(os.path.expanduser(name))
        if os.path.isabs(path):
            if os.path.exists(path):
                return path
            else:
                return None
        # search all directories in the path
        for path in os.getenv('PATH').split(os.pathsep):
            path = os.path.expanduser(path)
            path = os.path.expandvars(path)
            path = os.path.realpath(path)
            path = os.path.join(path, name)
            if os.path.exists(path):
                return path
        # search in the exttools directory
        path = get_pkg_path('exttools/' + name)
        if os.path.exists(path):
            return path
        return None

    def findallpaths(self, names):
        for name in names:
            path = self.findpath(name)
            if path is not None:
                return path
        return None

    def bootmsg(self, logger):
        msg = ("The keyboard should be in bootloader mode prior to programming.\n"
        "If the bootloader has not been activated then the programmer will\n"
        "not be able to connect and the process will fail.  Activate the\n"
        "bootloader by using the BOOT key (if it is programmed) or use the\n"
        "reset switch on your microcontroller.  If the process fails, make\n"
        "sure the keyboard is in bootloader mode and then try again.\n")
        logger(msg)
        time.sleep(1)


class TeensyLoader(ProgrammingTask):

    description = "Upload to Teensy with Teensy/HID Loader"
    windows = True
    posix = True
    teensy = True

    loader_tools = [
        'teensy_loader_cli.exe',
        'teensy_loader_cli',
        'hid_bootloader_cli.exe',
        'hid_bootloader_cli'
    ]

    def run(self):
        if self.info.binformat:
            raise ProgrammingException("Teensy Loader requires a build in HEX format.")
        if self.tool_path is None:
            raise ProgrammingException("Can't find teensy_loader_cli executable.")
        self.bootmsg(self.logger)
        cmd = "%s -mmcu=%s -w -v %s" % (
                self.tool_path, self.info.device.lower(), self.info.filename)
        self.logger(cmd)
        self.execute(cmd)


class FlipWindows(ProgrammingTask):

    description = "Upload to USB AVR with Flip"
    windows = True
    posix = False
    teensy = False

    loader_tools = [
        '%ProgramFiles(x86)%\\Atmel\\Flip 3.4.7\\bin\\batchisp.exe'
    ]

    def run(self):
        if self.info.binformat:
            raise ProgrammingException("Teensy Loader requires a build in HEX format.")
        if self.tool_path is None:
            raise ProgrammingException("Can't find Atmel Flip executable.")
        self.bootmsg(self.logger)
        cmd = ('"%s" -device %s -hardware USB -operation '
               'onfail abort loadbuffer "%s" memory FLASH erase F '
               'blankcheck program verify start reset 0') % (
            self.tool_path, self.info.device.lower(), self.info.filename)
        self.execute(cmd)


class AvrdudePosix(ProgrammingTask):

    description = "Upload to USB AVR with AVRdude"
    windows = False
    posix = True
    teensy = False

    loader_tools = [
    ]

    def run(self):
        self.logger("Not implemented.")


class DfuProgrammer(ProgrammingTask):

    description = "Upload to USB AVR with dfu-programmer"
    windows = True
    posix = True
    teensy = False

    loader_tools = [
        'dfu-programmer.exe',
        'dfu-programmer',
    ]

    def run(self):
        if self.info.binformat:
            raise ProgrammingException("dfu-programmer requires a build in HEX format.")
        if self.tool_path is None:
            raise ProgrammingException("Can't find dfu-programmer executable.")
        self.bootmsg(self.logger)
        cmd = ('"%s" %s erase') % (self.tool_path, self.info.device.lower())
        self.logger(cmd)
        self.execute(cmd)
        cmd = ('"%s" %s flash "%s"') % (self.tool_path, self.info.device.lower(), self.info.filename)
        self.logger(cmd)
        self.execute(cmd)
        cmd = ('"%s" %s launch') % (self.tool_path, self.info.device.lower())
        self.logger(cmd)
        self.execute(cmd)


class ProgrammingException(Exception):
    pass


class ProgrammingInfo(object):
    pass


class ProgrammingWindow(simpledialog.Dialog):

    def __init__(self, root, title, info):
        self.info = info
        self.queue = queue.Queue()
        self.collecttasks()
        self.runthread = None
        simpledialog.Dialog.__init__(self, root, title)

    def collecttasks(self):
        # in the future this should be automatically scanned from a directory
        self.tasks = [
            TeensyLoader,
            FlipWindows,
            DfuProgrammer,
            AvrdudePosix
        ]
        # the first matching task will be pre-selected for the user
        self.besttask = None
        for t in self.tasks:
            if (((t.windows and self.info.windows) or
                 (t.posix and not self.info.windows)) and
                (t.teensy == self.info.teensy)):
                self.besttask = t
                break

    # overrides simpledialog.Dialog.body()
    def body(self, master):
        self.resizable(0, 0)
        self.taskvar = StringVar()
        Label(master, text="Board:  ").grid(column=0, row=0, sticky=(E))
        Label(master, text=self.info.description).grid(column=1, row=0, columnspan=3, sticky=(E,W))
        Label(master, text="File:  ").grid(column=0, row=1, sticky=(E))
        Label(master, text=self.info.filename).grid(column=1, row=1, columnspan=3, sticky=(E,W))
        Label(master, text="Task:  ").grid(column=0, row=2, sticky=(E))
        self.combo = Combobox(master, textvariable=self.taskvar, state='readonly')
        self.combo['values'] = [t.description for t in self.tasks]
        self.combo.bind('<<ComboboxSelected>>', self.taskselect)
        self.combo.grid(column=1, row=2, sticky=(E,W))
        self.button = Button(master, text="Run", command=self.run)
        self.button.state(['disabled'])
        self.button.grid(column=2, row=2, columnspan=2, sticky=(W))
        master.columnconfigure(1, weight=1)
        
        if self.besttask is not None:
            self.taskvar.set(self.besttask.description)
            self.taskselect(None)
        
        self.text = Text(master, width=90, height=20, wrap=WORD)
        self.text.grid(column=0, row=3, columnspan=3, sticky=(N, W, E, S))
        self.scroll = Scrollbar(master, orient=VERTICAL, command=self.text.yview)
        self.scroll.grid(column=3, row=3, sticky=(N, W, E, S))
        self.text["yscrollcommand"] = self.scroll.set
        
        self.bodyframe = master
        self.bodyframe.after(250, self.showtext)

    # overrides simpledialog.Dialog.buttonbox()
    def buttonbox(self):
        w = Button(self, text="Close", width=10, command=self.ok, default=ACTIVE)
        w.pack(padx=5, pady=5)
        self.bind("<Escape>", self.ok)

    # overrides simpledialog.Dialog.apply()
    def apply(self):
        if (self.runthread is not None) and (self.runthread.is_alive()):
            if self.runningtask.busy:
                self.runningtask.die = True
                time.sleep(1)

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
        msg = 'Running task "%s"\n' % (self.taskvar.get(),)
        self.logtext(msg)
        self.runthread = threading.Thread(target=self.process)
        self.runthread.start()
        self.bodyframe.after(500, self.waitprocess)

    def process(self):
        try:
            self.runningtask = self.selectedtask(self.logtext, self.info)
            self.runningtask.run()
        except ProgrammingException as err:
            msg = str(err)
            messagebox.showerror(title="Can't complete programming",
                                 message='Error: ' + msg,
                                 parent=self.parent)
        except Exception as err:
            msg = traceback.format_exc()
            messagebox.showerror(title="Process Error",
                                 message='Error: ' + msg,
                                 parent=self.parent)

    def waitprocess(self):
        if self.runthread and self.runthread.isAlive():
            self.bodyframe.after(500,self.waitprocess)
        else:
            self.logtext('\n\n')
            self.combo.state(['!disabled'])
            self.button.state(['!disabled'])

    def logtext(self, text):
        self.queue.put(text)
        self.queue.put('\n')

    def showtext(self):
        if self.queue.qsize() != 0:
            try:
                while True:
                    line = self.queue.get_nowait()
                    self.text.insert('end', line)
            except queue.Empty:
                pass
            self.text.see('end')
            self.text.update_idletasks()
        self.bodyframe.after(250, self.showtext)

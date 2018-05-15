#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
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

"""A collection of utility functions for programming builds to various AVRs."""

import os
import os.path
import subprocess
import threading
import time

from .pkgdata import get_pkg_path


class ProgrammingException(Exception):
    """Raised when an error occurs during an AVR programming task."""
    pass


class ProgrammingTask(object):
    """This is the base class for all programming tasks.  Derived classes should
    define `description`, `windows`, `posix`, `teensy`, and `loader_tools`, as
    well as override the `run()` method.
    """

    loader_tools = []

    def __init__(self, logger, fwpath, device):
        self.logger = logger
        self.fwpath = fwpath
        self.binformat = fwpath.endswith('bin')
        self.device = device.lower()
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
        p = subprocess.Popen(args, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        th = threading.Thread(target=self.watchproc, args=(p,))
        th.start()
        for line in iter(p.stdout.readline, b''):
            self.logger(line.rstrip())
        self.busy = False
        th.join()
        return p.wait()

    @staticmethod
    def findpath(name):
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

    @staticmethod
    def bootmsg(logger):
        msg = ("The keyboard should be in bootloader mode prior to programming.\n"
               "If the bootloader has not been activated then the programmer will\n"
               "not be able to connect and the process will fail.  Activate the\n"
               "bootloader by using the BOOT key (if it is programmed) or use the\n"
               "reset switch on your microcontroller.  If the process fails, make\n"
               "sure the keyboard is in bootloader mode and then try again.\n")
        logger(msg)
        time.sleep(1)


class TeensyLoader(ProgrammingTask):
    """Loads to a Teensy controller on Windows or Linux."""

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
        if self.binformat:
            raise ProgrammingException("Teensy Loader requires a build in HEX format.")
        if self.tool_path is None:
            raise ProgrammingException("Can't find teensy_loader_cli executable.")
        self.bootmsg(self.logger)
        mmcu = '-mmcu=%s' % (self.device,)
        args = [self.tool_path, mmcu, '-w', '-v', self.fwpath]
        self.logger(' '.join(args))
        self.execute(args)


class FlipWindows(ProgrammingTask):
    """Loads to a generic AVR on Windows."""

    description = "Upload to USB AVR with Flip"
    windows = True
    posix = False
    teensy = False

    loader_tools = [
        '%ProgramFiles(x86)%\\Atmel\\Flip 3.4.7\\bin\\batchisp.exe'
    ]

    def run(self):
        if self.binformat:
            raise ProgrammingException("Teensy Loader requires a build in HEX format.")
        if self.tool_path is None:
            raise ProgrammingException("Can't find Atmel Flip executable.")
        self.bootmsg(self.logger)
        args = [self.tool_path, '-device', self.device, '-hardware', 'USB',
                '-operation', 'onfail', 'abort', 'loadbuffer', self.fwpath, 'memory',
                'FLASH', 'erase', 'F', 'blankcheck', 'program', 'verify', 'start', 'reset', '0']
        self.logger(' '.join(args))
        self.execute(args)


class AvrdudePosix(ProgrammingTask):
    """Loads to a generic AVR on Linux."""

    description = "Upload to USB AVR with AVRdude"
    windows = False
    posix = True
    teensy = False

    loader_tools = [
    ]

    def run(self):
        self.logger("Not implemented.")


class DfuProgrammer(ProgrammingTask):
    """Loads to a generic AVR on Linux."""

    description = "Upload to USB AVR with dfu-programmer"
    windows = True
    posix = True
    teensy = False

    loader_tools = [
        'dfu-programmer.exe',
        'dfu-programmer',
    ]

    def run(self):
        if self.binformat:
            raise ProgrammingException("dfu-programmer requires a build in HEX format.")
        if self.tool_path is None:
            raise ProgrammingException("Can't find dfu-programmer executable.")
        self.bootmsg(self.logger)
        args = [self.tool_path, self.device, 'erase']
        self.logger(' '.join(args))
        self.execute(args)
        args = [self.tool_path, self.device, 'flash', self.fwpath]
        self.logger(' '.join(args))
        self.execute(args)
        args = [self.tool_path, self.device, 'reset']
        self.logger(' '.join(args))
        self.execute(args)

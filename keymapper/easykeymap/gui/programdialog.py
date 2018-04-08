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

"""A dialog for reprogramming AVR boards using external tools."""

import os.path
import queue
import sys
import threading
import traceback

import wx

from ..programming import TeensyLoader, FlipWindows, DfuProgrammer, AvrdudePosix
from ..programming import ProgrammingException
from .scale import MARGIN


class ProgramDialog(wx.Dialog):
    """A dialog for reprogramming AVR boards using external tools."""

    def __init__(self, *args, **kwargs):
        """The `path` argument must be supplied as the absolute path to the
        built firmware file.
        """
        self.user_data = kwargs['user_data']
        del kwargs['user_data']
        self.path = os.path.normpath(kwargs['path'])
        del kwargs['path']
        kwargs['title'] = "AVR Programming"
        wx.Dialog.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_CHAR_HOOK, self.OnCharHook)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.queue = queue.Queue()
        self.runthread = None
        self.runningtask = None
        self.collect_tasks()

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.FlexGridSizer(2, gap=(MARGIN, MARGIN))
        grid_sizer.AddGrowableCol(1)

        st = wx.StaticText(self, label="Board:")
        grid_sizer.Add(st, flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        label = self.user_data.config.description
        st = wx.StaticText(self, label=label)
        grid_sizer.Add(st, flag=wx.ALIGN_CENTER_VERTICAL)

        st = wx.StaticText(self, label="File:")
        grid_sizer.Add(st, flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        st = wx.StaticText(self, label=self.path)
        grid_sizer.Add(st, flag=wx.ALIGN_CENTER_VERTICAL)

        st = wx.StaticText(self, label="Task:")
        grid_sizer.Add(st, flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        task_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.task_ch = wx.Choice(self, choices=[t.description for t in self.tasks])
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.task_ch)
        task_sizer.Add(self.task_ch, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.run_btn = wx.Button(self, label="Run", style=wx.BORDER_NONE)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.run_btn)
        task_sizer.Add(self.run_btn, flag=wx.ALIGN_CENTER_VERTICAL)

        grid_sizer.Add(task_sizer, flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        main_sizer.Add(grid_sizer, flag=wx.EXPAND|wx.ALL, border=MARGIN)

        font = wx.Font(wx.FontInfo().FaceName("Consolas"))
        if not font.IsOk():
            font = wx.Font(wx.FontInfo().Family(wx.FONTFAMILY_TELETYPE))
        self.main_tc = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.main_tc.SetOwnFont(font)
        self._set_textctrl_size_by_chars(self.main_tc, 90, 20)
        main_sizer.Add(self.main_tc, flag=wx.EXPAND|wx.ALL, border=MARGIN)

        # dlgbtn_sizer = wx.StdDialogButtonSizer()
        # dlgbtn_sizer.AddButton(wx.Button(self, wx.ID_OK))
        # dlgbtn_sizer.Realize()
        # main_sizer.Add(dlgbtn_sizer, flag=wx.EXPAND|wx.ALL, border=MARGIN)
        # self.FindWindow(wx.ID_OK).SetDefault()

        self.SetSizerAndFit(main_sizer)
        self.Layout()

        if self.besttask is not None:
            self.task_ch.SetSelection(self.tasks.index(self.besttask))
            self.selectedtask = self.besttask
        else:
            self.run_btn.Enable(False)

    def _set_textctrl_size_by_chars(self, tc, w, h):
        sz = tc.GetTextExtent('X')
        sz = wx.Size(sz.x * w, sz.y * h)
        tc.SetInitialSize(tc.GetSizeFromTextSize(sz))

    def OnChoice(self, event):
        self.selectedtask = self.tasks[self.task_ch.GetSelection()]
        self.run_btn.Enable(True)

    def OnButton(self, event):
        self.task_ch.Enable(False)
        self.run_btn.Enable(False)
        msg = 'Running task "{0}"\n'.format(self.selectedtask.description)
        self.log_text(msg)
        self.runthread = threading.Thread(target=self.process)
        self.runthread.start()
        self.timer.Start(250)

    def OnTimer(self, event):
        if not (self.runthread and self.runthread.isAlive()):
            self.log_text('\n\n')
            self.task_ch.Enable(True)
            self.run_btn.Enable(True)
            self.timer.Stop()
        self.show_text()

    def OnClose(self, event):
        if event.CanVeto():
            if self.runthread and self.runthread.is_alive():
                self.runningtask.die = True
                wx.Sleep(1)
                self.timer.Stop()
        event.Skip()

    def OnCharHook(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def collect_tasks(self):
        # in the future this should be automatically scanned from a directory
        self.tasks = [
            TeensyLoader,
            FlipWindows,
            DfuProgrammer,
            AvrdudePosix
        ]
        self.selectedtask = None
        # the first matching task will be pre-selected for the user
        windows = sys.platform.startswith('win32')
        teensy = self.user_data.config.teensy
        self.besttask = None
        for t in self.tasks:
            if ((t.windows and windows) or (t.posix and not windows)) and (t.teensy == teensy):
                self.besttask = t
                break

    def process(self):
        try:
            device = self.user_data.config.firmware.device
            self.runningtask = self.selectedtask(self.log_text, self.path, device)
            self.runningtask.run()
        except ProgrammingException as err:
            msg = 'Error: ' + str(err)
            wx.MessageBox(msg, caption="Can't complete programming",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)
        except Exception as err:
            msg = 'Error: ' + traceback.format_exc()
            wx.MessageBox(msg, caption="Process Error",
                          style=wx.ICON_ERROR|wx.OK|wx.CENTRE, parent=self)

    def log_text(self, text):
        self.queue.put(text)
        self.queue.put('\n')

    def show_text(self):
        if self.queue.qsize() != 0:
            try:
                while True:
                    line = self.queue.get_nowait()
                    self.main_tc.AppendText(line)
            except queue.Empty:
                pass
            self.main_tc.ShowPosition(self.main_tc.GetLastPosition())

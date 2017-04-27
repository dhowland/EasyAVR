#!/usr/bin/env python
#
# Easy AVR USB Keyboard Firmware
# Copyright (C) 2017 David Howland
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

import os
import sys
import os.path
from cx_Freeze import setup, Executable
from glob import glob
from easykeymap import __version__

# fixing cx_Freeze's failures
install_path = sys.exec_prefix
#   doesn't copy the tcl/tk dependencies
tcl_dll_path = os.path.join(install_path, 'DLLs', 'tcl86t.dll')
tk_dll_path = os.path.join(install_path, 'DLLs', 'tk86t.dll')
#   can't process TCL search without this
os.environ['TCL_LIBRARY'] = os.path.join(install_path, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(install_path, 'tcl', 'tk8.6')
#   includes DLLs from TortoiseSVN for no reason
TortoiseSVN_prefix = 'C:\\Program Files\\TortoiseSVN'

data_files = [
    "easykeymap\\builds",
    "easykeymap\\configs",
    "easykeymap\\exttools",
    "easykeymap\\icons",
    "easykeymap\\manuals"
]

setup(
    name = 'easykeymap',
    version = __version__,
    author = 'David Howland',
    author_email = 'dhowland@gmail.com',
    description = 'Easy AVR USB Keyboard Firmware Keymapper',
    long_description = 'Easy to use keymapping GUI for keyboards based on USB AVRs.',
    license = "GPLv2",
    keywords = "Easy AVR Keymap keyboard firmware",
    url = 'https://github.com/dhowland/EasyAVR',
    platforms = 'any',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: C',
        'Topic :: Utilities',
    ],
    
    options = {
        "build_exe": {
            'packages': ['easykeymap', 'easykeymap.boards', 'easykeymap.templates'],
            'include_files': [tcl_dll_path, tk_dll_path] + data_files,
            # 'include_msvcr': True,
            'bin_path_excludes': [TortoiseSVN_prefix],
            'zip_include_packages': '*',
            'zip_exclude_packages': None,
        }
    },
    
    executables = [
        Executable(
            "main.py",
            base="Win32GUI",
            targetName="easykeymap.exe",
            icon="easykeymap\\icons\\keycap.ico",
            copyright="Copyright 2016 David Howland"
        )
    ]
)

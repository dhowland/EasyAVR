#!/usr/bin/env python3
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

from cx_Freeze import setup, Executable
from easykeymap import __version__

# fixing cx_Freeze's failures
#   includes DLLs from TortoiseSVN for no reason
TortoiseSVN_prefix = 'C:\\Program Files\\TortoiseSVN'

data_files = [
    "easykeymap\\builds",
    "easykeymap\\configs",
    "easykeymap\\exttools",
    "easykeymap\\res"
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
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: C',
        'Topic :: Utilities',
    ],
    
    options = {
        "build_exe": {
            'packages': ['easykeymap', 'easykeymap.boards', 'easykeymap.gui', 'easykeymap.templates'],
            'include_files': data_files,
            # 'include_msvcr': True,
            'bin_path_excludes': [TortoiseSVN_prefix],
            'zip_include_packages': '*',
            'zip_exclude_packages': None,
        }
    },
    
    executables = [
        Executable(
            "easykeymap\\__main__.py",
            base="Win32GUI",
            targetName="easykeymap.exe",
            icon="easykeymap\\res\\keycap.ico",
            copyright="Copyright 2016 David Howland"
        )
    ]
)

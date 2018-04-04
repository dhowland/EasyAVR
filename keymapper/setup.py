#!/usr/bin/env python3
#
# Easy AVR USB Keyboard Firmware
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

from setuptools import setup, find_packages
from easykeymap import __version__

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
    install_requires = ['wxPython >= 4.0.1'],
    packages = find_packages(),
    package_data = {
        'easykeymap': ['builds/*.hex', 'configs/*.cfg', 'res/*.*']
    },
    entry_points = {
        'gui_scripts': [
            'easykeymap = easykeymap.__main__:main',
        ]
    }
)

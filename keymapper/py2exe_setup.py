#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by: python.exe -m py2exe easykeymap.gui -W py2exe_setup.py

from distutils.core import setup
import py2exe
from glob import glob
from easykeymap import __version__


RT_BITMAP = 2
RT_MANIFEST = 24

# A manifest which specifies the executionlevel
# and windows common-controls library version 6

manifest_template = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="*"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="%(level)s"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="*"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
'''

manifest_encoded = (manifest_template % dict(prog="easykeymap", level="asInvoker")).encode("utf-8")

easykeymap = {
    'version': __version__,
    'copyright': "Copyright 2016 David Howland",
    'comments': "Easy AVR USB Keyboard Keymapper",
    'script': "main.py",
    'dest_base': "easykeymap",
    'icon_resources': [(1, "easykeymap\\icons\\keycap.ico")],
    'other_resources': [(RT_MANIFEST, 1, manifest_encoded)],
}

py2exe_options = dict(
    packages = ['easykeymap', 'easykeymap.boards', 'easykeymap.templates'],
    excludes = ['pkg_resources'],
    ignores = ['Tkinter'],
    optimize=0,
    compressed=False, # uncompressed may or may not have a faster startup
    bundle_files=3,
    dist_dir='dist_exe',
    )

data_files = [
    # ("Microsoft.VC90.CRT", glob("Microsoft.VC90.CRT\\*.*")),
    ("builds", glob("easykeymap\\builds\\*.hex")),
    ("configs", glob("easykeymap\\configs\\*.cfg")),
    ("exttools", glob("easykeymap\\exttools\\*.exe")),
    ("icons", glob("easykeymap\\icons\\*.ico")),
    ("manuals", glob("easykeymap\\manuals\\*.txt"))
]

# Some options can be overridden by command line options...

setup(name="easykeymap",
      # console based executables
      console=[],

      # windows subsystem executables (no console)
      windows=[easykeymap],

      # py2exe options
      options={"py2exe": py2exe_options},
      
      data_files=data_files,
      )

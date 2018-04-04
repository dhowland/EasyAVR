
Keymapper Notes
===============

Working with the keymapper code requires the following tools:

- Python_ 3.5+
- wxPython_ 4.0+
- cx_Freeze_ 5.1+
- Sphinx_ 1.7+

.. _Python: https://www.python.org/
.. _cx_Freeze: https://anthony-tuininga.github.io/cx_Freeze/
.. _wxPython: https://www.wxpython.org/
.. _Sphinx: http://www.sphinx-doc.org/en/master/

Updating the Documentation
--------------------------

Modify the .rst files in ``./docs/source/`` as needed.  To use the Sphinx 
tool to regenerate the HTML, run ``docs.bat``.

Building the Keymapper
----------------------

The keymapper can be run from source, but for releases it is usually built 
into a Python package and a Windows executable.  After making changes and 
incorporating any new firmware, run ``package.bat`` and ``cxFreeze.bat``.  
After the builds complete, the Python package will be placed in the 
``./keymapper/dist/`` directory.  The Windows executable will be placed in  
the ``./keymapper/build/exe.win32-3.6/`` directory.  Rename the directory to 
something more descriptive, then Zip it up.

The EasyAVR keymapper build will include anything that you place into the 
``./keymapper/easykeymap/exttools`` directory.  This location is meant to 
include useful executables for programming boards.  Official EasyAVR releases 
currently include ``dfu-programmer.exe`` and ``teensy_loader_cli.exe`` in the 
build, however these files are not stored in the git repository.  They must 
be downloaded by the developer.

Modifying the Keymapper
-----------------------

TODO

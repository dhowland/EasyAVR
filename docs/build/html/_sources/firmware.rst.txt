
Firmware Notes
==============

Working with the firmware code requires the following tools:

- `Atmel Studio 7`_
- Python_ 3.5+

.. _Atmel Studio 7: https://www.microchip.com/avr-support/atmel-studio-7
.. _Python: https://www.python.org/

Atmel Studio is Windows-only, so Windows is also a requirement.

Building the Firmware
---------------------

A project workspace is included for Atmel Studio 7.  This is the primary development environment.  After making changes and confirming that the new code compiles, the firmware must be rebuilt for all supported hardware configurations.  A python script for doing so is included in the root directory of the source.  The relevant files are ``incorporate.py``, ``incorporate.bat``, and ``compile.bat``.  Check the .bat files to ensure that the paths used match your development environment, then run ``incorporate.bat`` from the root directory of the source.  It will compile all hardware configs, check that they fit into memory, and generate the build files directly into the python source tree at ``./keymapper/easykeymap/``.

Modifying the Firmware
----------------------

TODO

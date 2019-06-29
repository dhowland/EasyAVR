
Installation
============

EasyAVR releases are available on Github:
https://github.com/dhowland/EasyAVR/releases

Windows
-------

Windows users may use the compiled executable version of the EasyAVR
keymapper.  This option requires much less effort to install.

Prerequisites:

- `Teensy Loader`_ (for Teensy-based boards)
- `Atmel Flip`_ (for everything else)

.. _Teensy Loader: http://www.pjrc.com/teensy/loader.html
.. _Atmel Flip: http://www.microchip.com/developmenttools/productdetails.aspx?partno=flip

Download the Windows executable from the releases page.  The filename will be 
something like this: ``easykeymap_windows_3_00_00.zip``

Unzip the file to a local directory.  Launch the keymapper by running 
``easykeymap.exe``.

Multiplatform
-------------

Linux, Mac, and Windows users may use the Python package.  This requires an 
existing Python installation.  This option requires a little more effort to 
install, but does not rely on Windows.

Prerequisites:

- Python_ 3.5+
- wxPython_ 4.0+
- `Teensy Loader`_ (for Teensy-based boards)
- dfu-programmer_ (for everything else)

.. _Python: https://www.python.org/
.. _wxPython: https://www.wxpython.org/
.. _Teensy Loader: http://www.pjrc.com/teensy/loader.html
.. _dfu-programmer: https://github.com/dfu-programmer/dfu-programmer

Installation of the prerequisites is platform-dependent.  Here is an example 
for Ubuntu Bionic (18.04)::

    sudo apt install python3 python3-pip python3-wxgtk4.0
    sudo apt install dfu-programmer

wxPython 4.0 is very recent, so old operating systems may require more work.  
Here is an example for Ubuntu Xenial (16.04)::

    sudo apt install python3 python3-pip
    sudo apt install libwxgtk3.0
    sudo apt install libsdl1.2debian
    sudo pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython
    sudo apt install dfu-programmer

View the documentation for each of the prerequisites for help on getting them 
installed for your platform.

Download the Python package from the releases page.  The filename will be 
something like this: ``easykeymap-3.0.0.tar.gz``

Install like this::

    sudo pip3 install -U /path/to/easykeymap-3.0.0.tar.gz

Launch the keymapper like this::

    python3 -m easykeymap

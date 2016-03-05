# EasyAVR
Easy AVR USB Keyboard Firmware and Keymapper

Find info and downloads at the DT Wiki:
https://deskthority.net/wiki/Easy_AVR_USB_Keyboard_Firmware

Ask questions in the GH thread:
https://geekhack.org/index.php?topic=51252

View the source code on Github:
https://github.com/dhowland/EasyAVR

#### Table of Contents

1. [Windows User Tutorial](#windows-user-tutorial)
2. [Linux and Mac User Tutorial](#linux-and-mac-user-tutorial)
3. [Supporting Custom Boards](#supporting-custom-boards)
4. [Developer Notes](#developer-notes)

## Windows User Tutorial

#### Requirements

* [Atmel Flip](http://www.atmel.com/tools/FLIP.aspx)
* [Teensy Loader](http://www.pjrc.com/teensy/loader.html) (for Teensy-based boards)
* Optional: [Python](https://www.python.org/) 2.7 or 3.3+

#### Installation

Windows users have two options for using the Easy AVR keymapper.  The easiest option is to use the stand-alone compiled executables.  Alternatively, users familiar with the Python interpreter may run the Python scripts directly.

*Compiled executables*

1. Download the executables from [the wiki page](https://deskthority.net/wiki/Easy_AVR_USB_Keyboard_Firmware#Downloads)
2. Extract the zip to the chosen installation location
3. Start the tool by running easykeymap.exe

*Python scripts*

1. Download the source code from [Github](https://github.com/dhowland/EasyAVR) and extract
2. Start the tool with the run.bat (requires python in the PATH)
3. Optionally, the easykeymap package can be installed with setuptools

		python setup.py install
		python -m easykeymap.gui

#### Creating a keymap

1. Create a new layout and select your board -or- open a previously saved layout (File menu)
2. Copy/Paste the default layer to populate any Fn layers that you intend to use (Edit menu)
3. Modify your layout using one of the three edit methods:
	* Select a key in the keymapper and press the new assignment on your physical keyboard
	* Select a key in the keymapper and then choose a new scancode from the menu
	* Open the scancode picker, select a key in the keymapper, then select the new assignment in the picker
4. Read the manuals for help on using advanced features of the firmware such as macros and LED assignments (Help menu)
5. Save your new layout (File menu)
6. Build your firmware into a .hex file (File menu)

#### Programming the firmware

The programming of the firmware to your board depends on your hardware.  Boards based on a Teensy (e.g. Phantom) use the Teensy Loader app.  Other AVR boards use the Atmel Flip app.

*Flip*

1. Open the Atmel Flip app
2. Click the red "Load HEX File" icon and open the .hex file you created in the keymapper
3. Click the microchip "Select a Target Device" icon and choose the AVR used by your board (usually ATmega32U4 or ATmega32U2)
4. Put your keyboard into bootloader mode
5. Click the USB "Select a Communications Medium" icon and choose "USB" from the menu
6. With the AVR now connected, click the "Run" button to reprogram with the new firmware
7. With a successful completion, click the "Start Application" button

*Teensy*

Follow the instructions at the [Teensy website](http://www.pjrc.com/teensy/loader_vista.html)

## Linux and Mac User Tutorial

#### Requirements

* [dfu-programmer](https://github.com/dfu-programmer/dfu-programmer)
* [Teensy Loader](http://www.pjrc.com/teensy/loader.html) (for Teensy-based boards)
* [Python](https://www.python.org/) 2.7 or 3.3+

#### Installation

*dfu-programmer*

dfu-programmer can be installed on Linux using your chosen package manager.  Typically, it will look something like this:

`sudo apt-get install dfu-programmer`

dfu-programmer can be installed on OSX by following [these directions](http://www.uriahbaalke.com/?p=106) or with [Homebrew](http://brew.sh/) as follows:

`brew install dfu-programmer`

*Easy AVR*

1. Download the source code from [Github](https://github.com/dhowland/EasyAVR) and extract
2. Start the tool with the easykeymap.sh
3. Optionally, the easykeymap package can be installed with setuptools

		sudo python setup.py install
		python -m easykeymap.gui

#### Programming the firmware

*dfu-programmer*

1. Create a firmware as explained in [Creating a keymap](#creating-a-keymap)
2. Put your keyboard into bootloader mode
3. Program your .hex file (replace device type as necessary)

		sudo dfu-programmer atmega32u4 erase
		sleep 10
		sudo dfu-programmer atmega32u4 flash /path/to/firmware.hex
		sudo dfu-programmer atmega32u4 launch

AVR-dude may also be used on Linux, as explained [here](https://geekhack.org/index.php?topic=51252.msg2066099#msg2066099).

*Teensy*

Follow the instructions at the [Teensy website](http://www.pjrc.com/teensy/loader_linux.html)

## Supporting Custom Boards

#### Requirements

* A text editor

TODO

## Developer Notes

#### Requirements

* [Python](https://www.python.org/) 2.7 and 3.3+ (both would be needed for complete testing)
* [Atmel Studio 7](http://www.atmel.com/tools/atmelstudio.aspx)

TODO


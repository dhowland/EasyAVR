
Supporting Custom Boards
========================

EasyAVR can be extended to support custom keyboards that aren't already 
included in the default install.  To add support for a custom keyboard, you 
will need the following:

- The EasyAVR keymapper
- A text editor
- Reading comprehension

Know Your Hardware
------------------

You are going to need to know how the controller is connected to your 
keyboard matrix.  This is often the most difficult part for new users, so get 
this figured out before doing anything else.  AVR pins have names such as B6, 
C1, F4, and so on.  You need to be able to specify which pins are connected 
to the rows and columns of the keyboard matrix, and which are connected to 
the LEDs.  If you want to add support for a handwired board, you should know 
this already.  If you want to add support for a board that is already 
supported by another firmware, you can often just look at that source code 
for the pin list.

Design the Layout
-----------------

Create the layout at <http://www.keyboard-layout-editor.com/>.  You should 
start with the ANSI 104 or ISO 105 presets, because those legends will be 
recognized and automatically translated.  Really all that matters is getting 
the sizes of the keys correct.  Properties such as colors, rotation, and 
stepped keys aren't supported by EasyAVR.

When you're done, download the layout data by using the "Download JSON" 
button.  Don't copy/paste from the "Raw data" tab, it isn't valid JSON.

Create the Custom Board
-----------------------

In the keymapper, choose "Define Keyboard..." in the File menu.  This starts 
the New Keyboard Definition Wizard.  Follow the directions.

The keymapper automatically creates a directory on your filesystem to hold 
custom boards and layout configs.  The path is ``~/.EasyAVR/``, which is 
probably ``/home/username/.EasyAVR`` on Linux or 
``C:\Users\username\.EasyAVR`` on Windows.

After completing the wizard, the generated config will be in 
``~/.EasyAVR/boards/``.  Open the file in a text editor.  This file is a pure 
Python script that describes the keyboard hardware.  You must use correct 
`Python syntax`_!

.. _Python syntax: https://docs.python.org/3/

Read ALL comments in the file and follow those directions.  In particular, 
make sure to fix the row/column matrix for each key in keyboard_definition, 
because the tool was not given that information and had to make a wild guess.

Save your edits, then restart the EasyAVR keymapper.  Create a new layout, 
select the board you just configured, and test it.  Remember that if you 
change the hardware description in the config file, you must not load saved 
keymaps created with the old config file because it could lead to corrupted 
builds

Layout Mod Configs
==================

The .cfg files allow the user to modify the layout of the keyboard.  This is 
used for keyboards that allow the builder to configure many different layouts 
with the same PCB.  For example, the Phantom can be configured for ANSI and 
ISO layouts, as well as many other custom layouts.

By default, the layout mapper will show every possible key for a supported 
hardware.  Selecting an alternate layout from the .cfg file will change the 
appearance of the layout.  Each line in the .cfg file changes one key in the 
layout.

All lines must be one of the following:
    | blank
    | comment
    | config header
    | modifier command

Blank lines are ignored.  Comments are lines that start with "#".  They are 
also ignored.

Config headers delineate and name each layout.  They are formatted as a 
string in brackets, like this: ``[name]``

Beneath each config header is a list of modifier commands.  Modifier commands 
must be one either ``MAKE_KEY(row, column, width, height)``, or 
``MAKE_SPACER(row, column, width)``

All arguments are integers.  Row and column are the layout coordinates (not 
the Matrix coordinates) of the key to be modified.  The layout coordinates of 
a key may be found at the top of the editor box in the GUI.  Width and height 
are in units of 1/4 of a key.  That means a normal 1u key is (width=4, 
height=4).  An ANSI 2u backspace is (width=8, height=4). An ISO Enter is 
(width=5, height=8).  A 6.25u space bar is (width=25, height=4).

MAKE_KEY() will change the size of a key at the given location.

MAKE_SPACER() will change a given location into empty space of a given width.

To remove a key, change it to a spacer with zero width.  Do not set a key to
zero width.

Note: Old versions of the tool also had a MAKE_BLANK() command.  It is still 
supported for backwards compatibility, but it is now identical to 
MAKE_SPACER().

Example
-------

Here is an example .cfg that turns the generic Costar layout into either a 
standard ANSI layout or a standard ISO layout::

    [ANSI 104]
    # Remove the non-US Backslash key
    MAKE_SPACER(5, 1, 0)
    # Extend the left Shift key to 2.25u
    MAKE_KEY(5, 0, 9, 4)
    # Remove the non-US Hashmark key
    MAKE_SPACER(4, 12, 0)
    # Extend the Enter key to 2.25u width
    MAKE_KEY(4, 13, 9, 4)
    
    [ISO 105]
    # Remove the Backslash key
    MAKE_BLANK(3, 13, 6)
    # Extend the Enter key to 2u height (negative height extends upwards)
    MAKE_KEY(4, 13, 5, -8)

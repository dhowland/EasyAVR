
USB Options
===========

An EasyAVR keyboard actually appears as four devices when it is plugged in to 
a PC.  Each is called an "HID endpoint", where HID stands for Human Interface 
Device.  The extra devices are required for some of the advanced features of 
the firmware.  In most cases it is best to simply leave all of them enabled. 
However, in some situations the extra devices cause problems.  Therefore, 
they may be optionally disabled.  This may help work around problems on 
platforms that are confused by the extra endpoints, but it will prevent those 
features from working.

.. image:: easykeymap_ss8.png

Endpoints
---------

Keyboard
    This is a standards-compliant USB HID keyboard.  In other words, this is a
    basic keyboard with no special features.  It is boot compatible, which
    means it requires no driver and will work with BIOS setup screens.  Per the
    spec, it supports 6-key rollover.  This endpoint is required and cannot be
    disabled.

Media/Power
    This endpoint, combined with the Keyboard endpoint, implements a Microsoft
    Windows "Enhanced Keyboard".  It provides "consumer controls" which are the
    media keys, and "system power control" which are the power keys
    (SCANCODE_NEXT_TRACK through SCANCODE_FAVES and SCANCODE_POWER through
    SCANCODE_WAKE in the :doc:`functions` chapter).

NKRO
    This is an additional keyboard endpoint that provides n-key rollover.  With
    n-key rollover, any number of keys may be pressed at the same time.  In
    other words, there is no 6 key limit.  This endpoint may not be available
    on extremely limited devices, such as the Techkeys Card.

Mouse
    This is a standards-compliant USB HID Mouse.  It allows the use of mouse
    keys (SCANCODE_MOUSE1 through SCANCODE_MOUSEYU in the :doc:`functions`
    chapter).  This endpoint may not be available on extremely limited devices,
    such as the Techkeys Card.

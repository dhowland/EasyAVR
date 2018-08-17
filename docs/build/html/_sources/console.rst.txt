The Config Console
==================

The config console enables the user to tune the keyboard behavior without 
reprogramming the firmware.  Configuration options are stored in non-volatile 
memory and therefore persist even when the keyboard is unplugged.

Accessing the Config Console
----------------------------

Map a key to SCANCODE_CONFIG using the keymapper GUI and reprogram the 
firmware.  Open a text editor such as Notepad on Windows or TextEdit on Mac.  
Place the cursor in a new file, ready to type.  Press the SCANCODE_CONFIG 
key.  The keyboard will print out a menu into the text editor.

To select options in the menus, press a single number then press enter.  
Don't forget to quit the config console before moving on to other things!

The data entry interface is very basic.  It works by watching what you type, 
but it can't "see" what is in the text editor.  If you use navigation keys or 
anything else to try and correct typos, the config console will probably get 
confused.  It is necessary to type correctly to have your input recognized.  
It shouldn't be a problem because the interface only requires the use of 
numbers and Enter.  Characters other than 0-9 are interpreted as 0.

Here is a transcript of a typical session::

    Main Menu:
    1) Config menu
    2) Timing menu
    3) LED menu
    4) Debug menu
    5) Reset
    9) Quit
    > 1

    Config Menu:
    1) Virtual Num Pad: OFF
    2) Win Lock on Scroll Lock: OFF
    3) Default Layer: 0
    4) Boot Keyboard: OFF
    5) Unlinked Num Lock: OFF
    6) Alternate Debounce Style: OFF
    9) Back
    > 4
    Boot Keyboard [0=OFF, 1=ON]> 1

    Config Menu:
    1) Virtual Num Pad: OFF
    2) Win Lock on Scroll Lock: OFF
    3) Default Layer: 0
    4) Boot Keyboard: ON
    5) Unlinked Num Lock: OFF
    6) Alternate Debounce Style: OFF
    9) Back
    > 9

    Main Menu:
    1) Config menu
    2) Timing menu
    3) LED menu
    4) Debug menu
    5) Reset
    9) Quit
    > 2

    Timing Menu:
    1) Debounce Time (ms): 12
    2) Max Hold Time for Tap (ms): 240
    3) Max Delay Time for Double Tap (ms): 120
    4) Base Mouse Movement: 5 
    5) Mouse Movement Multiplier: 15
    6) Min Hold Time for Repeat (ms): 800
    7) Repeat Period (ms): 32
    8) Matrix Setup Wait (cycles): 5  
    9) Back
    > 1
    Debounce Time (ms) [1-99]> 14

    Timing Menu:
    1) Debounce Time (ms): 14
    2) Max Hold Time for Tap (ms): 240
    3) Max Delay Time for Double Tap (ms): 120
    4) Base Mouse Movement: 5 
    5) Mouse Movement Multiplier: 15
    6) Min Hold Time for Repeat (ms): 800
    7) Repeat Period (ms): 32
    8) Matrix Setup Wait (cycles): 5  
    9) Back
    > 9

    Main Menu:
    1) Config menu
    2) Timing menu
    3) LED menu
    4) Debug menu
    5) Reset
    9) Quit
    > 9


Config Menu Options
-------------------

Virtual Num Pad
    On tenkeyless boards, the number row will act like the equivalent number
    pad keys when Num Lock is active.  This allows the user to enter special
    characters using Alt+num combinations.

Win Lock on Scroll Lock
    When the Scroll Lock is active the Windows key is disabled.  This is
    useful for gaming.

Default Layer
    The layer to use at startup and when no Fn keys are active.  Usually this
    would be set to 0.

Boot Keyboard
    This setting allows you to disable the NKRO feature so that the keyboard
    works exactly as a HID-compliant boot compatible USB keyboard (6KRO).

Unlinked Num Lock
    Activating this setting will cause the keyboard or numpad to ignore the
    system Num Lock and keep track of Num Lock internally.  This prevents the
    keyboard or numpad from affecting other keyboards attached to the system.

Alternate Debounce Style
    This toggles between two debounce algorithms.  By default, key presses are
    detected with a "hair trigger" for minimum response time.  It is recommended
    that users set the debounce time to at least 12ms using this option.  The
    alternate algorithm is more traditional, detecting a key press after a
    confirmation time.  The alternate setting limits Debounce Time to 32ms or
    less.  This setting will not take effect until the keyboard is unplugged.
    Changing this setting resets the debounce time to default (see below).
    More info here_.

.. _here: https://medium.com/@dhowland/debounce-algorithms-in-easy-avr-usb-keyboard-firmware-2288a15a96c8

Timing Menu Options
-------------------

Debounce Time
    The number of milliseconds that the keyboard will prevent a key to change
    state after the switch actuates or de-actuates.  Users should not change
    this setting unless they are seeing chattering (double key presses).
    In that case, increase the time by a few ms.  Default is 12ms, or 6ms for
    the alternate debounce algorithm.

Max Hold Time for Tap
    The maximum number of milliseconds that a key may be held for the press
    to be detected as a tap.  The smaller this value, the faster a user has to
    be to register a key tap.  Default is 240ms.

Max Delay Time for Double Tap
    The maximum number of milliseconds that may elapse between key taps for
    the two actuations to be detected as a double tap.  The smaller the value,
    the faster a user has to be to register a double or triple-tap sequence.
    Default is 120ms.

Base Mouse Movement
    This unitless value controls the minimum speed of the mouse when the user
    presses a mouse movement key.  It should be small enough to allow for
    fine-point control of the mouse.  Default is 5.

Mouse Movement Multiplier
    This unitless value is added to the base mouse movement value for each
    consecutive tap on the mouse movement key.  If a user triple-taps the key,
    the resulting movement value will be (BASE + (MULT * 2)).  Default is 15.

Min Hold Time for Repeat
    The minimum number of milliseconds that a key must be held for rapid fire
    mode to to kick in.  This has no effect on keys that haven't been assigned
    rapid fire mode.  Default is 800ms.

Repeat Period
    The number of milliseconds between repeated key presses when a key is held
    in rapid fire mode.  The smaller the value, the faster the repeat speed.
    Default is 32ms.

Matrix Setup Wait
    The number of busywait cycles to delay after setting the matrix selection
    outputs before reading keys for a given row/column.  Increasing this value
    can clean up unexpected keypress behavior on boards with slower matrix
    circuitry.  Default is 5.

LED Menu Options
----------------

Default Dimmer Level
    This sets the default brightness of the LED indicators and backlights.
    Although the SCANCODE_BL_ENABLE key only cycles between five levels
    (1, 4, 8, 12, and 16), this setting may be set anywhere between 1 (dimmest)
    and 16 (brightest).

Default Backlight Enable
    This changes the default configuration of the backlight zones on keyboards
    that support backlighting.  The SCANCODE_BL_ENABLE key is used to cycle
    through the different lighting zones, in order.  The number of this setting
    specifies where in that cycle to initialize the backlights.  This only
    takes effect at power-up.

Default Backlight Mode
    This changes the default configuration of the backlight modes on keyboards
    that support backlighting.  The SCANCODE_BL_MODE key is used to cycle
    through the different lighting modes, in order.  The number of this setting
    specifies where in that cycle to initialize the backlights.  This only
    takes effect at power-up.

Clearing All Saved Settings
---------------------------

If you set a configuration option that renders the keyboard unusable, you can
clear non-volatile memory by unplugging the keyboard and holding the ENTER key
(as defined on Layer 0) while plugging it back in.

Special Functions and Modes
===========================

Special Functions
-----------------

In addition to the standard USB keyboard scancodes, EasyAVR supports several
special functions, many of which are not available on regular keyboards.

=========================  ====================================================
Scancode                   Description
=========================  ====================================================
SCANCODE_FN0               Activate the "Default" layer
SCANCODE_FN1               Activate the 1st function layer (or deactivate, depending on mode)
SCANCODE_FN2               Activate the 2nd function layer (or deactivate, depending on mode)
SCANCODE_FN3               Activate the 3rd function layer (or deactivate, depending on mode)
SCANCODE_FN4               Activate the 4th function layer (or deactivate, depending on mode)
SCANCODE_FN5               Activate the 5th function layer (or deactivate, depending on mode)
SCANCODE_FN6               Activate the 6th function layer (or deactivate, depending on mode)
SCANCODE_FN7               Activate the 7th function layer (or deactivate, depending on mode)
SCANCODE_FN8               Activate the 8th function layer (or deactivate, depending on mode)
SCANCODE_FN9               Activate the 9th function layer (or deactivate, depending on mode)

SCANCODE_BL_DIMMER         Cycle through backlight brightness levels, also
                           controls indicator LED brightness
SCANCODE_BL_MODE           Cycle through the backlighting modes (static,
                           breathing, reactive, and erosion)
SCANCODE_BL_ENABLE         Enable/disable the backlight and cycle through the
                           different lighting zones

SCANCODE_KEYLOCK           (toggle) Disable sending scancodes to PC
SCANCODE_WINLOCK           (toggle) Disable the windows key
SCANCODE_ESCGRAVE          Acts like grave key if shift is pressed (to make tilde).
                           Otherwise acts like Esc key.  Used for 60% keyboards.
SCANCODE_BOOT              Jump to bootloader (Keyboard will not work again until it is reset)
SCANCODE_CONFIG            Go into interactive configuration console

SCANCODE_M1                Play macro 1
SCANCODE_M2                Play macro 2
SCANCODE_M3                Play macro 3
SCANCODE_M4                Play macro 4
SCANCODE_M5                Play macro 5
SCANCODE_M6                Play macro 6
SCANCODE_M7                Play macro 7
SCANCODE_M8                Play macro 8
SCANCODE_M9                Play macro 9
SCANCODE_M10               Play macro 10
SCANCODE_M11               Play macro 11
SCANCODE_M12               Play macro 12
SCANCODE_M13               Play macro 13
SCANCODE_M14               Play macro 14
SCANCODE_M15               Play macro 15
SCANCODE_M16               Play macro 16
SCANCODE_MRAM_RECORD       Start/Stop recording the RAM macro
SCANCODE_MRAM_PLAY         Play the RAM macro

SCANCODE_MOUSE1            Mouse button 1
SCANCODE_MOUSE2            Mouse button 2
SCANCODE_MOUSE3            Mouse button 3
SCANCODE_MOUSEXL           Move mouse pointer left
SCANCODE_MOUSEXR           Move mouse pointer right
SCANCODE_MOUSEYD           Move mouse pointer down
SCANCODE_MOUSEYU           Move mouse pointer up
                           (Double-tap the mouse keys to move the cursor faster.
                           Triple-tap for even more speed, and so on.)

SCANCODE_POWER             Power down the system
SCANCODE_SLEEP             Put the system to sleep
SCANCODE_WAKE              Wake the system from sleep state

SCANCODE_NEXT_TRACK        Skip to next track in Windows
SCANCODE_PREV_TRACK        Skip to last track in Windows
SCANCODE_STOP              Stop playback in Windows
SCANCODE_PLAY_PAUSE        Play or Pause playback in Windows
SCANCODE_BRIGHT_INC        Increase screen brightness in Windows
SCANCODE_BRIGHT_DEC        Decrease screen brightness in Windows
SCANCODE_MUTE              Mute main volume in Windows
SCANCODE_BASS_BOOST        Toggle bass boost in Windows
SCANCODE_VOL_INC           Increase main volume in Windows
SCANCODE_VOL_DEC           Decrease main volume in Windows
SCANCODE_BASS_INC          Increase bass equalizer in Windows
SCANCODE_BASS_DEC          Decrease bass equalizer in Windows
SCANCODE_TREB_INC          Increase treble equalizer in Windows
SCANCODE_TREB_DEC          Decrease treble equalizer in Windows
SCANCODE_MAIL              Open system mail reader in Windows
SCANCODE_CALC              Open calculator in Windows
SCANCODE_MYCOMP            Open My Computer in Windows
SCANCODE_SEARCH            Open search dialog in Windows
SCANCODE_BROWSER           Open web browser to homepage in Windows
SCANCODE_BACK              Navigate backward in Windows
SCANCODE_FORWARD           Navigate forward in Windows
SCANCODE_WWWSTOP           Stop navigation in Windows
SCANCODE_REFRESH           Refresh navigation in Windows
SCANCODE_FAVES             Open favorites dialog in Windows
=========================  ====================================================

Layers
------

The system contains ten keymap layers that may be configured by the user. 
There is a default layer which is used when no Fn keys are active.  This is 
layer 0 by default, but that can be changed in the config console.  The most 
used mapping layer should be default.  There are also nine further function 
layers. 'Layer 1' is accessed using the 'Fn 1' special modifier key, 'Layer 
2' by 'Fn 2', and so on.

Holding a Fn key in normal mode accesses the associated layer, and using one 
of the lock modes on that Fn key keeps the associated layer active from that 
point forward until another Fn key is pressed. If a new layer is locked while 
another layer is already locked, then the most recent lock takes precedence 
(only one layer can ever be locked at a time).

A Fn key may be accessed from within another Fn layer (chaining).  The 
firmware keeps track of which Fn keys are active and the order they were 
activated.

Key Modes
---------

Any individual key on any layer may be assigned a special operating mode.  
These modes change the key press behavior to something different than the 
normal momentary switch behavior.  The possible settings are described in the 
table, below.  These special modes only work on standard keys (HID 
scancodes), modifiers, and Fn keys.

A key 'tap' is a rapid press and release of a key by itself.  A 'double tap' 
is two taps in quick succession. Think of mouse clicks.

Normal
    Momentary switch.  Press to activate the key and un-press to deactivate.

Toggle
    Toggle switch.  Press to change the state of the key.  If the key is
    deactivated, pressing will activate it and vice-versa.

Tap Key
    Also known as a 'dual use' key.  When a key is assigned to this mode, it
    acts the same as normal but, if tapped, will send a normal scancode of 
    your choosing.  This is only available on modifiers and Fn keys.

Lockable
    Acts the same as normal but double tapping the key will toggle it active.
    Pressing the key again will deactivate it.

Rapid Fire
    This is an auto-repeating mode.  The key acts the same as normal except it
    will be rapidly retyped when the key is held.  Think of old video game
    controllers.  This is only available on standard keys.

When a scancode is bound to a tap key, it will be sent on the upstroke, but
only if the mod/fn key was tapped and not combined with another key. This is
useful in several situations.  For example, the Application key may be used as
a function key but also retain it's use as a normal key.  In another example,
the function keys may be used to simulate Matias half-keyboard by making the
space bar a Fn key with Space as its tap action.

Automatic Modifiers
-------------------

Any key may be assigned an additional modifier state of any combination of 
Shift, Ctrl, Alt, and GUI (meta).  As long as the key is pressed, it will 
also hold the assigned modifiers.  This means you can create a "login" key by 
binding it to Del with Ctrl+Alt.  Or, you could create a "#" key by binding 
it to Shift+3.  This feature only makes sense when the key is in Normal mode. 
Remember that the auto mods can interfere with the actual modifier keys if 
they are held at the same time.

RAM Macros
----------

The system supports one RAM-based macro that can be recorded on the fly.  
Simply press the 'Macro Rec' key, which will set the "Recording" LED Mode to 
indicate that the keyboard is listening.  Type the pattern to be recorded and 
then press the 'Macro Rec' key again.  To play it back, press the 'Macro 
Play' key.  The macro will be lost when the keyboard loses power.  Only 
normal scancodes are supported in the RAM macro at this time.

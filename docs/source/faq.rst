
Frequently Asked Questions
==========================

I recently upgraded to a newer version and now the keyboard doesn't work in Windows.
    Sometimes Windows gets confused when the USB endpoints are changed around.
    You can either remove the keyboard in the "devices" control panel and
    reconnect it, or you can simply move it to a different usb port.  If
    neither is an option, you can work around the problem by disabling NKRO.

I get a runtime error, "The program can't start because MSVCP100.dll is missing from your computer."
    Install the Visual Studio 2010 redistributable package for x86 from Microsoft_.

.. _Microsoft: http://www.microsoft.com/en-in/download/details.aspx?id=5555

Hey, my number row is mapping to numpad and I didn't tell it to do that!
    Virtual Numpad is enabled.  Either turn off NumLock or disable Virtual Numpad.

Why is my numpad is sending the wrong scancodes? -or- Why won't the Numlock LED turn on?
    You have "Unlink Numlock" enabled.  Disable that setting to get normal 
    numpad scancodes.

Why doesn't my Windows key work?
    Turn off Scroll Lock or disable the "Win Lock on Scroll Lock" setting.

Why does my QFR turn on the Windows Lock LED when Scroll Lock is pressed?
    Disable the "Win Lock on Scroll Lock" setting.

I lost all my configuration settings!
    You probably installed a new version of the firmware.  If the firmware 
    detects an different version of EEPROM data, it erases everything and 
    installs defaults to be on the safe side.  The settings are easy to 
    change, just put them back the way you like.

I bricked my keyboard! What are you going to do about it?
    I'll help you fix it if I can, but I don't owe you anything.  I've 
    programmed all sorts of boards with all kinds of firmware (both good and 
    bad) and I've never bricked anything.  Just press the reset switch.  If 
    you really managed to brick it, it's your own fault.

My computer acts weird when the keyboard is plugged in, or the keyboard just isn't recognized by some of my computers.
    Try disabling the advanced USB interfaces in the config console.  This 
    will limit you to 6KRO, but it should improve compatibility with quirky 
    hosts.

If this software is supposed to be so "easy", why do I have to use Flip or Teensy Loader?
    It has to do with the bootloader software that's already part of the 
    supported boards.  The short answer is that a goal of the project is to be 
    easy to setup and use with good compatibility, and that means using the 
    "OEM" software loading methods.

Can you add a swap Caps/Ctrl (or Backspace/Backslash, Esc/grave, etc.) feature?
    Those are great features on a normal keyboard.  However, this firmware is 
    used on programmable keyboards.  The way to implement those features is 
    with alternate layers.  You have 10 to work with.

Why am I getting unwanted extra characters while typing in Linux when pressing the NON_US_HASHMARK_AND_TILDE and/or the BACKSLASH_AND_PIPE key?
    The bit-packed vector that is used for NKRO support is not well supported 
    in linux when using those keys.  I think there may be some kind of 
    translation layer for internationalization that is causing keys to be 
    virtually lifted and redetected even though the user holds the key steady 
    IRL.  To work around this you can use the "Basic keyboard" config option 
    to disable NKRO and use 6KRO instead.

The F13-F24 keys don't work.
    The NKRO field is not wide enough to fit those nonstandard scancodes.  AVR 
    microcontrollers are extremely limited in memory and this was a compromise 
    that had to be made.  To use those scancodes, disable NKRO.

The BOOT key doesn't work.
    This usually means that the firmware doesn't have the correct address of 
    the bootloader.  Make sure the "Teensy" config item is set correctly for 
    your board.  On boards that use the Astar microcontroller, this is a known 
    problem.  The custom bootloader on the Astar requires a special value in 
    memory that is not reserved by the EasyAVR firmware.

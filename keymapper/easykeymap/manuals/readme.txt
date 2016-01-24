README: Easy AVR USB Keyboard Firmware - Beginner's guide
metalliqaz@geekhack

==============
Introduction
============

This is a keyboard firmware and keymapping GUI for custom keyboards based on
USB AVRs.  It is powerful but also really easy to use.  It supports a wide
variety of custom PCBs, such as Phantom, GH60, and bpiphany's Costar replacement
controllers.  It also features several advanced functions not found on retail
keyboards. (see documentation in the Help menu)

The homepage for this package may be found at the following URLs:
https://deskthority.net/wiki/Easy_AVR_USB_Keyboard_Firmware
https://geekhack.org/index.php?topic=51252
https://github.com/dhowland/EasyAVR

If you need help, go to the wiki and read the FAQ.  If you still need help,
post your question in the Geekhack thread.

===================
Creating A Keymap
=================

If you're reading this, you already managed to download and install the package.
Run it with python 3.3 or greater.  'python -m easykeymap.gui' should work.

Select "File->New Default Layout...".  In the popup window, select your keyboard
and then select your layout at the bottom.  Not all keyboards have multiple
layouts.  <All Keys> is the default.  Press OK.

Now you need to assign scancodes to keys.  There are three ways to do this.
First, you can simply select a key in the GUI and then use your keyboard to
press the key that you want assigned to it.  Second, you can select a key in
the GUI and then manually assign a scancode from the "Set" drop-down.  Third,
you can use the scancode picker from the "View" menu.  Select the key on the
layout, then select the assignment from the picker window.

Layers are accessed with FN keys.  To map each layer, select it using the radio
buttons near the top.  Make it easy on yourself and create your default layer
first, then copy/paste it to other layers using the "Edit" menu.

You're going to want to make sure you assign SCANCODE_BOOT somewhere on one of
your layers.  I like to use Fn+Esc.  It makes reprogramming easier.

When you're done with your layout, save it with "File->Save Layout As...".

=====================
Programming A Build
===================

Build your layout with "File->Build Firmware...".  This will create a .hex file
that can be loaded onto your custom keyboard.

Open your programming tool.  In Windows, this is the Teensy Loader for boards
with a Teensy controller (such as Phantom) or this is Atmel Flip for everything
else.  If you're on Mac or Unix, ask Geekhack for help.  Load the .hex file
you created above.

Put your keyboard into boot mode.  Either press the key sequence that was
previously programmed for boot, or use a hardware reset.  Teensy controllers
have a button.  Most bpiphany controllers have a magnetic switch.  KMAC uses
the Caps Lock key while plugging it in.  Other PDBs have a jumper.  Know your
hardware.

Once the bootloader is running, use your programming tool to connect and then
program flash.  When that completes, use your programming tool to reboot the
keyboard.

This is the sequence in Flip:
  Device->Select
  Settings->Communications->USB, then press "Open"
  File->Load HEX File
  press "Run", let it reprogram
  press "Start Application"

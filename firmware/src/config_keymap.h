/*
 * Easy AVR USB Keyboard Firmware
 * Copyright (C) 2013-2016 David Howland
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


#ifndef CONFIG_KEYMAP_H_
#define CONFIG_KEYMAP_H_

#include <stddef.h>
#include <stdint.h>
#include <avr/pgmspace.h>

#include <LUFA/Drivers/USB/USB.h>

#include "matrix.h"

#define FN_BUFFER_SIZE (4)

/* This shall equal the number of the HID report LEDs (num, caps, scroll, compose, kana) */
#define LED_LAYERS_SIZE (5)

/* Media codes in the consumer page, not defined by LUFA */
/* http://download.microsoft.com/download/1/6/1/161ba512-40e2-4cc9-843a-923143f3456c/translate.pdf */
/* http://download.microsoft.com/download/1/6/1/161ba512-40e2-4cc9-843a-923143f3456c/scancode.doc */
/* http://download.microsoft.com/download/E/3/A/E3AEC7D7-245D-491F-BB8A-E1E05A03677A/keyboard-support-windows-8.docx */
#define SC_WIN_CP_NEXT_TRACK 0xB5	/* Scan Next Track (OSC) */
#define SC_WIN_CP_PREV_TRACK 0xB6	/* Scan Previous Track (OSC) */
#define SC_WIN_CP_STOP 0xB7			/* Stop (OSC) */
#define SC_WIN_CP_PLAY_PAUSE 0xCD	/* Play/Pause (OSC) */
#define SC_WIN_CP_BRIGHT_INC 0x6F	/* Brightness Increment (RTC) */
#define SC_WIN_CP_BRIGHT_DEC 0x70	/* Brightness Decrement (RTC) */
#define SC_WIN_CP_MUTE 0xE2			/* Mute (OOC) */
#define SC_WIN_CP_BASS_BOOST 0xE5	/* Bass Boost (OOC) */
#define SC_WIN_CP_VOL_INC 0xE9		/* Volume Increment (RTC) */
#define SC_WIN_CP_VOL_DEC 0xEA		/* Volume Decrement (RTC) */
#define SC_WIN_CP_BASS_INC 0x0152	/* Bass Increment (RTC) */
#define SC_WIN_CP_BASS_DEC 0x0153	/* Bass Decrement (RTC) */
#define SC_WIN_CP_TREB_INC 0x0154	/* Treble Increment (RTC) */
#define SC_WIN_CP_TREB_DEC 0x0155	/* Treble Decrement (RTC) */
#define SC_WIN_CP_MEDIA_SEL 0x0183	/* AL Consumer Control Configuration (Sel) */
#define SC_WIN_CP_MAIL 0x018A		/* AL Email Reader (Sel) */
#define SC_WIN_CP_CALC 0x0192		/* AL Calculator (Sel) */
#define SC_WIN_CP_MY_COMP 0x0194	/* AL Local Browser (Sel) */
#define SC_WIN_CP_SEARCH 0x0221		/* AC Search (Sel) */
#define SC_WIN_CP_HOME 0x0223		/* AC Home (Sel) */
#define SC_WIN_CP_BACK 0x0224		/* AC Back (Sel) */
#define SC_WIN_CP_FORWARD 0x0225	/* AC Forward (Sel) */
#define SC_WIN_CP_WWWSTOP 0x0226	/* AC Stop (Sel) */
#define SC_WIN_CP_REFRESH 0x0227	/* AC Refresh (Sel) */
#define SC_WIN_CP_FAVES 0x022A		/* AC Bookmarks (Sel) */
/* Power controls */
#define SC_WIN_GDP_POWER 0x81		/* System Power Down */
#define SC_WIN_GDP_SLEEP 0x82		/* System Sleep */
#define SC_WIN_GDP_WAKE 0x83		/* System Wake Up */


/* What follows are "fake" scancodes that are used to represent all the
   special functions that may be mapped to keys in custom layouts.  The
   HID Page 6 spec uses 8 bits of space, but modern OSes only use the
   first half.  Therefore, I override those codes.  These codes are never
   sent over the wire.  Instead, they are intercepted and used to trigger
   internal functions or are remapped to other devices. */

#define SCANCODE_NEXT_TRACK 0x97
#define SCANCODE_PREV_TRACK 0x98
#define SCANCODE_STOP 0x99
#define SCANCODE_PLAY_PAUSE 0x9A
#define SCANCODE_BRIGHT_INC 0x9B
#define SCANCODE_BRIGHT_DEC 0x9C
#define SCANCODE_MUTE 0x9D
#define SCANCODE_BASS_BOOST 0x9E
#define SCANCODE_VOL_INC 0x9F
#define SCANCODE_VOL_DEC 0xA0
#define SCANCODE_BASS_INC 0xA1
#define SCANCODE_BASS_DEC 0xA2
#define SCANCODE_TREB_INC 0xA3
#define SCANCODE_TREB_DEC 0xA4
#define SCANCODE_MEDIA_SEL 0xA5
#define SCANCODE_MAIL 0xA6
#define SCANCODE_CALC 0xA7
#define SCANCODE_MYCOMP 0xA8
#define SCANCODE_SEARCH 0xA9
#define SCANCODE_BROWSER 0xAA
#define SCANCODE_BACK 0xAB
#define SCANCODE_FORWARD 0xAC
#define SCANCODE_WWWSTOP 0xAD
#define SCANCODE_REFRESH 0xAE
#define SCANCODE_FAVES 0xAF

#define NUMBER_OF_MEDIA_KEYS (25)

/* buttons must be sequential and below XY*/
#define SCANCODE_MOUSE1 0xB1
#define SCANCODE_MOUSE2 0xB2
#define SCANCODE_MOUSE3 0xB3
#define SCANCODE_MOUSE4 0xB4
#define SCANCODE_MOUSE5 0xB5
#define SCANCODE_MOUSEXR 0xB6
#define SCANCODE_MOUSEXL 0xB7
#define SCANCODE_MOUSEYU 0xB8
#define SCANCODE_MOUSEYD 0xB9

#define NUMBER_OF_MOUSE_BUTTONS (5)

#define SCANCODE_POWER 0xBD
#define SCANCODE_SLEEP 0xBE
#define SCANCODE_WAKE 0xBF

#define SCANCODE_BL_DIMMER 0xC1
#define SCANCODE_BL_MODE 0xC2
#define SCANCODE_BL_ENABLE 0xC3
#define SCANCODE_KEYLOCK 0xC8
#define SCANCODE_WINLOCK 0xC9
#define SCANCODE_ESCGRAVE 0xCA
#define SCANCODE_MRAM_RECORD 0xCC
#define SCANCODE_MRAM_PLAY 0xCD
#define SCANCODE_BOOT 0xCE
#define SCANCODE_CONFIG 0xCF

#define SCANCODE_M1 0xD0
#define SCANCODE_M2 0xD1
#define SCANCODE_M3 0xD2
#define SCANCODE_M4 0xD3
#define SCANCODE_M5 0xD4
#define SCANCODE_M6 0xD5
#define SCANCODE_M7 0xD6
#define SCANCODE_M8 0xD7
#define SCANCODE_M9 0xD8
#define SCANCODE_M10 0xD9
#define SCANCODE_M11 0xDA
#define SCANCODE_M12 0xDB
#define SCANCODE_M13 0xDC
#define SCANCODE_M14 0xDD
#define SCANCODE_M15 0xDE
#define SCANCODE_M16 0xDF

/* Must be larger than the 0xE0 range */
#define SCANCODE_FN0 0xF0
#define SCANCODE_FN1 0xF1
#define SCANCODE_FN2 0xF2
#define SCANCODE_FN3 0xF3
#define SCANCODE_FN4 0xF4
#define SCANCODE_FN5 0xF5
#define SCANCODE_FN6 0xF6
#define SCANCODE_FN7 0xF7
#define SCANCODE_FN8 0xF8
#define SCANCODE_FN9 0xF9

#define NUMBER_OF_LAYERS (10)

#ifdef __AVR_ATmega16U2__
#define MACRO_BUFFER_SIZE (512)
#elif __AVR_AT90USB1286__
#define MACRO_BUFFER_SIZE (1024 * 4)
#else
#define MACRO_BUFFER_SIZE (1024 * 2)
#endif

#ifdef __AVR_ATmega32U2__
#define MACRO_RAM_SIZE (40)
#elif __AVR_ATmega32U4__
#define MACRO_RAM_SIZE (80)
#elif __AVR_AT90USB1286__
#define MACRO_RAM_SIZE (160)
#endif /* Larger ATmega Devices */

#define NUMBER_OF_MACROS (16)

/* Action word definition
Gui
| Alt
| | Shift
| | | Ctrl
| | | | Rapidfire (alpha only)
| | | | | Tapkey (mod only)
| | | | | | Lockable
| | | | | | | Toggle
0 0 0 0 0 0 0 0
*/
#define ACTION_NORMAL (0x00)
#define ACTION_TOGGLE (0x01)
#define ACTION_LOCKABLE (0x02)
#define ACTION_TAPKEY (0x04)
#define ACTION_RAPIDFIRE (0x08)
#define KEY_ACTION_MASK (0x0F)
#define MOD_ACTION_MASK (0xF0)

extern const uint16_t PROGMEM MACRO_BUFFER[MACRO_BUFFER_SIZE];
extern const uint8_t PROGMEM LAYERS[NUMBER_OF_LAYERS][NUMBER_OF_ROWS][NUMBER_OF_COLS];
extern const uint8_t PROGMEM ACTIONS[NUMBER_OF_LAYERS][NUMBER_OF_ROWS][NUMBER_OF_COLS];
extern const uint8_t PROGMEM TAPKEYS[NUMBER_OF_LAYERS][NUMBER_OF_ROWS][NUMBER_OF_COLS];
extern const uint8_t PROGMEM LED_LAYERS[LED_LAYERS_SIZE];

#endif /* CONFIG_KEYMAP_H_ */

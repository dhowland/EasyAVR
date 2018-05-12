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


#ifndef DEBUG_H_
#define DEBUG_H_

#include <stddef.h>
#include <stdint.h>

#include "scheduler.h"

#if defined(__AVR_AT90USB1286__) || (defined(__AVR_ATmega32U4__) && (defined(BOARD_SIZE_TKL) || defined(BOARD_SIZE_SIXTY) || defined(BOARD_SIZE_PAD)) && !defined(SIMPLE_DEVICE))
#define ENABLE_DEBUG_CONSOLE
#endif /* Debug targets */

#define EVENT_BUFFER_SIZE 16
#define MODE_UPDATE 0
#define MODE_REOCCUR 1
#define EVENT_CODE_DEBUG_RESET_STATUS 0x01
#define EVENT_CODE_DEBUG_FAULT_WORD 0x02
#define EVENT_CODE_SCHED_ADD 0x10
#define EVENT_CODE_SCHED_OVER 0x11
#define EVENT_CODE_SCHED_REM 0x12
#define EVENT_CODE_SCHED_FULL 0x13
#define EVENT_CODE_SCHED_OVER_CNT 0x14
#define EVENT_CODE_KEYMAP_BUF_FULL 0x40
#define EVENT_CODE_KEYMAP_DA_NOT_FOUND 0x41
#define EVENT_CODE_KEYMAP_FN_BUF_FULL 0x42
#define EVENT_CODE_KEYMAP_FN_NOT_FOUND 0x43
#define EVENT_CODE_KEYMAP_INVALID_CODE 0x44
#define EVENT_CODE_KEYMAP_LOST_CODE 0x45
#define EVENT_CODE_NVM_RELOAD_DEFAULTS 0x50
#define EVENT_CODE_NVM_ERASE_SETTINGS 0x51
#define EVENT_CODE_USB_CONNECT 0xA0
#define EVENT_CODE_USB_DISCONNECT 0xA1
#define EVENT_CODE_USB_RESET 0xA2
#define EVENT_CODE_USB_SUSPEND 0xA3
#define EVENT_CODE_USB_WAKEUP 0xA4
#define EVENT_CODE_USB_CONFIG_CHANGE 0xA5
#define EVENT_CODE_USB_STATE_CHANGE 0xA6

typedef enum {
	CONSOLE_IDLE,
	CONSOLE_MENU_MAIN,
	CONSOLE_PROCESS_MAIN,
	CONSOLE_MENU_DEBUG,
	CONSOLE_PROCESS_DEBUG,
	CONSOLE_MENU_CONFIG,
	CONSOLE_PROCESS_CONFIG,
	CONSOLE_PROMPT_CONFIG,
	CONSOLE_MENU_TIMING,
	CONSOLE_PROCESS_TIMING,
	CONSOLE_PROMPT_TIMING,
	CONSOLE_MENU_LED,
	CONSOLE_PROCESS_LED,
	CONSOLE_PROMPT_LED,
	CONSOLE_EVENTS1,
	CONSOLE_EVENTS2,
	CONSOLE_EVENTS3,
	CONSOLE_EXAMINE1,
	CONSOLE_EXAMINE2,
	CONSOLE_CLOCKS,
	CONSOLE_VNUMPAD,
	CONSOLE_VWINLOCK,
	CONSOLE_DEFAULTLAYER,
	CONSOLE_BOOTKEYBOARD,
	CONSOLE_VNUMLOCK,
	CONSOLE_DBSTYLE,
	CONSOLE_DEFAULTDIMMER,
	CONSOLE_DEFAULTBACKLIGHT,
	CONSOLE_DEFAULTBLMODE,
	CONSOLE_DEBOUNCE,
	CONSOLE_TAP,
	CONSOLE_DOUBLETAP,
	CONSOLE_MOUSEBASE,
	CONSOLE_MOUSEMULT,
	CONSOLE_HOLD,
	CONSOLE_REPEAT,
	CONSOLE_SETUP
} console_state_t;

typedef struct {
	uint8_t code;
	uint16_t status;
} event_buffer_t;

typedef enum {
	NO_RESET,
	RESET_REQUESTED,
	RESET_TO_BOOT
} reset_req_t;

extern volatile uint8_t g_reset_requested;

extern console_state_t g_console_state;

void init_debug(void);

void console_main(void);
void console_input(void);
void console_output(void);

void report_event(uint8_t code, uint16_t status, uint8_t mode);
void append_event(uint8_t code, uint16_t status);

void word_to_str(uint16_t w, char* dst);
void byte_to_str(uint8_t b, char* dst);
char nibble_to_char(uint8_t c);
void dec_to_string(uint16_t w, char* dst);
uint8_t sc_to_int(uint8_t sc);
uint16_t sc_to_word(uint8_t * buf, const size_t length, const uint8_t base);

#endif /* DEBUG_H_ */

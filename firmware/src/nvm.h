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


#ifndef NVM_H_
#define NVM_H_

#include <stddef.h>
#include <stdint.h>

#ifdef __AVR_ATmega16U2__
#define EEPROM_SIZE 512
#else
#define EEPROM_SIZE 1024
#endif

#define EEPROM_REV (0x21)

#define NUMBER_OF_NVM_PARAMETERS (18)
#define LENGTH_OF_NVM_PARAMETERS (21)

#define NVM_ID_WINLOCK_ON_SCROLLLOCK (1)
#define NVM_ID_SWAP_NUM_ROW_ON_NUMLOCK (2)
#define NVM_ID_DEFAULT_LAYER (3)
#define NVM_ID_INIT_DIMMER_LEVEL (4)
#define NVM_ID_BOOT_KEYBOARD_ONLY (5)
#define NVM_ID_DEBOUNCE_MS (6)
#define NVM_ID_VIRTUAL_NUMLOCK (7)
#define NVM_ID_INIT_BACKLIGHT_ENABLE (8)
#define NVM_ID_MAX_TAP_MS (9)
#define NVM_ID_DOUBLETAP_DELAY_MS (10)
#define NVM_ID_MOUSE_MIN_DELTA (11)
#define NVM_ID_MOUSE_DELTA_MULT (12)
#define NVM_ID_HOLD_KEY_MS (13)
#define NVM_ID_REPEAT_MS (14)
#define NVM_ID_MATRIX_SETUP_WAIT (15)
#define NVM_ID_DEBOUNCE_STYLE (16)
#define NVM_ID_INIT_BACKLIGHT_MODE (17)

typedef struct {
	const void * var;
	const uint8_t index;
	const uint8_t bytes;
} nvm_map_t;

typedef union {
	int16_t word;
	uint8_t bytes[2];
} nvm_int16_t;

extern uint8_t g_winlock_on_scrolllock;
extern uint8_t g_swap_num_row_on_numlock;
extern uint8_t g_default_layer;
extern uint8_t g_init_dimmer_level;
extern uint8_t g_boot_keyboard_only;
extern uint8_t g_debounce_ms;
extern uint8_t g_virtual_numlock;
extern uint8_t g_init_backlight_enable;
extern int16_t g_max_tap_ms;
extern int16_t g_doubletap_delay_ms;
extern uint8_t g_mouse_min_delta;
extern uint8_t g_mouse_delta_mult;
extern int16_t g_hold_key_ms;
extern uint8_t g_repeat_ms;
extern uint8_t g_matrix_setup_wait;
extern uint8_t g_debounce_style;
extern uint8_t g_init_backlight_mode;

void init_nvm(void);
void nvm_init_eeprom(void);
void nvm_update_param(const uint8_t id);

#endif /* NVM_H_ */

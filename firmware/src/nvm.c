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

#include <stddef.h>
#include <stdint.h>
#include <avr/pgmspace.h>
#include <avr/eeprom.h>

#include "debug.h"
#include "scheduler.h"
#include "matrix.h"
#include "mouse.h"
#include "led.h"
#include "keymap.h"
#include "nvm.h"

uint8_t g_eeprom_rev;
uint8_t g_winlock_on_scrolllock;
uint8_t g_swap_num_row_on_numlock;
uint8_t g_default_layer;
uint8_t g_init_dimmer_level;
uint8_t g_boot_keyboard_only;
uint8_t g_debounce_ms;
uint8_t g_virtual_numlock;
uint8_t g_init_backlight_enable;
int16_t g_max_tap_ms;
int16_t g_doubletap_delay_ms;
uint8_t g_mouse_min_delta;
uint8_t g_mouse_delta_mult;
int16_t g_hold_key_ms;
uint8_t g_repeat_ms;
uint8_t g_matrix_setup_wait;
uint8_t g_debounce_style;
uint8_t g_init_backlight_mode;

#ifndef SIMPLE_DEVICE

uint8_t EEMEM NVM_EEPROM[EEPROM_SIZE];

const nvm_map_t PROGMEM NVM_MAP[NUMBER_OF_NVM_PARAMETERS] = {
	{&g_eeprom_rev, 0, 1},
	{&g_winlock_on_scrolllock, 1, 1},
	{&g_swap_num_row_on_numlock, 2, 1},
	{&g_default_layer, 3, 1},
	{&g_init_dimmer_level, 4, 1},
	{&g_boot_keyboard_only, 5, 1},
	{&g_debounce_ms, 6, 1},
	{&g_virtual_numlock, 7, 1},
	{&g_init_backlight_enable, 8, 1},
	{&g_max_tap_ms, 9, 2},
	{&g_doubletap_delay_ms, 11, 2},
	{&g_mouse_min_delta, 13, 1},
	{&g_mouse_delta_mult, 14, 1},
	{&g_hold_key_ms, 15, 2},
	{&g_repeat_ms, 17, 1},
	{&g_matrix_setup_wait, 18, 1},
	{&g_debounce_style, 19, 1},
	{&g_init_backlight_mode, 20, 1},
};


void init_nvm(void)
{
	int8_t i;
	uint8_t * byte_ptr;
	int16_t * word_ptr;
	uint8_t nvm_index;
	uint8_t nvm_bytes;
	
	for (i = 0; i<NUMBER_OF_NVM_PARAMETERS; i++)
	{
		nvm_index = pgm_read_byte(&NVM_MAP[i].index);
		nvm_bytes = pgm_read_byte(&NVM_MAP[i].bytes);
		if (nvm_bytes == 2)
		{
			word_ptr = (int16_t*)pgm_read_word(&NVM_MAP[i].var);
			*word_ptr = eeprom_read_word((uint16_t*)&NVM_EEPROM[nvm_index]);
		} else {
			byte_ptr = (uint8_t*)pgm_read_word(&NVM_MAP[i].var);
			*byte_ptr = eeprom_read_byte(&NVM_EEPROM[nvm_index]);
		}
	}
	if (g_eeprom_rev != EEPROM_REV)
	{
		report_event(EVENT_CODE_NVM_RELOAD_DEFAULTS, g_eeprom_rev, MODE_REOCCUR);
		nvm_init_eeprom();
	}
}

void nvm_init_eeprom(void)
{
	uint8_t update_array[LENGTH_OF_NVM_PARAMETERS];
	nvm_int16_t trans;
	
	/* default values */
	g_eeprom_rev = EEPROM_REV;
	g_winlock_on_scrolllock = 0;
	g_swap_num_row_on_numlock = 0;
	g_default_layer = 0;
	g_init_dimmer_level = NUMBER_OF_BACKLIGHT_LEVELS;
	g_boot_keyboard_only = 0;
	g_debounce_ms = DEFAULT_DEBOUNCE_MS;
	g_virtual_numlock = 0;
	g_init_backlight_enable = 0;
	g_max_tap_ms = DEFAULT_TAP_MAX_MS;
	g_doubletap_delay_ms = DEFAULT_DOUBLETAP_DELAY_MS;
	g_mouse_min_delta = DEFAULT_MOUSE_MIN_DELTA;
	g_mouse_delta_mult = DEFAULT_MOUSE_DELTA_MULT;
	g_hold_key_ms = DEFAULT_HOLD_KEY_MS;
	g_repeat_ms = DEFAULT_REPEAT_MS;
	g_matrix_setup_wait = DEFAULT_MATRIX_SETUP_WAIT;
	g_debounce_style = 0;
	g_init_backlight_mode = 0;
	
	update_array[0] = g_eeprom_rev;
	update_array[1] = g_winlock_on_scrolllock;
	update_array[2] = g_swap_num_row_on_numlock;
	update_array[3] = g_default_layer;
	update_array[4] = g_init_dimmer_level;
	update_array[5] = g_boot_keyboard_only;
	update_array[6] = g_debounce_ms;
	update_array[7] = g_virtual_numlock;
	update_array[8] = g_init_backlight_enable;
	trans.word = g_max_tap_ms;
	update_array[9] = trans.bytes[0];
	update_array[10] = trans.bytes[1];
	trans.word = g_doubletap_delay_ms;
	update_array[11] = trans.bytes[0];
	update_array[12] = trans.bytes[1];
	update_array[13] = g_mouse_min_delta;
	update_array[14] = g_mouse_delta_mult;
	trans.word = g_hold_key_ms;
	update_array[15] = trans.bytes[0];
	update_array[16] = trans.bytes[1];
	update_array[17] = g_repeat_ms;
	update_array[18] = g_matrix_setup_wait;
	update_array[19] = g_debounce_style;
	update_array[20] = g_init_backlight_mode;
	
	eeprom_write_block(update_array, NVM_EEPROM, sizeof(update_array));
}

void nvm_update_param(const uint8_t id)
{
	uint8_t * byte_ptr;
	int16_t * word_ptr;
	uint8_t nvm_index;
	uint8_t nvm_bytes;
	
	
	nvm_index = pgm_read_byte(&NVM_MAP[id].index);
	nvm_bytes = pgm_read_byte(&NVM_MAP[id].bytes);
	if (nvm_bytes == 2)
	{
		word_ptr = (int16_t*)pgm_read_word(&NVM_MAP[id].var);
		eeprom_write_word((uint16_t*)&NVM_EEPROM[nvm_index], *word_ptr);
	} else {
		byte_ptr = (uint8_t*)pgm_read_word(&NVM_MAP[id].var);
		eeprom_write_byte(&NVM_EEPROM[nvm_index], *byte_ptr);
	}
}

#else

void init_nvm(void)
{
	g_eeprom_rev = EEPROM_REV;
	g_winlock_on_scrolllock = 0;
	g_swap_num_row_on_numlock = 0;
	g_default_layer = 0;
	g_init_dimmer_level = NUMBER_OF_BACKLIGHT_LEVELS;
	g_boot_keyboard_only = 0;
	g_debounce_ms = DEFAULT_DEBOUNCE_MS;
	g_virtual_numlock = 0;
	g_init_backlight_enable = 0;
	g_max_tap_ms = DEFAULT_TAP_MAX_MS;
	g_doubletap_delay_ms = DEFAULT_DOUBLETAP_DELAY_MS;
	g_mouse_min_delta = DEFAULT_MOUSE_MIN_DELTA;
	g_mouse_delta_mult = DEFAULT_MOUSE_DELTA_MULT;
	g_hold_key_ms = DEFAULT_HOLD_KEY_MS;
	g_repeat_ms = DEFAULT_REPEAT_MS;
	g_matrix_setup_wait = DEFAULT_MATRIX_SETUP_WAIT;
	g_debounce_style = 0;
	g_init_backlight_mode = 0;
}

#endif /* SIMPLE_DEVICE */

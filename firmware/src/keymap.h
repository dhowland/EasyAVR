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


#ifndef KEYMAP_H_
#define KEYMAP_H_

#include <stddef.h>
#include <stdint.h>

#include "config_keymap.h"

/* MUST be 6 */
#define HID_ROLLOVER_SIZE (6)

#if defined (BOARD_SIZE_COSTAR) && defined (__AVR_ATmega32U2__)
#define KEYMAP_MEMORY_SAVE
#endif /* ATmega32U2 boards with 8x18 matrix */

typedef struct {
	const uint8_t scancode;
	const uint8_t mask;
} mod_map_t;

typedef struct {
	const uint8_t numcode;
	const uint8_t navcode;
} kp_map_t;

typedef enum {
	SC_CLASS_FN,
	SC_CLASS_MOD,
	SC_CLASS_MACRO,
	SC_CLASS_MOUSE,
	SC_CLASS_MEDIA,
	SC_CLASS_SPEC,
	SC_CLASS_NORM,
	SC_CLASS_NULL
} sc_class_t;

extern uint8_t g_modifier_state;
extern uint8_t g_report_buffer[HID_ROLLOVER_SIZE+1];
extern uint8_t g_modifier_service;
extern uint8_t g_alphanum_service;
extern uint8_t g_media_service;
extern uint8_t g_power_service;
extern uint8_t g_mousebutton_state;
extern int8_t g_mouse_req_X;
extern int8_t g_mouse_req_Y;
extern uint16_t g_media_key;
extern uint8_t g_powermgmt_field;
extern uint8_t g_hid_lock_flags;
extern uint8_t g_winlock_flag;
#if MACRO_RAM_SIZE
extern uint16_t g_ram_macro[MACRO_RAM_SIZE];
int8_t g_ram_macro_ptr;
int8_t g_ram_macro_length;
#endif /* MACRO_RAM_SIZE */

void enqueue_key(const uint8_t code);
void delete_key(const uint8_t code);
void toggle_key(const uint8_t code);
void enqueue_fn(const uint8_t code);
void delete_fn(const uint8_t code);
void set_media(const uint8_t code);
void unset_media(const uint8_t code);
void set_power(const uint8_t code);
void unset_power(const uint8_t code);
void init_keymap(void);
void doubletap_down(const uint8_t row, const uint8_t col, const int16_t idle_time);
void doubletap_up(const uint8_t row, const uint8_t col, const int16_t hold_time, uint8_t * const tap);
void record_stroke(const uint8_t code);
void play_macro(const uint8_t code);
void led_fn_activate(const uint8_t bit);
void led_fn_deactivate(const uint8_t bit);
void fn_down(const uint8_t code, const uint8_t action);
void fn_up(const uint8_t code, const uint8_t action, const uint8_t tapkey, const uint8_t tap);
void mod_down(const uint8_t code, const uint8_t action);
void mod_up(const uint8_t code, const uint8_t action, const uint8_t tapkey, const uint8_t tap);
void alpha_down(const uint8_t code, const uint8_t action);
void alpha_up(const uint8_t code, const uint8_t action, const uint8_t tapkey, const uint8_t tap);
void handle_code_actuate(const uint8_t code, const uint8_t action, const uint8_t tapkey);
void handle_code_deactuate(const uint8_t code, const uint8_t action, const uint8_t tapkey, const uint8_t tap);
uint8_t translate_code(uint8_t code);
void keymap_actuate(const uint8_t row, const uint8_t col, const int16_t hold_time);
void keymap_deactuate(const uint8_t row, const uint8_t col, const int16_t hold_time);
void keymap_interrupt(const uint8_t row, const uint8_t col);
void get_keyboard_report(uint8_t * const buffer);
void get_nkro_report(uint8_t * const buffer);
void get_modifier_report(uint8_t * const buffer);
void initial_actuate(const uint8_t row, const uint8_t col);

#endif /* KEYMAP_H_ */
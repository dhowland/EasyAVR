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
#include <avr/io.h>

#include <LUFA/Drivers/USB/USB.h>

#include "keymap.h"
#include "autokey.h"
#include "led.h"
#include "nvm.h"
#include "scheduler.h"
#include "debug.h"

volatile uint8_t g_reset_requested;

console_state_t g_console_state;

#ifdef ENABLE_DEBUG_CONSOLE
const char PROGMEM g_main_menu[] = "\nMain Menu:\n1) Config menu\n2) Timing menu\n3) Debug menu\n4) Reset\n9) Quit\n> ";
const char PROGMEM g_debug_menu[] = "\nDebug Menu:\n1) Print events\n2) Clear events\n3) Examine memory\n"
									"4) Print/clear clock-ins\n9) Back\n> ";
#else /* ENABLE_DEBUG_CONSOLE */
const char PROGMEM g_main_menu[] = "\nMain Menu:\n1) Config menu\n2) Timing menu\n4) Reset\n9) Quit\n> ";
#endif /* ENABLE_DEBUG_CONSOLE */
const char PROGMEM g_config_menu[] = "\nConfig Menu:\n1) Toggle virtual num pad\n2) Toggle win lock on scroll lock\n"
									 "3) Set default layer\n4) Toggle basic keyboard\n"
									 "5) Toggle unlink num lock\n6) Set default dimmer level\n"
									 "7) Set default backlight enable\n9) Back\n> ";
const char PROGMEM g_timing_menu[] = "\nTiming Menu:\n1) Set debounce time\n2) Set max hold time for tap\n"
									 "3) Set max delay time for double tap\n4) Set base mouse movement\n"
									 "5) Set mouse movement multiplier\n6) Set min hold time for repeat\n"
									 "7) Set repeat period\n8) Set matrix setup wait\n9) Back\n> ";
const char PROGMEM g_not_rec[] = "Input not recognized.\n";
const char PROGMEM g_vnumpad_yes[] = "Number row will be swapped for numpad keys when num lock is enabled.\n";
const char PROGMEM g_vnumpad_no[] = "Num lock will not affect number row.\n";
const char PROGMEM g_vwinlock_yes[] = "Windows key will be disabled when scroll lock is enabled.\n";
const char PROGMEM g_vwinlock_no[] = "Scroll lock will not affect win lock.\n";
const char PROGMEM g_bootkeyboard_full[] = "Keyboard is limited to standard 6KRO boot-compatible keyboard.\n";
const char PROGMEM g_bootkeyboard_half[] = "Keyboard acts as 6KRO keyboard plus mouse and media keys.\n";
const char PROGMEM g_bootkeyboard_none[] = "Keyboard acts as extended NKRO keyboard with mouse and media keys.\n";
const char PROGMEM g_vnumlock_yes[] = "Num lock will function independently of the system num lock.\n";
const char PROGMEM g_vnumlock_no[] = "Num lock is linked to the system num lock.\n";
const char PROGMEM g_event_print_1[] = "\n[";
const char PROGMEM g_event_print_2[] = "] C-0x";
const char PROGMEM g_event_print_3[] = " S-0x";
const char PROGMEM g_exam_prompt1[] = "Address (hex)> ";
const char PROGMEM g_exam_prompt2[] = "Bytes (hex)> ";
const char PROGMEM g_deflayer_prompt[] = "Enter new default layer (0-9)> ";
const char PROGMEM g_set_print[] = "Set:";
const char PROGMEM g_debounce_prompt[] = "Enter new debounce time in ms (1-99)> ";
const char PROGMEM g_tap_prompt[] = "Enter new tap time in ms (1-999)> ";
const char PROGMEM g_doubletap_prompt[] = "Enter new doubletap delay time in ms (1-999)> ";
const char PROGMEM g_mouse_base_prompt[] = "Enter new base mouse movement (1-99)> ";
const char PROGMEM g_mouse_mult_prompt[] = "Enter new mouse movement multiplier (1-99)> ";
const char PROGMEM g_hold_prompt[] = "Enter new hold time in ms (1-999)> ";
const char PROGMEM g_repeat_prompt[] = "Enter new repeat time in ms (1-99)> ";
const char PROGMEM g_setup_prompt[] = "Enter new matrix setup wait in cycles (1-255)> ";
const char PROGMEM g_defbl_prompt[] = "Enter new default backlight enable (1-" STR_MAX_BACKLIGHT_ENABLES ")> ";
const char PROGMEM g_defdim_prompt[] = "Enter new default dimmer level (1-16)> ";
const char PROGMEM g_out_of_range[] = "Out of range.\n";

#ifdef ENABLE_DEBUG_CONSOLE
uint8_t g_event_index;
event_buffer_t g_event_buffer[EVENT_BUFFER_SIZE];
uint8_t g_event_buffer_count;
uint8_t* g_ex_ptr;
uint8_t* g_ex_end;
#endif /* ENABLE_DEBUG_CONSOLE */

void init_debug(void)
{
	
}

void console_main(void)
{
	int8_t i;
	uint16_t word;
	uint8_t code;
	char word_print[4];
	
	if (g_autokey_status == AUTOKEY_IDLE)
	{
		switch (g_console_state)
		{
		case CONSOLE_IDLE:
			break;
		case CONSOLE_MENU_MAIN:
			queue_autotext(g_main_menu);
			begin_read();
			g_console_state = CONSOLE_PROCESS_MAIN;
			break;
		case CONSOLE_PROCESS_MAIN:
			g_console_state = CONSOLE_MENU_MAIN;
			code = sc_to_int(g_read_buffer[0]);
			if (code == 9)
			{
				g_console_state = CONSOLE_IDLE;
			}
			else if (code == 4)
			{
				g_reset_requested = RESET_REQUESTED;
			}
			else if (code == 1)
			{
				g_console_state = CONSOLE_MENU_CONFIG;
			}
			else if (code == 2)
			{
				g_console_state = CONSOLE_MENU_TIMING;
			}
#ifdef ENABLE_DEBUG_CONSOLE
			else if (code == 3)
			{
				g_console_state = CONSOLE_MENU_DEBUG;
			}
#endif /* ENABLE_DEBUG_CONSOLE */
			else
			{
				queue_autotext(g_not_rec);
			}
			break;
		case CONSOLE_MENU_CONFIG:
			queue_autotext(g_config_menu);
			begin_read();
			g_console_state = CONSOLE_PROCESS_CONFIG;
			break;
		case CONSOLE_PROCESS_CONFIG:
			g_console_state = CONSOLE_MENU_CONFIG;
			code = sc_to_int(g_read_buffer[0]);
			if (code == 9)
			{
				g_console_state = CONSOLE_MENU_MAIN;
			}
			else if (code == 1)
			{
				g_swap_num_row_on_numlock ^= 1;
				nvm_update_param(NVM_ID_SWAP_NUM_ROW_ON_NUMLOCK);
				if (g_swap_num_row_on_numlock)
					queue_autotext(g_vnumpad_yes);
				else
					queue_autotext(g_vnumpad_no);
			}
			else if (code == 2)
			{
				g_winlock_on_scrolllock ^= 1;
				nvm_update_param(NVM_ID_WINLOCK_ON_SCROLLLOCK);
				if (g_winlock_on_scrolllock)
					queue_autotext(g_vwinlock_yes);
				else
					queue_autotext(g_vwinlock_no);
			}
			else if (code == 3)
			{
				queue_autotext(g_set_print);
				byte_to_str(g_default_layer, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
				queue_autotext(g_deflayer_prompt);
				begin_read();
				g_console_state = CONSOLE_DEFAULTLAYER;
			}
			else if (code == 4)
			{
				if (g_boot_keyboard_only == KB_TYPE_NKRO_PLUS)
				{
					g_boot_keyboard_only = KB_TYPE_6KRO_PLUS;
					nvm_update_param(NVM_ID_BOOT_KEYBOARD_ONLY);
					queue_autotext(g_bootkeyboard_half);
				}
				else if (g_boot_keyboard_only == KB_TYPE_6KRO_PLUS)
				{
					g_boot_keyboard_only = KB_TYPE_6KRO_ONLY;
					nvm_update_param(NVM_ID_BOOT_KEYBOARD_ONLY);
					queue_autotext(g_bootkeyboard_full);
				}
				else
				{
					g_boot_keyboard_only = KB_TYPE_NKRO_PLUS;
					nvm_update_param(NVM_ID_BOOT_KEYBOARD_ONLY);
					queue_autotext(g_bootkeyboard_none);
				}
			}
			else if (code == 5)
			{
				g_virtual_numlock ^= 1;
				nvm_update_param(NVM_ID_VIRTUAL_NUMLOCK);
				if (g_virtual_numlock)
					queue_autotext(g_vnumlock_yes);
				else
					queue_autotext(g_vnumlock_no);
			}
			else if (code == 6)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_init_dimmer_level, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
				queue_autotext(g_defdim_prompt);
				begin_read();
				g_console_state = CONSOLE_DEFAULTDIMMER;
			}
			else if (code == 7)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_init_backlight_mode+1, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
				queue_autotext(g_defbl_prompt);
				begin_read();
				g_console_state = CONSOLE_DEAFAULTBACKLIGHT;
			}
			else
			{
				queue_autotext(g_not_rec);
			}
			break;
		case CONSOLE_MENU_TIMING:
			queue_autotext(g_timing_menu);
			begin_read();
			g_console_state = CONSOLE_PROCESS_TIMING;
			break;
		case CONSOLE_PROCESS_TIMING:
			g_console_state = CONSOLE_MENU_TIMING;
			code = sc_to_int(g_read_buffer[0]);
			if (code == 9)
			{
				g_console_state = CONSOLE_MENU_MAIN;
			}
			else if (code == 1)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_debounce_ms, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
				queue_autotext(g_debounce_prompt);
				begin_read();
				g_console_state = CONSOLE_DEBOUNCE;
			}
			else if (code == 2)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_max_tap_ms, word_print);
				word_print[3] = '\n';
				queue_ram_autotext(word_print, 4);
				queue_autotext(g_tap_prompt);
				begin_read();
				g_console_state = CONSOLE_TAP;
			}
			else if (code == 3)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_doubletap_delay_ms*(-1), word_print);
				word_print[3] = '\n';
				queue_ram_autotext(word_print, 4);
				queue_autotext(g_doubletap_prompt);
				begin_read();
				g_console_state = CONSOLE_DOUBLETAP;
			}
			else if (code == 4)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_mouse_min_delta, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
				queue_autotext(g_mouse_base_prompt);
				begin_read();
				g_console_state = CONSOLE_MOUSEBASE;
			}
			else if (code == 5)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_mouse_delta_mult, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
				queue_autotext(g_mouse_mult_prompt);
				begin_read();
				g_console_state = CONSOLE_MOUSEMULT;
			}
			else if (code == 6)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_hold_key_ms, word_print);
				word_print[3] = '\n';
				queue_ram_autotext(word_print, 4);
				queue_autotext(g_hold_prompt);
				begin_read();
				g_console_state = CONSOLE_HOLD;
			}
			else if (code == 7)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_repeat_ms, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
				queue_autotext(g_repeat_prompt);
				begin_read();
				g_console_state = CONSOLE_REPEAT;
			}
			else if (code == 8)
			{
				queue_autotext(g_set_print);
				dec_to_string(g_matrix_setup_wait, word_print);
				word_print[3] = '\n';
				queue_ram_autotext(word_print, 4);
				queue_autotext(g_setup_prompt);
				begin_read();
				g_console_state = CONSOLE_SETUP;
			}
			break;
#ifdef ENABLE_DEBUG_CONSOLE
		case CONSOLE_MENU_DEBUG:
			queue_autotext(g_debug_menu);
			begin_read();
			g_console_state = CONSOLE_PROCESS_DEBUG;
			break;
		case CONSOLE_PROCESS_DEBUG:
			g_console_state = CONSOLE_MENU_DEBUG;
			code = sc_to_int(g_read_buffer[0]);
			if (code == 9)
			{
				g_console_state = CONSOLE_MENU_MAIN;
			}
			else if (code == 1)
			{
				g_console_state = CONSOLE_EVENTS1;
			}
			else if (code == 2)
			{
				for (i=0; i<EVENT_BUFFER_SIZE; i++)
				{
					g_event_buffer[i].code = 0;
					g_event_buffer[i].status = 0;
				}
				g_event_buffer_count = 0;
			}
			else if (code == 3)
			{
				queue_autotext(g_exam_prompt1);
				begin_read();
				g_console_state = CONSOLE_EXAMINE1;
			}
			else if (code == 4)
			{
				g_console_state = CONSOLE_CLOCKS;
			}
			else
			{
				queue_autotext(g_not_rec);
			}
			break;
		case CONSOLE_EVENTS1:
			if (g_event_index >= EVENT_BUFFER_SIZE)
			{
				g_event_index = 0;
				word_print[0] = '\n';
				queue_ram_autotext(word_print, 1);
				g_console_state = CONSOLE_MENU_DEBUG;
			} else {
				queue_autotext(g_event_print_1);
				byte_to_str(g_event_index, word_print);
				queue_ram_autotext(word_print, 2);
				queue_autotext(g_event_print_2);
				g_console_state = CONSOLE_EVENTS2;
			}
			break;
		case CONSOLE_EVENTS2:
			byte_to_str(g_event_buffer[g_event_index].code, word_print);
			queue_ram_autotext(word_print, 2);
			queue_autotext(g_event_print_3);
			g_console_state = CONSOLE_EVENTS3;
			break;
		case CONSOLE_EVENTS3:
			word_to_str(g_event_buffer[g_event_index].status, word_print);
			queue_ram_autotext(word_print, sizeof(word_print));
			g_console_state = CONSOLE_EVENTS1;
			g_event_index++;
			break;
		case CONSOLE_EXAMINE1:
			g_ex_ptr = (uint8_t *)sc_to_word(g_read_buffer, g_read_buffer_length, 16);
			g_ex_end = 0;
			queue_autotext(g_exam_prompt2);
			begin_read();
			g_console_state = CONSOLE_EXAMINE2;
			break;
		case CONSOLE_EXAMINE2:
			if (!g_ex_end)
				g_ex_end = g_ex_ptr + sc_to_word(g_read_buffer, g_read_buffer_length, 16);
			while(g_ex_ptr < g_ex_end)
			{
				byte_to_str(*g_ex_ptr, word_print);
				if (g_ex_ptr == (g_ex_end-1))
					word_print[2] = '\n';
				else
					word_print[2] = ' ';
				if ( queue_ram_autotext(word_print, 3) )
					g_ex_ptr++;
				else
					break;
			}
			if (g_ex_ptr >= g_ex_end)
				g_console_state = CONSOLE_MENU_DEBUG;
			break;
		case CONSOLE_CLOCKS:
			/* lots of variable name reuse here (g_event_index and code) */
			if (g_event_index >= (NUMBER_OF_SCHEDULE_SLOTS*NUMBER_OF_ITEMS_PER_SLOT))
			{
				g_event_index = 0;
				word_print[0] = '\n';
				queue_ram_autotext(word_print, 1);
				g_console_state = CONSOLE_MENU_DEBUG;
				reset_max_clocks();
			} else {
				i = g_event_index % NUMBER_OF_SCHEDULE_SLOTS;
				code = g_event_index / NUMBER_OF_SCHEDULE_SLOTS;
				if (i == 0)
					word_print[0] = '\n';
				else
					word_print[0] = ' ';
				queue_ram_autotext(word_print, 1);
				word_to_str(g_schedule_clocks[i][code], word_print);
				queue_ram_autotext(word_print, sizeof(word_print));
				g_event_index++;
			}
			break;
#endif /* ENABLE_DEBUG_CONSOLE */
		case CONSOLE_DEFAULTLAYER:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if (word < NUMBER_OF_LAYERS)
			{
				g_default_layer = (uint8_t)(word & 0x00FF);
				nvm_update_param(NVM_ID_DEFAULT_LAYER);
				queue_autotext(g_set_print);
				byte_to_str(g_default_layer, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
		case CONSOLE_DEBOUNCE:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word < 100) && (word > 0))
			{
				g_debounce_ms = (int8_t)(word & 0x00FF);
				nvm_update_param(NVM_ID_DEBOUNCE_MS);
				queue_autotext(g_set_print);
				dec_to_string(g_debounce_ms, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_TAP:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word < 1000) && (word > 0))
			{
				g_max_tap_ms = word;
				nvm_update_param(NVM_ID_MAX_TAP_MS);
				queue_autotext(g_set_print);
				dec_to_string(g_max_tap_ms, word_print);
				word_print[3] = '\n';
				queue_ram_autotext(word_print, 4);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_DOUBLETAP:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word < 1000) && (word > 0))
			{
				g_doubletap_delay_ms = word*(-1);
				nvm_update_param(NVM_ID_DOUBLETAP_DELAY_MS);
				queue_autotext(g_set_print);
				dec_to_string(g_doubletap_delay_ms*(-1), word_print);
				word_print[3] = '\n';
				queue_ram_autotext(word_print, 4);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_MOUSEBASE:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word < 100) && (word > 0))
			{
				g_mouse_min_delta = (int8_t)(word & 0x00FF);
				nvm_update_param(NVM_ID_MOUSE_MIN_DELTA);
				queue_autotext(g_set_print);
				dec_to_string(g_mouse_min_delta, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_MOUSEMULT:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word < 100) && (word > 0))
			{
				g_mouse_delta_mult = (int8_t)(word & 0x00FF);
				nvm_update_param(NVM_ID_MOUSE_DELTA_MULT);
				queue_autotext(g_set_print);
				dec_to_string(g_mouse_delta_mult, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_HOLD:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word < 1000) && (word > 0))
			{
				g_hold_key_ms = word;
				nvm_update_param(NVM_ID_HOLD_KEY_MS);
				queue_autotext(g_set_print);
				dec_to_string(g_hold_key_ms, word_print);
				word_print[3] = '\n';
				queue_ram_autotext(word_print, 4);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_REPEAT:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word < 100) && (word > 0))
			{
				g_repeat_ms = (int8_t)(word & 0x00FF);
				nvm_update_param(NVM_ID_REPEAT_MS);
				queue_autotext(g_set_print);
				dec_to_string(g_repeat_ms, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_SETUP:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word <= 255) && (word > 0))
			{
				g_matrix_setup_wait = (int8_t)(word & 0x00FF);
				nvm_update_param(NVM_ID_MATRIX_SETUP_WAIT);
				queue_autotext(g_set_print);
				dec_to_string(g_matrix_setup_wait, word_print);
				word_print[3] = '\n';
				queue_ram_autotext(word_print, 4);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_DEFAULTDIMMER:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word <= NUMBER_OF_BACKLIGHT_LEVELS) && (word > 0))
			{
				g_init_dimmer_level = (int8_t)(word & 0x00FF);
				nvm_update_param(NVM_ID_INIT_DIMMER_LEVEL);
				queue_autotext(g_set_print);
				dec_to_string(g_init_dimmer_level, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
		case CONSOLE_DEAFAULTBACKLIGHT:
			word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((word <= MAX_BACKLIGHT_ENABLES) && (word > 0))
			{
				i = (int8_t)(word & 0x00FF);
				g_init_backlight_mode = i - 1;
				nvm_update_param(NVM_ID_INIT_BACKLIGHT_MODE);
				queue_autotext(g_set_print);
				dec_to_string(g_init_backlight_mode+1, word_print);
				word_print[2] = '\n';
				queue_ram_autotext(word_print, 3);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
		default:
			g_console_state = CONSOLE_IDLE;
		}
	}
}

void report_event(uint8_t code, uint16_t status, uint8_t mode)
{
#ifdef ENABLE_DEBUG_CONSOLE
	int8_t i;
	
	if (mode == MODE_UPDATE)
	{
		for (i=0; i<g_event_buffer_count; i++)
		{
			if (g_event_buffer[i].code == code)
			{
				g_event_buffer[i].status = status;
				break;
			}
		}
		if (i >= g_event_buffer_count)
		{
			append_event(code, status);
		}
	} else {
		append_event(code, status);
	}
}

void append_event(uint8_t code, uint16_t status)
{
	if (g_event_buffer_count < EVENT_BUFFER_SIZE)
	{
		g_event_buffer[g_event_buffer_count].code = code;
		g_event_buffer[g_event_buffer_count].status = status;
		g_event_buffer_count++;
	}
#endif /* ENABLE_DEBUG_CONSOLE */
}

void word_to_str(uint16_t w, char* dst)
{
	byte_to_str((uint8_t)((w & 0xFF00) >> 8), dst);
	byte_to_str((uint8_t)(w & 0x00FF), dst+2);
}

void byte_to_str(uint8_t b, char* dst)
{
	dst[0] = nibble_to_char((b & 0xF0) >> 4);
	dst[1] = nibble_to_char(b & 0x0F);
}

char nibble_to_char(uint8_t c)
{
	return (c<10) ? (c+'0') : (c+('A'-10)) ;
}

/* Left-aligns, always fills in 3 characters, max input is 999 */
void dec_to_string(uint16_t w, char* dst)
{
	int8_t i = 0;
	uint8_t d = 100;
	
	dst[0] = '0';
	dst[1] = ' ';
	dst[2] = ' ';
	
	while (d > 0)
	{
		if (i || (w >= d))
		{
			dst[i] = nibble_to_char(w / d);
			w = w % d;
			i++;
		}
		d = d / 10;
	}
}

uint8_t sc_to_int(uint8_t sc)
{
	if ( (sc >= HID_KEYBOARD_SC_KEYPAD_1_AND_END ) &&
		 (sc <= HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP) )
	{
		return (sc - 0x58);
	}
	else if ( (sc >= HID_KEYBOARD_SC_1_AND_EXCLAMATION ) &&
			  (sc <= HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS) )
	{
		return (sc - 0x1D);
	}
	else if ( (sc >= HID_KEYBOARD_SC_A ) &&
			  (sc <= HID_KEYBOARD_SC_F ) )
	{
		return (sc + 0x06);
	}
	else
	{
		return 0;
	}
}

uint16_t sc_to_word(uint8_t * buf, const size_t length, const uint8_t base)
{
	int8_t i;
	uint16_t val=0;
	
	for (i=0; i<length; i++)
	{
		val = (val * base) + sc_to_int(buf[i]);
	}
	return val;
}

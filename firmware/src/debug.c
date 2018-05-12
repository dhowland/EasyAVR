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
int8_t g_console_index;

#ifdef ENABLE_DEBUG_CONSOLE
const char PROGMEM g_main_menu[] = "\nMain Menu:\n1) Config menu\n2) Timing menu\n3) LED menu\n4) Debug menu\n5) Reset\n9) Quit\n> ";
const char PROGMEM g_debug_menu[] = "\nDebug Menu:\n1) Print events\n2) Clear events\n3) Examine memory\n"
									"4) Print/clear clock-ins\n9) Back\n> ";
#else /* ENABLE_DEBUG_CONSOLE */
const char PROGMEM g_main_menu[] = "\nMain Menu:\n1) Config menu\n2) Timing menu\n3) LED menu\n5) Reset\n9) Quit\n> ";
#endif /* ENABLE_DEBUG_CONSOLE */
const char PROGMEM g_config_menu_begin[] = "\nConfig Menu:";
const char PROGMEM g_timing_menu_begin[] = "\nTiming Menu:";
const char PROGMEM g_led_menu_begin[] = "\nLED Menu:";
const char PROGMEM g_menu_1[] = "\n1) ";
const char PROGMEM g_menu_2[] = "\n2) ";
const char PROGMEM g_menu_3[] = "\n3) ";
const char PROGMEM g_menu_4[] = "\n4) ";
const char PROGMEM g_menu_5[] = "\n5) ";
const char PROGMEM g_menu_6[] = "\n6) ";
const char PROGMEM g_menu_7[] = "\n7) ";
const char PROGMEM g_menu_8[] = "\n8) ";
const char PROGMEM g_menu_end[] = "\n9) Back\n> ";

const char PROGMEM g_vnumpad_desc[] = "Virtual Num Pad";
const char PROGMEM g_vwinlock_desc[] = "Win Lock on Scroll Lock";
const char PROGMEM g_deflayer_desc[] = "Default Layer";
const char PROGMEM g_bootkb_desc[] = "Boot Keyboard";
const char PROGMEM g_vnumlock_desc[] = "Unlinked Num Lock";
const char PROGMEM g_dbstyle_desc[] = "Alternate Debounce Style";
const char PROGMEM g_debounce_desc[] = "Debounce Time (ms)";
const char PROGMEM g_tap_desc[] = "Max Hold Time for Tap (ms)";
const char PROGMEM g_doubletap_desc[] = "Max Delay Time for Double Tap (ms)";
const char PROGMEM g_mousebase_desc[] = "Base Mouse Movement";
const char PROGMEM g_mousemult_desc[] = "Mouse Movement Multiplier";
const char PROGMEM g_hold_desc[] = "Min Hold Time for Repeat (ms)";
const char PROGMEM g_repeat_desc[] = "Repeat Period (ms)";
const char PROGMEM g_setup_desc[] = "Matrix Setup Wait (cycles)";
const char PROGMEM g_defdim_desc[] = "Default Dimmer Level";
#ifdef MAX_NUMBER_OF_BACKLIGHTS
const char PROGMEM g_defblen_desc[] = "Default Backlight Enable";
const char PROGMEM g_defblmode_desc[] = "Default Backlight Mode";
const char PROGMEM g_range_1_4[] = " [1-4]> ";
#endif /* MAX_NUMBER_OF_BACKLIGHTS */

const char PROGMEM g_range_bool[] = " [0=OFF, 1=ON]> ";
const char PROGMEM g_range_0_9[] = " [0-9]> ";
const char PROGMEM g_range_1_99[] = " [1-99]> ";
const char PROGMEM g_range_1_999[] = " [1-999]> ";
const char PROGMEM g_range_1_255[] = " [1-255]> ";
const char PROGMEM g_range_1_16[] = " [1-16]> ";

const char PROGMEM g_on_print[] = ": ON";
const char PROGMEM g_off_print[] = ": OFF";

const char PROGMEM g_invalid_selection[] = "Invalid selection.\n";
const char PROGMEM g_out_of_range[] = "Out of range.\n";

const char PROGMEM g_event_print_1[] = "\n[";
const char PROGMEM g_event_print_2[] = "] C-0x";
const char PROGMEM g_event_print_3[] = " S-0x";
const char PROGMEM g_exam_prompt1[] = "Address (hex)> ";
const char PROGMEM g_exam_prompt2[] = "Bytes (hex)> ";

#ifdef ENABLE_DEBUG_CONSOLE
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
	uint16_t read_word;
	uint8_t read_byte;
	char word_print[4];
	
	if (g_autokey_status == AUTOKEY_IDLE)
	{
		switch (g_console_state)
		{
		default:
			g_console_state = CONSOLE_IDLE;
		case CONSOLE_IDLE:
			break;
/*
 *  MAIN MENU
 */
		case CONSOLE_MENU_MAIN:
			queue_autotext(g_main_menu);
			begin_read();
			g_console_state = CONSOLE_PROCESS_MAIN;
			break;
		case CONSOLE_PROCESS_MAIN:
			g_console_state = CONSOLE_MENU_MAIN;
			g_console_index = 0;
			read_byte = sc_to_int(g_read_buffer[0]);
			if (read_byte == 9)
			{
				g_console_state = CONSOLE_IDLE;
			}
			else if (read_byte == 5)
			{
				g_reset_requested = RESET_REQUESTED;
			}
			else if (read_byte == 1)
			{
				g_console_state = CONSOLE_MENU_CONFIG;
			}
			else if (read_byte == 2)
			{
				g_console_state = CONSOLE_MENU_TIMING;
			}
			else if (read_byte == 3)
			{
				g_console_state = CONSOLE_MENU_LED;
			}
#ifdef ENABLE_DEBUG_CONSOLE
			else if (read_byte == 4)
			{
				g_console_state = CONSOLE_MENU_DEBUG;
			}
#endif /* ENABLE_DEBUG_CONSOLE */
			else
			{
				queue_autotext(g_invalid_selection);
			}
			break;
/*
 *  DEBUG MENU
 */
#ifdef ENABLE_DEBUG_CONSOLE
		case CONSOLE_MENU_DEBUG:
			queue_autotext(g_debug_menu);
			begin_read();
			g_console_state = CONSOLE_PROCESS_DEBUG;
			break;
		case CONSOLE_PROCESS_DEBUG:
			g_console_state = CONSOLE_MENU_DEBUG;
			read_byte = sc_to_int(g_read_buffer[0]);
			if (read_byte == 9)
			{
				g_console_state = CONSOLE_MENU_MAIN;
			}
			else if (read_byte == 1)
			{
				g_console_state = CONSOLE_EVENTS1;
			}
			else if (read_byte == 2)
			{
				for (int8_t i=0; i<EVENT_BUFFER_SIZE; i++)
				{
					g_event_buffer[i].code = 0;
					g_event_buffer[i].status = 0;
				}
				g_event_buffer_count = 0;
			}
			else if (read_byte == 3)
			{
				queue_autotext(g_exam_prompt1);
				begin_read();
				g_console_state = CONSOLE_EXAMINE1;
			}
			else if (read_byte == 4)
			{
				g_console_state = CONSOLE_CLOCKS;
			}
			else
			{
				queue_autotext(g_invalid_selection);
			}
			break;
		case CONSOLE_EVENTS1:
			if (g_console_index >= EVENT_BUFFER_SIZE)
			{
				g_console_index = 0;
				word_print[0] = '\n';
				queue_ram_autotext(word_print, 1);
				g_console_state = CONSOLE_MENU_DEBUG;
			} else {
				queue_autotext(g_event_print_1);
				byte_to_str(g_console_index, word_print);
				queue_ram_autotext(word_print, 2);
				queue_autotext(g_event_print_2);
				g_console_state = CONSOLE_EVENTS2;
			}
			break;
		case CONSOLE_EVENTS2:
			byte_to_str(g_event_buffer[g_console_index].code, word_print);
			queue_ram_autotext(word_print, 2);
			queue_autotext(g_event_print_3);
			g_console_state = CONSOLE_EVENTS3;
			break;
		case CONSOLE_EVENTS3:
			word_to_str(g_event_buffer[g_console_index].status, word_print);
			queue_ram_autotext(word_print, sizeof(word_print));
			g_console_state = CONSOLE_EVENTS1;
			g_console_index++;
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
			if (g_console_index >= (NUMBER_OF_SCHEDULE_SLOTS * NUMBER_OF_ITEMS_PER_SLOT))
			{
				g_console_index = 0;
				word_print[0] = '\n';
				queue_ram_autotext(word_print, 1);
				g_console_state = CONSOLE_MENU_DEBUG;
				reset_max_clocks();
			} else {
				const int8_t i = g_console_index % NUMBER_OF_SCHEDULE_SLOTS;
				const int8_t j = g_console_index / NUMBER_OF_SCHEDULE_SLOTS;
				if (i == 0)
					word_print[0] = '\n';
				else
					word_print[0] = ' ';
				queue_ram_autotext(word_print, 1);
				word_to_str(g_schedule_clocks[i][j], word_print);
				queue_ram_autotext(word_print, sizeof(word_print));
				g_console_index++;
			}
			break;
#endif /* ENABLE_DEBUG_CONSOLE */
/*
 *  CONFIG MENU
 */
		case CONSOLE_MENU_CONFIG:
			switch (g_console_index)
			{
			case 0:
				queue_autotext(g_config_menu_begin);
				break;
			case 1:
				queue_autotext(g_menu_1);
				queue_autotext(g_vnumpad_desc);
				break;
			case 2:
				if (g_virtual_numlock)
					queue_autotext(g_on_print);
				else
					queue_autotext(g_off_print);
				break;
			case 3:
				queue_autotext(g_menu_2);
				queue_autotext(g_vwinlock_desc);
				break;
			case 4:
				if (g_winlock_on_scrolllock)
					queue_autotext(g_on_print);
				else
					queue_autotext(g_off_print);
				break;
			case 5:
				queue_autotext(g_menu_3);
				queue_autotext(g_deflayer_desc);
				break;
			case 6:
				word_print[0] = ':';
				word_print[1] = ' ';
				dec_to_string(g_default_layer, word_print+2);
				queue_ram_autotext(word_print, 3);
				break;
			case 7:
				queue_autotext(g_menu_4);
				queue_autotext(g_bootkb_desc);
				break;
			case 8:
				if (g_boot_keyboard_only)
					queue_autotext(g_on_print);
				else
					queue_autotext(g_off_print);
				break;
			case 9:
				queue_autotext(g_menu_5);
				queue_autotext(g_vnumlock_desc);
				break;
			case 10:
				if (g_virtual_numlock)
					queue_autotext(g_on_print);
				else
					queue_autotext(g_off_print);
				break;
			case 11:
				queue_autotext(g_menu_6);
				queue_autotext(g_dbstyle_desc);
				break;
			case 12:
				if (g_debounce_style)
					queue_autotext(g_on_print);
				else
					queue_autotext(g_off_print);
				break;
			default:
				queue_autotext(g_menu_end);
				begin_read();
				g_console_state = CONSOLE_PROCESS_CONFIG;
			}
			g_console_index++;
			break;
		case CONSOLE_PROCESS_CONFIG:
			g_console_state = CONSOLE_PROMPT_CONFIG;
			read_byte = sc_to_int(g_read_buffer[0]);
			g_console_index = read_byte;
			if (read_byte == 9)
			{
				g_console_state = CONSOLE_MENU_MAIN;
			}
			else if (read_byte == 1)
			{
				queue_autotext(g_vnumpad_desc);
			}
			else if (read_byte == 2)
			{
				queue_autotext(g_vwinlock_desc);
			}
			else if (read_byte == 3)
			{
				queue_autotext(g_deflayer_desc);
			}
			else if (read_byte == 4)
			{
				queue_autotext(g_bootkb_desc);
			}
			else if (read_byte == 5)
			{
				queue_autotext(g_vnumlock_desc);
			}
			else if (read_byte == 6)
			{
				queue_autotext(g_dbstyle_desc);
			}
			else
			{
				queue_autotext(g_invalid_selection);
				g_console_state = CONSOLE_MENU_CONFIG;
				g_console_index = 0;
			}
			break;
		case CONSOLE_PROMPT_CONFIG:
			switch (g_console_index)
			{
			case 1:
				queue_autotext(g_range_bool);
				g_console_state = CONSOLE_VNUMPAD;
				break;
			case 2:
				queue_autotext(g_range_bool);
				g_console_state = CONSOLE_VWINLOCK;
				break;
			case 3:
				queue_autotext(g_range_0_9);
				g_console_state = CONSOLE_DEFAULTLAYER;
				break;
			case 4:
				queue_autotext(g_range_bool);
				g_console_state = CONSOLE_BOOTKEYBOARD;
				break;
			case 5:
				queue_autotext(g_range_bool);
				g_console_state = CONSOLE_VNUMLOCK;
				break;
			case 6:
				queue_autotext(g_range_bool);
				g_console_state = CONSOLE_DBSTYLE;
				break;
			default:
				g_console_state = CONSOLE_MENU_CONFIG;
			}
			begin_read();
			g_console_index = 0;
			break;
		case CONSOLE_VNUMPAD:
			read_byte = sc_to_int(g_read_buffer[0]);
			if (read_byte <= 1)
			{
				g_swap_num_row_on_numlock = read_byte;
				nvm_update_param(NVM_ID_SWAP_NUM_ROW_ON_NUMLOCK);
			} else {
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
		case CONSOLE_VWINLOCK:
			read_byte = sc_to_int(g_read_buffer[0]);
			if (read_byte <= 1)
			{
				g_winlock_on_scrolllock = read_byte;
				nvm_update_param(NVM_ID_WINLOCK_ON_SCROLLLOCK);
			} else {
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
		case CONSOLE_DEFAULTLAYER:
			read_byte = sc_to_int(g_read_buffer[0]);
			if (read_byte < NUMBER_OF_LAYERS)
			{
				g_default_layer = read_byte;
				nvm_update_param(NVM_ID_DEFAULT_LAYER);
			} else {
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
		case CONSOLE_BOOTKEYBOARD:
			read_byte = sc_to_int(g_read_buffer[0]);
			if (read_byte <= 1)
			{
				g_boot_keyboard_only = read_byte;
				nvm_update_param(NVM_ID_BOOT_KEYBOARD_ONLY);
			} else {
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
		case CONSOLE_VNUMLOCK:
			read_byte = sc_to_int(g_read_buffer[0]);
			if (read_byte <= 1)
			{
				g_virtual_numlock = read_byte;
				nvm_update_param(NVM_ID_VIRTUAL_NUMLOCK);
			} else {
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
		case CONSOLE_DBSTYLE:
			read_byte = sc_to_int(g_read_buffer[0]);
			if (read_byte <= 1)
			{
				g_debounce_style = read_byte;
				nvm_update_param(NVM_ID_DEBOUNCE_STYLE);
				if (g_debounce_style)
				{
					g_debounce_ms = DEFAULT_ALT_DEBOUNCE_MS;
					nvm_update_param(NVM_ID_DEBOUNCE_MS);
				} else {
					g_debounce_ms = DEFAULT_DEBOUNCE_MS;
					nvm_update_param(NVM_ID_DEBOUNCE_MS);
				}
			} else {
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_CONFIG;
			break;
/*
 *  TIMING MENU
 */
		case CONSOLE_MENU_TIMING:
			word_print[0] = ':';
			word_print[1] = ' ';
			switch (g_console_index)
			{
			case 0:
				queue_autotext(g_timing_menu_begin);
				break;
			case 1:
				queue_autotext(g_menu_1);
				queue_autotext(g_debounce_desc);
				break;
			case 2:
				dec_to_string(g_debounce_ms, word_print+2);
				queue_ram_autotext(word_print, 4);
				break;
			case 3:
				queue_autotext(g_menu_2);
				queue_autotext(g_tap_desc);
				break;
			case 4:
				dec_to_string(g_max_tap_ms, word_print+2);
				queue_ram_autotext(word_print, 5);
				break;
			case 5:
				queue_autotext(g_menu_3);
				queue_autotext(g_doubletap_desc);
				break;
			case 6:
				dec_to_string(g_doubletap_delay_ms*(-1), word_print+2);
				queue_ram_autotext(word_print, 5);
				break;
			case 7:
				queue_autotext(g_menu_4);
				queue_autotext(g_mousebase_desc);
				break;
			case 8:
				dec_to_string(g_mouse_min_delta, word_print+2);
				queue_ram_autotext(word_print, 4);
				break;
			case 9:
				queue_autotext(g_menu_5);
				queue_autotext(g_mousemult_desc);
				break;
			case 10:
				dec_to_string(g_mouse_delta_mult, word_print+2);
				queue_ram_autotext(word_print, 4);
				break;
			case 11:
				queue_autotext(g_menu_6);
				queue_autotext(g_hold_desc);
				break;
			case 12:
				dec_to_string(g_hold_key_ms, word_print+2);
				queue_ram_autotext(word_print, 5);
				break;
			case 13:
				queue_autotext(g_menu_7);
				queue_autotext(g_repeat_desc);
				break;
			case 14:
				dec_to_string(g_repeat_ms, word_print+2);
				queue_ram_autotext(word_print, 4);
				break;
			case 15:
				queue_autotext(g_menu_8);
				queue_autotext(g_setup_desc);
				break;
			case 16:
				dec_to_string(g_matrix_setup_wait, word_print+2);
				queue_ram_autotext(word_print, 5);
				break;
			default:
				queue_autotext(g_menu_end);
				begin_read();
				g_console_state = CONSOLE_PROCESS_TIMING;
			}
			g_console_index++;
			break;
		case CONSOLE_PROCESS_TIMING:
			g_console_state = CONSOLE_PROMPT_TIMING;
			read_byte = sc_to_int(g_read_buffer[0]);
			g_console_index = read_byte;
			if (read_byte == 9)
			{
				g_console_state = CONSOLE_MENU_MAIN;
			}
			else if (read_byte == 1)
			{
				queue_autotext(g_debounce_desc);
			}
			else if (read_byte == 2)
			{
				queue_autotext(g_tap_desc);
			}
			else if (read_byte == 3)
			{
				queue_autotext(g_doubletap_desc);
			}
			else if (read_byte == 4)
			{
				queue_autotext(g_mousebase_desc);
			}
			else if (read_byte == 5)
			{
				queue_autotext(g_mousemult_desc);
			}
			else if (read_byte == 6)
			{
				queue_autotext(g_hold_desc);
			}
			else if (read_byte == 7)
			{
				queue_autotext(g_repeat_desc);
			}
			else if (read_byte == 8)
			{
				queue_autotext(g_setup_desc);
			}
			else
			{
				queue_autotext(g_invalid_selection);
				g_console_state = CONSOLE_MENU_TIMING;
				g_console_index = 0;
			}
			break;
		case CONSOLE_PROMPT_TIMING:
			switch (g_console_index)
			{
			case 1:
				queue_autotext(g_range_1_99);
				g_console_state = CONSOLE_DEBOUNCE;
				break;
			case 2:
				queue_autotext(g_range_1_999);
				g_console_state = CONSOLE_TAP;
				break;
			case 3:
				queue_autotext(g_range_1_999);
				g_console_state = CONSOLE_DOUBLETAP;
				break;
			case 4:
				queue_autotext(g_range_1_99);
				g_console_state = CONSOLE_MOUSEBASE;
				break;
			case 5:
				queue_autotext(g_range_1_99);
				g_console_state = CONSOLE_MOUSEMULT;
				break;
			case 6:
				queue_autotext(g_range_1_999);
				g_console_state = CONSOLE_HOLD;
				break;
			case 7:
				queue_autotext(g_range_1_99);
				g_console_state = CONSOLE_REPEAT;
				break;
			case 8:
				queue_autotext(g_range_1_255);
				g_console_state = CONSOLE_SETUP;
				break;
			default:
				g_console_state = CONSOLE_MENU_TIMING;
			}
			begin_read();
			g_console_index = 0;
			break;
		case CONSOLE_DEBOUNCE:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word < 100) && (read_word > 0))
			{
				g_debounce_ms = (int8_t)(read_word & 0x00FF);
				nvm_update_param(NVM_ID_DEBOUNCE_MS);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_TAP:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word < 1000) && (read_word > 0))
			{
				g_max_tap_ms = read_word;
				nvm_update_param(NVM_ID_MAX_TAP_MS);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_DOUBLETAP:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word < 1000) && (read_word > 0))
			{
				g_doubletap_delay_ms = read_word*(-1);
				nvm_update_param(NVM_ID_DOUBLETAP_DELAY_MS);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_MOUSEBASE:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word < 100) && (read_word > 0))
			{
				g_mouse_min_delta = (int8_t)(read_word & 0x00FF);
				nvm_update_param(NVM_ID_MOUSE_MIN_DELTA);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_MOUSEMULT:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word < 100) && (read_word > 0))
			{
				g_mouse_delta_mult = (int8_t)(read_word & 0x00FF);
				nvm_update_param(NVM_ID_MOUSE_DELTA_MULT);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_HOLD:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word < 1000) && (read_word > 0))
			{
				g_hold_key_ms = read_word;
				nvm_update_param(NVM_ID_HOLD_KEY_MS);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_REPEAT:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word < 100) && (read_word > 0))
			{
				g_repeat_ms = (int8_t)(read_word & 0x00FF);
				nvm_update_param(NVM_ID_REPEAT_MS);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
		case CONSOLE_SETUP:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word <= 255) && (read_word > 0))
			{
				g_matrix_setup_wait = (int8_t)(read_word & 0x00FF);
				nvm_update_param(NVM_ID_MATRIX_SETUP_WAIT);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_TIMING;
			break;
/*
 *  LED MENU
 */
		case CONSOLE_MENU_LED:
			word_print[0] = ':';
			word_print[1] = ' ';
			switch (g_console_index)
			{
			case 0:
				queue_autotext(g_led_menu_begin);
				break;
			case 1:
				queue_autotext(g_menu_1);
				queue_autotext(g_defdim_desc);
				break;
			case 2:
				dec_to_string(g_init_dimmer_level, word_print+2);
				queue_ram_autotext(word_print, 4);
				break;
#ifdef MAX_NUMBER_OF_BACKLIGHTS
			case 3:
				queue_autotext(g_menu_2);
				queue_autotext(g_defblen_desc);
				break;
			case 4:
				dec_to_string(g_init_backlight_enable+1, word_print+2);
				queue_ram_autotext(word_print, 4);
				break;
			case 5:
				queue_autotext(g_menu_3);
				queue_autotext(g_defblmode_desc);
				break;
			case 6:
				dec_to_string(g_init_backlight_mode+1, word_print+2);
				queue_ram_autotext(word_print, 3);
				break;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
			default:
				queue_autotext(g_menu_end);
				begin_read();
				g_console_state = CONSOLE_PROCESS_LED;
			}
			g_console_index++;
			break;
		case CONSOLE_PROCESS_LED:
			g_console_state = CONSOLE_PROMPT_LED;
			read_byte = sc_to_int(g_read_buffer[0]);
			g_console_index = read_byte;
			if (read_byte == 9)
			{
				g_console_state = CONSOLE_MENU_MAIN;
			}
			else if (read_byte == 1)
			{
				queue_autotext(g_defdim_desc);
			}
#ifdef MAX_NUMBER_OF_BACKLIGHTS
			else if (read_byte == 2)
			{
				queue_autotext(g_defblen_desc);
			}
			else if (read_byte == 3)
			{
				queue_autotext(g_defblmode_desc);
			}
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
			else
			{
				queue_autotext(g_invalid_selection);
				g_console_state = CONSOLE_MENU_LED;
				g_console_index = 0;
			}
			break;
		case CONSOLE_PROMPT_LED:
			switch (g_console_index)
			{
			case 1:
				queue_autotext(g_range_1_16);
				g_console_state = CONSOLE_DEFAULTDIMMER;
				break;
#ifdef MAX_NUMBER_OF_BACKLIGHTS
			case 2:
				queue_autotext(g_range_1_16);
				g_console_state = CONSOLE_DEFAULTBACKLIGHT;
				break;
			case 3:
				queue_autotext(g_range_1_4);
				g_console_state = CONSOLE_DEFAULTBLMODE;
				break;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
			default:
				g_console_state = CONSOLE_MENU_LED;
			}
			begin_read();
			g_console_index = 0;
			break;
		case CONSOLE_DEFAULTDIMMER:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word <= NUMBER_OF_BACKLIGHT_LEVELS) && (read_word > 0))
			{
				g_init_dimmer_level = (int8_t)(read_word & 0x00FF);
				nvm_update_param(NVM_ID_INIT_DIMMER_LEVEL);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_LED;
			break;
#ifdef MAX_NUMBER_OF_BACKLIGHTS
		case CONSOLE_DEFAULTBACKLIGHT:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word <= MAX_BACKLIGHT_ENABLES) && (read_word > 0))
			{
				g_init_backlight_enable = ((int8_t)(read_word & 0x00FF)) - 1;
				nvm_update_param(NVM_ID_INIT_BACKLIGHT_ENABLE);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_LED;
			break;
		case CONSOLE_DEFAULTBLMODE:
			read_word = sc_to_word(g_read_buffer, g_read_buffer_length, 10);
			if ((read_word <= NUMBER_OF_BACKLIGHT_MODES) && (read_word > 0))
			{
				g_init_backlight_mode = ((int8_t)(read_word & 0x00FF)) - 1;
				nvm_update_param(NVM_ID_INIT_BACKLIGHT_MODE);
			}
			else
			{
				queue_autotext(g_out_of_range);
			}
			g_console_state = CONSOLE_MENU_LED;
			break;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
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

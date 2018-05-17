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

#include "debug.h"
#include "scheduler.h"
#include "autokey.h"
#include "matrix.h"
#include "USB.h"
#include "mouse.h"
#include "led.h"
#include "nvm.h"
#include "keymap.h"

const mod_map_t PROGMEM MODIFIER_MAP[8] = {
	{ HID_KEYBOARD_SC_LEFT_CONTROL,  HID_KEYBOARD_MODIFIER_LEFTCTRL   },
	{ HID_KEYBOARD_SC_LEFT_SHIFT,    HID_KEYBOARD_MODIFIER_LEFTSHIFT  },
	{ HID_KEYBOARD_SC_LEFT_ALT,      HID_KEYBOARD_MODIFIER_LEFTALT    },
	{ HID_KEYBOARD_SC_LEFT_GUI,      HID_KEYBOARD_MODIFIER_LEFTGUI    },
	{ HID_KEYBOARD_SC_RIGHT_CONTROL, HID_KEYBOARD_MODIFIER_RIGHTCTRL  },
	{ HID_KEYBOARD_SC_RIGHT_SHIFT,   HID_KEYBOARD_MODIFIER_RIGHTSHIFT },
	{ HID_KEYBOARD_SC_RIGHT_ALT,     HID_KEYBOARD_MODIFIER_RIGHTALT   },
	{ HID_KEYBOARD_SC_RIGHT_GUI,     HID_KEYBOARD_MODIFIER_RIGHTGUI   }
};

const mod_map_t PROGMEM MOUSEBUTTON_MAP[NUMBER_OF_MOUSE_BUTTONS] = {
	{ SCANCODE_MOUSE1, 0x01 },
	{ SCANCODE_MOUSE2, 0x02 },
	{ SCANCODE_MOUSE3, 0x04 },
	{ SCANCODE_MOUSE4, 0x08 },
	{ SCANCODE_MOUSE5, 0x10 }
};

const uint16_t PROGMEM MEDIA_MAP[NUMBER_OF_MEDIA_KEYS] = {
	/* SCANCODE_NEXT_TRACK	*/	SC_WIN_CP_NEXT_TRACK,
	/* SCANCODE_PREV_TRACK	*/	SC_WIN_CP_PREV_TRACK,
	/* SCANCODE_STOP		*/	SC_WIN_CP_STOP,
	/* SCANCODE_PLAY_PAUSE	*/	SC_WIN_CP_PLAY_PAUSE,
	/* SCANCODE_BRIGHT_INC	*/	SC_WIN_CP_BRIGHT_INC,
	/* SCANCODE_BRIGHT_DEC	*/	SC_WIN_CP_BRIGHT_DEC,
	/* SCANCODE_MUTE		*/	SC_WIN_CP_MUTE,
	/* SCANCODE_BASS_BOOST	*/	SC_WIN_CP_BASS_BOOST,
	/* SCANCODE_VOL_INC		*/	SC_WIN_CP_VOL_INC,
	/* SCANCODE_VOL_DEC		*/	SC_WIN_CP_VOL_DEC,
	/* SCANCODE_BASS_INC	*/	SC_WIN_CP_BASS_INC,
	/* SCANCODE_BASS_DEC	*/	SC_WIN_CP_BASS_DEC,
	/* SCANCODE_TREB_INC	*/	SC_WIN_CP_TREB_INC,
	/* SCANCODE_TREB_DEC	*/	SC_WIN_CP_TREB_DEC,
	/* SCANCODE_MEDIA_SEL	*/	SC_WIN_CP_MEDIA_SEL,
	/* SCANCODE_MAIL		*/	SC_WIN_CP_MAIL,
	/* SCANCODE_CALC		*/	SC_WIN_CP_CALC,
	/* SCANCODE_MYCOMP		*/	SC_WIN_CP_MY_COMP,
	/* SCANCODE_SEARCH		*/	SC_WIN_CP_SEARCH,
	/* SCANCODE_BROWSER		*/	SC_WIN_CP_HOME,
	/* SCANCODE_BACK		*/	SC_WIN_CP_BACK,
	/* SCANCODE_FORWARD		*/	SC_WIN_CP_FORWARD,
	/* SCANCODE_WWWSTOP		*/	SC_WIN_CP_WWWSTOP,
	/* SCANCODE_REFRESH		*/	SC_WIN_CP_REFRESH,
	/* SCANCODE_FAVES		*/	SC_WIN_CP_FAVES
};

#ifndef SIMPLE_DEVICE
const kp_map_t PROGMEM KP_MAP[11] = {
    { HID_KEYBOARD_SC_1_AND_EXCLAMATION         , HID_KEYBOARD_SC_END         },
    { HID_KEYBOARD_SC_2_AND_AT                  , HID_KEYBOARD_SC_DOWN_ARROW  },
    { HID_KEYBOARD_SC_3_AND_HASHMARK            , HID_KEYBOARD_SC_PAGE_DOWN   },
    { HID_KEYBOARD_SC_4_AND_DOLLAR              , HID_KEYBOARD_SC_LEFT_ARROW  },
    { HID_KEYBOARD_SC_5_AND_PERCENTAGE          , 0                           },
    { HID_KEYBOARD_SC_6_AND_CARET               , HID_KEYBOARD_SC_RIGHT_ARROW },
    { HID_KEYBOARD_SC_7_AND_AMPERSAND           , HID_KEYBOARD_SC_HOME        },
    { HID_KEYBOARD_SC_8_AND_ASTERISK            , HID_KEYBOARD_SC_UP_ARROW    },
    { HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS , HID_KEYBOARD_SC_PAGE_UP     },
    { HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS , HID_KEYBOARD_SC_INSERT      },
    { HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN , HID_KEYBOARD_SC_DELETE      },
};
#endif /* SIMPLE_DEVICE */

uint8_t g_last_keypress;
uint8_t g_locked_layer;
uint8_t g_layer_select;
uint8_t g_modifier_state;
uint8_t g_report_buffer[HID_ROLLOVER_SIZE+1];
uint8_t g_nkro_field[NKRO_ARRAY_LENGTH];
uint8_t g_modifier_service;
uint8_t g_alphanum_service;
uint8_t g_media_service;
uint8_t g_power_service;
#ifdef KEYMAP_MEMORY_SAVE
uint8_t g_matrixlayer[NUMBER_OF_ROWS][NUMBER_OF_COLS];
#else
uint8_t g_matrixcode[NUMBER_OF_ROWS][NUMBER_OF_COLS];
uint8_t g_matrixaction[NUMBER_OF_ROWS][NUMBER_OF_COLS];
uint8_t g_matrixtapkey[NUMBER_OF_ROWS][NUMBER_OF_COLS];
#endif /* KEYMAP_MEMORY_SAVE */
int8_t g_buffer_length;
uint8_t g_rollover_error;
uint8_t g_fn_buffer[FN_BUFFER_SIZE+1];
int8_t g_fn_buffer_length;
uint8_t g_mousebutton_state;
int8_t g_mouse_req_X;
int8_t g_mouse_req_Y;
uint16_t g_media_key;
uint8_t g_powermgmt_field;
uint8_t g_hid_lock_flags;
uint8_t g_keylock_flag;
uint8_t g_winlock_flag;
uint8_t g_double_tap_key;
uint8_t g_double_tap_repeat;
#if MACRO_RAM_SIZE
uint8_t g_recording_macro;
uint16_t g_ram_macro[MACRO_RAM_SIZE];
int8_t g_ram_macro_ptr;
int8_t g_ram_macro_length;
#endif /* MACRO_RAM_SIZE */

/* Functions for working with the keypress queue
 * This is a very simple queue implementation that uses only an array and one state var.
 * operations are O(n) (d'oh!) but the array should always be very small.
 * The byte at the end of the buffer must always remain zero so that the below functions
 * will shift zeros into the buffer as it is emptied.
 */
void enqueue_key(const uint8_t code)
{
	int8_t i;
	const uint8_t pos = (code / 8);
	const uint8_t off = (code % 8);
	
	g_nkro_field[pos] |= (1 << off);
	
	g_alphanum_service = 1;
	
	for (i=0; i<g_buffer_length; i++)
	{
		if (g_report_buffer[i] == code)
		{
			return;
		}
	}
	if (g_buffer_length < HID_ROLLOVER_SIZE)
	{
		g_report_buffer[g_buffer_length] = code;
		g_buffer_length++;
	} else {
		//report_event(EVENT_CODE_KEYMAP_BUF_FULL, 0, MODE_UPDATE);
		g_report_buffer[HID_ROLLOVER_SIZE] = 0;
		g_rollover_error = 1;
	}
}

void delete_key(const uint8_t code)
{
	int8_t i;
	const uint8_t pos = (code / 8);
	const uint8_t off = (code % 8);
	
	g_nkro_field[pos] &= ~(1 << off);
	
	g_alphanum_service = 1;
	
	for (i=0; i<g_buffer_length; i++)
	{
		if (g_report_buffer[i] == code)
		{
			goto found;
		}
	}
	//report_event(EVENT_CODE_KEYMAP_DA_NOT_FOUND, code, MODE_UPDATE);
	return;
	for (; i<g_buffer_length; i++)
	{
found:
		g_report_buffer[i] = g_report_buffer[i+1];
	}
	g_buffer_length--;
	g_rollover_error = 0;
}

void toggle_key(const uint8_t code)
{
	int8_t i;
	const uint8_t pos = (code / 8);
	const uint8_t off = (code % 8);
	
	g_nkro_field[pos] ^= (1 << off);
	
	g_alphanum_service = 1;
	
	for (i=0; i<g_buffer_length; i++)
	{
		if (g_report_buffer[i] == code)
		{
			goto found;
		}
	}
	if (g_buffer_length < HID_ROLLOVER_SIZE)
	{
		g_report_buffer[g_buffer_length] = code;
		g_buffer_length++;
	} else {
		g_report_buffer[HID_ROLLOVER_SIZE] = 0;
		g_rollover_error = 1;
	}
	return;
	for (; i<g_buffer_length; i++)
	{
found:
		g_report_buffer[i] = g_report_buffer[i+1];
	}
	g_buffer_length--;
	g_rollover_error = 0;
}

void enqueue_fn(const uint8_t code)
{
	if (g_fn_buffer_length < FN_BUFFER_SIZE)
	{
		g_fn_buffer[g_fn_buffer_length] = code;
		g_fn_buffer_length++;
	} else {
		report_event(EVENT_CODE_KEYMAP_FN_BUF_FULL, 0, MODE_UPDATE);
		g_fn_buffer[FN_BUFFER_SIZE] = 0;
	}
}

void delete_fn(const uint8_t code)
{
	int8_t i;
	
	for (i=0; i<g_fn_buffer_length; i++)
	{
		if (g_fn_buffer[i] == code)
		{
			break;
		}
	}
	if (i >= g_fn_buffer_length)
	{
		report_event(EVENT_CODE_KEYMAP_FN_NOT_FOUND, code, MODE_UPDATE);
		return;
	}
	for (; i<g_fn_buffer_length; i++)
	{
		g_fn_buffer[i] = g_fn_buffer[i+1];
	}
	g_fn_buffer_length--;
}
/* End keypress queue functions */

uint8_t inline getmap(const uint8_t row, const uint8_t col)
{
	return pgm_read_byte(&LAYERS[g_layer_select][row][col]);
}

uint8_t inline getaction(const uint8_t row, const uint8_t col)
{
	return pgm_read_byte(&ACTIONS[g_layer_select][row][col]);
}

uint8_t inline gettapkey(const uint8_t row, const uint8_t col)
{
	return pgm_read_byte(&TAPKEYS[g_layer_select][row][col]);
}

uint8_t inline get_modfier_mask(const uint8_t code)
{
	return pgm_read_byte(&MODIFIER_MAP[(code-HID_KEYBOARD_SC_LEFT_CONTROL)].mask);
}

void inline set_modifier(const uint8_t code)
{
	g_modifier_state |= get_modfier_mask(code);
	if (g_winlock_flag)
		g_modifier_state &= 0x77;
	g_modifier_service = 1;
}

void inline unset_modifier(const uint8_t code)
{
	g_modifier_state &= ~(get_modfier_mask(code));
	g_modifier_service = 1;
}

void inline toggle_modifier(const uint8_t code)
{
	g_modifier_state ^= get_modfier_mask(code);
	if (g_winlock_flag)
		g_modifier_state &= 0x77;
	g_modifier_service = 1;
}

uint8_t inline is_mod_set(const uint8_t code)
{
	return ((g_modifier_state & get_modfier_mask(code)) != 0);
}

void set_media(const uint8_t code)
{
	const uint8_t i = (code - SCANCODE_NEXT_TRACK);
	if (!g_media_key)
		g_media_key = pgm_read_word(&MEDIA_MAP[i]);
	g_media_service = 1;
}

void unset_media(const uint8_t code)
{
	const uint8_t i = (code - SCANCODE_NEXT_TRACK);
	if (g_media_key == pgm_read_word(&MEDIA_MAP[i]))
		g_media_key = 0;
	g_media_service = 1;
}

void set_power(const uint8_t code)
{
	const uint8_t n = (code - SCANCODE_POWER);
	/* Assume power keys never coincide */
	g_powermgmt_field = (1 << n);
	g_power_service = 1;
}

void unset_power(const uint8_t code)
{
	/* Assume power keys never coincide */
	g_powermgmt_field = 0;
	g_power_service = 1;
}

void inline set_mousebutton(const uint8_t code)
{
	const uint8_t i = (code - SCANCODE_MOUSE1);
	g_mousebutton_state |= pgm_read_byte(&MOUSEBUTTON_MAP[i].mask);
	g_mouse_service = 1;
}

void inline unset_mousebutton(const uint8_t code)
{
	const uint8_t i = (code - SCANCODE_MOUSE1);
	g_mousebutton_state &= ~(pgm_read_byte(&MOUSEBUTTON_MAP[i].mask));
	g_mouse_service = 1;
}

void init_keymap(void)
{
	g_layer_select = g_default_layer;
}

void doubletap_down(const uint8_t row, const uint8_t col, const int16_t idle_time)
{
	const uint8_t key = (row * NUMBER_OF_COLS) + col;
	
	if ((key == g_double_tap_key) &&  (idle_time > g_doubletap_delay_ms))
	{
		g_double_tap_repeat++;
	}
	else
	{
		g_double_tap_key = 0;
		g_double_tap_repeat = 0;
	}
}

void doubletap_up(const uint8_t row, const uint8_t col, const int16_t hold_time, uint8_t * const tap)
{
	if (hold_time < g_max_tap_ms)
	{
		*tap = 1;
		g_double_tap_key = (row * NUMBER_OF_COLS) + col;
	}
	else
	{
		*tap = 0;
		g_double_tap_key = 0;
		g_double_tap_repeat = 0;
	}
}

#if MACRO_RAM_SIZE
void record_stroke(const uint8_t code)
{
	g_ram_macro[g_ram_macro_ptr] = (((uint16_t)g_modifier_state << 8) | (uint16_t)code);
	g_ram_macro_ptr++;
	if (g_ram_macro_ptr >= MACRO_RAM_SIZE)
	{
		g_recording_macro = 0;
		g_ram_macro_length = g_ram_macro_ptr;
		led_host_off(LED_RECORDING);
	}
}

void inline toggle_macro_record(void)
{
	g_recording_macro ^= 1;
	if (g_recording_macro)
	{
		g_ram_macro_ptr = 0;
		led_host_on(LED_RECORDING);
	}
	else
	{
		if (g_ram_macro_ptr)
		{
			g_ram_macro_length = g_ram_macro_ptr;
		}
		led_host_off(LED_RECORDING);
	}
}
#endif /* MACRO_RAM_SIZE */

void play_macro(const uint8_t code)
{
	const uint8_t n = (code - SCANCODE_M1);
	uint16_t i;
	
	if (g_keylock_flag)
		return;
	
	if (n < NUMBER_OF_MACROS)
	{
		i = pgm_read_word(&MACRO_BUFFER[n]);
		queue_macro(&MACRO_BUFFER[i]);
	}
}

void inline send_tapkey(const uint8_t code)
{
	if ((code > 0) && (code <= MAX_NKRO_CODE))
	{
		queue_autokeys(code, g_modifier_state);
	}
	else if ((code & 0xE0) == 0xE0)
	{
		unset_modifier(code);
		queue_autokeys(0, get_modfier_mask(code));
	}
}

void led_fn_activate(const uint8_t bit)
{
	const uint8_t code = pgm_read_byte(&LED_LAYERS[bit]);
	
	if (code)
		fn_down(code, 0);
}

void led_fn_deactivate(const uint8_t bit)
{
	const uint8_t code = pgm_read_byte(&LED_LAYERS[bit]);
	
	if (code)
		fn_up(code, 0, 0, 0);
}

void fn_down(const uint8_t code, const uint8_t action)
{
	if (g_layer_select != 0)
	{
		led_host_off((g_layer_select + (LED_FN1_ACTIVE-1)));
	}
	g_layer_select = (code - SCANCODE_FN0);
	enqueue_fn(g_layer_select);
	if (g_layer_select != 0)
	{
		led_host_on((g_layer_select + (LED_FN1_ACTIVE-1)));
	}
	if (g_layer_select != g_default_layer)
	{
		led_host_on(LED_ANY_ACTIVE);
	}
	if ((action & ACTION_TOGGLE) && (g_locked_layer != g_layer_select))
	{
		g_locked_layer = g_layer_select;
		return;
	}
	if ((g_locked_layer == g_layer_select) && (!g_double_tap_repeat))
	{
		g_locked_layer = g_default_layer;
	}
}

void fn_up(const uint8_t code, const uint8_t action, const uint8_t tapkey, const uint8_t tap)
{
	const uint8_t layerid = (code - SCANCODE_FN0);
	
	if (g_layer_select != 0)
	{
		led_host_off((g_layer_select + (LED_FN1_ACTIVE-1)));
	}
	if (tap && (g_layer_select == layerid))
	{
		if ((g_double_tap_repeat) && (action & ACTION_LOCKABLE))
		{
			g_locked_layer = g_layer_select;
		}
		if ((g_last_keypress == code) && (action & ACTION_TAPKEY))
		{
			send_tapkey(tapkey);
		}
	}
	delete_fn(layerid);
	if (g_fn_buffer_length == 0)
	{
		g_layer_select = g_locked_layer;
	}
	else
	{
		g_layer_select = g_fn_buffer[g_fn_buffer_length-1];
	}
	if (g_layer_select != 0)
	{
		led_host_on((g_layer_select + (LED_FN1_ACTIVE-1)));
	}
	if (g_layer_select == g_default_layer)
	{
		led_host_off(LED_ANY_ACTIVE);
	}
}

void mod_down(const uint8_t code, const uint8_t action)
{
	switch(action & KEY_ACTION_MASK)
	{
	case ACTION_RAPIDFIRE:
	case ACTION_TAPKEY:
	case ACTION_LOCKABLE:
	case ACTION_NORMAL:
		set_modifier(code);
		break;
	case ACTION_TOGGLE:
		toggle_modifier(code);
		break;
	default:
		break;
	}
}

void mod_up(const uint8_t code, const uint8_t action, const uint8_t tapkey, const uint8_t tap)
{
	switch(action & KEY_ACTION_MASK)
	{
	case ACTION_TAPKEY:
		unset_modifier(code);
		if ((tap) && (g_last_keypress == code))
		{
			send_tapkey(tapkey);
		}
		break;
	case ACTION_RAPIDFIRE:
	case ACTION_NORMAL:
		unset_modifier(code);
		break;
	case ACTION_LOCKABLE:
		if ((tap) && (g_double_tap_repeat))
			set_modifier(code);
		else
			unset_modifier(code);
		break;
	case ACTION_TOGGLE:
	default:
		break;
	}
}

void alpha_down(const uint8_t code, const uint8_t action)
{
	switch(action & KEY_ACTION_MASK)
	{
	case ACTION_NORMAL:
	case ACTION_LOCKABLE:
	case ACTION_TAPKEY:
	case ACTION_RAPIDFIRE:
		enqueue_key(code);
		break;
	case ACTION_TOGGLE:
		toggle_key(code);
		break;
	default:
		break;
	}
}

void alpha_up(const uint8_t code, const uint8_t action, const uint8_t tapkey, const uint8_t tap)
{
	switch(action & KEY_ACTION_MASK)
	{
	case ACTION_LOCKABLE:
		if ((tap) && (g_double_tap_repeat))
			break;
	case ACTION_NORMAL:
	case ACTION_TAPKEY:
	case ACTION_RAPIDFIRE:
		delete_key(code);
		break;
	case ACTION_TOGGLE:
	default:
		break;
	}
}

void handle_code_actuate(const uint8_t code, const uint8_t action, const uint8_t tapkey)
{
	const uint8_t modaction = (action & MOD_ACTION_MASK);
	
	if (modaction)
	{
		// Autokey macros are assumed to be mutually exclusive with keypresses
		g_autokey_modifier = modaction;
		g_modifier_service = 1;
	}
	
	switch(code)
	{
	case HID_KEYBOARD_SC_A:
	case HID_KEYBOARD_SC_B:
	case HID_KEYBOARD_SC_C:
	case HID_KEYBOARD_SC_D:
	case HID_KEYBOARD_SC_E:
	case HID_KEYBOARD_SC_F:
	case HID_KEYBOARD_SC_G:
	case HID_KEYBOARD_SC_H:
	case HID_KEYBOARD_SC_I:
	case HID_KEYBOARD_SC_J:
	case HID_KEYBOARD_SC_K:
	case HID_KEYBOARD_SC_L:
	case HID_KEYBOARD_SC_M:
	case HID_KEYBOARD_SC_N:
	case HID_KEYBOARD_SC_O:
	case HID_KEYBOARD_SC_P:
	case HID_KEYBOARD_SC_Q:
	case HID_KEYBOARD_SC_R:
	case HID_KEYBOARD_SC_S:
	case HID_KEYBOARD_SC_T:
	case HID_KEYBOARD_SC_U:
	case HID_KEYBOARD_SC_V:
	case HID_KEYBOARD_SC_W:
	case HID_KEYBOARD_SC_X:
	case HID_KEYBOARD_SC_Y:
	case HID_KEYBOARD_SC_Z:
	case HID_KEYBOARD_SC_1_AND_EXCLAMATION:
	case HID_KEYBOARD_SC_2_AND_AT:
	case HID_KEYBOARD_SC_3_AND_HASHMARK:
	case HID_KEYBOARD_SC_4_AND_DOLLAR:
	case HID_KEYBOARD_SC_5_AND_PERCENTAGE:
	case HID_KEYBOARD_SC_6_AND_CARET:
	case HID_KEYBOARD_SC_7_AND_AMPERSAND:
	case HID_KEYBOARD_SC_8_AND_ASTERISK:
	case HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS:
	case HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS:
	case HID_KEYBOARD_SC_ENTER:
	case HID_KEYBOARD_SC_ESCAPE:
	case HID_KEYBOARD_SC_BACKSPACE:
	case HID_KEYBOARD_SC_TAB:
	case HID_KEYBOARD_SC_SPACE:
	case HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE:
	case HID_KEYBOARD_SC_EQUAL_AND_PLUS:
	case HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE:
	case HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE:
	case HID_KEYBOARD_SC_BACKSLASH_AND_PIPE:
	case HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE:
	case HID_KEYBOARD_SC_SEMICOLON_AND_COLON:
	case HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE:
	case HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE:
	case HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN:
	case HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN:
	case HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK:
	case HID_KEYBOARD_SC_CAPS_LOCK:
	case HID_KEYBOARD_SC_F1:
	case HID_KEYBOARD_SC_F2:
	case HID_KEYBOARD_SC_F3:
	case HID_KEYBOARD_SC_F4:
	case HID_KEYBOARD_SC_F5:
	case HID_KEYBOARD_SC_F6:
	case HID_KEYBOARD_SC_F7:
	case HID_KEYBOARD_SC_F8:
	case HID_KEYBOARD_SC_F9:
	case HID_KEYBOARD_SC_F10:
	case HID_KEYBOARD_SC_F11:
	case HID_KEYBOARD_SC_F12:
	case HID_KEYBOARD_SC_PRINT_SCREEN:
	case HID_KEYBOARD_SC_SCROLL_LOCK:
	case HID_KEYBOARD_SC_PAUSE:
	case HID_KEYBOARD_SC_INSERT:
	case HID_KEYBOARD_SC_HOME:
	case HID_KEYBOARD_SC_PAGE_UP:
	case HID_KEYBOARD_SC_DELETE:
	case HID_KEYBOARD_SC_END:
	case HID_KEYBOARD_SC_PAGE_DOWN:
	case HID_KEYBOARD_SC_RIGHT_ARROW:
	case HID_KEYBOARD_SC_LEFT_ARROW:
	case HID_KEYBOARD_SC_DOWN_ARROW:
	case HID_KEYBOARD_SC_UP_ARROW:
	case HID_KEYBOARD_SC_NUM_LOCK:
	case HID_KEYBOARD_SC_KEYPAD_SLASH:
	case HID_KEYBOARD_SC_KEYPAD_ASTERISK:
	case HID_KEYBOARD_SC_KEYPAD_MINUS:
	case HID_KEYBOARD_SC_KEYPAD_PLUS:
	case HID_KEYBOARD_SC_KEYPAD_ENTER:
	case HID_KEYBOARD_SC_KEYPAD_1_AND_END:
	case HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW:
	case HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN:
	case HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW:
	case HID_KEYBOARD_SC_KEYPAD_5:
	case HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW:
	case HID_KEYBOARD_SC_KEYPAD_7_AND_HOME:
	case HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW:
	case HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP:
	case HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT:
	case HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE:
	case HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE:
	case HID_KEYBOARD_SC_APPLICATION:
	case HID_KEYBOARD_SC_POWER:
	case HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN:
	case HID_KEYBOARD_SC_F13:
	case HID_KEYBOARD_SC_F14:
	case HID_KEYBOARD_SC_F15:
	case HID_KEYBOARD_SC_F16:
	case HID_KEYBOARD_SC_F17:
	case HID_KEYBOARD_SC_F18:
	case HID_KEYBOARD_SC_F19:
	case HID_KEYBOARD_SC_F20:
	case HID_KEYBOARD_SC_F21:
	case HID_KEYBOARD_SC_F22:
	case HID_KEYBOARD_SC_F23:
	case HID_KEYBOARD_SC_F24:
#ifdef MACRO_RAM_SIZE
		if (g_recording_macro)
			record_stroke(code);
#endif /* MACRO_RAM_SIZE */
		alpha_down(code, action);
		break;
	case HID_KEYBOARD_SC_LOCKING_CAPS_LOCK:
		if (!(g_hid_lock_flags & HID_KEYBOARD_LED_CAPSLOCK))
			queue_autokeys(HID_KEYBOARD_SC_CAPS_LOCK, g_modifier_state);
		break;
	case HID_KEYBOARD_SC_LOCKING_NUM_LOCK:
		if (!(g_hid_lock_flags & HID_KEYBOARD_LED_NUMLOCK))
			queue_autokeys(HID_KEYBOARD_SC_NUM_LOCK, g_modifier_state);
		break;
	case HID_KEYBOARD_SC_LOCKING_SCROLL_LOCK:
		if (!(g_hid_lock_flags & HID_KEYBOARD_LED_SCROLLLOCK))
			queue_autokeys(HID_KEYBOARD_SC_SCROLL_LOCK, g_modifier_state);
		break;
#ifdef MAX_NUMBER_OF_BACKLIGHTS
	case SCANCODE_BL_DIMMER:
		backlight_dimmer();
		break;
	case SCANCODE_BL_MODE:
		backlight_mode();
		break;
	case SCANCODE_BL_ENABLE:
		backlight_enable();
		break;
#else
	case SCANCODE_BL_DIMMER:
		led_dimmer();
		break;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
	case SCANCODE_KEYLOCK:
		g_keylock_flag ^= 1;
		if (g_keylock_flag == 0)
			led_host_off(LED_KB_LOCK);
		else
			led_host_on(LED_KB_LOCK);
		break;
	case SCANCODE_WINLOCK:
		g_winlock_flag ^= 1;
		if (g_winlock_flag == 0)
			led_host_off(LED_WIN_LOCK);
		else
			led_host_on(LED_WIN_LOCK);
		break;
	case SCANCODE_ESCGRAVE:
		break;
	case SCANCODE_POWER:
	case SCANCODE_SLEEP:
	case SCANCODE_WAKE:
		set_power(code);
		break;
	case SCANCODE_BOOT:
		g_reset_requested = RESET_TO_BOOT;
		break;
	case SCANCODE_CONFIG:
		if (g_console_state == CONSOLE_IDLE)
			g_console_state = CONSOLE_MENU_MAIN;
		break;
	case SCANCODE_NEXT_TRACK:
	case SCANCODE_PREV_TRACK:
	case SCANCODE_STOP:
	case SCANCODE_PLAY_PAUSE:
	case SCANCODE_BRIGHT_INC:
	case SCANCODE_BRIGHT_DEC:
	case SCANCODE_MUTE:
	case SCANCODE_BASS_BOOST:
	case SCANCODE_VOL_INC:
	case SCANCODE_VOL_DEC:
	case SCANCODE_BASS_INC:
	case SCANCODE_BASS_DEC:
	case SCANCODE_TREB_INC:
	case SCANCODE_TREB_DEC:
	case SCANCODE_MEDIA_SEL:
	case SCANCODE_MAIL:
	case SCANCODE_CALC:
	case SCANCODE_MYCOMP:
	case SCANCODE_SEARCH:
	case SCANCODE_BROWSER:
	case SCANCODE_BACK:
	case SCANCODE_FORWARD:
	case SCANCODE_WWWSTOP:
	case SCANCODE_REFRESH:
	case SCANCODE_FAVES:
		set_media(code);
		break;
	case SCANCODE_MOUSE1:
	case SCANCODE_MOUSE2:
	case SCANCODE_MOUSE3:
	case SCANCODE_MOUSE4:
	case SCANCODE_MOUSE5:
		set_mousebutton(code);
		break;
	case SCANCODE_MOUSEXR:
		g_mouse_req_X++;
		goto mousemove;
	case SCANCODE_MOUSEXL:
		g_mouse_req_X--;
		goto mousemove;
	case SCANCODE_MOUSEYU:
		g_mouse_req_Y--;
		goto mousemove;
	case SCANCODE_MOUSEYD:
		g_mouse_req_Y++;
	mousemove:
		if ((g_mouse_active == 0) || (g_mouse_multiply < g_double_tap_repeat))
			g_mouse_multiply = g_double_tap_repeat;
		break;
	case SCANCODE_M1:
	case SCANCODE_M2:
	case SCANCODE_M3:
	case SCANCODE_M4:
	case SCANCODE_M5:
	case SCANCODE_M6:
	case SCANCODE_M7:
	case SCANCODE_M8:
	case SCANCODE_M9:
	case SCANCODE_M10:
	case SCANCODE_M11:
	case SCANCODE_M12:
	case SCANCODE_M13:
	case SCANCODE_M14:
	case SCANCODE_M15:
	case SCANCODE_M16:
		play_macro(code);
		break;
#ifdef MACRO_RAM_SIZE
	case SCANCODE_MRAM_RECORD:
		toggle_macro_record();
		break;
	case SCANCODE_MRAM_PLAY:
		if (!g_recording_macro)
			queue_ram_macro(g_ram_macro, g_ram_macro_length);
		break;
#endif /* MACRO_RAM_SIZE */
	case HID_KEYBOARD_SC_LEFT_CONTROL:
	case HID_KEYBOARD_SC_LEFT_SHIFT:
	case HID_KEYBOARD_SC_LEFT_ALT:
	case HID_KEYBOARD_SC_LEFT_GUI:
	case HID_KEYBOARD_SC_RIGHT_CONTROL:
	case HID_KEYBOARD_SC_RIGHT_SHIFT:
	case HID_KEYBOARD_SC_RIGHT_ALT:
	case HID_KEYBOARD_SC_RIGHT_GUI:
		mod_down(code, action);
		break;
	case SCANCODE_FN0:
	case SCANCODE_FN1:
	case SCANCODE_FN2:
	case SCANCODE_FN3:
	case SCANCODE_FN4:
	case SCANCODE_FN5:
	case SCANCODE_FN6:
	case SCANCODE_FN7:
	case SCANCODE_FN8:
	case SCANCODE_FN9:
		fn_down(code, action);
		break;
	default:
		report_event(EVENT_CODE_KEYMAP_INVALID_CODE, code, MODE_UPDATE);
		break;
	}
	
	g_last_keypress = code;
}

void handle_code_deactuate(const uint8_t code, const uint8_t action, const uint8_t tapkey, const uint8_t tap)
{
	const uint8_t modaction = (action & MOD_ACTION_MASK);
		
	if (modaction)
	{
		g_autokey_modifier = 0;
		g_modifier_service = 1;
	}
	
	switch(code)
	{
	case HID_KEYBOARD_SC_A:
	case HID_KEYBOARD_SC_B:
	case HID_KEYBOARD_SC_C:
	case HID_KEYBOARD_SC_D:
	case HID_KEYBOARD_SC_E:
	case HID_KEYBOARD_SC_F:
	case HID_KEYBOARD_SC_G:
	case HID_KEYBOARD_SC_H:
	case HID_KEYBOARD_SC_I:
	case HID_KEYBOARD_SC_J:
	case HID_KEYBOARD_SC_K:
	case HID_KEYBOARD_SC_L:
	case HID_KEYBOARD_SC_M:
	case HID_KEYBOARD_SC_N:
	case HID_KEYBOARD_SC_O:
	case HID_KEYBOARD_SC_P:
	case HID_KEYBOARD_SC_Q:
	case HID_KEYBOARD_SC_R:
	case HID_KEYBOARD_SC_S:
	case HID_KEYBOARD_SC_T:
	case HID_KEYBOARD_SC_U:
	case HID_KEYBOARD_SC_V:
	case HID_KEYBOARD_SC_W:
	case HID_KEYBOARD_SC_X:
	case HID_KEYBOARD_SC_Y:
	case HID_KEYBOARD_SC_Z:
	case HID_KEYBOARD_SC_1_AND_EXCLAMATION:
	case HID_KEYBOARD_SC_2_AND_AT:
	case HID_KEYBOARD_SC_3_AND_HASHMARK:
	case HID_KEYBOARD_SC_4_AND_DOLLAR:
	case HID_KEYBOARD_SC_5_AND_PERCENTAGE:
	case HID_KEYBOARD_SC_6_AND_CARET:
	case HID_KEYBOARD_SC_7_AND_AMPERSAND:
	case HID_KEYBOARD_SC_8_AND_ASTERISK:
	case HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS:
	case HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS:
	case HID_KEYBOARD_SC_ENTER:
	case HID_KEYBOARD_SC_ESCAPE:
	case HID_KEYBOARD_SC_BACKSPACE:
	case HID_KEYBOARD_SC_TAB:
	case HID_KEYBOARD_SC_SPACE:
	case HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE:
	case HID_KEYBOARD_SC_EQUAL_AND_PLUS:
	case HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE:
	case HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE:
	case HID_KEYBOARD_SC_BACKSLASH_AND_PIPE:
	case HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE:
	case HID_KEYBOARD_SC_SEMICOLON_AND_COLON:
	case HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE:
	case HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE:
	case HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN:
	case HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN:
	case HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK:
	case HID_KEYBOARD_SC_CAPS_LOCK:
	case HID_KEYBOARD_SC_F1:
	case HID_KEYBOARD_SC_F2:
	case HID_KEYBOARD_SC_F3:
	case HID_KEYBOARD_SC_F4:
	case HID_KEYBOARD_SC_F5:
	case HID_KEYBOARD_SC_F6:
	case HID_KEYBOARD_SC_F7:
	case HID_KEYBOARD_SC_F8:
	case HID_KEYBOARD_SC_F9:
	case HID_KEYBOARD_SC_F10:
	case HID_KEYBOARD_SC_F11:
	case HID_KEYBOARD_SC_F12:
	case HID_KEYBOARD_SC_PRINT_SCREEN:
	case HID_KEYBOARD_SC_SCROLL_LOCK:
	case HID_KEYBOARD_SC_PAUSE:
	case HID_KEYBOARD_SC_INSERT:
	case HID_KEYBOARD_SC_HOME:
	case HID_KEYBOARD_SC_PAGE_UP:
	case HID_KEYBOARD_SC_DELETE:
	case HID_KEYBOARD_SC_END:
	case HID_KEYBOARD_SC_PAGE_DOWN:
	case HID_KEYBOARD_SC_RIGHT_ARROW:
	case HID_KEYBOARD_SC_LEFT_ARROW:
	case HID_KEYBOARD_SC_DOWN_ARROW:
	case HID_KEYBOARD_SC_UP_ARROW:
	case HID_KEYBOARD_SC_NUM_LOCK:
	case HID_KEYBOARD_SC_KEYPAD_SLASH:
	case HID_KEYBOARD_SC_KEYPAD_ASTERISK:
	case HID_KEYBOARD_SC_KEYPAD_MINUS:
	case HID_KEYBOARD_SC_KEYPAD_PLUS:
	case HID_KEYBOARD_SC_KEYPAD_ENTER:
	case HID_KEYBOARD_SC_KEYPAD_1_AND_END:
	case HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW:
	case HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN:
	case HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW:
	case HID_KEYBOARD_SC_KEYPAD_5:
	case HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW:
	case HID_KEYBOARD_SC_KEYPAD_7_AND_HOME:
	case HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW:
	case HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP:
	case HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT:
	case HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE:
	case HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE:
	case HID_KEYBOARD_SC_APPLICATION:
	case HID_KEYBOARD_SC_POWER:
	case HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN:
	case HID_KEYBOARD_SC_F13:
	case HID_KEYBOARD_SC_F14:
	case HID_KEYBOARD_SC_F15:
	case HID_KEYBOARD_SC_F16:
	case HID_KEYBOARD_SC_F17:
	case HID_KEYBOARD_SC_F18:
	case HID_KEYBOARD_SC_F19:
	case HID_KEYBOARD_SC_F20:
	case HID_KEYBOARD_SC_F21:
	case HID_KEYBOARD_SC_F22:
	case HID_KEYBOARD_SC_F23:
	case HID_KEYBOARD_SC_F24:
		alpha_up(code, action, tapkey, tap);
		break;
	case HID_KEYBOARD_SC_LOCKING_CAPS_LOCK:
		if (g_hid_lock_flags & HID_KEYBOARD_LED_CAPSLOCK)
			queue_autokeys(HID_KEYBOARD_SC_CAPS_LOCK, g_modifier_state);
		break;
	case HID_KEYBOARD_SC_LOCKING_NUM_LOCK:
		if (g_hid_lock_flags & HID_KEYBOARD_LED_NUMLOCK)
			queue_autokeys(HID_KEYBOARD_SC_NUM_LOCK, g_modifier_state);
		break;
	case HID_KEYBOARD_SC_LOCKING_SCROLL_LOCK:
		if (g_hid_lock_flags & HID_KEYBOARD_LED_SCROLLLOCK)
			queue_autokeys(HID_KEYBOARD_SC_SCROLL_LOCK, g_modifier_state);
		break;
	case SCANCODE_BL_DIMMER:
	case SCANCODE_BL_MODE:
	case SCANCODE_BL_ENABLE:
	case SCANCODE_KEYLOCK:
	case SCANCODE_WINLOCK:
		break;
	case SCANCODE_ESCGRAVE:
#ifdef KEYMAP_MEMORY_SAVE
		/* If using keymap memory save, we don't know which was pressed. Just pull 'em both. */
		alpha_up(HID_KEYBOARD_SC_ESCAPE, action, tapkey, tap);
		alpha_up(HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE, action, tapkey, tap);
#endif /* KEYMAP_MEMORY_SAVE */
		break;
	case SCANCODE_POWER:
	case SCANCODE_SLEEP:
	case SCANCODE_WAKE:
		unset_power(code);
		break;
	case SCANCODE_BOOT:
	case SCANCODE_CONFIG:
		break;
	case SCANCODE_NEXT_TRACK:
	case SCANCODE_PREV_TRACK:
	case SCANCODE_STOP:
	case SCANCODE_PLAY_PAUSE:
	case SCANCODE_BRIGHT_INC:
	case SCANCODE_BRIGHT_DEC:
	case SCANCODE_MUTE:
	case SCANCODE_BASS_BOOST:
	case SCANCODE_VOL_INC:
	case SCANCODE_VOL_DEC:
	case SCANCODE_BASS_INC:
	case SCANCODE_BASS_DEC:
	case SCANCODE_TREB_INC:
	case SCANCODE_TREB_DEC:
	case SCANCODE_MEDIA_SEL:
	case SCANCODE_MAIL:
	case SCANCODE_CALC:
	case SCANCODE_MYCOMP:
	case SCANCODE_SEARCH:
	case SCANCODE_BROWSER:
	case SCANCODE_BACK:
	case SCANCODE_FORWARD:
	case SCANCODE_WWWSTOP:
	case SCANCODE_REFRESH:
	case SCANCODE_FAVES:
		unset_media(code);
		break;
	case SCANCODE_MOUSE1:
	case SCANCODE_MOUSE2:
	case SCANCODE_MOUSE3:
	case SCANCODE_MOUSE4:
	case SCANCODE_MOUSE5:
		unset_mousebutton(code);
		break;
	case SCANCODE_MOUSEXR:
		g_mouse_req_X--;
		break;
	case SCANCODE_MOUSEXL:
		g_mouse_req_X++;
		break;
	case SCANCODE_MOUSEYU:
		g_mouse_req_Y++;
		break;
	case SCANCODE_MOUSEYD:
		g_mouse_req_Y--;
		break;
	case SCANCODE_M1:
	case SCANCODE_M2:
	case SCANCODE_M3:
	case SCANCODE_M4:
	case SCANCODE_M5:
	case SCANCODE_M6:
	case SCANCODE_M7:
	case SCANCODE_M8:
	case SCANCODE_M9:
	case SCANCODE_M10:
	case SCANCODE_M11:
	case SCANCODE_M12:
	case SCANCODE_M13:
	case SCANCODE_M14:
	case SCANCODE_M15:
	case SCANCODE_M16:
	case SCANCODE_MRAM_RECORD:
	case SCANCODE_MRAM_PLAY:
		break;
	case HID_KEYBOARD_SC_LEFT_CONTROL:
	case HID_KEYBOARD_SC_LEFT_SHIFT:
	case HID_KEYBOARD_SC_LEFT_ALT:
	case HID_KEYBOARD_SC_LEFT_GUI:
	case HID_KEYBOARD_SC_RIGHT_CONTROL:
	case HID_KEYBOARD_SC_RIGHT_SHIFT:
	case HID_KEYBOARD_SC_RIGHT_ALT:
	case HID_KEYBOARD_SC_RIGHT_GUI:
#ifdef MACRO_RAM_SIZE
		if ((g_recording_macro) && (g_last_keypress == code))
			record_stroke(0);
#endif /* MACRO_RAM_SIZE */
		mod_up(code, action, tapkey, tap);
		break;
	case SCANCODE_FN0:
	case SCANCODE_FN1:
	case SCANCODE_FN2:
	case SCANCODE_FN3:
	case SCANCODE_FN4:
	case SCANCODE_FN5:
	case SCANCODE_FN6:
	case SCANCODE_FN7:
	case SCANCODE_FN8:
	case SCANCODE_FN9:
		fn_up(code, action, tapkey, tap);
		break;
	default:
		report_event(EVENT_CODE_KEYMAP_LOST_CODE, code, MODE_UPDATE);
		break;
	}
}

#ifndef SIMPLE_DEVICE
uint8_t translate_code(uint8_t code)
{
	const uint8_t noshift = ((g_modifier_state & 0x22) == 0);
	
	/* I'm thinking a translation table might be better for this, so I can also get
	   things like Enter, plus, minus, and dot.  Maybe its own layer */
	if ( (g_swap_num_row_on_numlock) && (noshift) &&
	     (g_hid_lock_flags & HID_KEYBOARD_LED_NUMLOCK) &&
		 (code >= HID_KEYBOARD_SC_1_AND_EXCLAMATION) &&
		 (code <= HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS) )
	{
		code += (HID_KEYBOARD_SC_KEYPAD_1_AND_END-HID_KEYBOARD_SC_1_AND_EXCLAMATION);
	}
	
	if (g_virtual_numlock)
	{
		if (code == HID_KEYBOARD_SC_NUM_LOCK)
		{
			code = 0;
			g_hid_lock_flags ^= HID_KEYBOARD_LED_NUMLOCK;
			if (g_hid_lock_flags & HID_KEYBOARD_LED_NUMLOCK)
				led_host_on(LED_NUM_LOCK);
			else
				led_host_off(LED_NUM_LOCK);
		}
		else if ( (code >= HID_KEYBOARD_SC_KEYPAD_1_AND_END) &&
		          (code <= HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE) )
		{
			if ((g_hid_lock_flags & HID_KEYBOARD_LED_NUMLOCK) && (noshift))
				code = pgm_read_byte(&KP_MAP[code-HID_KEYBOARD_SC_KEYPAD_1_AND_END].numcode);
			else
				code = pgm_read_byte(&KP_MAP[code-HID_KEYBOARD_SC_KEYPAD_1_AND_END].navcode);
		}
	}
	
	if (code == SCANCODE_ESCGRAVE)
	{
		if (noshift)
			code = HID_KEYBOARD_SC_ESCAPE;
		else
			code = HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE;
	}
	
	return code;
}
#endif /* SIMPLE_DEVICE */

void keymap_actuate(const uint8_t row, const uint8_t col, const int16_t idle_time)
{
#ifdef SIMPLE_DEVICE
	const uint8_t code = getmap(row,col);
#else
	const uint8_t code = translate_code(getmap(row,col));
#endif /* SIMPLE_DEVICE */
	const uint8_t action = getaction(row,col);
	const uint8_t tapkey = gettapkey(row,col);
	
#ifdef KEYMAP_MEMORY_SAVE
	g_matrixlayer[row][col] = g_layer_select;
#else
	g_matrixcode[row][col] = code;
	g_matrixaction[row][col] = action;
	g_matrixtapkey[row][col] = tapkey;
#endif /* KEYMAP_MEMORY_SAVE */
	
	doubletap_down(row,col,idle_time);
	
	handle_code_actuate(code, action, tapkey);

#ifdef MAX_NUMBER_OF_BACKLIGHTS
	backlight_react();
#endif /* MAX_NUMBER_OF_BACKLIGHTS */

	USB_wakeup();
}

void keymap_deactuate(const uint8_t row, const uint8_t col, const int16_t hold_time)
{
#ifdef KEYMAP_MEMORY_SAVE
	const uint8_t layer = g_matrixlayer[row][col];
	const uint8_t code = pgm_read_byte(&LAYERS[layer][row][col]);
	const uint8_t action = pgm_read_byte(&ACTIONS[layer][row][col]);
	const uint8_t tapkey = pgm_read_byte(&TAPKEYS[layer][row][col]);
#else
	const uint8_t code = g_matrixcode[row][col];
	const uint8_t action = g_matrixaction[row][col];
	const uint8_t tapkey = g_matrixtapkey[row][col];
#endif /* KEYMAP_MEMORY_SAVE */
	uint8_t tap;
	
	doubletap_up(row,col,hold_time, &tap);
	
	handle_code_deactuate(code, action, tapkey, tap);

#ifdef KEYMAP_MEMORY_SAVE
	g_matrixlayer[row][col] = 0;
#else
	g_matrixcode[row][col] = 0;
	g_matrixaction[row][col] = 0;
	g_matrixtapkey[row][col] = 0;
#endif /* KEYMAP_MEMORY_SAVE */
}

void keymap_interrupt(const uint8_t row, const uint8_t col)
{
#ifdef KEYMAP_MEMORY_SAVE
	const uint8_t layer = g_matrixlayer[row][col];
	const uint8_t code = pgm_read_byte(&LAYERS[layer][row][col]);
	const uint8_t action = pgm_read_byte(&ACTIONS[layer][row][col]);
#else
	const uint8_t code = g_matrixcode[row][col];
	const uint8_t action = g_matrixaction[row][col];
#endif /* KEYMAP_MEMORY_SAVE */
	
	if (action & ACTION_RAPIDFIRE)
	{
		send_tapkey(code);
	}
}

void get_keyboard_report(uint8_t * const buffer)
{
	if (g_keylock_flag)
		return;
	
	/* Skip the for loop, HID_ROLLOVER_SIZE is always 6 */
	if (g_rollover_error)
	{
		buffer[0] = HID_KEYBOARD_SC_ERROR_ROLLOVER;
		buffer[1] = HID_KEYBOARD_SC_ERROR_ROLLOVER;
		buffer[2] = HID_KEYBOARD_SC_ERROR_ROLLOVER;
		buffer[3] = HID_KEYBOARD_SC_ERROR_ROLLOVER;
		buffer[4] = HID_KEYBOARD_SC_ERROR_ROLLOVER;
		buffer[5] = HID_KEYBOARD_SC_ERROR_ROLLOVER;
	}
	else
	{
		buffer[0] = g_report_buffer[0];
		buffer[1] = g_report_buffer[1];
		buffer[2] = g_report_buffer[2];
		buffer[3] = g_report_buffer[3];
		buffer[4] = g_report_buffer[4];
		buffer[5] = g_report_buffer[5];
	}
}

void get_nkro_report(uint8_t * const buffer)
{
	uint8_t i;
	
	if (g_keylock_flag)
		return;
	
	for (i=0; i<NKRO_ARRAY_LENGTH; i++)
	{
		buffer[i] = g_nkro_field[i];
	}
}

void get_modifier_report(uint8_t * const buffer)
{
	if (g_keylock_flag)
		return;
	
	*buffer = (g_modifier_state | g_autokey_modifier);
}

void initial_actuate(const uint8_t row, const uint8_t col)
{
#ifndef SIMPLE_DEVICE
	const uint8_t code = pgm_read_byte(&LAYERS[0][row][col]);
	
	if ((code == HID_KEYBOARD_SC_ENTER) ||
	    (code == HID_KEYBOARD_SC_KEYPAD_ENTER))
	{
		report_event(EVENT_CODE_NVM_ERASE_SETTINGS, 0, MODE_REOCCUR);
		nvm_init_eeprom();
	}
#endif /* SIMPLE_DEVICE */
}

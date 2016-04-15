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

#include "scheduler.h"
#include "keymap.h"
#include "autokey.h"

uint8_t g_keyboard_service;
uint16_t const * g_macro_waiting;
uint16_t * g_ram_macro_waiting;
char const * g_autotext_waiting;
uint8_t g_autokey_status;
uint8_t g_autokey_buffer;
uint8_t g_autokey_modifier;
uint16_t g_send_buffer[SEND_BUFFER_SIZE];
uint8_t g_send_buffer_length;
uint8_t g_send_buffer_pos;
uint8_t g_send_wait;
uint8_t g_read_buffer[READ_BUFFER_SIZE];
uint8_t g_read_buffer_length;
uint8_t g_read_key_last;

void init_autokey(void)
{
	g_macro_waiting = (uint16_t*)0;
	g_ram_macro_waiting = (uint16_t*)0;
	g_autotext_waiting = (char*)0;
}

void autokey_send(void)
{
	union16_t code;
	
	/* Check if we still have work to do */
	if (g_send_buffer_length != 0)
	{
		/* Wait for the last keystroke to get sent */
		if (!g_keyboard_service)
		{
			/* Check for a pause action */
			if (g_send_wait == 0)
			{
				/* Make sure that every key comes up to allow for repeated keystrokes */
				if (g_autokey_buffer == 0)
				{
					/* Check to see if we're done */
					if (g_send_buffer_pos == g_send_buffer_length)
					{
						g_send_buffer_pos = g_send_buffer_length = 0;
					} else {
						/* The modifiers are kept in the upper byte */
						code.word = g_send_buffer[g_send_buffer_pos++];
						if (code.bytes.lsb == 1)
						{
							/* This is a wait, and the mod is a delay count */
							g_send_wait = code.bytes.msb;
						} else {
							g_autokey_modifier = code.bytes.msb;
							g_autokey_buffer = code.bytes.lsb;
							if (g_autokey_buffer)
								enqueue_key(g_autokey_buffer);
						}
					}
				} else {
					if (g_autokey_buffer)
						delete_key(g_autokey_buffer);
					g_autokey_buffer = 0;
				}
			} else {
				/* Wait for a pause action to time out */
				g_send_wait -= 1;
			}
		}
	} else {
		/* Wait for the final keystroke to get sent */
		if (!g_keyboard_service)
		{
			g_autokey_modifier = 0;
			g_autokey_status = AUTOKEY_ENDSEND;
		}
	}
	/* We have seen that the USB has taken a report */
	if (!g_keyboard_service)
		g_keyboard_service = 1;
}

void autokey_read(void)
{
	const uint8_t code = g_report_buffer[0];
	/* Check to see if there is something new to record */
	if (g_read_key_last != code)
	{
		g_read_key_last = code;
		if (code == 0)
			return;
		if ((code == HID_KEYBOARD_SC_ENTER) ||
		    (code == HID_KEYBOARD_SC_KEYPAD_ENTER))
		{
			g_autokey_status = AUTOKEY_ENDREAD;
			return;
		}
		if (code == HID_KEYBOARD_SC_BACKSPACE)
		{
			if (g_read_buffer_length > 0)
			{
				g_read_buffer_length--;
				g_read_buffer[g_read_buffer_length] = 0;
			}
			return;
		}
		if (g_read_buffer_length < READ_BUFFER_SIZE)
		{
			/* I only check the zeroth spot, so it is actually possible to miss something */
			g_read_buffer[g_read_buffer_length] = code;
			g_read_buffer_length++;
		}
	}
}

void autokey_setidle(void)
{
	if (g_report_buffer[0] == 0)
		g_autokey_status = AUTOKEY_IDLE;
}

void autokey_cycle(void)
{
	if (g_autokey_status & AUTOKEY_SENDING)
		autokey_send();
	else if (g_macro_waiting != (uint16_t*)0)
		queue_macro(g_macro_waiting);
#ifdef MACRO_RAM_SIZE
	else if (g_ram_macro_waiting != (uint16_t*)0)
		queue_ram_macro(g_ram_macro_waiting, g_ram_macro_ptr);
#endif /* MACRO_RAM_SIZE */
#ifndef SIMPLE_DEVICE
	else if (g_autotext_waiting != (char*)0)
		queue_autotext(g_autotext_waiting);
#endif /* SIMPLE_DEVICE */
	else if (g_autokey_status & AUTOKEY_READING)
		autokey_read();
	else
		autokey_setidle();
}

uint8_t queue_autotext(char const * const str)
{
	int8_t i;
	char c;
	
	for (i=0; ; i++)
	{
		if (g_send_buffer_length >= SEND_BUFFER_SIZE)
		{
			g_autotext_waiting = &str[i];
			break;
		}
		c = pgm_read_word(&str[i]);
		if (c == 0)
		{
			g_autotext_waiting = (char*)0;
			break;
		}
		g_send_buffer[g_send_buffer_length] = char_to_sc(c);
		g_send_buffer_length++;
	}
	if (g_send_buffer_length > 0)
		g_autokey_status = AUTOKEY_SETSEND;
	return 1;
}

uint8_t queue_ram_autotext(char * const str, size_t const len)
{
	int8_t i;
	
	if (len > (SEND_BUFFER_SIZE - g_send_buffer_length))
		return 0;
	for (i=0; i<len; i++)
	{
		g_send_buffer[g_send_buffer_length] = char_to_sc(str[i]);
		g_send_buffer_length++;
	}
	if (len > 0)
		g_autokey_status = AUTOKEY_SETSEND;
	return 1;
}

uint8_t queue_autokeys(uint8_t const key, uint8_t const mod)
{
	union16_t val;
	
	if (g_send_buffer_length >= SEND_BUFFER_SIZE)
		return 0;
	val.bytes.msb = mod;
	val.bytes.lsb = key;
	g_send_buffer[g_send_buffer_length] = val.word;
	g_send_buffer_length++;
	g_autokey_status = AUTOKEY_SETSEND;
	return 1;
}

uint8_t queue_macro(uint16_t const * const macro)
{
	int8_t i;
	uint16_t w;
	
	if (g_send_buffer_length != 0)
		return 0;
	for(i=0; ; i++)
	{
		if (g_send_buffer_length >= SEND_BUFFER_SIZE)
		{
			g_macro_waiting = &macro[i];
			break;
		}
		w = pgm_read_word(&macro[i]);
		if (w == 0)
		{
			g_macro_waiting = (uint16_t*)0;
			break;
		}
		g_send_buffer[g_send_buffer_length] = w;
		g_send_buffer_length++;
	}
	if (g_send_buffer_length > 0)
		g_autokey_status = AUTOKEY_SETSEND;
	return 1;
}

#ifdef MACRO_RAM_SIZE
uint8_t queue_ram_macro(uint16_t * const macro, size_t const len)
{
	int8_t i;
	
	if (g_send_buffer_length != 0)
		return 0;
	g_ram_macro_ptr = len;
	for (i=0; i<len; i++)
	{
		if (g_send_buffer_length >= SEND_BUFFER_SIZE)
		{
			g_ram_macro_waiting = &macro[i];
			break;
		}
		g_send_buffer[g_send_buffer_length] = macro[i];
		g_send_buffer_length++;
		g_ram_macro_ptr--;
		if (g_ram_macro_ptr == 0)
		{
			g_ram_macro_waiting = (uint16_t*)0;
			break;
		}
	}
	if (g_send_buffer_length > 0)
		g_autokey_status = AUTOKEY_SETSEND;
	return 1;
}
#endif

void begin_read(void)
{
	int8_t i;
	
	for (i=0; i<READ_BUFFER_SIZE; i++)
		g_read_buffer[i] = 0;
	g_read_buffer_length = 0;
	g_read_key_last = g_report_buffer[0];
	g_autokey_status = AUTOKEY_SETREAD;
}

#define ASCII_SHIFT (HID_KEYBOARD_MODIFIER_LEFTSHIFT << 8)
static const uint16_t PROGMEM asciitable[128] = {
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	HID_KEYBOARD_SC_BACKSPACE,
	HID_KEYBOARD_SC_TAB,
	HID_KEYBOARD_SC_ENTER,
	0x00,
	0x00,
	HID_KEYBOARD_SC_ENTER,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	HID_KEYBOARD_SC_ESCAPE,
	0x00,
	0x00,
	0x00,
	0x00,
	HID_KEYBOARD_SC_SPACE,
	(ASCII_SHIFT | HID_KEYBOARD_SC_1_AND_EXCLAMATION),
	(ASCII_SHIFT | HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE),
	(ASCII_SHIFT | HID_KEYBOARD_SC_3_AND_HASHMARK),
	(ASCII_SHIFT | HID_KEYBOARD_SC_4_AND_DOLLAR),
	(ASCII_SHIFT | HID_KEYBOARD_SC_5_AND_PERCENTAGE),
	(ASCII_SHIFT | HID_KEYBOARD_SC_7_AND_AMPERSAND),
	HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE,
	(ASCII_SHIFT | HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS),
	(ASCII_SHIFT | HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS),
	(ASCII_SHIFT | HID_KEYBOARD_SC_8_AND_ASTERISK),
	(ASCII_SHIFT | HID_KEYBOARD_SC_EQUAL_AND_PLUS),
	HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN,
	HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE,
	HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN,
	HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK,
	HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS,
	HID_KEYBOARD_SC_1_AND_EXCLAMATION,
	HID_KEYBOARD_SC_2_AND_AT,
	HID_KEYBOARD_SC_3_AND_HASHMARK,
	HID_KEYBOARD_SC_4_AND_DOLLAR,
	HID_KEYBOARD_SC_5_AND_PERCENTAGE,
	HID_KEYBOARD_SC_6_AND_CARET,
	HID_KEYBOARD_SC_7_AND_AMPERSAND,
	HID_KEYBOARD_SC_8_AND_ASTERISK,
	HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS,
	(ASCII_SHIFT | HID_KEYBOARD_SC_SEMICOLON_AND_COLON),
	HID_KEYBOARD_SC_SEMICOLON_AND_COLON,
	(ASCII_SHIFT | HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN),
	HID_KEYBOARD_SC_EQUAL_AND_PLUS,
	(ASCII_SHIFT | HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN),
	(ASCII_SHIFT | HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK),
	(ASCII_SHIFT | HID_KEYBOARD_SC_2_AND_AT),
	(ASCII_SHIFT | HID_KEYBOARD_SC_A),
	(ASCII_SHIFT | HID_KEYBOARD_SC_B),
	(ASCII_SHIFT | HID_KEYBOARD_SC_C),
	(ASCII_SHIFT | HID_KEYBOARD_SC_D),
	(ASCII_SHIFT | HID_KEYBOARD_SC_E),
	(ASCII_SHIFT | HID_KEYBOARD_SC_F),
	(ASCII_SHIFT | HID_KEYBOARD_SC_G),
	(ASCII_SHIFT | HID_KEYBOARD_SC_H),
	(ASCII_SHIFT | HID_KEYBOARD_SC_I),
	(ASCII_SHIFT | HID_KEYBOARD_SC_J),
	(ASCII_SHIFT | HID_KEYBOARD_SC_K),
	(ASCII_SHIFT | HID_KEYBOARD_SC_L),
	(ASCII_SHIFT | HID_KEYBOARD_SC_M),
	(ASCII_SHIFT | HID_KEYBOARD_SC_N),
	(ASCII_SHIFT | HID_KEYBOARD_SC_O),
	(ASCII_SHIFT | HID_KEYBOARD_SC_P),
	(ASCII_SHIFT | HID_KEYBOARD_SC_Q),
	(ASCII_SHIFT | HID_KEYBOARD_SC_R),
	(ASCII_SHIFT | HID_KEYBOARD_SC_S),
	(ASCII_SHIFT | HID_KEYBOARD_SC_T),
	(ASCII_SHIFT | HID_KEYBOARD_SC_U),
	(ASCII_SHIFT | HID_KEYBOARD_SC_V),
	(ASCII_SHIFT | HID_KEYBOARD_SC_W),
	(ASCII_SHIFT | HID_KEYBOARD_SC_X),
	(ASCII_SHIFT | HID_KEYBOARD_SC_Y),
	(ASCII_SHIFT | HID_KEYBOARD_SC_Z),
	HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE,
	HID_KEYBOARD_SC_BACKSLASH_AND_PIPE,
	HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE,
	(ASCII_SHIFT | HID_KEYBOARD_SC_6_AND_CARET),
	(ASCII_SHIFT | HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE),
	HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE,
	HID_KEYBOARD_SC_A,
	HID_KEYBOARD_SC_B,
	HID_KEYBOARD_SC_C,
	HID_KEYBOARD_SC_D,
	HID_KEYBOARD_SC_E,
	HID_KEYBOARD_SC_F,
	HID_KEYBOARD_SC_G,
	HID_KEYBOARD_SC_H,
	HID_KEYBOARD_SC_I,
	HID_KEYBOARD_SC_J,
	HID_KEYBOARD_SC_K,
	HID_KEYBOARD_SC_L,
	HID_KEYBOARD_SC_M,
	HID_KEYBOARD_SC_N,
	HID_KEYBOARD_SC_O,
	HID_KEYBOARD_SC_P,
	HID_KEYBOARD_SC_Q,
	HID_KEYBOARD_SC_R,
	HID_KEYBOARD_SC_S,
	HID_KEYBOARD_SC_T,
	HID_KEYBOARD_SC_U,
	HID_KEYBOARD_SC_V,
	HID_KEYBOARD_SC_W,
	HID_KEYBOARD_SC_X,
	HID_KEYBOARD_SC_Y,
	HID_KEYBOARD_SC_Z,
	(ASCII_SHIFT | HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE),
	(ASCII_SHIFT | HID_KEYBOARD_SC_BACKSLASH_AND_PIPE),
	(ASCII_SHIFT | HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE),
	(ASCII_SHIFT | HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE),
	HID_KEYBOARD_SC_DELETE
};

uint16_t char_to_sc(char const c)
{
	return pgm_read_word(&asciitable[(uint8_t)c]);
}

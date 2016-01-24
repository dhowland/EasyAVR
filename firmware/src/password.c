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

#include "keymap.h"
#include "autokey.h"
#include "password.h"

#ifdef MACRO_RAM_SIZE

const char PROGMEM CDATA[] = "abcdefghijklmnopqrstuvwxyz"
                             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                             "0123456789"
                             "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";

uint8_t g_pw_state;
uint8_t g_pw_pos;
//uint8_t g_pw_iter;
#define g_pw_iter g_ram_macro_ptr
phase_t g_pw_phase;
int8_t g_pw_select;

void init_password(void)
{
	g_pw_phase = PHASE_COMPLETE;
}

void password_cycle(void)
{
	if (g_pw_phase != PHASE_COMPLETE)
	{
		scramble();
	}
}

void updatestate(void)
{
	pwdefs_t const * pwdef = &PWDEFS[g_pw_select];
	uint8_t pi = g_pw_iter % g_ram_macro_length;
	uint8_t si = g_pw_iter % pgm_read_byte(&pwdef->scrambler_len);
	
	g_pw_state = g_pw_state + sc_to_char(g_ram_macro[pi]);
	if (g_pw_state & 0x80)
		g_pw_state = (g_pw_state << 1) + 1;
	else
		g_pw_state = g_pw_state << 1;
	g_pw_state = g_pw_state ^ pgm_read_byte(&pwdef->scrambler[si]);
}

char getcdata(void)
{
	int8_t i;
	uint8_t len = 0;
	pwdefs_t const * pwdef = &PWDEFS[g_pw_select];
	uint8_t use_lowers = pgm_read_byte(&pwdef->use_lowers);
	uint8_t use_uppers = pgm_read_byte(&pwdef->use_uppers);
	uint8_t use_numbers = pgm_read_byte(&pwdef->use_numbers);
	uint8_t use_symbols = pgm_read_byte(&pwdef->use_symbols);
	
	switch(g_pw_iter)
	{
		case 0:
			if (use_lowers)
			{
				i = g_pw_state % LOWERS_LEN;
				break;
			}
		case 1:
			if (use_uppers)
			{
				i = (g_pw_state % UPPERS_LEN) + LOWERS_END;
				break;
			}
		case 2:
			if (use_numbers)
			{
				i = (g_pw_state % NUMBERS_LEN) + UPPERS_END;
				break;
			}
		case 3:
			if (use_symbols)
			{
				i = (g_pw_state % SYMBOLS_LEN) + NUMBERS_END;
				break;
			}
		default:
			if (use_lowers) len += LOWERS_LEN;
			if (use_uppers) len += UPPERS_LEN;
			if (use_numbers) len += NUMBERS_LEN;
			if (use_symbols) len += SYMBOLS_LEN;
			i = g_pw_state % len;
			if (!use_lowers)
				i += LOWERS_LEN;
			if ((!use_uppers) && (i >= LOWERS_END))
				i += UPPERS_LEN;
			if ((!use_numbers) && (i >= UPPERS_END))
				i += NUMBERS_LEN;
			break;
	}
	return pgm_read_byte(&CDATA[i]);
}

void scramble(void)
{
	pwdefs_t const * pwdef = &PWDEFS[g_pw_select];
	uint8_t output_len = pgm_read_byte(&pwdef->output_len);
	uint16_t * outbuf = &g_ram_macro[MACRO_RAM_SIZE - output_len];
	
	switch(g_pw_phase)
	{
		case PHASE_INIT:
			g_pw_state = 0;
			g_pw_phase = PHASE_STATE;
			g_pw_iter = 0;
			if (0 == pgm_read_byte(&pwdef->scrambler_len))
				g_pw_phase = PHASE_COMPLETE;
			break;
		case PHASE_STATE:
			g_pw_state = (g_pw_state + pgm_read_byte(&pwdef->scrambler[g_pw_iter]));
			g_pw_iter++;
			if (g_pw_iter >= pgm_read_byte(&pwdef->scrambler_len))
			{
				g_pw_phase = PHASE_POS;
				g_pw_iter = 0;
				g_pw_pos = g_pw_state;
			}
			break;
		case PHASE_POS:
			g_pw_pos = (g_pw_pos + sc_to_char(g_ram_macro[g_pw_iter]));
			g_pw_iter++;
			if (g_pw_iter >= g_ram_macro_length)
			{
				g_pw_pos = g_pw_pos % output_len;
				g_pw_phase = PHASE_SCRAMBLE;
				g_pw_iter = 0;
			}
			break;
		case PHASE_SCRAMBLE:
			updatestate();
			outbuf[g_pw_pos] = char_to_sc(getcdata());
			g_pw_pos = (g_pw_pos + 1) % output_len;
			g_pw_iter++;
			if (g_pw_iter >= output_len)
			{
				g_pw_phase = PHASE_MOVE;
				g_pw_iter = 0;
			}
			break;
		case PHASE_MOVE:
			g_ram_macro[g_pw_iter] = outbuf[g_pw_iter];
			g_pw_iter++;
			if (g_pw_iter >= output_len)
			{
				g_pw_phase = PHASE_COMPLETE;
				g_ram_macro_length = output_len;
				queue_ram_macro(g_ram_macro, output_len);
			}
			break;
		default:
			break;
	}
}

typedef struct {
	const char unshifted;
	const char shifted;
} ascii_t;

static const ascii_t PROGMEM antiasciitable[] = {
	/* HID_KEYBOARD_SC_A                                 */	{'a', 'A'},
	/* HID_KEYBOARD_SC_B                                 */	{'b', 'B'},
	/* HID_KEYBOARD_SC_C                                 */	{'c', 'C'},
	/* HID_KEYBOARD_SC_D                                 */	{'d', 'D'},
	/* HID_KEYBOARD_SC_E                                 */	{'e', 'E'},
	/* HID_KEYBOARD_SC_F                                 */	{'f', 'F'},
	/* HID_KEYBOARD_SC_G                                 */	{'g', 'G'},
	/* HID_KEYBOARD_SC_H                                 */	{'h', 'H'},
	/* HID_KEYBOARD_SC_I                                 */	{'i', 'I'},
	/* HID_KEYBOARD_SC_J                                 */	{'j', 'J'},
	/* HID_KEYBOARD_SC_K                                 */	{'k', 'K'},
	/* HID_KEYBOARD_SC_L                                 */	{'l', 'L'},
	/* HID_KEYBOARD_SC_M                                 */	{'m', 'M'},
	/* HID_KEYBOARD_SC_N                                 */	{'n', 'N'},
	/* HID_KEYBOARD_SC_O                                 */	{'o', 'O'},
	/* HID_KEYBOARD_SC_P                                 */	{'p', 'P'},
	/* HID_KEYBOARD_SC_Q                                 */	{'q', 'Q'},
	/* HID_KEYBOARD_SC_R                                 */	{'r', 'R'},
	/* HID_KEYBOARD_SC_S                                 */	{'s', 'S'},
	/* HID_KEYBOARD_SC_T                                 */	{'t', 'T'},
	/* HID_KEYBOARD_SC_U                                 */	{'u', 'U'},
	/* HID_KEYBOARD_SC_V                                 */	{'v', 'V'},
	/* HID_KEYBOARD_SC_W                                 */	{'w', 'W'},
	/* HID_KEYBOARD_SC_X                                 */	{'x', 'X'},
	/* HID_KEYBOARD_SC_Y                                 */	{'y', 'Y'},
	/* HID_KEYBOARD_SC_Z                                 */	{'z', 'Z'},
	/* HID_KEYBOARD_SC_1_AND_EXCLAMATION                 */	{'1', '!'},
	/* HID_KEYBOARD_SC_2_AND_AT                          */	{'2', '@'},
	/* HID_KEYBOARD_SC_3_AND_HASHMARK                    */	{'3', '#'},
	/* HID_KEYBOARD_SC_4_AND_DOLLAR                      */	{'4', '$'},
	/* HID_KEYBOARD_SC_5_AND_PERCENTAGE                  */	{'5', '%'},
	/* HID_KEYBOARD_SC_6_AND_CARET                       */	{'6', '^'},
	/* HID_KEYBOARD_SC_7_AND_AMPERSAND                   */	{'7', '&'},
	/* HID_KEYBOARD_SC_8_AND_ASTERISK                    */	{'8', '*'},
	/* HID_KEYBOARD_SC_9_AND_OPENING_PARENTHESIS         */	{'9', '('},
	/* HID_KEYBOARD_SC_0_AND_CLOSING_PARENTHESIS         */	{'0', ')'},
	/* HID_KEYBOARD_SC_ENTER                             */	{0, 0},
	/* HID_KEYBOARD_SC_ESCAPE                            */	{0, 0},
	/* HID_KEYBOARD_SC_BACKSPACE                         */	{0, 0},
	/* HID_KEYBOARD_SC_TAB                               */	{0, 0},
	/* HID_KEYBOARD_SC_SPACE                             */	{' ', ' '},
	/* HID_KEYBOARD_SC_MINUS_AND_UNDERSCORE              */	{'-', '_'},
	/* HID_KEYBOARD_SC_EQUAL_AND_PLUS                    */	{'=', '+'},
	/* HID_KEYBOARD_SC_OPENING_BRACKET_AND_OPENING_BRACE */	{'[', '{'},
	/* HID_KEYBOARD_SC_CLOSING_BRACKET_AND_CLOSING_BRACE */	{']', '}'},
	/* HID_KEYBOARD_SC_BACKSLASH_AND_PIPE                */	{'\\', '|'},
	/* HID_KEYBOARD_SC_NON_US_HASHMARK_AND_TILDE         */	{'#', '~'},
	/* HID_KEYBOARD_SC_SEMICOLON_AND_COLON               */	{';', ':'},
	/* HID_KEYBOARD_SC_APOSTROPHE_AND_QUOTE              */	{'\'', '"'},
	/* HID_KEYBOARD_SC_GRAVE_ACCENT_AND_TILDE            */	{'`', '~'},
	/* HID_KEYBOARD_SC_COMMA_AND_LESS_THAN_SIGN          */	{',', '<'},
	/* HID_KEYBOARD_SC_DOT_AND_GREATER_THAN_SIGN         */	{'.', '>'},
	/* HID_KEYBOARD_SC_SLASH_AND_QUESTION_MARK           */	{'/', '?'},
	/* HID_KEYBOARD_SC_CAPS_LOCK                         */	{0, 0},
	/* HID_KEYBOARD_SC_F1                                */	{0, 0},
	/* HID_KEYBOARD_SC_F2                                */	{0, 0},
	/* HID_KEYBOARD_SC_F3                                */	{0, 0},
	/* HID_KEYBOARD_SC_F4                                */	{0, 0},
	/* HID_KEYBOARD_SC_F5                                */	{0, 0},
	/* HID_KEYBOARD_SC_F6                                */	{0, 0},
	/* HID_KEYBOARD_SC_F7                                */	{0, 0},
	/* HID_KEYBOARD_SC_F8                                */	{0, 0},
	/* HID_KEYBOARD_SC_F9                                */	{0, 0},
	/* HID_KEYBOARD_SC_F10                               */	{0, 0},
	/* HID_KEYBOARD_SC_F11                               */	{0, 0},
	/* HID_KEYBOARD_SC_F12                               */	{0, 0},
	/* HID_KEYBOARD_SC_PRINT_SCREEN                      */	{0, 0},
	/* HID_KEYBOARD_SC_SCROLL_LOCK                       */	{0, 0},
	/* HID_KEYBOARD_SC_PAUSE                             */	{0, 0},
	/* HID_KEYBOARD_SC_INSERT                            */	{0, 0},
	/* HID_KEYBOARD_SC_HOME                              */	{0, 0},
	/* HID_KEYBOARD_SC_PAGE_UP                           */	{0, 0},
	/* HID_KEYBOARD_SC_DELETE                            */	{0, 0},
	/* HID_KEYBOARD_SC_END                               */	{0, 0},
	/* HID_KEYBOARD_SC_PAGE_DOWN                         */	{0, 0},
	/* HID_KEYBOARD_SC_RIGHT_ARROW                       */	{0, 0},
	/* HID_KEYBOARD_SC_LEFT_ARROW                        */	{0, 0},
	/* HID_KEYBOARD_SC_DOWN_ARROW                        */	{0, 0},
	/* HID_KEYBOARD_SC_UP_ARROW                          */	{0, 0},
	/* HID_KEYBOARD_SC_NUM_LOCK                          */	{0, 0},
	/* HID_KEYBOARD_SC_KEYPAD_SLASH                      */	{'/', '/'},
	/* HID_KEYBOARD_SC_KEYPAD_ASTERISK                   */	{'*', '*'},
	/* HID_KEYBOARD_SC_KEYPAD_MINUS                      */	{'-', '-'},
	/* HID_KEYBOARD_SC_KEYPAD_PLUS                       */	{'+', '+'},
	/* HID_KEYBOARD_SC_KEYPAD_ENTER                      */	{0, 0},
	/* HID_KEYBOARD_SC_KEYPAD_1_AND_END                  */	{'1', 0},
	/* HID_KEYBOARD_SC_KEYPAD_2_AND_DOWN_ARROW           */	{'2', 0},
	/* HID_KEYBOARD_SC_KEYPAD_3_AND_PAGE_DOWN            */	{'3', 0},
	/* HID_KEYBOARD_SC_KEYPAD_4_AND_LEFT_ARROW           */	{'4', 0},
	/* HID_KEYBOARD_SC_KEYPAD_5                          */	{'5', 0},
	/* HID_KEYBOARD_SC_KEYPAD_6_AND_RIGHT_ARROW          */	{'6', 0},
	/* HID_KEYBOARD_SC_KEYPAD_7_AND_HOME                 */	{'7', 0},
	/* HID_KEYBOARD_SC_KEYPAD_8_AND_UP_ARROW             */	{'8', 0},
	/* HID_KEYBOARD_SC_KEYPAD_9_AND_PAGE_UP              */	{'9', 0},
	/* HID_KEYBOARD_SC_KEYPAD_0_AND_INSERT               */	{'0', 0},
	/* HID_KEYBOARD_SC_KEYPAD_DOT_AND_DELETE             */	{'.', 0},
	/* HID_KEYBOARD_SC_NON_US_BACKSLASH_AND_PIPE         */	{'\\', '|'},
	/* HID_KEYBOARD_SC_APPLICATION                       */	{0, 0},
	/* HID_KEYBOARD_SC_POWER                             */	{0, 0},
	/* HID_KEYBOARD_SC_KEYPAD_EQUAL_SIGN                 */	{0, 0},
	/* HID_KEYBOARD_SC_F13                               */	{0, 0},
	/* HID_KEYBOARD_SC_F14                               */	{0, 0},
	/* HID_KEYBOARD_SC_F15                               */	{0, 0},
	/* HID_KEYBOARD_SC_F16                               */	{0, 0},
	/* HID_KEYBOARD_SC_F17                               */	{0, 0},
	/* HID_KEYBOARD_SC_F18                               */	{0, 0},
	/* HID_KEYBOARD_SC_F19                               */	{0, 0},
	/* HID_KEYBOARD_SC_F20                               */	{0, 0},
	/* HID_KEYBOARD_SC_F21                               */	{0, 0},
	/* HID_KEYBOARD_SC_F22                               */	{0, 0},
	/* HID_KEYBOARD_SC_F23                               */	{0, 0},
	/* HID_KEYBOARD_SC_F24                               */	{0, 0}
};

char sc_to_char(uint16_t const sc)
{
	const uint8_t mod = ((union16_t)sc).bytes.msb;
	const uint8_t code = ((union16_t)sc).bytes.lsb - HID_KEYBOARD_SC_A;
	
	if ((mod & 0x22) == 0)
		return pgm_read_byte(&antiasciitable[code].unshifted);
	else
		return pgm_read_byte(&antiasciitable[code].shifted);
}

#else /* MACRO_RAM_SIZE */

void init_password(void)
{
}

#endif /* MACRO_RAM_SIZE */

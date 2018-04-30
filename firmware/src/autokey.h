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


#ifndef AUTOKEY_H_
#define AUTOKEY_H_

#include <stddef.h>
#include <stdint.h>

#define SEND_BUFFER_SIZE (8)
#define READ_BUFFER_SIZE (6)

#define AUTOKEY_IDLE (0)
#define AUTOKEY_BUSY (1)
#define AUTOKEY_SENDING (2)
#define AUTOKEY_READING (4)

#define AUTOKEY_SETSEND (g_autokey_status | 0x03)
#define AUTOKEY_ENDSEND (g_autokey_status & 0xFD)

#define AUTOKEY_SETREAD (g_autokey_status | 0x05)
#define AUTOKEY_ENDREAD (g_autokey_status & 0xFB)

typedef union {
	uint16_t word;
	struct {
		uint8_t lsb;
		uint8_t msb;
	} bytes;
} union16_t;

extern uint8_t g_autokey_status;
extern uint8_t g_autokey_modifier;
extern uint8_t g_read_buffer[READ_BUFFER_SIZE];
extern uint8_t g_read_buffer_length;

void init_autokey(void);
void autokey_send(void);
void autokey_read(void);
void autokey_setidle(void);
void autokey_cycle(void);
uint8_t queue_autotext(char const * const str);
uint8_t queue_ram_autotext(char * const str, size_t const len);
uint8_t queue_autokeys(uint8_t const key, uint8_t const mod);
uint8_t queue_macro(uint16_t const * const macro);
uint8_t queue_ram_macro(uint16_t * const macro, size_t const len);
void begin_read(void);
uint16_t char_to_sc(char const c);

#endif /* AUTOKEY_H_ */
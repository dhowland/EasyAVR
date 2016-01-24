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


#ifndef CONFIG_PASSWORD_H_
#define CONFIG_PASSWORD_H_

#include <stddef.h>
#include <stdint.h>
#include <avr/pgmspace.h>

#define NUMBER_OF_PWDATA (4)
#define MAX_SCRAMBLER_SIZE (40)

typedef struct {
	const char scrambler[MAX_SCRAMBLER_SIZE];
	const uint8_t scrambler_len;
	const uint8_t use_lowers;
	const uint8_t use_uppers;
	const uint8_t use_numbers;
	const uint8_t use_symbols;
	const uint8_t output_len;
} pwdefs_t;

extern const pwdefs_t PROGMEM PWDEFS[NUMBER_OF_PWDATA];

#endif /* CONFIG_PASSWORD_H_ */

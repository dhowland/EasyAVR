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


#ifndef CONFIG_MATRIX_H_
#define CONFIG_MATRIX_H_

#include <stddef.h>
#include <stdint.h>
#include <avr/pgmspace.h>

#include "io_ref.h"

#define DEFAULT_DEBOUNCE_MS (12)
#define DEFAULT_ALT_DEBOUNCE_MS (6)
#define DEFAULT_TAP_MAX_MS (240)
#define DEFAULT_DOUBLETAP_DELAY_MS (-120)
#define DEFAULT_HOLD_KEY_MS (800)
#define DEFAULT_REPEAT_MS (32)
#if (F_CPU == 16000000UL)
#define DEFAULT_MATRIX_SETUP_WAIT (5)
#else
#define DEFAULT_MATRIX_SETUP_WAIT (1)
#endif

#define PULLUP_UNUSED_PINS

#ifdef BOARD_SIZE_SQUARE
#define NUMBER_OF_ROWS (12)
#define NUMBER_OF_COLS (12)
#endif
#ifdef BOARD_SIZE_JUMBO
#define NUMBER_OF_ROWS (7)
#define NUMBER_OF_COLS (24)
#endif
#ifdef BOARD_SIZE_FULLSIZE
#define NUMBER_OF_ROWS (6)
#define NUMBER_OF_COLS (22)
#endif
#ifdef BOARD_SIZE_COSTAR
#define NUMBER_OF_ROWS (8)
#define NUMBER_OF_COLS (18)
#endif
#ifdef BOARD_SIZE_TKL
#define NUMBER_OF_ROWS (6)
#define NUMBER_OF_COLS (17)
#endif
#ifdef BOARD_SIZE_SIXTY
#define NUMBER_OF_ROWS (5)
#define NUMBER_OF_COLS (15)
#endif
#ifdef BOARD_SIZE_PAD
#define NUMBER_OF_ROWS (6)
#define NUMBER_OF_COLS (6)
#endif
#ifdef BOARD_SIZE_CARD
#define NUMBER_OF_ROWS (1)
#define NUMBER_OF_COLS (6)
#endif

#define MAX_DIMENSION (NUMBER_OF_COLS)

#if defined(__AVR_ATmega32U4__) && (F_CPU == 8000000UL)
/* 8MHz is used for KMAC and similar boards with the special key on the bootloader pin */
#define KMAC_ALIKE
#endif

typedef struct {
	const uint8_t port_mask;
	const uint8_t port_dir;
} matrix_init_t;

typedef struct {
} matrix_strobe_t;

typedef struct {
	const uint8_t port_ref;
	const uint8_t mask;
} matrix_sense_t;

extern const uint8_t PROGMEM STROBE_COLS;
extern const uint8_t PROGMEM STROBE_LOW;
extern const uint8_t PROGMEM NUMBER_OF_STROBE;
extern const uint8_t PROGMEM NUMBER_OF_SENSE;
extern const matrix_init_t PROGMEM MATRIX_INIT_LIST[NUM_PORTS];
extern const uint8_t PROGMEM MATRIX_STROBE_LIST[MAX_DIMENSION][NUM_PORTS];
extern const matrix_sense_t PROGMEM MATRIX_SENSE_LIST[MAX_DIMENSION];
#ifdef KMAC_ALIKE
extern const uint8_t PROGMEM KMAC_KEY[2];
#endif /* KMAC_ALIKE */

#endif /* CONFIG_MATRIX_H_ */

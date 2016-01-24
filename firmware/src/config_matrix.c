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

#include "io_ref.h"
#include "matrix.h"


const uint8_t PROGMEM STROBE_COLS = 0;
const uint8_t PROGMEM STROBE_LOW = 0;
const uint8_t PROGMEM NUMBER_OF_STROBE = 0;
const uint8_t PROGMEM NUMBER_OF_SENSE = 0;
const matrix_init_t PROGMEM MATRIX_INIT_LIST[NUM_PORTS] = { { 0 } };
const uint8_t PROGMEM MATRIX_STROBE_LIST[MAX_DIMENSION][NUM_PORTS] = { { 0 } };
const matrix_sense_t PROGMEM MATRIX_SENSE_LIST[MAX_DIMENSION] = { { 0 } };
#ifdef KMAC_ALIKE
const uint8_t PROGMEM KMAC_KEY[2] = { 0, 0 };
#endif /* KMAC_ALIKE */

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

const uint16_t PROGMEM MACRO_BUFFER[MACRO_BUFFER_SIZE] = { 0 };
const uint8_t PROGMEM LAYERS[NUMBER_OF_LAYERS][NUMBER_OF_ROWS][NUMBER_OF_COLS] = { { { 0 } } };
const uint8_t PROGMEM ACTIONS[NUMBER_OF_LAYERS][NUMBER_OF_ROWS][NUMBER_OF_COLS] = { { { 0 } } };
const uint8_t PROGMEM TAPKEYS[NUMBER_OF_LAYERS][NUMBER_OF_ROWS][NUMBER_OF_COLS] = { { { 0 } } };
const uint8_t PROGMEM LED_LAYERS[LED_LAYERS_SIZE] = { 0 };

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


#ifndef MATRIX_H_
#define MATRIX_H_

#include <stddef.h>
#include <stdint.h>

#include "scheduler.h"
#include "config_matrix.h"

#define MATRIX_REPEAT_MS SCHEDULE_CYCLE_MS

extern int16_t g_matrixstate[NUMBER_OF_ROWS][NUMBER_OF_COLS];

void init_matrix(void);
void initial_scan(void);
void matrix_subscan(const int8_t start, const int8_t finish);
void matrix_scan(void);
void matrix_scan_first_half(void);
void matrix_scan_second_half(void);
void matrix_scan_first_quarter(void);
void matrix_scan_second_quarter(void);
void matrix_scan_third_quarter(void);
void matrix_scan_fourth_quarter(void);
void debounce_logic(uint8_t read_status, uint8_t row, uint8_t col);

#endif /* MATRIX_H_ */

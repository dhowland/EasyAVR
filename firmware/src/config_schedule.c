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

#include "USB.h"
#include "matrix.h"
#include "mouse.h"
#include "led.h"
#include "autokey.h"
#include "scheduler.h"


#ifdef SIMPLE_DEVICE

/*	1x4
	+----------------+
	| led_cycle      |
	+----------------+
	| matrix_scan    |
	+----------------+
	| autokey_cycle  |
	+----------------+
	|                |
	+----------------+ */

void (* const g_sched_list[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT])(void) PROGMEM = {
	{
		&led_cycle,
		&matrix_scan,
		&autokey_cycle,
		NULL
	}
};

#else /* ndef SIMPLE_DEVICE */

#ifdef EXPANDED_SCHEDULE

/*	4x4
	+----------------+----------------+----------------+----------------+
	| led_cycle      | led_cycle      | led_cycle      | led_cycle      |
	+----------------+----------------+----------------+----------------+
	| matrix_scan_1  | matrix_scan_2  | matrix_scan_3  | matrix_scan_4  |
	+----------------+----------------+----------------+----------------+
	| update_mouse   | autokey_cycle  | console_main   |                |
	+----------------+----------------+----------------+----------------+
	|                |                |                |                |
	+----------------+----------------+----------------+----------------+ */

void (* const g_sched_list[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT])(void) PROGMEM = {
	{
		&led_cycle,
		&matrix_scan_first_quarter,
		&update_mouse,
		NULL
	},
	{
		&led_cycle,
		&matrix_scan_second_quarter,
		&autokey_cycle,
		NULL
	},
	{
		&led_cycle,
		&matrix_scan_third_quarter,
		&console_main,
		NULL
	},
	{
		&led_cycle,
		&matrix_scan_fourth_quarter,
		NULL,
		NULL
	}
};

#else /* ndef EXPANDED_SCHEDULE */

/*	2x5
	+----------------+----------------+
	| led_cycle      | led_cycle      |
	+----------------+----------------+
	| matrix_scan_1  | matrix_scan_2  |
	+----------------+----------------+
	| update_mouse   | autokey_cycle  |
	+----------------+----------------+
	|                | console_main   |
	+----------------+----------------+
	|                |                |
	+----------------+----------------+ */

void (* const g_sched_list[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT])(void) PROGMEM = {
	{
		&led_cycle,
		&matrix_scan_first_half,
		&update_mouse,
		NULL,
		NULL
	},
	{
		&led_cycle,
		&matrix_scan_second_half,
		&autokey_cycle,
		&console_main,
		NULL
	}
};

#endif /* EXPANDED_SCHEDULE */
#endif /* SIMPLE_DEVICE */

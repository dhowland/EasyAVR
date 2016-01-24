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
#include "password.h"
#include "led.h"
#include "autokey.h"
#include "scheduler.h"


#ifdef SIMPLE_DEVICE

/*	1x4
	+----------------+
	| USB_cycle      |
	+----------------+
	| matrix_scan    |
	+----------------+
	| autokey_cycle  |
	+----------------+
	| led_cycle      |
	+----------------+ */
void (* const g_sched_list[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT])(void) PROGMEM = {
	{
		&USB_cycle,
		&matrix_scan,
		&autokey_cycle,
		&led_cycle
	}
};

#else /* ndef SIMPLE_DEVICE */

#ifdef EXPANDED_SCHEDULE

/*	4x4
	+----------------+----------------+----------------+----------------+
	| USB_cycle      | matrix_scan_2  | USB_cycle      | matrix_scan_4  |
	+----------------+----------------+----------------+----------------+
	| matrix_scan_1  | password_cycle | matrix_scan_3  | autokey_cycle  |
	+----------------+----------------+----------------+----------------+
	| led_cycle      | update_mouse   | led_cycle      | console_main   |
	+----------------+----------------+----------------+----------------+
	|                | led_cycle      |                | led_cycle      |
	+----------------+----------------+----------------+----------------+ */

void (* const g_sched_list[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT])(void) PROGMEM = {
	{
		&USB_cycle,
		&matrix_scan_first_quarter,
		&led_cycle,
		NULL
	},
	{
		&matrix_scan_second_quarter,
		&password_cycle,
		&update_mouse,
		&led_cycle
	},
	{
		&USB_cycle,
		&matrix_scan_third_quarter,
		&led_cycle,
		NULL
	},
	{
		&matrix_scan_fourth_quarter,
		&autokey_cycle,
		&console_main,
		&led_cycle
	}
};

#else /* ndef EXPANDED_SCHEDULE */

/*	2x5
	+----------------+----------------+
	| USB_cycle      | USB_cycle      |
	+----------------+----------------+
	| matrix_scan_1  | matrix_scan_2  |
	+----------------+----------------+
	| password_cycle | autokey_cycle  |
	+----------------+----------------+
	| update_mouse   | console_main   |
	+----------------+----------------+
	| led_cycle      | led_cycle      |
	+----------------+----------------+ */

void (* const g_sched_list[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT])(void) PROGMEM = {
	{
		&USB_cycle,
		&matrix_scan_first_half,
		&password_cycle,
		&update_mouse,
		&led_cycle
	},
	{
		&USB_cycle,
		&matrix_scan_second_half,
		&autokey_cycle,
		&console_main,
		&led_cycle
	}
};

#endif /* EXPANDED_SCHEDULE */
#endif /* SIMPLE_DEVICE */

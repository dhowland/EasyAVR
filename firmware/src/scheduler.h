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


#ifndef SCHEDULER_H_
#define SCHEDULER_H_

#include <stddef.h>
#include <stdint.h>
#include <avr/io.h>

#include "debug.h"
#include "config_schedule.h"

#define SCHEDULE_CYCLE_MS (SCHEDULE_PERIOD_MS * NUMBER_OF_SCHEDULE_SLOTS)
#define CLOCK_KHZ (F_CPU/1000)

#define SCHEDULE_CYCLE_CLOCKS (CLOCK_KHZ * SCHEDULE_PERIOD_MS)
#define SCHEDULE_LIMIT ((SCHEDULE_CYCLE_CLOCKS * 3) / 4)

/* Generic names for timer registers so timer can be easily selected */
#define TCCRA (TCCR1A)
#define TCCRB (TCCR1B)
#define TCCRC (TCCR1C)
#define OCRA  (OCR1A)
#define TCNT  (TCNT1)
#define TIMSK (TIMSK1)
#define OCIEA (OCIE1A)
#define TCMAX (0xFFFF)

#ifdef ENABLE_DEBUG_CONSOLE
extern uint16_t g_schedule_clocks[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT];
#endif /* ENABLE_DEBUG_CONSOLE */

void init_scheduler(void);
void schedule_start(void);
void schedule_stop(void);
void schedule_tick(void);
void exec_slice(void);
void clock_in(void);
void reset_max_clocks(void);

#endif /* SCHEDULER_H_ */

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
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/wdt.h>
#include <avr/pgmspace.h>

#include "debug.h"
#include "scheduler.h"


volatile uint8_t g_next_slice;
volatile uint8_t g_next_item;
#ifdef ENABLE_DEBUG_CONSOLE
uint16_t g_schedule_clocks[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT];
#endif /* ENABLE_DEBUG_CONSOLE */


/* Setup interrupt vector for cycle */
ISR(TIMER1_COMPA_vect)
{
	schedule_tick();
}


void init_scheduler(void)
{
	/* initialize the timer */
	GTCCR = 0;	// no synchronized counters
	TCCRA = 0;	// normal mode, no output ports
	TCCRC = 0;	// no force output compare
	OCRA = SCHEDULE_CYCLE_CLOCKS;
}

void schedule_start(void)
{
	g_next_slice = 0;
	
	/* Start the timer */
	TCNT = 0;	// clear timer state
	TCCRB = 0x1;	// normal mode, no input capture, configured prescaled clock
	TIMSK = _BV(OCIEA);	// enable output compare A interrupt
	
	/* enable the watchdog timer */
    /* USB can take up to 30ms anyway, so give it time to do its thing */
	wdt_enable(WDTO_60MS);
	/* enable watchdog interrupts (see lowlevel.c) */
	WDTCSR |= (_BV(WDIF) | _BV(WDIE));
}

void schedule_stop(void)
{
	/* enable the watchdog timer */
	wdt_disable();
	/* disable watchdog interrupts */
	WDTCSR &= (uint8_t)~(_BV(WDIE));
	
	/* Stop the timer */
	TIMSK = 0;	// disable output compare A interrupt
	TCCRB = 0;	// stop clock
}

inline void schedule_tick(void)
{
	TCNT = 0;	// clear timer state
	
	/* execute the schedule for this slice */
	exec_slice();
	if (++g_next_slice >= NUMBER_OF_SCHEDULE_SLOTS)
		g_next_slice = 0;
	
	/* service the watchdog timer */
	wdt_reset();
}

inline void exec_slice(void)
{
	void (*slot_ptr)(void);
	
	for(g_next_item=0; g_next_item<NUMBER_OF_ITEMS_PER_SLOT; g_next_item++)
	{
		slot_ptr = pgm_read_ptr(&g_sched_list[g_next_slice][g_next_item]);
		if (slot_ptr != NULL)
		{
			(*slot_ptr)();
			clock_in();
		}
	}
}

inline void clock_in(void)
{
#ifdef ENABLE_DEBUG_CONSOLE
	const uint16_t count = TCNT;
	
	/* check for cycle overrun */
	//if (count > SCHEDULE_LIMIT)
	//{
		//report_event(EVENT_CODE_SCHED_OVER, ((g_next_slice<<8)|g_next_item), MODE_UPDATE);
		//report_event(EVENT_CODE_SCHED_OVER_CNT, count, MODE_UPDATE);
	//}
	
	if (count > g_schedule_clocks[g_next_slice][g_next_item])
		g_schedule_clocks[g_next_slice][g_next_item] = count;
}

void reset_max_clocks(void)
{
	int8_t i,j;
	
	for (i=0; i<NUMBER_OF_SCHEDULE_SLOTS; i++)
		for (j=0; j<NUMBER_OF_ITEMS_PER_SLOT; j++)
			g_schedule_clocks[i][j] = 0;
#endif /* ENABLE_DEBUG_CONSOLE */
}

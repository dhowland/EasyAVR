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

/* Concept
	This is an implementation of mouse movement using keyboard directional keys.
	The design is meant to allow useful control of the mouse cursor on the screen
	while being lightweight.
	
	The control scheme is meant to allow the cursor to be moved with enough speed
	that long movements aren't tedious, while still having enough precision to
	make accurate selections on the screen.  Pressing the Mouse-Up, -Down, -Left,
	or -Right keys causes the cursor to move slowly.  Double or triple tapping
	causes the cursor to move increasingly faster.
	
	Accurate control of the mouse requires unit movements at less than the update
	rate of the USB mouse reports.  Therefore, a 10 report cycle is used to evenly
	distribute requests to get a smooth mouse movement.  The report cycle is
	managed at the USB update rate.
 */
#include <stddef.h>
#include <stdint.h>

#include "keymap.h"
#include "nvm.h"
#include "mouse.h"

int8_t g_mouse_report_X;
int8_t g_mouse_report_Y;
uint8_t g_mouse_active;
uint8_t g_mouse_service;
uint8_t g_cumulative_count;
uint8_t g_slot;
uint8_t g_mouse_multiply;

void init_mouse(void)
{
	/* Calculations involving the cycle slot assume it is never zero */
	g_slot = 1;
}

/* Calculate the requested mouse movement based on the user input.
	This takes the button presses and calculates the report deltas based
	on how many times the direction keys have been tapped.
*/
void update_mouse(void)
{
	uint16_t total_cycle_request;
	int8_t mouse_report;
	
	if (g_mouse_req_X || g_mouse_req_Y)
	{
		/* Tell the USB code that we have data to send */
		g_mouse_active = 1;
		/* Check to see if the USB code is ready for a new mouse report */
		if (!g_mouse_service)
		{
			/* Calculate a mouse delta (over a mouse cycle) based on the number of taps */
			total_cycle_request = (g_mouse_min_delta + (g_mouse_multiply * g_mouse_delta_mult));
			mouse_report = mouse_cycle(total_cycle_request);
			/* Get direction (+/-) from the mouse_req var */
			g_mouse_report_X = mouse_report * g_mouse_req_X;
			g_mouse_report_Y = mouse_report * g_mouse_req_Y;
			/* Signal a new report */
			g_mouse_service = 1;
		}
	} else {
		/* Signal a final report before halting movement */
		if (g_mouse_active)
			g_mouse_service = 1;
		/* When the user lifts up their fingers, reset everything */
		g_mouse_active = 0;
		g_cumulative_count = 0;
		g_mouse_report_X = 0;
		g_mouse_report_Y = 0;
		/* If we have stopped controlling the mouse, get ready for a fast response
			when we start up again.  The nature of the algorithm that splits up requests
			over the mouse cycle puts small requests at the end of the cycle. */
		g_slot = MOUSE_CYCLES;
	}
}

/* Calculate the requested X or Y value for the current USB mouse update slot.
	This takes the current request from the mouse control (total over a
	multi-cycle period) and calculates the current setting based on how much
	has already been sent in the cycle and the current slot.
	Basically, this bridges program cycle and USB processing, which are
	asynchronous.
*/
int8_t mouse_cycle(uint16_t total_cycle_request)
{
	uint8_t cumulative_request;
	int8_t request;
	
	/* How much of the total movement should have been sent by now */
	cumulative_request = (uint8_t)((total_cycle_request * g_slot) / MOUSE_CYCLES);
	/* Considering how much has already been sent, how much needs to be sent now */
	request = (int8_t)(cumulative_request - g_cumulative_count);
	/* Update the total sent this cycle */
	g_cumulative_count += request;
	
	if (++g_slot > MOUSE_CYCLES)
	{
		g_cumulative_count = 0;
		g_slot = 1;
	}
	
	return request;
}

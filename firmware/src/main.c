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

// compiler includes
#include <stddef.h>
#include <stdint.h>
#include <avr/wdt.h>
#include <util/delay.h>

// library includes
#include <asf.h>

// project includes
#include "debug.h"
#include "lowlevel.h"
#include "scheduler.h"
#include "led.h"
#include "matrix.h"
#include "keymap.h"
#include "mouse.h"
#include "autokey.h"
#include "nvm.h"
#include "USB.h"

/* Foward declarations to avoid warnings */
void application_init(void);
void application_loop(void);
void application_cleanup(void);

/* This function launches all initialization tasks. */
void application_init(void)
{	
	/* Initialize modules */
	init_lowlevel();
	init_debug();
	init_nvm();
	init_matrix();
	init_led();
	init_keymap();
	init_mouse();
	init_autokey();
	init_scheduler();
	init_USB();
	
	/* Check for an Enter key held while plugging in */
	initial_scan();
	
	/* Start USB */
	USB_Init();
	
	/* Enable global interrupts */
	sei();
}

/* This function executes the main program */
void application_loop(void)
{
	/* USB enumeration takes a long time, so let that finish first */
	while (USB_DeviceState < DEVICE_STATE_Configured)
		USB_service();
	
	schedule_start();
	while(1)
	{
		if (g_reset_requested != NO_RESET)
			break;
		USB_service();
	}
	schedule_stop();
}

/* Called only in the event of an unrecoverable system failure.  This function
   collects debugging information and finally halts the system to wait for a
   breakpoint. */
void application_cleanup(void)
{
	// If USB is used, detach from the bus and reset it
	USB_Disable();
	// Disable all interrupts
	cli();
	// Wait two seconds for the USB detachment to register on the host
	Delay_MS(2000);
	if (g_reset_requested == RESET_TO_BOOT)
	{
		// enable bootloader then force a reset
		reset_to_bootloader();
	}
	if (g_reset_requested != NO_RESET)
	{
		wdt_enable(WDTO_250MS);
		for (;;);
	}
}

int main(void)
{
	/* Run anything required by ASF */
	board_init();
	
	/* This is the top level progression of the embedded software.  First, the init
	   code is used to setup the hardware and initialize data structures in RAM */
	application_init();
	
	/* The main application loop implements the embedded functions.  This should be
	   the final function call at this level */
	application_loop();
	
	/* In the event of an unexpected issue, the main application loop will return
	   and the cleanup function will execute to collect debugging information and
	   halt the system. */
	application_cleanup();
}

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


int main(void)
{
	/* Run anything required by ASF */
	board_init();
	
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
	
	/* USB enumeration takes a long time, so let that finish first */
	while (USB_DeviceState < DEVICE_STATE_Configured)
		USB_service();
	
	/* Operate the keyboard until the user requests a reset */
	schedule_start();
	while (g_reset_requested == NO_RESET)
		USB_service();
	schedule_stop();
	
	/* Detach from the USB bus and reset it */
	USB_Disable();
	
	/* Disable all interrupts */
	cli();
	
	/* Wait two seconds for the USB detachment to register on the host */
	Delay_MS(2000);
	
	/* If requested, go to bootloader after reset */
	if (g_reset_requested == RESET_TO_BOOT)
		reset_to_bootloader();
	
	/* Force a reset */
	set_wdt_for_reset();
	for (;;);
}

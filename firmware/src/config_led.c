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
#include "led.h"


const uint8_t PROGMEM NUMBER_OF_LEDS = 12;
const uint8_t PROGMEM NUMBER_OF_INDICATORS = 8;
const led_def_t PROGMEM LEDS_LIST[MAX_NUMBER_OF_LEDS] = { { 0 } };
const led_fn_t PROGMEM LED_FN[NUMBER_OF_LED_FUNCTIONS] = {
	/* LED_NUM_LOCK    */  { 255, 0 },
	/* LED_CAPS_LOCK   */  { 255, 0 },
	/* LED_SCROLL_LOCK */  { 255, 0 },
	/* LED_COMPOSE     */  { 255, 0 },
	/* LED_KANA        */  { 255, 0 },
	/* LED_WIN_LOCK    */  { 255, 0 },
	/* LED_FN_ACTIVE   */  { 255, 0 },
	/* LED_FN2_ACTIVE  */  { 255, 0 },
	/* LED_FN3_ACTIVE  */  { 255, 0 },
	/* LED_FN4_ACTIVE  */  { 255, 0 },
	/* LED_FN5_ACTIVE  */  { 255, 0 },
	/* LED_FN6_ACTIVE  */  { 255, 0 },
	/* LED_FN7_ACTIVE  */  { 255, 0 },
	/* LED_FN8_ACTIVE  */  { 255, 0 },
	/* LED_FN9_ACTIVE  */  { 255, 0 },
	/* LED_ANY_ACTIVE  */  { 255, 0 },
	/* LED_RECORDING   */  { 255, 0 },
	/* LED_USB_INIT    */  { 255, 0 },
	/* LED_USB_ERROR   */  { 255, 0 },
	/* LED_USB_SUSPEND */  { 255, 0 },
	/* LED_USB_NORMAL  */  { 255, 0 },
	/* LED_KB_LOCK     */  { 255, 0 }
};

#ifdef MAX_NUMBER_OF_BACKLIGHTS
const uint8_t PROGMEM NUMBER_OF_BACKLIGHTS = 0;
const uint8_t PROGMEM NUMBER_OF_BACKLIGHT_ENABLES = 0;
const uint8_t PROGMEM BACKLIGHT_MASK[MAX_NUMBER_OF_LEDS] = { 0 };
const uint8_t PROGMEM BLMODE_LIST[MAX_BACKLIGHT_ENABLES][MAX_NUMBER_OF_LEDS] = { { 0 } };
#endif /* MAX_NUMBER_OF_BACKLIGHTS */

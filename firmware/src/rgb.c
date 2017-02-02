/*
 * Easy AVR USB Keyboard Firmware
 * Copyright (C) 2013-2016 David Howland, Edward Fan
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

#include "rgb.h"

const struct cRGB PROGMEM rgb_led_const[160] = {};
const uint8_t PROGMEM rgb_count_const = 0;
const uint8_t PROGMEM rgb_pin_const = _BV(PC7);

void init_rgb(void) {
	
	int rgb_pin = pgm_read_byte(&(rgb_pin_const));
	int rgb_count = pgm_read_byte(&(rgb_count_const));
	struct cRGB rgb_led[rgb_count];
	
	for (int n=0; n<rgb_count; n++) {
		 rgb_led[n].r = pgm_read_byte(&(rgb_led_const[n].r));
		 rgb_led[n].g = pgm_read_byte(&(rgb_led_const[n].g));
		 rgb_led[n].b = pgm_read_byte(&(rgb_led_const[n].b));
	}
	
	ws2812_setleds_pin(rgb_led, rgb_count, rgb_pin);
	ws2812_setleds_pin(rgb_led, 1, rgb_pin); // timing is bugged for 1st LED after changes somewhere, probably compiler-side; this fixes it
} 
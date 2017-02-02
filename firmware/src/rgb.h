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


#ifndef RGB_H_
#define RGB_H_

#include "light_ws2812.h"
#include <avr/pgmspace.h>

extern const struct cRGB PROGMEM rgb_led_const[160];
extern const uint8_t PROGMEM rgb_count_const;
extern const uint8_t PROGMEM rgb_pin_const;

void init_rgb(void);

#endif /* RGB_H_ */
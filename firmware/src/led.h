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
 

#ifndef LED_H_
#define LED_H_

#include <stddef.h>
#include <stdint.h>

#include "scheduler.h"
#include "config_led.h"

#define MAX_BLIPS (10)
#define LED_BLIP_WIDTH (250)
#define LED_BLIP_REPEAT (240)
#define NUMBER_OF_BACKLIGHT_MODES (4)

typedef enum {
	BL_MODE_STATIC,
	BL_MODE_BREATHING,
	BL_MODE_REACTIVE,
	BL_MODE_ERODE
} bl_mode_t;

void init_led(void);
void led_output(const uint8_t led_id, const uint8_t setting);
void blip_cycle(void);
void led_cycle(void);
void set_led_status(uint8_t status);
void led_host_on(const led_function_t led_id);
void led_host_off(const led_function_t led_id);
void show_led_host_setting(void);
void led_dimmer(void);
void pwm_cycle(void);
void led_pwm(void);
void backlight_enable(void);
void backlight_mode(void);
void backlight_dimmer(void);
void backlight_react(void);
void backlighting_tick(void);
void backlighting_pwm(void);
void set_backlighting(void);

#endif /* LED_H_ */

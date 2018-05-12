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


#ifndef CONFIG_LED_H_
#define CONFIG_LED_H_

#include <stddef.h>
#include <stdint.h>
#include <avr/pgmspace.h>

#define LED_STATUS_NORM (0)
#define LED_STATUS_CONNECT (1)
#define LED_STATUS_ERROR (3)
#define LED_STATUS_SUSPEND (2)
#define LED_STATUS_WAKEUP LED_STATUS_NORM
#define LED_STATUS_RESET LED_STATUS_NORM

typedef struct {
	const uint8_t led_id;
	const uint8_t blips;
} led_fn_t;

typedef enum {
	LED_NUM_LOCK,
	LED_CAPS_LOCK,
	LED_SCROLL_LOCK,
	LED_COMPOSE,
	LED_KANA,
	LED_WIN_LOCK,
	LED_FN1_ACTIVE,
	LED_FN2_ACTIVE,
	LED_FN3_ACTIVE,
	LED_FN4_ACTIVE,
	LED_FN5_ACTIVE,
	LED_FN6_ACTIVE,
	LED_FN7_ACTIVE,
	LED_FN8_ACTIVE,
	LED_FN9_ACTIVE,
	LED_ANY_ACTIVE,
	LED_RECORDING,
	LED_USB_INIT,
	LED_USB_ERROR,
	LED_USB_SUSPEND,
	LED_USB_NORMAL,
	LED_KB_LOCK,
	NUMBER_OF_LED_FUNCTIONS
} led_function_t;

/* Pretty much depends on a 1ms cycle time */
#define NUMBER_OF_BACKLIGHT_LEVELS (16)
#define BACKLIGHT_MODULUS_MASK (0xF0)	// requires levels=16
#define BACKLIGHT_DIMMER_SKIP (4)
#define BACKLIGHT_DIMMER_MASK (0xFC)	// requires skip=4
#define MINIMUM_BACKLIGHT_LEVEL (1)
#define BACKLIGHT_CHANGE_DELAY (48)
#define DYNAMIC_BACKLIGHT_PEAK (24)
#define DYNAMIC_BACKLIGHT_TROUGH (4)
#define BACKLIGHT_ERODE_SKIP (4)

#define MAX_NUMBER_OF_LEDS (16)
#define MAX_NUMBER_OF_INDICATORS (8)
extern const uint8_t PROGMEM NUMBER_OF_LEDS;
extern const uint8_t PROGMEM NUMBER_OF_INDICATORS;

#if (defined(__AVR_ATmega32U4__) && !defined(BOARD_SIZE_COSTAR)) || defined(__AVR_AT90USB1286__)
#define MAX_NUMBER_OF_BACKLIGHTS (8)
#define MAX_BACKLIGHT_ENABLES (16)
extern const uint8_t PROGMEM NUMBER_OF_BACKLIGHTS;
extern const uint8_t PROGMEM NUMBER_OF_BACKLIGHT_ENABLES;
#endif /* Bigger devices and smaller matrices */

typedef enum {
	LED_DRIVER_PULLUP,
	LED_DRIVER_PULLDOWN
} led_driver_t;

typedef struct {
	const uint8_t port_ref;
	const uint8_t pin;
	const led_driver_t driver;
} led_def_t;

extern const led_def_t PROGMEM LEDS_LIST[MAX_NUMBER_OF_LEDS];
extern const led_fn_t PROGMEM LED_FN[NUMBER_OF_LED_FUNCTIONS];
#ifdef MAX_NUMBER_OF_BACKLIGHTS
extern const uint8_t PROGMEM BACKLIGHT_MASK[MAX_NUMBER_OF_LEDS];
extern const uint8_t PROGMEM BLMODE_LIST[MAX_BACKLIGHT_ENABLES][MAX_NUMBER_OF_LEDS];
#endif /* MAX_NUMBER_OF_BACKLIGHTS */

#endif /* CONFIG_LED_H_ */

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

#include "debug.h"
#include "nvm.h"
#include "io_ref.h"
#include "led.h"


uint8_t g_led_host[MAX_NUMBER_OF_INDICATORS];
uint8_t g_led_blip_timer;
uint8_t g_led_blip_cycle;
uint8_t g_led_dimmer;
uint8_t g_led_state;
uint8_t g_pwm_cycle_pos;
uint8_t g_pwm_led_counter;
#ifdef MAX_NUMBER_OF_BACKLIGHTS
uint8_t g_bl_enable_index;
bl_mode_t g_bl_mode;
uint8_t g_bl_dimmer;
uint8_t g_bl_tick_counter;
uint8_t g_bl_breathe_direction;
uint8_t g_bl_state;
uint8_t g_bl_usb_on;
uint8_t g_pwm_bl_counter;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */

const uint8_t PROGMEM BLIP_MAP[MAX_BLIPS+1] = { 1, 5, 8, 10, 12, 15, 16, 20, 20, 24, 24 };

void init_led(void)
{
	uint8_t i;
	const uint8_t n = pgm_read_byte(&NUMBER_OF_LEDS);
	/* Configure pins for output */
	for (i = 0; i < n; i++)
	{
		pin_output(pgm_read_byte(&LEDS_LIST[i].port_ref), pgm_read_byte(&LEDS_LIST[i].pin));
		led_output(i, 0);
	}
	g_led_dimmer = g_init_dimmer_level;
#ifdef MAX_NUMBER_OF_BACKLIGHTS
	g_bl_dimmer = g_init_dimmer_level;
	g_bl_mode = g_init_backlight_mode;
	g_bl_enable_index = g_init_backlight_enable;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
}

void led_output(const uint8_t led_id, const uint8_t setting)
{
	const led_driver_t direction = pgm_read_byte(&LEDS_LIST[led_id].driver);
	
	if (setting ^ direction)
		pin_set(pgm_read_byte(&LEDS_LIST[led_id].port_ref),
				pgm_read_byte(&LEDS_LIST[led_id].pin));
	else
		pin_clear(pgm_read_byte(&LEDS_LIST[led_id].port_ref),
				  pgm_read_byte(&LEDS_LIST[led_id].pin));
}

void blip_cycle(void)
{
	if (g_led_blip_timer == (LED_BLIP_WIDTH-1))
	{
		if (g_led_blip_cycle == (LED_BLIP_REPEAT-1))
		{
			g_led_blip_cycle = 0;
		}
		else
		{
			g_led_blip_cycle += 1;
		}
		g_led_blip_timer = 0;
	}
	else
	{
		g_led_blip_timer += 1;
	}
}

void led_cycle(void)
{
	pwm_cycle();
	led_pwm();
	blip_cycle();
	show_led_host_setting();
#ifdef MAX_NUMBER_OF_BACKLIGHTS
	backlighting_tick();
	backlighting_pwm();
	set_backlighting();
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
}

void set_led_status(const uint8_t status)
{
	switch (status)
	{
		case LED_STATUS_CONNECT:
			led_host_on(LED_USB_INIT);
			led_host_off(LED_USB_ERROR);
			led_host_off(LED_USB_SUSPEND);
			led_host_off(LED_USB_NORMAL);
#ifdef MAX_NUMBER_OF_BACKLIGHTS
			g_bl_usb_on = 0;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
			break;
		case LED_STATUS_SUSPEND:
			led_host_off(LED_USB_INIT);
			led_host_off(LED_USB_ERROR);
			led_host_on(LED_USB_SUSPEND);
			led_host_off(LED_USB_NORMAL);
#ifdef MAX_NUMBER_OF_BACKLIGHTS
			g_bl_usb_on = 0;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
			break;
		case LED_STATUS_ERROR:
			led_host_off(LED_USB_INIT);
			led_host_on(LED_USB_ERROR);
			led_host_off(LED_USB_SUSPEND);
			led_host_off(LED_USB_NORMAL);
#ifdef MAX_NUMBER_OF_BACKLIGHTS
			g_bl_usb_on = 0;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
			break;
		default:
			led_host_off(LED_USB_INIT);
			led_host_off(LED_USB_ERROR);
			led_host_off(LED_USB_SUSPEND);
			led_host_on(LED_USB_NORMAL);
#ifdef MAX_NUMBER_OF_BACKLIGHTS
			g_bl_usb_on = 1;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
			break;
	}
}

void led_host_on(const led_function_t led_fn)
{
	const uint8_t led_id = pgm_read_byte(&LED_FN[led_fn].led_id);
	const uint8_t blips = pgm_read_byte(&LED_FN[led_fn].blips);
	const uint8_t n = pgm_read_byte(&NUMBER_OF_INDICATORS);
	
	if (led_id < n)
	{
		if (blips == 0)
		{
			// set least significant bit for solid, which is tracked separately
			g_led_host[led_id] |= 0x01;
		}
		else
		{
			// new blip count overrides any previous blip count
			g_led_host[led_id] &= 0x01;
			g_led_host[led_id] += (blips * 2);
		}
	}
}

void led_host_off(const led_function_t led_fn)
{
	const uint8_t led_id = pgm_read_byte(&LED_FN[led_fn].led_id);
	const uint8_t blips = pgm_read_byte(&LED_FN[led_fn].blips);
	const uint8_t n = pgm_read_byte(&NUMBER_OF_INDICATORS);
	
	if (led_id < n)
	{
		if (blips == 0)
		{
			// clear least significant bit for solid, which is tracked separately
			g_led_host[led_id] &= 0xFE;
		}
		else
		{
			// only clear blip count if this function is currently active
			if ((g_led_host[led_id] / 2) == blips)
				g_led_host[led_id] &= 0x01;
		}
	}
}

void show_led_host_setting(void)
{
	int8_t i;
	const uint8_t n = pgm_read_byte(&NUMBER_OF_INDICATORS);
	
	for (i=0; i<n; i++)
	{
		if (g_led_state)
		{
			const uint8_t set = g_led_host[i];
			if (set < 2)
			{
				if (set == 0)
					led_output(i, 0);
				else
					led_output(i, 1);
			}
			else
			{
				const uint8_t loop = pgm_read_byte(&BLIP_MAP[set/2]);
				const uint8_t pos = (g_led_blip_cycle % loop);
				if ((pos < set) && ((pos & 0x01) == 1))
					led_output(i, 1);
				else
					led_output(i, 0);
			}
		}
		else
		{
			led_output(i, 0);
		}
	}
}

void led_dimmer(void)
{
	if (g_led_dimmer >= NUMBER_OF_BACKLIGHT_LEVELS)
		g_led_dimmer = MINIMUM_BACKLIGHT_LEVEL;
	else
		g_led_dimmer = ((g_led_dimmer + BACKLIGHT_DIMMER_SKIP) & BACKLIGHT_DIMMER_MASK);
}

void pwm_cycle(void)
{
	if (++g_pwm_cycle_pos > NUMBER_OF_BACKLIGHT_LEVELS)
	{
		g_pwm_cycle_pos = 1;
		g_pwm_led_counter = 0;
#ifdef MAX_NUMBER_OF_BACKLIGHTS
		g_pwm_bl_counter = 0;
#endif /* MAX_NUMBER_OF_BACKLIGHTS */
	}
}

void led_pwm(void)
{
	uint8_t request;
	
	if (g_led_dimmer >= NUMBER_OF_BACKLIGHT_LEVELS)
	{
		// this short-circuits the 16*16 overflow situation
		g_led_state = 1;
	}
	else
	{
		request = g_pwm_cycle_pos * g_led_dimmer;
		if (request > g_pwm_led_counter)
		{
			g_led_state = 1;
			g_pwm_led_counter += NUMBER_OF_BACKLIGHT_LEVELS;
		}
		else
		{
			g_led_state = 0;
		}
	}
}

#ifdef MAX_NUMBER_OF_BACKLIGHTS
void backlight_enable(void)
{
	const uint8_t n = pgm_read_byte(&NUMBER_OF_BACKLIGHT_ENABLES);
	
	if (++g_bl_enable_index >= n)
		g_bl_enable_index = 0;
}

void backlight_mode(void)
{
	if (++g_bl_mode >= NUMBER_OF_BACKLIGHT_MODES)
		g_bl_mode = 0;
	if (g_bl_mode == BL_MODE_STATIC)
	{
		g_bl_dimmer = g_led_dimmer;
	}
	else if (g_bl_mode == BL_MODE_BREATHING)
	{
		g_bl_dimmer = DYNAMIC_BACKLIGHT_TROUGH;
	}
	else if (g_bl_mode == BL_MODE_REACTIVE)
	{
		g_bl_dimmer = DYNAMIC_BACKLIGHT_TROUGH;
		g_bl_breathe_direction = 0;
	}
	else /* BL_MODE_ERODE */
	{
		g_bl_dimmer = NUMBER_OF_BACKLIGHT_LEVELS;
		g_bl_breathe_direction = 1;
	}
}

void backlight_dimmer(void)
{
	led_dimmer();
	if (g_bl_mode == BL_MODE_STATIC)
		g_bl_dimmer = g_led_dimmer;
}

void backlight_react(void)
{
	if (g_bl_mode == BL_MODE_REACTIVE)
	{
		g_bl_dimmer = DYNAMIC_BACKLIGHT_PEAK;
	}
	else if (g_bl_mode == BL_MODE_ERODE)
	{
		if (g_bl_dimmer > BACKLIGHT_ERODE_SKIP)
			g_bl_dimmer -= BACKLIGHT_ERODE_SKIP;
		else if (g_bl_dimmer > 0)
			g_bl_dimmer -= 1;
		else
			g_bl_dimmer = 0;
	}
}

void backlighting_tick(void)
{
	if (++g_bl_tick_counter >= BACKLIGHT_CHANGE_DELAY)
	{
		g_bl_tick_counter = 0;
		if (g_bl_mode == BL_MODE_BREATHING)
		{
			if (g_bl_breathe_direction)
			{
				if (++g_bl_dimmer >= DYNAMIC_BACKLIGHT_PEAK)
					g_bl_breathe_direction = 0;
			}
			else
			{
				if (--g_bl_dimmer <= DYNAMIC_BACKLIGHT_TROUGH)
					g_bl_breathe_direction = 1;
			}
		}
		else if (g_bl_mode == BL_MODE_REACTIVE)
		{
			if (g_bl_dimmer > DYNAMIC_BACKLIGHT_TROUGH)
				g_bl_dimmer--;
		}
		else if (g_bl_mode == BL_MODE_ERODE)
		{
			if (g_bl_dimmer < NUMBER_OF_BACKLIGHT_LEVELS)
				g_bl_dimmer++;
		}
	}
}

void backlighting_pwm(void)
{
	uint8_t request;
	
	if (g_bl_dimmer >= NUMBER_OF_BACKLIGHT_LEVELS)
	{
		// this short-circuits the 16*16 overflow situation
		g_bl_state = 1;
	}
	else
	{
		request = g_pwm_cycle_pos * g_bl_dimmer;
		if (g_bl_breathe_direction)
			request &= BACKLIGHT_MODULUS_MASK;
		if (request > g_pwm_bl_counter)
		{
			g_bl_state = 1;
			g_pwm_bl_counter += NUMBER_OF_BACKLIGHT_LEVELS;
		}
		else
		{
			g_bl_state = 0;
		}
	}
}

void set_backlighting(void)
{
	int8_t i;
	uint8_t setting;
	const uint8_t n = pgm_read_byte(&NUMBER_OF_LEDS);
	
	for (i=0; i<n; i++)
	{
		if (pgm_read_byte(&BACKLIGHT_MASK[i]))
		{
			setting = g_bl_usb_on && g_bl_state && pgm_read_byte(&BLMODE_LIST[g_bl_enable_index][i]);
			led_output(i, setting);
		}
	}
}
#endif /* MAX_NUMBER_OF_BACKLIGHTS */

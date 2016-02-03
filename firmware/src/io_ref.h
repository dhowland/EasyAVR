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


#ifndef IO_REF_H_
#define IO_REF_H_

#include <stddef.h>
#include <stdint.h>

#define REF_PORTB 0
#define REF_PORTC 1
#define REF_PORTD 2
#define REF_PORTE 3
#define REF_PORTF 4
#define REF_PORTA 5

#ifdef __AVR_AT90USB1286__
#define NUM_PORTS 6
#else
#ifdef __AVR_ATmega32U4__
#define NUM_PORTS 5
#else
#define NUM_PORTS 3
#endif
#endif

typedef struct {
	volatile uint8_t * const ddr;
	volatile uint8_t * const port;
	volatile uint8_t * const pin;
} port_reg_t;

void pin_output(const uint8_t port_ref, const uint8_t pin);
void pin_input(const uint8_t port_ref, const uint8_t pin);
void port_dir_mask(const uint8_t port_ref, const uint8_t mask, const uint8_t outpins);
void pin_set(const uint8_t port_ref, const uint8_t pin);
void pin_clear(const uint8_t port_ref, const uint8_t pin);
void pin_toggle(const uint8_t port_ref, const uint8_t pin);
void port_set_clear_mask(const uint8_t port_ref, const uint8_t savemask, const uint8_t setpins);
uint8_t pin_get(const uint8_t port_ref, const uint8_t pin);
uint8_t port_get_mask(const uint8_t port_ref, const uint8_t mask);

#endif /* IO_REF_H_ */

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
#include <avr/io.h>

#include "io_ref.h"

const port_reg_t PORT_REG[NUM_PORTS] = {
	{ &DDRB, &PORTB, &PINB },
	{ &DDRC, &PORTC, &PINC },
	{ &DDRD, &PORTD, &PIND },
#ifdef __AVR_ATmega32U4__
	{ &DDRE, &PORTE, &PINE },
	{ &DDRF, &PORTF, &PINF },
#endif
#ifdef __AVR_AT90USB1286__
	{ &DDRE, &PORTE, &PINE },
	{ &DDRF, &PORTF, &PINF },
	{ &DDRA, &PORTA, &PINA },
#endif
};

void pin_output(const uint8_t port_ref, const uint8_t pin)
{
	*PORT_REG[port_ref].ddr |= (uint8_t)_BV(pin);
}

void pin_input(const uint8_t port_ref, const uint8_t pin)
{
	*PORT_REG[port_ref].ddr &= (uint8_t)~_BV(pin);
}

void port_dir_mask(const uint8_t port_ref, const uint8_t mask, const uint8_t outpins)
{
	*PORT_REG[port_ref].ddr = outpins | (*PORT_REG[port_ref].ddr & (~mask));
}

void pin_set(const uint8_t port_ref, const uint8_t pin)
{
	*PORT_REG[port_ref].port |= (uint8_t)_BV(pin);
}

void pin_clear(const uint8_t port_ref, const uint8_t pin)
{
	*PORT_REG[port_ref].port &= (uint8_t)~_BV(pin);
}

void pin_toggle(const uint8_t port_ref, const uint8_t pin)
{
	*PORT_REG[port_ref].pin |= (uint8_t)_BV(pin);
}

/* use inverted mask to save an op for speed.  mask says which bits to save instead of which to change */
void port_set_clear_mask(const uint8_t port_ref, const uint8_t savemask, const uint8_t setpins)
{
	*PORT_REG[port_ref].port = setpins | (*PORT_REG[port_ref].port & savemask);
}

uint8_t pin_get(const uint8_t port_ref, const uint8_t pin)
{
	return ((*PORT_REG[port_ref].pin & (uint8_t)_BV(pin)) != 0);
}

uint8_t port_get_mask(const uint8_t port_ref, const uint8_t mask)
{
	return (*PORT_REG[port_ref].pin & mask);
}

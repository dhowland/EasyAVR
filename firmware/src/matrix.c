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
#include <avr/sfr_defs.h>
#include <avr/cpufunc.h>

#include "io_ref.h"
#include "nvm.h"
#include "matrix.h"
#include "keymap.h"

uint8_t g_strobe_cols;
uint8_t g_strobe_low;
uint8_t g_number_of_strobe;
uint8_t g_number_of_sense;
uint8_t g_strobe_masks[NUM_PORTS];
int16_t g_matrixstate[NUMBER_OF_ROWS][NUMBER_OF_COLS];
#ifdef KMAC_ALIKE
uint8_t g_kmac_row;
uint8_t g_kmac_col;
#endif /* KMAC_ALIKE */

void init_matrix(void)
{
	int8_t i;
	uint8_t port_mask;
	uint8_t port_dir;
	uint8_t in_pins;
	
	g_strobe_cols = pgm_read_byte(&STROBE_COLS);
	g_strobe_low = pgm_read_byte(&STROBE_LOW);
	g_number_of_strobe = pgm_read_byte(&NUMBER_OF_STROBE);
	g_number_of_sense = pgm_read_byte(&NUMBER_OF_SENSE);
	for (i=0; i<NUM_PORTS; i++)
	{
		/* set port directions for inputs and outputs */
		port_mask = pgm_read_byte(&MATRIX_INIT_LIST[i].port_mask);
#ifdef PULLUP_UNUSED_PINS
		if (g_strobe_low)
			port_mask = 0xFF;
#endif
		port_dir = pgm_read_byte(&MATRIX_INIT_LIST[i].port_dir);
		port_dir_mask(i, port_mask, port_dir);
		/* save the mask for later to save cycles */
		g_strobe_masks[i] = (~port_dir);
		/* Set pull-up resistors for inputs */
		in_pins = (port_mask & (~port_dir));
		if (g_strobe_low)
		{
			port_set_clear_mask(i, (~in_pins), in_pins);
		}
		else
		{
			port_set_clear_mask(i, (~in_pins), 0);
		}
	}
#ifdef KMAC_ALIKE
	g_kmac_row = pgm_read_byte(&KMAC_KEY[0]);
	g_kmac_col = pgm_read_byte(&KMAC_KEY[1]);
	pin_set(REF_PORTE, 2);
#endif /* KMAC_ALIKE */
}

void initial_scan(void)
{
#ifndef SIMPLE_DEVICE
	int8_t i,j,n;
	uint8_t status;
	
	/* This function should track the matrix_subscan() logic.
	   Yeah, it's a messy duplicate, but it saves (real)time to do it this way. */
	
	for (i=0; i<g_number_of_strobe; i++)
	{
		for(n=0; n<NUM_PORTS; n++)
		{
			port_set_clear_mask(n, g_strobe_masks[n], pgm_read_byte(&MATRIX_STROBE_LIST[i][n]));
		}
		_delay_loop_1(g_matrix_setup_wait);
		for (j=0; j<g_number_of_sense; j++)
		{
			if (g_strobe_low)
			{
				status = port_get_mask(pgm_read_byte(&MATRIX_SENSE_LIST[j].port_ref), pgm_read_byte(&MATRIX_SENSE_LIST[j].mask)) == 0;
			}
			else
			{
				status = port_get_mask(pgm_read_byte(&MATRIX_SENSE_LIST[j].port_ref), pgm_read_byte(&MATRIX_SENSE_LIST[j].mask)) != 0;
			}
			if (status)
			{
				if (g_strobe_cols)
				{
					initial_actuate(j, i);
				}
				else
				{
					initial_actuate(i, j);
				}
			}
		}
	}
#endif /* SIMPLE_DEVICE */
}

void matrix_subscan(const int8_t start, const int8_t finish)
{
	int8_t i,j,n;
	uint8_t status;
	
	for (i=start; i<finish; i++)
	{
		/* Strobe the output pin(s) */
		for(n=0; n<NUM_PORTS; n++)
		{
			/* Only bother with output ports (ports with no outputs will have masks == 0, inverted) */
			if (g_strobe_masks[n] != 0xFF)
			{
				port_set_clear_mask(n, g_strobe_masks[n], pgm_read_byte(&MATRIX_STROBE_LIST[i][n]));
			}
		}
		/* Give it time to settle */
		_delay_loop_1(g_matrix_setup_wait);
		for (j=0; j<g_number_of_sense; j++)
		{
			/* Sense the input pin */
#ifdef KMAC_ALIKE
			if ((j == g_kmac_row) && (i == g_kmac_col))
			{
				debounce_logic((pin_get(REF_PORTE, 2) == 0), g_kmac_row, g_kmac_col);
			}
			else
#endif /* KMAC_ALIKE */
			{
				if (g_strobe_low)
				{
					status = port_get_mask(pgm_read_byte(&MATRIX_SENSE_LIST[j].port_ref), pgm_read_byte(&MATRIX_SENSE_LIST[j].mask)) == 0;
				}
				else
				{
					status = port_get_mask(pgm_read_byte(&MATRIX_SENSE_LIST[j].port_ref), pgm_read_byte(&MATRIX_SENSE_LIST[j].mask)) != 0;
				}
				if (g_strobe_cols)
				{
					debounce_logic(status, j, i);
				}
				else
				{
					debounce_logic(status, i, j);
				}
			}
		}
	}
}

void matrix_scan(void)
{
	matrix_subscan(0, g_number_of_strobe);
}

void matrix_scan_first_half(void)
{
	matrix_subscan(0, (g_number_of_strobe/2));
}

void matrix_scan_second_half(void)
{
	matrix_subscan((g_number_of_strobe/2), g_number_of_strobe);
}

void matrix_scan_first_quarter(void)
{
	matrix_subscan(0, (g_number_of_strobe/4));
}

void matrix_scan_second_quarter(void)
{
	matrix_subscan((g_number_of_strobe/4), ((2*g_number_of_strobe)/4));
}

void matrix_scan_third_quarter(void)
{
	matrix_subscan(((2*g_number_of_strobe)/4), ((3*g_number_of_strobe)/4));
}

void matrix_scan_fourth_quarter(void)
{
	matrix_subscan(((3*g_number_of_strobe)/4), g_number_of_strobe);
}

void debounce_logic(const uint8_t read_status, const uint8_t row, const uint8_t col)
{
	const int16_t state = g_matrixstate[row][col];
	int16_t * const matrixptr = &g_matrixstate[row][col];
	
	if (read_status)
	/* Switch is closed */
	{
		if (state < 0)
		/* Switch was previously open */
		{
			if (state > (-(int16_t)g_debounce_ms))
			/* Switch is still locked out */
			{
				*matrixptr -= MATRIX_REPEAT_MS;
			}
			else
			/* Switch is allowed to change state */
			{
				keymap_actuate(row,col,state);
				*matrixptr = MATRIX_REPEAT_MS;
			}
		}
		else
		/* Switch was previously closed */
		{
			if (state < g_hold_key_ms)
			/* Still in the tap time */
			{
				*matrixptr += MATRIX_REPEAT_MS;
			}
			else
			/* Key is being held */
			{
				keymap_interrupt(row,col);
				*matrixptr -= g_repeat_ms;
			}
		}
	}
	else
	/* Switch is open */
	{
		if (state > 0)
		/* Switch was previously closed */
		{
			if (state < g_debounce_ms)
			/* Switch is still locked out */
			{
				*matrixptr += MATRIX_REPEAT_MS;
			}
			else
			/* Switch is allowed to change state */
			{
				keymap_deactuate(row,col,state);
				*matrixptr = -MATRIX_REPEAT_MS;
			}
		}
		else
		/* Switch was previously open */
		{
			if (state > g_doubletap_delay_ms)
			/* Still in the doubletap time */
			{
				*matrixptr -= MATRIX_REPEAT_MS;
			}
			else
			/* Key is being ignored */
			{
			}
		}
	}
}

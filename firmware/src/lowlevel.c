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
#include <avr/wdt.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <avr/signature.h>
#include <avr/power.h>
#include <avr/pgmspace.h>

#include "lowlevel.h"


#if defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega32U2__)
/* ATmega32u4 datasheet gives bootloader location as 0x3800 (word address) */
const uint16_t PROGMEM BOOTLOADER = 0x3800;
/* Teensy 2.0 datasheet gives bootloader location as 0x7E00 (byte address) */
//const uint16_t PROGMEM BOOTLOADER = 0x3F00;
#endif /* ATmega32 boards */
#if defined(__AVR_ATmega16U2__)
/* ATmega16u2 datasheet gives bootloader location as 0x1800 (word address) */
const uint16_t PROGMEM BOOTLOADER = 0x1800;
#endif /* ATmega16 boards */
#if defined(__AVR_AT90USB1286__)
/* AT90USB128 datasheet gives bootloader location as 0xF000 (word address) */
const uint16_t PROGMEM BOOTLOADER = 0xF000;
/* Teensy 2.0++ datasheet gives bootloader location as 0x1FC00 (byte address) */
//const uint16_t PROGMEM BOOTLOADER = 0xFE00;
#endif /* AT90USB128 boards */

/* Disable WDT after bootloader reset (from AVR docs) */
uint16_t boot_key __attribute__ ((section (".noinit")));

#ifdef ENABLE_DEBUG_CONSOLE
uint8_t mcusr_mirror __attribute__ ((section (".noinit")));
uint16_t fault_word __attribute__ ((section (".noinit")));
uint8_t * saved_stack_ptr __attribute__ ((section (".noinit")));
uint8_t saved_stack[SAVED_STACK_SIZE] __attribute__ ((section (".noinit")));
#endif /* ENABLE_DEBUG_CONSOLE */

void get_mcusr(void) __attribute__((naked)) __attribute__((section(".init3")));
void get_mcusr(void)
{
	uint8_t mcusr_bkup = MCUSR;
	MCUSR = 0;
	wdt_disable();
	/* Also check for bootloader request */
	if ((mcusr_bkup & (1 << WDRF)) && (boot_key == MAGIC_BOOT_KEY))
	{
		boot_key = 0;
		((void (*)(void))pgm_read_ptr(&BOOTLOADER))();
	}
#if defined(__AVR_ATmega32U4__) || defined(__AVR_AT90USB1286__)
	/* Also disable JTAG so I get my Port F back */
	MCUCR |= (1<<JTD);
	MCUCR |= (1<<JTD);
#endif
#ifdef ENABLE_DEBUG_CONSOLE
	mcusr_mirror = mcusr_bkup;
#endif /* ENABLE_DEBUG_CONSOLE */
}

#ifdef ENABLE_DEBUG_CONSOLE
extern uint8_t _end;
extern uint8_t __stack;
#define STACK_CANARY 0xc5
void stack_paint(void) __attribute__((naked)) __attribute__((section (".init1")));
void stack_paint(void)
{
#if 0
	uint8_t *p = &_end;

	while(p <= &__stack)
	{
		*p = STACK_CANARY;
		p++;
	}
#else
	__asm volatile ("    ldi r30,lo8(_end)\n"
	"    ldi r31,hi8(_end)\n"
	"    ldi r24,lo8(0xc5)\n" /* STACK_CANARY = 0xc5 */
	"    ldi r25,hi8(__stack)\n"
	"    rjmp .cmp\n"
	".loop:\n"
	"    st Z+,r24\n"
	".cmp:\n"
	"    cpi r30,lo8(__stack)\n"
	"    cpc r31,r25\n"
	"    brlo .loop\n"
	"    breq .loop"::);
#endif
}
#endif /* ENABLE_DEBUG_CONSOLE */

ISR(WDT_vect)
{
#ifdef ENABLE_DEBUG_CONSOLE
	int16_t i;
	uint8_t* stack_ptr = *(uint8_t**)SP_L_ADR;
	
	fault_word = 1;
	saved_stack_ptr = stack_ptr;
	for (i=0; i<SAVED_STACK_SIZE; i++)
	{
		/* increment the ptr first because the SP is always pointing just below
		   the data on the stack */
		if (++stack_ptr > (uint8_t*)LAST_RAM_ADR)
			break;
		saved_stack[i] = *stack_ptr;
	}
	for (; i<SAVED_STACK_SIZE; i++)
	{
		saved_stack[i] = 0;
	}
#endif /* ENABLE_DEBUG_CONSOLE */
	
	// not re-enabling WDT Interrupt, which means we will reset very soon
}

void init_lowlevel(void)
{
	/* Report saved information */
#ifdef ENABLE_DEBUG_CONSOLE
	report_event(EVENT_CODE_DEBUG_RESET_STATUS, mcusr_mirror, MODE_UPDATE);
	if (fault_word)
	{
		report_event(EVENT_CODE_DEBUG_FAULT_WORD, fault_word, MODE_REOCCUR);
		fault_word = 0;
	}
#endif /* ENABLE_DEBUG_CONSOLE */
		
	powersave();
}

void powersave(void)
{
#ifdef __AVR_ATmega32U4__
	power_all_enable();
	power_adc_disable();
	power_spi_disable();
	power_timer0_disable();
	// timer 1 is used
	power_timer2_disable();
	power_timer3_disable();
	power_twi_disable();
	power_usart0_disable();
	power_usart1_disable();
	power_usb_enable();
#endif
	
	clock_prescale_set(clock_div_1);
}

void reset_to_bootloader(void)
{
	// Set the bootloader key to the magic value
	boot_key = MAGIC_BOOT_KEY;
}

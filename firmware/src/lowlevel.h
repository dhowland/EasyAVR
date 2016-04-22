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


#ifndef LOWLEVEL_H_
#define LOWLEVEL_H_

#define MAGIC_BOOT_KEY 0xDEAD

#ifdef ENABLE_DEBUG_CONSOLE
#define SP_L_ADR (0x005D)
#define SAVED_STACK_SIZE (0x80) /* Stack has been observed to take up to 128 bytes */
#ifdef __AVR_AT90USB1286__
#define LAST_RAM_ADR (0x20FF)
#endif
#ifdef __AVR_ATmega32U4__
#define LAST_RAM_ADR (0x0AFF)
#endif
#ifdef __AVR_ATmega32U2__
#define LAST_RAM_ADR (0x04FF)
#endif
extern uint16_t fault_word;
extern uint8_t * saved_stack_ptr;
extern uint8_t saved_stack[];
#endif /* ENABLE_DEBUG_CONSOLE */


void init_lowlevel(void);
void powersave(void);
void reset_to_bootloader(void);

#endif /* LOWLEVEL_H_ */
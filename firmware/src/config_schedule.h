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


#ifndef CONFIG_SCHEDULE_H_
#define CONFIG_SCHEDULE_H_

/* 8MHz devices and large encoded matrices */
#if defined(__AVR_ATmega32U2__) || (F_CPU == 8000000UL) || defined(BOARD_SIZE_COSTAR) || defined(BOARD_SIZE_FULLSIZE) || defined(BOARD_SIZE_JUMBO) || defined(BOARD_SIZE_SQUARE)
#define EXPANDED_SCHEDULE
#endif

/* Boards that don't have enough space/keys to handle extended features */
#if defined(__AVR_ATmega16U2__) || defined(BOARD_SIZE_CARD)
#define SIMPLE_DEVICE
#endif

#ifdef SIMPLE_DEVICE
#define NUMBER_OF_SCHEDULE_SLOTS 1
#define NUMBER_OF_ITEMS_PER_SLOT 4
#else
#ifdef EXPANDED_SCHEDULE
#define NUMBER_OF_SCHEDULE_SLOTS 4
#define NUMBER_OF_ITEMS_PER_SLOT 4
#else
#define NUMBER_OF_SCHEDULE_SLOTS 2
#define NUMBER_OF_ITEMS_PER_SLOT 5
#endif /* EXPANDED_SCHEDULE */
#endif /* SIMPLE_DEVICE */

#define SCHEDULE_PERIOD_MS 1

extern void (* const g_sched_list[NUMBER_OF_SCHEDULE_SLOTS][NUMBER_OF_ITEMS_PER_SLOT])(void);

#endif /* CONFIG_SCHEDULE_H_ */

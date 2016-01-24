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


#ifndef MOUSE_H_
#define MOUSE_H_

#include <stddef.h>
#include <stdint.h>

#include "scheduler.h"
#include "config_mouse.h"


extern int8_t g_mouse_report_X;
extern int8_t g_mouse_report_Y;
extern uint8_t g_mouse_active;
extern uint8_t g_mouse_service;
extern uint8_t g_mouse_multiply;

void init_mouse(void);
void update_mouse(void);
int8_t mouse_cycle(uint16_t total_cycle_request);

#endif /* MOUSE_H_ */
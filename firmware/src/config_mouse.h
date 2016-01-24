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


#ifndef CONFIG_MOUSE_H_
#define CONFIG_MOUSE_H_

#include "scheduler.h"

#ifndef SIMPLE_DEVICE
#define ENABLE_MOUSE
#endif /* SIMPLE_DEVICE */

#define DEFAULT_MOUSE_DELTA_MULT (15)
#define DEFAULT_MOUSE_MIN_DELTA (5)

#define MOUSE_CYCLES (10)

#endif /* CONFIG_MOUSE_H_ */
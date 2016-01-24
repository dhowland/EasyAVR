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


#ifndef PASSWORD_H_
#define PASSWORD_H_

#include <stddef.h>
#include <stdint.h>

#include "config_password.h"

#define LOWERS_LEN (26)
#define LOWERS_END (LOWERS_LEN)
#define UPPERS_LEN (26)
#define UPPERS_END (LOWERS_END + UPPERS_LEN)
#define NUMBERS_LEN (10)
#define NUMBERS_END (UPPERS_END + NUMBERS_LEN)
#define SYMBOLS_LEN (32)
#define SYMBOLS_END (NUMBERS_END + SYMBOLS_LEN)

typedef enum {
	PHASE_INIT,
	PHASE_STATE,
	PHASE_POS,
	PHASE_SCRAMBLE,
	PHASE_MOVE,
	PHASE_COMPLETE
} phase_t;

extern phase_t g_pw_phase;
extern int8_t g_pw_select;

void init_password(void);
void password_cycle(void);
void updatestate(void);
char getcdata(void);
void scramble(void);
char sc_to_char(uint16_t const sc);

#endif /* PASSWORD_H_ */
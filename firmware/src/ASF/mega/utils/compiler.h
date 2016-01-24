/**
 * \file
 *
 * \brief Commonly used includes, types and macros.
 *
 * Copyright (c) 2011-2015 Atmel Corporation. All rights reserved.
 *
 * \asf_license_start
 *
 * \page License
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. The name of Atmel may not be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * 4. This software may only be redistributed and used in connection with an
 *    Atmel microcontroller product.
 *
 * THIS SOFTWARE IS PROVIDED BY ATMEL "AS IS" AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT ARE
 * EXPRESSLY AND SPECIFICALLY DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * \asf_license_stop
 *
 */
/*
 * Support and FAQ: visit <a href="http://www.atmel.com/design-support/">Atmel Support</a>
 */
#ifndef UTILS_COMPILER_H
#define UTILS_COMPILER_H

#if defined(__GNUC__)
#	include <avr/io.h>
#elif defined(__ICCAVR__)
#	include <ioavr.h>
#	include <intrinsics.h>
#else
#	error "Unsupported compiler."
#endif

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>

#include <parts.h>

#ifdef __ICCAVR__
/*! \name Compiler Keywords
 *
 * Port of some keywords from GCC to IAR Embedded Workbench.
 */
//! @{
#define __asm__              asm
#define __inline__           inline
#define __volatile__
//! @}
#endif

/**
 * \def UNUSED
 * \brief Marking \a v as a unused parameter or value.
 */
#define UNUSED(v)          (void)(v)

/**
 * \def unused
 * \brief Marking \a v as a unused parameter or value.
 */
#define unused(v)          do { (void)(v); } while(0)

/**
 * \def barrier
 * \brief Memory barrier
 */
#ifdef __GNUC__
#  define barrier()        asm volatile("" ::: "memory")
#else
#  define barrier()        asm ("")
#endif

/*
 * AVR arch does not care about alignment anyway.
 */
#define COMPILER_PACK_RESET(alignment)
#define COMPILER_PACK_SET(alignment)

//_____ M A C R O S ________________________________________________________


/**
 * \def __always_inline
 * \brief The function should always be inlined.
 *
 * This annotation instructs the compiler to ignore its inlining
 * heuristics and inline the function no matter how big it thinks it
 * becomes.
 */
#if (defined __GNUC__)
#	define __always_inline   inline __attribute__((__always_inline__))
#elif (defined __ICCAVR__)
#	define __always_inline   _Pragma("inline=forced")
#endif

/**
 * \def __always_optimize
 * \brief The function should always be optimized.
 *
 * This annotation instructs the compiler to ignore global optimization
 * settings and always compile the function with a high level of
 * optimization.
 */
#if (defined __GNUC__)
	#define __always_optimize   __attribute__((optimize(3)))
#elif (defined __ICCAVR__)
	#define __always_optimize   _Pragma("optimize=high")
#endif


/*! \brief This macro is used to test fatal errors.
 *
 * The macro tests if the expression is false. If it is, a fatal error is
 * detected and the application hangs up. If TEST_SUITE_DEFINE_ASSERT_MACRO
 * is defined, a unit test version of the macro is used, to allow execution
 * of further tests after a false expression.
 *
 * \param expr  Expression to evaluate and supposed to be nonzero.
 */
#if defined(_ASSERT_ENABLE_)
#  if defined(TEST_SUITE_DEFINE_ASSERT_MACRO)
	// Assert() is defined in unit_test/suite.h
#    include "unit_test/suite.h"
#  else
#    define Assert(expr) \
	{\
		if (!(expr)) while (true);\
	}
#  endif
#else
#  define Assert(expr) ((void) 0)
#endif


/*! \name MCU Endianism Handling
 */
//! @{
#define MSB(u16)             (((uint8_t* )&u16)[1])
#define LSB(u16)             (((uint8_t* )&u16)[0])
//! @}

#include "interrupt.h"
#include "progmem.h"

#if (defined __GNUC__)
  #define SHORTENUM                           __attribute__ ((packed))
#elif (defined __ICCAVR__)
  #define SHORTENUM                           /**/
#endif

#if (defined __GNUC__)
  #define FUNC_PTR                            void *
#elif (defined __ICCAVR__)
#if (FLASHEND > 0x1FFFF)    // Required for program code larger than 128K
  #define FUNC_PTR                            void __farflash *
#else
  #define FUNC_PTR                            void *
#endif  /* ENABLE_FAR_FLASH */
#endif


#if (defined __GNUC__)
  #define FLASH_DECLARE(x)                  const x __attribute__((__progmem__))
#elif (defined __ICCAVR__)
  #define FLASH_DECLARE(x)                  const __flash x
#endif

#if (defined __GNUC__)
  #define FLASH_EXTERN(x) extern const x
#elif (defined __ICCAVR__)
  #define FLASH_EXTERN(x) extern const __flash x
#endif


/*Defines the Flash Storage for the request and response of MAC*/
#define CMD_ID_OCTET    (0)

/* Converting of values from CPU endian to little endian. */
#define CPU_ENDIAN_TO_LE16(x)   (x)
#define CPU_ENDIAN_TO_LE32(x)   (x)
#define CPU_ENDIAN_TO_LE64(x)   (x)

/* Converting of values from little endian to CPU endian. */
#define LE16_TO_CPU_ENDIAN(x)   (x)
#define LE32_TO_CPU_ENDIAN(x)   (x)
#define LE64_TO_CPU_ENDIAN(x)   (x)

/* Converting of constants from little endian to CPU endian. */
#define CLE16_TO_CPU_ENDIAN(x)  (x)
#define CLE32_TO_CPU_ENDIAN(x)  (x)
#define CLE64_TO_CPU_ENDIAN(x)  (x)

/* Converting of constants from CPU endian to little endian. */
#define CCPU_ENDIAN_TO_LE16(x)  (x)
#define CCPU_ENDIAN_TO_LE32(x)  (x)
#define CCPU_ENDIAN_TO_LE64(x)  (x)

#if (defined __GNUC__)
  #define ADDR_COPY_DST_SRC_16(dst, src)  memcpy((&(dst)), (&(src)), sizeof(uint16_t))
  #define ADDR_COPY_DST_SRC_64(dst, src)  memcpy((&(dst)), (&(src)), sizeof(uint64_t))

/* Converts a 2 Byte array into a 16-Bit value */
#define convert_byte_array_to_16_bit(data) \
    (*(uint16_t *)(data))

/* Converts a 4 Byte array into a 32-Bit value */
#define convert_byte_array_to_32_bit(data) \
    (*(uint32_t *)(data))

/* Converts a 8 Byte array into a 64-Bit value */
#define convert_byte_array_to_64_bit(data) \
    (*(uint64_t *)(data))

/* Converts a 16-Bit value into a 2 Byte array */
#define convert_16_bit_to_byte_array(value, data) \
    ((*(uint16_t *)(data)) = (uint16_t)(value))

/* Converts spec 16-Bit value into a 2 Byte array */
#define convert_spec_16_bit_to_byte_array(value, data) \
    ((*(uint16_t *)(data)) = (uint16_t)(value))

/* Converts spec 16-Bit value into a 2 Byte array */
#define convert_16_bit_to_byte_address(value, data) \
    ((*(uint16_t *)(data)) = (uint16_t)(value))

/* Converts a 32-Bit value into a 4 Byte array */
#define convert_32_bit_to_byte_array(value, data) \
    ((*(uint32_t *)(data)) = (uint32_t)(value))

/* Converts a 64-Bit value into  a 8 Byte array */
/* Here memcpy requires much less footprint */
#define convert_64_bit_to_byte_array(value, data) \
    memcpy((data), (&(value)), sizeof(uint64_t))

#elif (defined __ICCAVR__)
  #define ADDR_COPY_DST_SRC_16(dst, src)  ((dst) = (src))
  #define ADDR_COPY_DST_SRC_64(dst, src)  ((dst) = (src))

/* Converts a 2 Byte array into a 16-Bit value */
#define convert_byte_array_to_16_bit(data) \
    (*(uint16_t *)(data))

/* Converts a 4 Byte array into a 32-Bit value */
#define convert_byte_array_to_32_bit(data) \
    (*(uint32_t *)(data))

/* Converts a 8 Byte array into a 64-Bit value */
#define convert_byte_array_to_64_bit(data) \
    (*(uint64_t *)(data))

/* Converts a 16-Bit value into a 2 Byte array */
#define convert_16_bit_to_byte_array(value, data) \
    ((*(uint16_t *)(data)) = (uint16_t)(value))

/* Converts spec 16-Bit value into a 2 Byte array */
#define convert_spec_16_bit_to_byte_array(value, data) \
    ((*(uint16_t *)(data)) = (uint16_t)(value))

/* Converts spec 16-Bit value into a 2 Byte array */
#define convert_16_bit_to_byte_address(value, data) \
    ((*(uint16_t *)(data)) = (uint16_t)(value))

/* Converts a 32-Bit value into a 4 Byte array */
#define convert_32_bit_to_byte_array(value, data) \
    ((*(uint32_t *)(data)) = (uint32_t)(value))

/* Converts a 64-Bit value into  a 8 Byte array */
#define convert_64_bit_to_byte_array(value, data) \
    ((*(uint64_t *)(data)) = (uint64_t)(value))
#endif

#define MEMCPY_ENDIAN memcpy
#define PGM_READ_BLOCK(dst, src, len) memcpy_P((dst), (src), (len))

#if (defined __GNUC__)
  #define PGM_READ_BYTE(x) pgm_read_byte(x)
  #define PGM_READ_WORD(x) pgm_read_word(x)
#elif (defined __ICCAVR__)
  #define PGM_READ_BYTE(x) *(x)
  #define PGM_READ_WORD(x) *(x)
#endif


typedef uint8_t                 U8 ;  //!< 8-bit unsigned integer.
typedef uint16_t                U16;  //!< 16-bit unsigned integer.
typedef uint32_t                U32;  //!< 32-bit unsigned integer.
typedef unsigned long long int  U64;  //!< 64-bit unsigned integer.

/*! \brief Toggles the endianism of \a u16 (by swapping its bytes).
 *
 * \param u16 U16 of which to toggle the endianism.
 *
 * \return Value resulting from \a u16 with toggled endianism.
 *
 * \note More optimized if only used with values known at compile time.
 */
#define Swap16(u16) ((U16)(((U16)(u16) >> 8) |\
                           ((U16)(u16) << 8)))

/*! \brief Toggles the endianism of \a u32 (by swapping its bytes).
 *
 * \param u32 U32 of which to toggle the endianism.
 *
 * \return Value resulting from \a u32 with toggled endianism.
 *
 * \note More optimized if only used with values known at compile time.
 */
#define Swap32(u32) ((U32)(((U32)Swap16((U32)(u32) >> 16)) |\
                           ((U32)Swap16((U32)(u32)) << 16)))

/*! \brief Toggles the endianism of \a u64 (by swapping its bytes).
 *
 * \param u64 U64 of which to toggle the endianism.
 *
 * \return Value resulting from \a u64 with toggled endianism.
 *
 * \note More optimized if only used with values known at compile time.
 */
#define Swap64(u64) ((U64)(((U64)Swap32((U64)(u64) >> 32)) |\
                           ((U64)Swap32((U64)(u64)) << 32)))
						   
#if (defined __GNUC__)
  #define nop() do { __asm__ __volatile__ ("nop"); } while (0)
#elif (defined __ICCAVR__)
  #define nop() __no_operation()
#endif

#if (defined __GNUC__)
#define FORCE_INLINE(type, name, ...) \
    static inline type name(__VA_ARGS__) __attribute__((always_inline)); \
    static inline type name(__VA_ARGS__)
#elif (defined __ICCAVR__)
#define FORCE_INLINE(type, name, ...) \
    PRAGMA(inline=forced) \
    static inline type name(__VA_ARGS__)
#endif

#endif  // UTILS_COMPILER_H

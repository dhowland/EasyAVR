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


#ifndef USB_DESCRIPTOR_H_
#define USB_DESCRIPTOR_H_

#include <stddef.h>
#include <stdint.h>

#include <LUFA/Drivers/USB/USB.h>

#include "scheduler.h"

#define PRODUCT_STR_LEN (36)
#define PRODUCT_STRING  L"EasyAVR Multimedia Keyboard v#.##.##"

/* Must be 6 for boot-compliant keyboard,
   Must be 16 for NKRO */
#define KEYBOARD_ARRAY_LENGTH (16)
#define MAX_NKRO_CODE (0x7F)

#define USB_KEYBOARD_UPDATE_RATE_MS (1)
#define USB_MOUSE_UPDATE_RATE_MS (5)
#define USB_MEDIA_UPDATE_RATE_MS (8)

/** Endpoint address of the Keyboard HID reporting IN endpoint. */
#define KEYBOARD_INTERFACE (0x00)
#define KEYBOARD_IN_EPADDR        (ENDPOINT_DIR_IN | 1)
#define HID_EPSIZE_KEYBOARD (KEYBOARD_ARRAY_LENGTH + 2)

#ifdef ENABLE_MOUSE

#define TOTAL_INTERFACES (0x03)

/** Endpoint address of the Mouse HID reporting IN endpoint. */
#define MOUSE_INTERFACE (0x01)
#define MOUSE_IN_EPADDR           (ENDPOINT_DIR_IN | 2)
#define HID_EPSIZE_MOUSE (3)

/* Media keys */
#define MEDIA_INTERFACE (0x02)
#define MEDIA_IN_EPADDR           (ENDPOINT_DIR_IN | 3)
#define HID_EPSIZE_MEDIA (2)

#else

#define TOTAL_INTERFACES (0x02)

/* Media keys */
#define MEDIA_INTERFACE (0x01)
#define MEDIA_IN_EPADDR           (ENDPOINT_DIR_IN | 2)
#define HID_EPSIZE_MEDIA (2)

#endif /* ENABLE_MOUSE */


/** Type define for the device configuration descriptor structure. This must be defined in the
	*  application code, as the configuration descriptor contains several sub-descriptors which
	*  vary between devices, and which describe the device's usage to the host.
	*/
typedef struct
{
	USB_Descriptor_Configuration_Header_t Config;

	// Keyboard HID Interface
	USB_Descriptor_Interface_t            HID1_KeyboardInterface;
	USB_HID_Descriptor_HID_t              HID1_KeyboardHID;
	USB_Descriptor_Endpoint_t             HID1_ReportINEndpoint;

#ifdef ENABLE_MOUSE
	// Mouse HID Interface
	USB_Descriptor_Interface_t            HID2_MouseInterface;
	USB_HID_Descriptor_HID_t              HID2_MouseHID;
	USB_Descriptor_Endpoint_t             HID2_ReportINEndpoint;
#endif /* ENABLE_MOUSE */

	// Media HID Interface
	USB_Descriptor_Interface_t            HID3_MediaInterface;
	USB_HID_Descriptor_HID_t              HID3_MediaHID;
	USB_Descriptor_Endpoint_t             HID3_ReportINEndpoint;
} USB_Descriptor_Configuration_t;

#ifndef SIMPLE_DEVICE
typedef struct
{
	USB_Descriptor_Configuration_Header_t Config;

	// Keyboard HID Interface
	USB_Descriptor_Interface_t            HID1_KeyboardInterface;
	USB_HID_Descriptor_HID_t              HID1_KeyboardHID;
	USB_Descriptor_Endpoint_t             HID1_ReportINEndpoint;
} USB_Descriptor_Configuration_boot_t;
#endif /* SIMPLE_DEVICE */

typedef struct
{
	uint8_t Modifier;
	uint8_t Reserved;
	uint8_t KeyCode[KEYBOARD_ARRAY_LENGTH];
} ATTR_PACKED USB_KeyboardModReport_Data_t;
		
typedef struct
{
	uint16_t  Button;
} ATTR_PACKED USB_MediaReport_Data_t;

uint16_t CALLBACK_USB_GetDescriptor(const uint16_t wValue,
									const uint8_t wIndex,
									const void** const DescriptorAddress)
									ATTR_WARN_UNUSED_RESULT ATTR_NON_NULL_PTR_ARG(3);

void EVENT_USB_Device_Connect(void);
void EVENT_USB_Device_Disconnect(void);
void EVENT_USB_Device_ConfigurationChanged(void);
void EVENT_USB_Device_ControlRequest(void);
void EVENT_USB_Device_StartOfFrame(void);
void EVENT_USB_Device_Reset(void);
void EVENT_USB_Device_Suspend(void);
void EVENT_USB_Device_WakeUp(void);

bool CALLBACK_HID_Device_CreateHIDReport(USB_ClassInfo_HID_Device_t* const HIDInterfaceInfo,
										 uint8_t* const ReportID,
										 const uint8_t ReportType,
										 void* ReportData,
										 uint16_t* const ReportSize);
void CALLBACK_HID_Device_ProcessHIDReport(USB_ClassInfo_HID_Device_t* const HIDInterfaceInfo,
										  const uint8_t ReportID,
										  const uint8_t ReportType,
										  const void* ReportData,
										  const uint16_t ReportSize);

void init_USB(void);
void USB_cycle(void);
void USB_wakeup(void);


#endif /* USB_DESCRIPTOR_H_ */

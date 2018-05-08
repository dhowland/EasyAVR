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

#define KEYBOARD_FLAG (0x01)
#define MEDIA_FLAG (0x02)
#define NKRO_FLAG (0x04)
#define MOUSE_FLAG (0x08)

#define PRODUCT_STR_LEN (36)
#define PRODUCT_STRING  L"EasyAVR Multimedia Keyboard v#.##.##"

#define NKRO_ARRAY_LENGTH (13)
#define NKRO_FIELD_BITS (0x68)
#define MAX_NKRO_CODE (0x67)

#define USB_KEYBOARD_UPDATE_RATE_MS (1)
#define USB_MOUSE_UPDATE_RATE_MS (5)
#define USB_MEDIA_UPDATE_RATE_MS (8)

#define KEYBOARD_INTERFACE (0x00)
#define KEYBOARD_IN_EPADDR        (ENDPOINT_DIR_IN | 1)
#define HID_EPSIZE_KEYBOARD (0x08)

#define MEDIA_INTERFACE (0x01)
#define MEDIA_IN_EPADDR           (ENDPOINT_DIR_IN | 2)
#define HID_EPSIZE_MEDIA (0x03)

#define NKRO_INTERFACE (0x02)
#define NKRO_IN_EPADDR            (ENDPOINT_DIR_IN | 3)
#define HID_EPSIZE_NKRO (NKRO_ARRAY_LENGTH + 1)

#define MOUSE_INTERFACE (0x03)
#define MOUSE_IN_EPADDR           (ENDPOINT_DIR_IN | 4)
#define HID_EPSIZE_MOUSE (0x03)

#define TOTAL_INTERFACES (0x04)

typedef struct
{
	USB_Descriptor_Configuration_Header_t Config;

	// Keyboard HID Interface
	USB_Descriptor_Interface_t            HID1_KeyboardInterface;
	USB_HID_Descriptor_HID_t              HID1_KeyboardHID;
	USB_Descriptor_Endpoint_t             HID1_ReportINEndpoint;

	// Media HID Interface
	USB_Descriptor_Interface_t            HID2_MediaInterface;
	USB_HID_Descriptor_HID_t              HID2_MediaHID;
	USB_Descriptor_Endpoint_t             HID2_ReportINEndpoint;

	// NKRO HID Interface
	USB_Descriptor_Interface_t            HID3_NkroInterface;
	USB_HID_Descriptor_HID_t              HID3_NkroHID;
	USB_Descriptor_Endpoint_t             HID3_ReportINEndpoint;

	// Mouse HID Interface
	USB_Descriptor_Interface_t            HID4_MouseInterface;
	USB_HID_Descriptor_HID_t              HID4_MouseHID;
	USB_Descriptor_Endpoint_t             HID4_ReportINEndpoint;
} USB_Descriptor_Configuration_t;

typedef struct
{
	uint8_t Modifier;
	uint8_t KeyCode[NKRO_ARRAY_LENGTH];
} ATTR_PACKED USB_NkroReport_Data_t;
		
typedef struct
{
	uint16_t  Button;
} ATTR_PACKED USB_MediaReport_Data_t;

typedef struct
{
	uint8_t  Field;
} ATTR_PACKED USB_PowerReport_Data_t;

extern USB_ClassInfo_HID_Device_t Keyboard_HID_Interface;
extern USB_ClassInfo_HID_Device_t Mouse_HID_Interface;
extern USB_ClassInfo_HID_Device_t Media_HID_Interface;
extern USB_ClassInfo_HID_Device_t Nkro_HID_Interface;

uint16_t CALLBACK_USB_GetDescriptor(const uint16_t wValue,
									const uint16_t wIndex,
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
void USB_service(void);
void USB_wakeup(void);


#endif /* USB_DESCRIPTOR_H_ */

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
#include <avr/pgmspace.h>

#include "debug.h"
#include "scheduler.h"
#include "autokey.h"
#include "keymap.h"
#include "mouse.h"
#include "led.h"
#include "nvm.h"
#include "USB.h"


const uint8_t PROGMEM EndpointOptions = 0x0F;

const USB_Descriptor_HIDReport_Datatype_t PROGMEM KeyboardReport[] =
{
	HID_DESCRIPTOR_KEYBOARD(6)
};

const USB_Descriptor_HIDReport_Datatype_t PROGMEM NkroReport[] =
{
	HID_RI_USAGE_PAGE(8, 0x01),
	HID_RI_USAGE(8, 0x06),
	HID_RI_COLLECTION(8, 0x01),
		HID_RI_USAGE_PAGE(8, 0x07),
		HID_RI_USAGE_MINIMUM(8, 0xE0),
		HID_RI_USAGE_MAXIMUM(8, 0xE7),
		HID_RI_LOGICAL_MINIMUM(8, 0x00),
		HID_RI_LOGICAL_MAXIMUM(8, 0x01),
		HID_RI_REPORT_SIZE(8, 0x01),
		HID_RI_REPORT_COUNT(8, 0x08),
		HID_RI_INPUT(8, HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE),
	
		HID_RI_LOGICAL_MINIMUM(8, 0x00),
		HID_RI_LOGICAL_MAXIMUM(8, 0x01),
		HID_RI_USAGE_PAGE(8, 0x07),
		HID_RI_USAGE_MINIMUM(8, 0x00),
		HID_RI_USAGE_MAXIMUM(8, MAX_NKRO_CODE),
		HID_RI_REPORT_COUNT(8, NKRO_FIELD_BITS),
		HID_RI_REPORT_SIZE(8, 0x01),
		HID_RI_INPUT(8, HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE),
	HID_RI_END_COLLECTION(0)
};

const USB_Descriptor_HIDReport_Datatype_t PROGMEM MouseReport[] =
{
	HID_DESCRIPTOR_MOUSE(-127, 127, 0, 0, 3, false)
};

const USB_Descriptor_HIDReport_Datatype_t PROGMEM MediaReport[] =
{
	/* https://web.archive.org/web/20100302061644/http://www.microsoft.com/whdc/archive/w2kbd.mspx */
	/* http://download.microsoft.com/download/E/3/A/E3AEC7D7-245D-491F-BB8A-E1E05A03677A/keyboard-support-windows-8.docx */
	HID_RI_USAGE_PAGE(8, 0x0C),				// Consumer
	HID_RI_USAGE(8, 0x01),					// Consumer Control
	HID_RI_COLLECTION(8, 0x01),				// Application
		HID_RI_REPORT_ID(8, 0x02),
		HID_RI_LOGICAL_MINIMUM(16, 0x0001),	// Consumer Control
		HID_RI_LOGICAL_MAXIMUM(16, 0x029C),	// Slow
		HID_RI_USAGE_MINIMUM(16, 0x0001),	// Consumer Control
		HID_RI_USAGE_MAXIMUM(16, 0x029C),	// Slow
		HID_RI_REPORT_SIZE(8, 0x10),		// 16 bits
		HID_RI_REPORT_COUNT(8, 0x01),		// one report
		HID_RI_INPUT(8, HID_IOF_DATA | HID_IOF_ARRAY | HID_IOF_ABSOLUTE),
	HID_RI_END_COLLECTION(0),
	
	HID_RI_USAGE_PAGE(8, 0x01),				// Generic Desktop
	HID_RI_USAGE(8, 0x80),					// System Control
	HID_RI_COLLECTION(8, 0x01),
		HID_RI_REPORT_ID(8, 0x03),
		//HID_RI_LOGICAL_MINIMUM(8, 0x00),
		//HID_RI_LOGICAL_MAXIMUM(8, 0x01),
		HID_RI_USAGE_MINIMUM(8, 0x81),		// System Power
		HID_RI_USAGE_MAXIMUM(8, 0x83),		// System Wake
		HID_RI_REPORT_SIZE(8, 0x01),
		HID_RI_REPORT_COUNT(8, 0x03),
		HID_RI_INPUT(8, HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_RELATIVE | HID_IOF_PREFERRED_STATE),
		HID_RI_REPORT_COUNT(8, 0x05),
		HID_RI_INPUT(8, HID_IOF_CONSTANT),
	HID_RI_END_COLLECTION(0)
};

const USB_Descriptor_Device_t PROGMEM DeviceDescriptor =
{
	.Header                 = {.Size = sizeof(USB_Descriptor_Device_t), .Type = DTYPE_Device},

	.USBSpecification       = VERSION_BCD(2,0,0),
	.Class                  = USB_CSCP_NoDeviceClass,
	.SubClass               = USB_CSCP_NoDeviceSubclass,
	.Protocol               = USB_CSCP_NoDeviceProtocol,

	.Endpoint0Size          = FIXED_CONTROL_ENDPOINT_SIZE,

	.VendorID               = 0x03EB,
	.ProductID              = 0x20FF,
	.ReleaseNumber          = VERSION_BCD(0,1,0),

	.ManufacturerStrIndex   = NO_DESCRIPTOR,
	.ProductStrIndex        = 0x01,
	.SerialNumStrIndex      = NO_DESCRIPTOR,

	.NumberOfConfigurations = FIXED_NUM_CONFIGURATIONS
};

const USB_Descriptor_Configuration_t PROGMEM ConfigurationDescriptor =
{
	.Config =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Configuration_Header_t), .Type = DTYPE_Configuration},

		.TotalConfigurationSize = sizeof(USB_Descriptor_Configuration_t),
		.TotalInterfaces        = TOTAL_INTERFACES,

		.ConfigurationNumber    = 1,
		.ConfigurationStrIndex  = NO_DESCRIPTOR,

		.ConfigAttributes       = (USB_CONFIG_ATTR_RESERVED | USB_CONFIG_ATTR_REMOTEWAKEUP),

		.MaxPowerConsumption    = USB_CONFIG_POWER_MA(500)
	},

	.HID1_KeyboardInterface =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Interface_t), .Type = DTYPE_Interface},

		.InterfaceNumber        = KEYBOARD_INTERFACE,
		.AlternateSetting       = 0x00,

		.TotalEndpoints         = 1,

		.Class                  = HID_CSCP_HIDClass,
		.SubClass               = HID_CSCP_BootSubclass,
		.Protocol               = HID_CSCP_KeyboardBootProtocol,

		.InterfaceStrIndex      = NO_DESCRIPTOR
	},

	.HID1_KeyboardHID =
	{
		.Header                 = {.Size = sizeof(USB_HID_Descriptor_HID_t), .Type = HID_DTYPE_HID},

		.HIDSpec                = VERSION_BCD(1,11,0),
		.CountryCode            = 0x00,
		.TotalReportDescriptors = 1,
		.HIDReportType          = HID_DTYPE_Report,
		.HIDReportLength        = sizeof(KeyboardReport)
	},

	.HID1_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},

		.EndpointAddress        = KEYBOARD_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = HID_EPSIZE_KEYBOARD,
		.PollingIntervalMS      = USB_KEYBOARD_UPDATE_RATE_MS
	},

	.HID2_MediaInterface =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Interface_t), .Type = DTYPE_Interface},

		.InterfaceNumber        = MEDIA_INTERFACE,
		.AlternateSetting       = 0x00,

		.TotalEndpoints         = 1,

		.Class                  = HID_CSCP_HIDClass,
		.SubClass               = HID_CSCP_NonBootSubclass,
		.Protocol               = HID_CSCP_NonBootProtocol,

		.InterfaceStrIndex      = NO_DESCRIPTOR
	},

	.HID2_MediaHID =
	{
		.Header                 = {.Size = sizeof(USB_HID_Descriptor_HID_t), .Type = HID_DTYPE_HID},

		.HIDSpec                = VERSION_BCD(1,11,0),
		.CountryCode            = 0x00,
		.TotalReportDescriptors = 1,
		.HIDReportType          = HID_DTYPE_Report,
		.HIDReportLength        = sizeof(MediaReport)
	},

	.HID2_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},

		.EndpointAddress        = MEDIA_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = HID_EPSIZE_MEDIA,
		.PollingIntervalMS      = USB_MEDIA_UPDATE_RATE_MS
	},

	.HID3_NkroInterface =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Interface_t), .Type = DTYPE_Interface},

		.InterfaceNumber        = NKRO_INTERFACE,
		.AlternateSetting       = 0x00,

		.TotalEndpoints         = 1,

		.Class                  = HID_CSCP_HIDClass,
		.SubClass               = HID_CSCP_NonBootSubclass,
		.Protocol               = HID_CSCP_NonBootProtocol,

		.InterfaceStrIndex      = NO_DESCRIPTOR
	},

	.HID3_NkroHID =
	{
		.Header                 = {.Size = sizeof(USB_HID_Descriptor_HID_t), .Type = HID_DTYPE_HID},

		.HIDSpec                = VERSION_BCD(1,11,0),
		.CountryCode            = 0x00,
		.TotalReportDescriptors = 1,
		.HIDReportType          = HID_DTYPE_Report,
		.HIDReportLength        = sizeof(NkroReport)
	},

	.HID3_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},

		.EndpointAddress        = NKRO_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = HID_EPSIZE_NKRO,
		.PollingIntervalMS      = USB_KEYBOARD_UPDATE_RATE_MS
	},

	.HID4_MouseInterface =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Interface_t), .Type = DTYPE_Interface},

		.InterfaceNumber        = MOUSE_INTERFACE,
		.AlternateSetting       = 0x00,

		.TotalEndpoints         = 1,

		.Class                  = HID_CSCP_HIDClass,
		.SubClass               = HID_CSCP_BootSubclass,
		.Protocol               = HID_CSCP_MouseBootProtocol,

		.InterfaceStrIndex      = NO_DESCRIPTOR
	},

	.HID4_MouseHID =
	{
		.Header                 = {.Size = sizeof(USB_HID_Descriptor_HID_t), .Type = HID_DTYPE_HID},

		.HIDSpec                = VERSION_BCD(1,11,0),
		.CountryCode            = 0x00,
		.TotalReportDescriptors = 1,
		.HIDReportType          = HID_DTYPE_Report,
		.HIDReportLength        = sizeof(MouseReport)
	},

	.HID4_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},

		.EndpointAddress        = MOUSE_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = HID_EPSIZE_MOUSE,
		.PollingIntervalMS      = USB_MOUSE_UPDATE_RATE_MS
	}
};

const USB_Descriptor_String_t PROGMEM LanguageString =
{
	.Header                 = {.Size = USB_STRING_LEN(1), .Type = DTYPE_String},

	.UnicodeString          = {LANGUAGE_ID_ENG}
};

const USB_Descriptor_String_t PROGMEM ProductString =
{
	.Header                 = {.Size = USB_STRING_LEN(PRODUCT_STR_LEN), .Type = DTYPE_String},

	.UnicodeString          = PRODUCT_STRING
};

uint16_t CALLBACK_USB_GetDescriptor(const uint16_t wValue,
                                    const uint16_t wIndex,
                                    const void** const DescriptorAddress)
{
	const uint8_t  DescriptorType   = (wValue >> 8);
	const uint8_t  DescriptorNumber = (wValue & 0xFF);
	const uint8_t  DescriptorIndex  = (wIndex & 0xFF);

	const void* Address = NULL;
	uint16_t    Size    = NO_DESCRIPTOR;

	switch (DescriptorType)
	{
		case DTYPE_Device:
			Address = &DeviceDescriptor;
			Size    = sizeof(USB_Descriptor_Device_t);
			break;
		case DTYPE_Configuration:
			Address = &ConfigurationDescriptor;
			Size    = pgm_read_word(&ConfigurationDescriptor.Config.TotalConfigurationSize);
			break;
		case DTYPE_String:
			switch (DescriptorNumber)
			{
				case 0x00:
					Address = &LanguageString;
					Size    = pgm_read_byte(&LanguageString.Header.Size);
					break;
				case 0x01:
					Address = &ProductString;
					Size    = pgm_read_byte(&ProductString.Header.Size);
					break;
			}
			break;
		case HID_DTYPE_HID:
			// Don't use a switch statement, because the compiler insists on using
			// up all my RAM with a CSWTCH structure (jump table)
			// https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49857
			Address = (&ConfigurationDescriptor.HID1_KeyboardHID + (DescriptorIndex *
			           (sizeof(USB_HID_Descriptor_HID_t) +
			            sizeof(USB_Descriptor_Endpoint_t) +
			            sizeof(USB_Descriptor_Interface_t))));
			Size = sizeof(USB_HID_Descriptor_HID_t);
			break;
		case HID_DTYPE_Report:
			if (DescriptorIndex == KEYBOARD_INTERFACE)
			{
				Address = &KeyboardReport;
				Size    = sizeof(KeyboardReport);
			}
			else if (DescriptorIndex == Media_HID_Interface.Config.InterfaceNumber)
			{
				Address = &MediaReport;
				Size    = sizeof(MediaReport);
			}
#ifndef SIMPLE_DEVICE
			else if (DescriptorIndex == Nkro_HID_Interface.Config.InterfaceNumber)
			{
				Address = &NkroReport;
				Size    = sizeof(NkroReport);
			}
			else if (DescriptorIndex == Mouse_HID_Interface.Config.InterfaceNumber)
			{
				Address = &MouseReport;
				Size    = sizeof(MouseReport);
			}
#endif /* SIMPLE_DEVICE */
			break;
	}

	*DescriptorAddress = Address;
	return Size;
}

USB_ClassInfo_HID_Device_t Keyboard_HID_Interface =
	{
		.Config =
		{
			.InterfaceNumber              = KEYBOARD_INTERFACE,
			.ReportINEndpoint             =
			{
				.Address              = KEYBOARD_IN_EPADDR,
				.Size                 = HID_EPSIZE_KEYBOARD,
				.Banks                = 1,
			},
			.PrevReportINBuffer           = NULL,
			.PrevReportINBufferSize       = sizeof(USB_KeyboardReport_Data_t),
		},
	};

#ifndef SIMPLE_DEVICE
USB_ClassInfo_HID_Device_t Mouse_HID_Interface =
	{
		.Config =
			{
				// .InterfaceNumber              = MOUSE_INTERFACE,
				.InterfaceNumber              = 0,  // disabled by default
				.ReportINEndpoint             =
					{
						.Address              = MOUSE_IN_EPADDR,
						.Size                 = HID_EPSIZE_MOUSE,
						.Banks                = 1,
					},
				.PrevReportINBuffer           = NULL,
				.PrevReportINBufferSize       = sizeof(USB_MouseReport_Data_t),
			},
	};
#endif /* SIMPLE_DEVICE */

USB_ClassInfo_HID_Device_t Media_HID_Interface =
{
	.Config =
	{
		// .InterfaceNumber              = MEDIA_INTERFACE,
		.InterfaceNumber              = 0,  // disabled by default
		.ReportINEndpoint             =
		{
			.Address              = MEDIA_IN_EPADDR,
			.Size                 = HID_EPSIZE_MEDIA,
			.Banks                = 1,
		},
		.PrevReportINBuffer           = NULL,
		.PrevReportINBufferSize       = sizeof(USB_MediaReport_Data_t),
	},
};

#ifndef SIMPLE_DEVICE
USB_ClassInfo_HID_Device_t Nkro_HID_Interface =
{
	.Config =
	{
		// .InterfaceNumber              = NKRO_INTERFACE,
		.InterfaceNumber              = 0,  // disabled by default
		.ReportINEndpoint             =
		{
			.Address              = NKRO_IN_EPADDR,
			.Size                 = HID_EPSIZE_NKRO,
			.Banks                = 1,
		},
		.PrevReportINBuffer           = NULL,
		.PrevReportINBufferSize       = sizeof(USB_NkroReport_Data_t),
	},
};
#endif /* SIMPLE_DEVICE */

void EVENT_USB_Device_Connect(void)
{
	//report_event(EVENT_CODE_USB_CONNECT, 0, MODE_REOCCUR);
	set_led_status(LED_STATUS_CONNECT);
}

void EVENT_USB_Device_Disconnect(void)
{
	//report_event(EVENT_CODE_USB_DISCONNECT, 0, MODE_REOCCUR);
	//set_led_status(LED_STATUS_DISCONNECT);
}

void EVENT_USB_Device_ConfigurationChanged(void)
{
	bool ConfigSuccess = true;

	ConfigSuccess &= HID_Device_ConfigureEndpoints(&Keyboard_HID_Interface);
	if (Media_HID_Interface.Config.InterfaceNumber)
		ConfigSuccess &= HID_Device_ConfigureEndpoints(&Media_HID_Interface);
#ifndef SIMPLE_DEVICE
	if (Nkro_HID_Interface.Config.InterfaceNumber)
		ConfigSuccess &= HID_Device_ConfigureEndpoints(&Nkro_HID_Interface);
	if (Mouse_HID_Interface.Config.InterfaceNumber)
		ConfigSuccess &= HID_Device_ConfigureEndpoints(&Mouse_HID_Interface);
#endif /* SIMPLE_DEVICE */
	
	if (ConfigSuccess)
		set_led_status(LED_STATUS_NORM);
	else
		set_led_status(LED_STATUS_ERROR);
	
	//report_event(EVENT_CODE_USB_CONFIG_CHANGE, 0, MODE_REOCCUR);
	USB_Device_EnableSOFEvents();
}

void EVENT_USB_Device_ControlRequest(void)
{
	HID_Device_ProcessControlRequest(&Keyboard_HID_Interface);
	if (Media_HID_Interface.Config.InterfaceNumber)
		HID_Device_ProcessControlRequest(&Media_HID_Interface);
#ifndef SIMPLE_DEVICE
	if (Nkro_HID_Interface.Config.InterfaceNumber)
		HID_Device_ProcessControlRequest(&Nkro_HID_Interface);
	if (Mouse_HID_Interface.Config.InterfaceNumber)
		HID_Device_ProcessControlRequest(&Mouse_HID_Interface);
#endif /* SIMPLE_DEVICE */
}

void EVENT_USB_Device_StartOfFrame(void)
{
	HID_Device_MillisecondElapsed(&Keyboard_HID_Interface);
	if (Media_HID_Interface.Config.InterfaceNumber)
		HID_Device_MillisecondElapsed(&Media_HID_Interface);
#ifndef SIMPLE_DEVICE
	if (Nkro_HID_Interface.Config.InterfaceNumber)
		HID_Device_MillisecondElapsed(&Nkro_HID_Interface);
	if (Mouse_HID_Interface.Config.InterfaceNumber)
		HID_Device_MillisecondElapsed(&Mouse_HID_Interface);
#endif /* SIMPLE_DEVICE */
}

void EVENT_USB_Device_Reset(void)
{
	//report_event(EVENT_CODE_USB_RESET, 0, MODE_REOCCUR);
	set_led_status(LED_STATUS_RESET);
}

void EVENT_USB_Device_Suspend(void)
{
	//report_event(EVENT_CODE_USB_SUSPEND, 0, MODE_REOCCUR);
	set_led_status(LED_STATUS_SUSPEND);
}

void EVENT_USB_Device_WakeUp(void)
{
	//report_event(EVENT_CODE_USB_WAKEUP, 0, MODE_REOCCUR);
	set_led_status(LED_STATUS_WAKEUP);
}

bool CALLBACK_HID_Device_CreateHIDReport(USB_ClassInfo_HID_Device_t* const HIDInterfaceInfo,
                                         uint8_t* const ReportID,
                                         const uint8_t ReportType,
                                         void* ReportData,
                                         uint16_t* const ReportSize)
{
	/* Outputs are ReportData and ReportSize.  ReportData is zeroed out before calling.
	   ReportSize must be set because this could be a control request. */
	
#ifdef SIMPLE_DEVICE
	if (HIDInterfaceInfo->Config.InterfaceNumber == KEYBOARD_INTERFACE)
	{
		USB_KeyboardReport_Data_t* const KeyboardReport = (USB_KeyboardReport_Data_t*)ReportData;
		get_keyboard_report(KeyboardReport->KeyCode);
		get_modifier_report(&KeyboardReport->Modifier);
		*ReportSize = sizeof(USB_KeyboardReport_Data_t);
		if (g_alphanum_service | g_modifier_service)
		{
			g_alphanum_service = 0;
			g_modifier_service = 0;
			return true;
		}
	}
#else /* ndef SIMPLE_DEVICE */
	static uint8_t nkro_active;
	
	if (HIDInterfaceInfo->Config.InterfaceNumber == KEYBOARD_INTERFACE)
	{
		if (Nkro_HID_Interface.Config.InterfaceNumber)
		{
			nkro_active <<= 1;
			nkro_active += (!g_boot_keyboard_only && HIDInterfaceInfo->State.UsingReportProtocol);
		}
		*ReportSize = sizeof(USB_KeyboardReport_Data_t);
		if ((nkro_active & 0x01) == 0)
		{
			USB_KeyboardReport_Data_t* const KeyboardReport = (USB_KeyboardReport_Data_t*)ReportData;
			get_modifier_report(&KeyboardReport->Modifier);
			get_keyboard_report(KeyboardReport->KeyCode);
			if (g_alphanum_service | g_modifier_service)
			{
				g_alphanum_service = 0;
				g_modifier_service = 0;
				return true;
			}
		}
		else if ((nkro_active & 0x02) == 0)
		{
			/* nkro_active has just changed over, send a blank report to clear things out */
			g_alphanum_service = 0;
			g_modifier_service = 0;
			return true;
		}
	}
	else if (HIDInterfaceInfo->Config.InterfaceNumber == Nkro_HID_Interface.Config.InterfaceNumber)
	{
		*ReportSize = sizeof(USB_NkroReport_Data_t);
		if ((nkro_active & 0x01) != 0)
		{
			USB_NkroReport_Data_t* const NkroReport = (USB_NkroReport_Data_t*)ReportData;
			get_modifier_report(&NkroReport->Modifier);
			get_nkro_report(NkroReport->KeyCode);
			if (g_alphanum_service | g_modifier_service)
			{
				g_alphanum_service = 0;
				g_modifier_service = 0;
				return true;
			}
		}
		else if ((nkro_active & 0x02) != 0)
		{
			/* nkro_active has just changed over, send a blank report to clear things out */
			g_alphanum_service = 0;
			g_modifier_service = 0;
			return true;
		}
	}
	else if (HIDInterfaceInfo->Config.InterfaceNumber == Mouse_HID_Interface.Config.InterfaceNumber)
	{
		USB_MouseReport_Data_t* const MouseReport = (USB_MouseReport_Data_t*)ReportData;
		MouseReport->Button = g_mousebutton_state;
		MouseReport->X = g_mouse_report_X;
		MouseReport->Y = g_mouse_report_Y;
		*ReportSize = sizeof(USB_MouseReport_Data_t);
		if (g_mouse_service)
		{
			g_mouse_service = 0;	
			return true;
		}
	}
#endif /* SIMPLE_DEVICE */
	else
	{
		if (g_power_service | (*ReportID == 3))
		{
			((USB_PowerReport_Data_t*)ReportData)->Field = g_powermgmt_field;
			*ReportSize = sizeof(USB_PowerReport_Data_t);
			*ReportID = 0x03;
			if (g_power_service)
			{
				g_power_service = 0;
				return true;
			}
		}
		else
		{
			((USB_MediaReport_Data_t*)ReportData)->Button = g_media_key;
			*ReportSize = sizeof(USB_MediaReport_Data_t);
			*ReportID = 0x02;
			if (g_media_service)
			{
				g_media_service = 0;
				return true;
			}
		}
	}
	
	return false;
}

void CALLBACK_HID_Device_ProcessHIDReport(USB_ClassInfo_HID_Device_t* const HIDInterfaceInfo,
                                          const uint8_t ReportID,
                                          const uint8_t ReportType,
                                          const void* ReportData,
                                          const uint16_t ReportSize)
{
	static uint8_t hid_lock_flags_lpv;
	uint8_t hid_lock_flags_new;
	
	if (HIDInterfaceInfo == &Keyboard_HID_Interface)
	{
		g_hid_lock_flags = *(uint8_t*)ReportData;
		hid_lock_flags_new = g_hid_lock_flags ^ hid_lock_flags_lpv;
		hid_lock_flags_lpv = g_hid_lock_flags;
		
		if (hid_lock_flags_new)
		{
			if (!g_virtual_numlock)
			{
				if (hid_lock_flags_new & HID_KEYBOARD_LED_NUMLOCK)
				{
					if (g_hid_lock_flags & HID_KEYBOARD_LED_NUMLOCK)
					{
						led_host_on(LED_NUM_LOCK);
						led_fn_activate(LED_NUM_LOCK);
					}
					else
					{
						led_host_off(LED_NUM_LOCK);
						led_fn_deactivate(LED_NUM_LOCK);
					}
				}
			}

			if (hid_lock_flags_new & HID_KEYBOARD_LED_CAPSLOCK)
			{
				if (g_hid_lock_flags & HID_KEYBOARD_LED_CAPSLOCK)
				{
					led_host_on(LED_CAPS_LOCK);
					led_fn_activate(LED_CAPS_LOCK);
				}
				else
				{
					led_host_off(LED_CAPS_LOCK);
					led_fn_deactivate(LED_CAPS_LOCK);
				}
			}

			if (hid_lock_flags_new & HID_KEYBOARD_LED_SCROLLLOCK)
			{
				if (g_hid_lock_flags & HID_KEYBOARD_LED_SCROLLLOCK)
				{
					led_host_on(LED_SCROLL_LOCK);
					led_fn_activate(LED_SCROLL_LOCK);
					if (g_winlock_on_scrolllock)
					{
						g_winlock_flag = 1;
						led_host_on(LED_WIN_LOCK);
					}
				}
				else
				{
					led_host_off(LED_SCROLL_LOCK);
					led_fn_deactivate(LED_SCROLL_LOCK);
					if (g_winlock_on_scrolllock)
					{
						g_winlock_flag = 0;
						led_host_off(LED_WIN_LOCK);
					}
				}
			}

			if (hid_lock_flags_new & HID_KEYBOARD_LED_COMPOSE)
			{
				if (g_hid_lock_flags & HID_KEYBOARD_LED_COMPOSE)
				{
					led_host_on(LED_COMPOSE);
					led_fn_activate(LED_COMPOSE);
				}
				else
				{
					led_host_off(LED_COMPOSE);
					led_fn_deactivate(LED_COMPOSE);
				}
			}

			if (hid_lock_flags_new & HID_KEYBOARD_LED_KANA)
			{
				if (g_hid_lock_flags & HID_KEYBOARD_LED_KANA)
				{
					led_host_on(LED_KANA);
					led_fn_activate(LED_KANA);
				}
				else
				{
					led_host_off(LED_KANA);
					led_fn_deactivate(LED_KANA);
				}
			}
		}
	}
}

void init_USB(void)
{
	const uint8_t endpoint_options = pgm_read_byte(&EndpointOptions);
	uint8_t	interface_count = KEYBOARD_INTERFACE;
	
	if (endpoint_options & MEDIA_FLAG)
	{
		Media_HID_Interface.Config.InterfaceNumber = ++interface_count;
		Media_HID_Interface.Config.ReportINEndpoint.Address = (ENDPOINT_DIR_IN | (interface_count + 1));
	}
#ifndef SIMPLE_DEVICE
	if (endpoint_options & NKRO_FLAG)
	{
		Nkro_HID_Interface.Config.InterfaceNumber = ++interface_count;
		Nkro_HID_Interface.Config.ReportINEndpoint.Address = (ENDPOINT_DIR_IN | (interface_count + 1));
	}
	if (endpoint_options & MOUSE_FLAG)
	{
		Mouse_HID_Interface.Config.InterfaceNumber = ++interface_count;
		Mouse_HID_Interface.Config.ReportINEndpoint.Address = (ENDPOINT_DIR_IN | (interface_count + 1));
	}
#endif /* SIMPLE_DEVICE */
}

void USB_service(void)
{
	static uint8_t stored_USB_DeviceState;
	
	/* Disable interrupts for asynchronous USB */
	cli();
	
	HID_Device_USBTask(&Keyboard_HID_Interface);
	if (Media_HID_Interface.Config.InterfaceNumber)
		HID_Device_USBTask(&Media_HID_Interface);
#ifndef SIMPLE_DEVICE
	if (Nkro_HID_Interface.Config.InterfaceNumber)
		HID_Device_USBTask(&Nkro_HID_Interface);
	if (Mouse_HID_Interface.Config.InterfaceNumber)
		HID_Device_USBTask(&Mouse_HID_Interface);
#endif /* SIMPLE_DEVICE */
	
	/* Re-enable interrupts */
	sei();
	
	USB_USBTask();
	
	if (stored_USB_DeviceState != USB_DeviceState)
	{
		report_event(EVENT_CODE_USB_STATE_CHANGE, USB_DeviceState, MODE_REOCCUR);
		stored_USB_DeviceState = USB_DeviceState;
	}
}


void USB_wakeup(void)
{
	//led_toggle(0);
	if (USB_Device_RemoteWakeupEnabled && (USB_DeviceState == DEVICE_STATE_Suspended))
	{
		USB_Device_SendRemoteWakeup();
	}
}

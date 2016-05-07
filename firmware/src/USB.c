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


/** HID class report descriptor. This is a special descriptor constructed with values from the
 *  USBIF HID class specification to describe the reports and capabilities of the HID device. This
 *  descriptor is parsed by the host and its contents used to determine what data (and in what encoding)
 *  the device will send, and what it may be sent back from the host. Refer to the HID specification for
 *  more details on HID report descriptors.
 */
#ifndef SIMPLE_DEVICE
const USB_Descriptor_HIDReport_Datatype_t PROGMEM BootKeyboardReport[] =
{
	/* Use the HID class driver's standard Keyboard report.
	 *   Max simultaneous keys: 6
	 */
	HID_DESCRIPTOR_KEYBOARD(6)
};
#endif /* SIMPLE_DEVICE */

const USB_Descriptor_HIDReport_Datatype_t PROGMEM KeyboardReport[] =
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
		HID_RI_REPORT_COUNT(8, 0x01),
		HID_RI_REPORT_SIZE(8, 0x08),
		HID_RI_INPUT(8, HID_IOF_CONSTANT),
		
		HID_RI_USAGE_PAGE(8, 0x08),
		HID_RI_USAGE_MINIMUM(8, 0x01),
		HID_RI_USAGE_MAXIMUM(8, 0x05),
		HID_RI_REPORT_COUNT(8, 0x05),
		HID_RI_REPORT_SIZE(8, 0x01),
		HID_RI_OUTPUT(8, HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE | HID_IOF_NON_VOLATILE),
		HID_RI_REPORT_COUNT(8, 0x01),
		HID_RI_REPORT_SIZE(8, 0x03),
		HID_RI_OUTPUT(8, HID_IOF_CONSTANT),
		
		HID_RI_LOGICAL_MINIMUM(8, 0x00),
		HID_RI_LOGICAL_MAXIMUM(8, 0x01),
		HID_RI_USAGE_PAGE(8, 0x07),
		HID_RI_USAGE_MINIMUM(8, 0x00),
		HID_RI_USAGE_MAXIMUM(8, 0x7F),
		HID_RI_REPORT_COUNT(8, 0x80),
		HID_RI_REPORT_SIZE(8, 0x01),
		HID_RI_INPUT(8, HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE),
	HID_RI_END_COLLECTION(0)
};

/** HID class report descriptor. This is a special descriptor constructed with values from the
 *  USBIF HID class specification to describe the reports and capabilities of the HID device. This
 *  descriptor is parsed by the host and its contents used to determine what data (and in what encoding)
 *  the device will send, and what it may be sent back from the host. Refer to the HID specification for
 *  more details on HID report descriptors.
 *
 *  This descriptor describes the mouse HID interface's report structure.
 */
#ifdef ENABLE_MOUSE
const USB_Descriptor_HIDReport_Datatype_t PROGMEM MouseReport[] =
{
	/* Use the HID class driver's standard Mouse report.
	 *   Min X/Y Axis values: -1
	 *   Max X/Y Axis values:  1
	 *   Min physical X/Y Axis values (used to determine resolution): -1
	 *   Max physical X/Y Axis values (used to determine resolution):  1
	 *   Buttons: 3
	 *   Absolute screen coordinates: false
	 */
	HID_DESCRIPTOR_MOUSE(-127, 127, 0, 0, 3, false)
};
#endif /* ENABLE_MOUSE */

const USB_Descriptor_HIDReport_Datatype_t PROGMEM MediaReport[] =
{
	/* http://msdn.microsoft.com/en-us/library/windows/hardware/gg463446.aspx */
	HID_RI_USAGE_PAGE(8, 0x0C),				// Consumer
	HID_RI_USAGE(8, 0x01),					// Consumer Control
	HID_RI_COLLECTION(8, 0x01),				// Application
		HID_RI_USAGE_PAGE(8, 0x0C),			// Consumer
		HID_RI_LOGICAL_MINIMUM(16, 0x0001),	// Consumer Control
		HID_RI_LOGICAL_MAXIMUM(16, 0x029C),	// Slow
		HID_RI_USAGE_MINIMUM(16, 0x0001),	// Consumer Control
		HID_RI_USAGE_MAXIMUM(16, 0x029C),	// Slow
		HID_RI_REPORT_SIZE(8, 0x10),		// 16 bits
		HID_RI_REPORT_COUNT(8, 0x01),		// one report
		HID_RI_INPUT(8, HID_IOF_DATA | HID_IOF_ARRAY | HID_IOF_ABSOLUTE),
	HID_RI_END_COLLECTION(0)
};

/** Device descriptor structure. This descriptor, located in FLASH memory, describes the overall
 *  device characteristics, including the supported USB version, control endpoint size and the
 *  number of device configurations. The descriptor is read out by the USB host when the enumeration
 *  process begins.
 */
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

/** Configuration descriptor structure. This descriptor, located in FLASH memory, describes the usage
 *  of the device in one of its supported configurations, including information about any device interfaces
 *  and endpoints. The descriptor is read out by the USB host during the enumeration process when selecting
 *  a configuration so that the host may correctly communicate with the USB device.
 */
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

		.MaxPowerConsumption    = USB_CONFIG_POWER_MA(100)
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

#ifdef ENABLE_MOUSE
	.HID2_MouseInterface =
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

	.HID2_MouseHID =
	{
		.Header                 = {.Size = sizeof(USB_HID_Descriptor_HID_t), .Type = HID_DTYPE_HID},

		.HIDSpec                = VERSION_BCD(1,11,0),
		.CountryCode            = 0x00,
		.TotalReportDescriptors = 1,
		.HIDReportType          = HID_DTYPE_Report,
		.HIDReportLength        = sizeof(MouseReport)
	},

	.HID2_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},

		.EndpointAddress        = MOUSE_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = HID_EPSIZE_MOUSE,
		.PollingIntervalMS      = USB_MOUSE_UPDATE_RATE_MS
	},
#endif /* ENABLE_MOUSE */

	.HID3_MediaInterface =
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

	.HID3_MediaHID =
	{
		.Header                 = {.Size = sizeof(USB_HID_Descriptor_HID_t), .Type = HID_DTYPE_HID},

		.HIDSpec                = VERSION_BCD(1,11,0),
		.CountryCode            = 0x00,
		.TotalReportDescriptors = 1,
		.HIDReportType          = HID_DTYPE_Report,
		.HIDReportLength        = sizeof(MediaReport)
	},

	.HID3_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},

		.EndpointAddress        = MEDIA_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = HID_EPSIZE_MEDIA,
		.PollingIntervalMS      = USB_MEDIA_UPDATE_RATE_MS
	}
};

#ifndef SIMPLE_DEVICE
const USB_Descriptor_Configuration_t PROGMEM SemiConfigurationDescriptor =
{
	.Config =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Configuration_Header_t), .Type = DTYPE_Configuration},

		.TotalConfigurationSize = sizeof(USB_Descriptor_Configuration_t),
		.TotalInterfaces        = TOTAL_INTERFACES,

		.ConfigurationNumber    = 1,
		.ConfigurationStrIndex  = NO_DESCRIPTOR,

		.ConfigAttributes       = (USB_CONFIG_ATTR_RESERVED | USB_CONFIG_ATTR_REMOTEWAKEUP),

		.MaxPowerConsumption    = USB_CONFIG_POWER_MA(100)
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
		.HIDReportLength        = sizeof(BootKeyboardReport)
	},

	.HID1_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},

		.EndpointAddress        = KEYBOARD_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = 0x08,
		.PollingIntervalMS      = USB_KEYBOARD_UPDATE_RATE_MS
	},

#ifdef ENABLE_MOUSE
	.HID2_MouseInterface =
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

	.HID2_MouseHID =
	{
		.Header                 = {.Size = sizeof(USB_HID_Descriptor_HID_t), .Type = HID_DTYPE_HID},
		
		.HIDSpec                = VERSION_BCD(1,11,0),
		.CountryCode            = 0x00,
		.TotalReportDescriptors = 1,
		.HIDReportType          = HID_DTYPE_Report,
		.HIDReportLength        = sizeof(MouseReport)
	},

	.HID2_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},
		
		.EndpointAddress        = MOUSE_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = HID_EPSIZE_MOUSE,
		.PollingIntervalMS      = USB_MOUSE_UPDATE_RATE_MS
	},
	#endif /* ENABLE_MOUSE */

	.HID3_MediaInterface =
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

	.HID3_MediaHID =
	{
		.Header                 = {.Size = sizeof(USB_HID_Descriptor_HID_t), .Type = HID_DTYPE_HID},
		
		.HIDSpec                = VERSION_BCD(1,11,0),
		.CountryCode            = 0x00,
		.TotalReportDescriptors = 1,
		.HIDReportType          = HID_DTYPE_Report,
		.HIDReportLength        = sizeof(MediaReport)
	},

	.HID3_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},
		
		.EndpointAddress        = MEDIA_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = HID_EPSIZE_MEDIA,
		.PollingIntervalMS      = USB_MEDIA_UPDATE_RATE_MS
		}
};

const USB_Descriptor_Configuration_boot_t PROGMEM BootConfigurationDescriptor =
{
	.Config =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Configuration_Header_t), .Type = DTYPE_Configuration},

		.TotalConfigurationSize = sizeof(USB_Descriptor_Configuration_boot_t),
		.TotalInterfaces        = 1,

		.ConfigurationNumber    = 1,
		.ConfigurationStrIndex  = NO_DESCRIPTOR,

		.ConfigAttributes       = (USB_CONFIG_ATTR_RESERVED | USB_CONFIG_ATTR_REMOTEWAKEUP),

		.MaxPowerConsumption    = USB_CONFIG_POWER_MA(100)
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
		.HIDReportLength        = sizeof(BootKeyboardReport)
	},

	.HID1_ReportINEndpoint =
	{
		.Header                 = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},

		.EndpointAddress        = KEYBOARD_IN_EPADDR,
		.Attributes             = (EP_TYPE_INTERRUPT | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
		.EndpointSize           = 0x08,
		.PollingIntervalMS      = USB_KEYBOARD_UPDATE_RATE_MS
	}
};
#endif /* SIMPLE_DEVICE */

/** Language descriptor structure. This descriptor, located in FLASH memory, is returned when the host requests
 *  the string descriptor with index 0 (the first index). It is actually an array of 16-bit integers, which indicate
 *  via the language ID table available at USB.org what languages the device supports for its string descriptors.
 */
const USB_Descriptor_String_t PROGMEM LanguageString =
{
	.Header                 = {.Size = USB_STRING_LEN(1), .Type = DTYPE_String},

	.UnicodeString          = {LANGUAGE_ID_ENG}
};

/** Product descriptor string. This is a Unicode string containing the product's details in human readable form,
 *  and is read out upon request by the host when the appropriate string ID is requested, listed in the Device
 *  Descriptor.
 */
const USB_Descriptor_String_t PROGMEM ProductString =
{
	.Header                 = {.Size = USB_STRING_LEN(PRODUCT_STR_LEN), .Type = DTYPE_String},

	.UnicodeString          = PRODUCT_STRING
};

/** This function is called by the library when in device mode, and must be overridden (see library "USB Descriptors"
 *  documentation) by the application code so that the address and size of a requested descriptor can be given
 *  to the USB library. When the device receives a Get Descriptor request on the control endpoint, this function
 *  is called so that the descriptor details can be passed back and the appropriate descriptor sent back to the
 *  USB host.
 */
uint16_t CALLBACK_USB_GetDescriptor(const uint16_t wValue,
                                    const uint8_t wIndex,
                                    const void** const DescriptorAddress)
{
	const uint8_t  DescriptorType   = (wValue >> 8);
	const uint8_t  DescriptorNumber = (wValue & 0xFF);

	const void* Address = NULL;
	uint16_t    Size    = NO_DESCRIPTOR;

	switch (DescriptorType)
	{
		case DTYPE_Device:
			Address = &DeviceDescriptor;
			Size    = sizeof(USB_Descriptor_Device_t);
			break;
		case DTYPE_Configuration:
#ifndef SIMPLE_DEVICE
			if (g_boot_keyboard_only_latched == KB_TYPE_6KRO_ONLY)
			{
				Address = &BootConfigurationDescriptor;
				Size    = sizeof(USB_Descriptor_Configuration_boot_t);
			}
			else if (g_boot_keyboard_only_latched == KB_TYPE_6KRO_PLUS)
			{
				Address = &SemiConfigurationDescriptor;
				Size    = sizeof(USB_Descriptor_Configuration_t);
			}
			else
#endif /* SIMPLE_DEVICE */
			{
				Address = &ConfigurationDescriptor;
				Size    = sizeof(USB_Descriptor_Configuration_t);
			}
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
			switch (wIndex)
			{
				case KEYBOARD_INTERFACE:
#ifndef SIMPLE_DEVICE
					if (g_boot_keyboard_only_latched == KB_TYPE_6KRO_ONLY)
					{
						Address = &BootConfigurationDescriptor.HID1_KeyboardHID;
					}
					else if (g_boot_keyboard_only_latched == KB_TYPE_6KRO_PLUS)
					{
						Address = &SemiConfigurationDescriptor.HID1_KeyboardHID;
					}
					else
#endif /* SIMPLE_DEVICE */
					{
						Address = &ConfigurationDescriptor.HID1_KeyboardHID;
					}
					Size    = sizeof(USB_HID_Descriptor_HID_t);
					break;
#ifdef ENABLE_MOUSE
				case MOUSE_INTERFACE:
					Address = &ConfigurationDescriptor.HID2_MouseHID;
					Size    = sizeof(USB_HID_Descriptor_HID_t);
					break;
#endif /* ENABLE_MOUSE */
				case MEDIA_INTERFACE:
					Address = &ConfigurationDescriptor.HID3_MediaHID;
					Size    = sizeof(USB_HID_Descriptor_HID_t);
					break;
			}
			break;
		case HID_DTYPE_Report:
			switch (wIndex)
			{
				case KEYBOARD_INTERFACE:
#ifndef SIMPLE_DEVICE
					if (NKRO_IS_DISABLED)
					{
						Address = &BootKeyboardReport;
						Size    = sizeof(BootKeyboardReport);
					}
					else
#endif /* SIMPLE_DEVICE */
					{
						Address = &KeyboardReport;
						Size    = sizeof(KeyboardReport);
					}
					break;
#ifdef ENABLE_MOUSE
				case MOUSE_INTERFACE:
					Address = &MouseReport;
					Size    = sizeof(MouseReport);
					break;
#endif /* ENABLE_MOUSE */
				case MEDIA_INTERFACE:
					Address = &MediaReport;
					Size    = sizeof(MediaReport);
					break;
			}
			break;
	}

	*DescriptorAddress = Address;
	return Size;
}

/** Buffer to hold the previously generated Keyboard HID report, for comparison purposes inside the HID class driver. */
static uint8_t PrevKeyboardHIDReportBuffer[sizeof(USB_KeyboardModReport_Data_t)];
// The above only works because USB_KeyboardModReport_Data_t is assumed to be bigger than USB_KeyboardReport_Data_t

/** Buffer to hold the previously generated Mouse HID report, for comparison purposes inside the HID class driver. */
#ifdef ENABLE_MOUSE
static uint8_t PrevMouseHIDReportBuffer[sizeof(USB_MouseReport_Data_t)];
#endif /* ENABLE_MOUSE */

static uint8_t PrevMediaHIDReportBuffer[sizeof(USB_MediaReport_Data_t)];

/** LUFA HID Class driver interface configuration and state information. This structure is
 *  passed to all HID Class driver functions, so that multiple instances of the same class
 *  within a device can be differentiated from one another.
 */
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
			.PrevReportINBuffer           = PrevKeyboardHIDReportBuffer,
			.PrevReportINBufferSize       = sizeof(PrevKeyboardHIDReportBuffer),
		},
	};

/** LUFA HID Class driver interface configuration and state information. This structure is
 *  passed to all HID Class driver functions, so that multiple instances of the same class
 *  within a device can be differentiated from one another. This is for the mouse HID
 *  interface within the device.
 */
#ifdef ENABLE_MOUSE
USB_ClassInfo_HID_Device_t Mouse_HID_Interface =
	{
		.Config =
			{
				.InterfaceNumber              = MOUSE_INTERFACE,
				.ReportINEndpoint             =
					{
						.Address              = MOUSE_IN_EPADDR,
						.Size                 = HID_EPSIZE_MOUSE,
						.Banks                = 1,
					},
				.PrevReportINBuffer           = PrevMouseHIDReportBuffer,
				.PrevReportINBufferSize       = sizeof(PrevMouseHIDReportBuffer),
			},
	};
#endif /* ENABLE_MOUSE */

USB_ClassInfo_HID_Device_t Media_HID_Interface =
{
	.Config =
	{
		.InterfaceNumber              = MEDIA_INTERFACE,
		.ReportINEndpoint             =
		{
			.Address              = MEDIA_IN_EPADDR,
			.Size                 = HID_EPSIZE_MEDIA,
			.Banks                = 1,
		},
		.PrevReportINBuffer           = PrevMediaHIDReportBuffer,
		.PrevReportINBufferSize       = sizeof(PrevMediaHIDReportBuffer),
	},
};

/** Event handler for the library USB Connection event. */
void EVENT_USB_Device_Connect(void)
{
	//report_event(EVENT_CODE_USB_CONNECT, 0, MODE_REOCCUR);
	set_led_status(LED_STATUS_CONNECT);
}

/** Event handler for the library USB Disconnection event. */
void EVENT_USB_Device_Disconnect(void)
{
	//report_event(EVENT_CODE_USB_DISCONNECT, 0, MODE_REOCCUR);
	//set_led_status(LED_STATUS_DISCONNECT);
}

/** Event handler for the library USB Configuration Changed event. */
void EVENT_USB_Device_ConfigurationChanged(void)
{
	bool ConfigSuccess = true;

	ConfigSuccess &= HID_Device_ConfigureEndpoints(&Keyboard_HID_Interface);
	if (MEDIA_IS_ENABLED)
	{
#ifdef ENABLE_MOUSE
		ConfigSuccess &= HID_Device_ConfigureEndpoints(&Mouse_HID_Interface);
#endif /* ENABLE_MOUSE */
		ConfigSuccess &= HID_Device_ConfigureEndpoints(&Media_HID_Interface);
	}
	
	if (ConfigSuccess)
		set_led_status(LED_STATUS_NORM);
	else
		set_led_status(LED_STATUS_ERROR);
	
	//report_event(EVENT_CODE_USB_CONFIG_CHANGE, 0, MODE_REOCCUR);
	USB_Device_EnableSOFEvents();
}

/** Event handler for the library USB Control Request reception event. */
void EVENT_USB_Device_ControlRequest(void)
{
	HID_Device_ProcessControlRequest(&Keyboard_HID_Interface);
	if (MEDIA_IS_ENABLED)
	{
#ifdef ENABLE_MOUSE
		HID_Device_ProcessControlRequest(&Mouse_HID_Interface);
#endif /* ENABLE_MOUSE */
		HID_Device_ProcessControlRequest(&Media_HID_Interface);
	}
}

/** Event handler for the USB device Start Of Frame event. */
void EVENT_USB_Device_StartOfFrame(void)
{
	HID_Device_MillisecondElapsed(&Keyboard_HID_Interface);
	if (MEDIA_IS_ENABLED)
	{
#ifdef ENABLE_MOUSE
		HID_Device_MillisecondElapsed(&Mouse_HID_Interface);
#endif /* ENABLE_MOUSE */
		HID_Device_MillisecondElapsed(&Media_HID_Interface);
	}
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

/** HID class driver callback function for the creation of HID reports to the host.
 *
 *  \param[in]     HIDInterfaceInfo  Pointer to the HID class interface configuration structure being referenced
 *  \param[in,out] ReportID    Report ID requested by the host if non-zero, otherwise callback should set to the generated report ID
 *  \param[in]     ReportType  Type of the report to create, either HID_REPORT_ITEM_In or HID_REPORT_ITEM_Feature
 *  \param[out]    ReportData  Pointer to a buffer where the created report should be stored
 *  \param[out]    ReportSize  Number of bytes written in the report (or zero if no report is to be sent)
 *
 *  \return Boolean true to force the sending of the report, false to let the library determine if it needs to be sent
 */
bool CALLBACK_HID_Device_CreateHIDReport(USB_ClassInfo_HID_Device_t* const HIDInterfaceInfo,
                                         uint8_t* const ReportID,
                                         const uint8_t ReportType,
                                         void* ReportData,
                                         uint16_t* const ReportSize)
{
	USB_KeyboardModReport_Data_t* KeyboardReport = (USB_KeyboardModReport_Data_t*)ReportData;
#ifdef ENABLE_MOUSE
	USB_MouseReport_Data_t* MouseReport = (USB_MouseReport_Data_t*)ReportData;
#endif /* ENABLE_MOUSE */
	USB_MediaReport_Data_t* MediaReport = (USB_MediaReport_Data_t*)ReportData;
	
	if (HIDInterfaceInfo == &Keyboard_HID_Interface)
	{
		g_keyboard_service = 0;
		if (NKRO_IS_ENABLED && HIDInterfaceInfo->State.UsingReportProtocol)
		{
			get_nkro_report(KeyboardReport->KeyCode);
			get_modifier_report(&KeyboardReport->Modifier);
		}
		else
		{
			get_keyboard_report(KeyboardReport->KeyCode);
			get_modifier_report(&KeyboardReport->Modifier);
		}
		if (NKRO_IS_DISABLED)
			*ReportSize = sizeof(USB_KeyboardReport_Data_t);
		else
			*ReportSize = sizeof(USB_KeyboardModReport_Data_t);
	}
#ifdef ENABLE_MOUSE
	else if (HIDInterfaceInfo == &Mouse_HID_Interface)
	{
		g_mouse_service = 0;
		MouseReport->Button = g_mousebutton_state;
		MouseReport->X = g_mouse_report_X;
		MouseReport->Y = g_mouse_report_Y;
		*ReportSize = sizeof(USB_MouseReport_Data_t);
		if (g_mouse_active)
			return true;
	}
#endif /* ENABLE_MOUSE */
	else
	{
		MediaReport->Button = g_media_key;
		*ReportSize = sizeof(USB_MediaReport_Data_t);
	}
	
	return false;
}

/** HID class driver callback function for the processing of HID reports from the host.
 *
 *  \param[in] HIDInterfaceInfo  Pointer to the HID class interface configuration structure being referenced
 *  \param[in] ReportID    Report ID of the received report from the host
 *  \param[in] ReportType  The type of report that the host has sent, either HID_REPORT_ITEM_Out or HID_REPORT_ITEM_Feature
 *  \param[in] ReportData  Pointer to a buffer where the received report has been stored
 *  \param[in] ReportSize  Size in bytes of the received HID report
 */
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
	if (NKRO_IS_DISABLED)
	{
		Keyboard_HID_Interface.Config.PrevReportINBufferSize = sizeof(USB_KeyboardReport_Data_t);
		Keyboard_HID_Interface.Config.ReportINEndpoint.Size = 8;
	}
}

void USB_cycle(void)
{
	static uint8_t stored_USB_DeviceState;
	
	HID_Device_USBTask(&Keyboard_HID_Interface);
	if (MEDIA_IS_ENABLED)
	{
#ifdef ENABLE_MOUSE
		HID_Device_USBTask(&Mouse_HID_Interface);
#endif /* ENABLE_MOUSE */
		HID_Device_USBTask(&Media_HID_Interface);
	}
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

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Easy AVR USB Keyboard Firmware Keymapper
# Copyright (C) 2018 David Howland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Functions for decoding and manipulating USB HID Configuration Descriptors."""

from struct import pack, unpack, calcsize


# Reference USB.h in the firmware
USB_Descriptor_Header_t = b'BB'
USB_Descriptor_Configuration_Header_t = USB_Descriptor_Header_t + b'HBBBBB'
USB_Descriptor_Interface_t = USB_Descriptor_Header_t + b'BBBBBBB'
USB_HID_Descriptor_HID_t = USB_Descriptor_Header_t + b'HBBBH'
USB_Descriptor_Endpoint_t = USB_Descriptor_Header_t + b'BBHB'
USB_Descriptor_Configuration_t = (USB_Descriptor_Configuration_Header_t + (
    (USB_Descriptor_Interface_t + USB_HID_Descriptor_HID_t + USB_Descriptor_Endpoint_t) * 4))

confdesc_format = b'<' + USB_Descriptor_Configuration_t
confdesc_size = calcsize(confdesc_format)

device_format = b'<' + (USB_Descriptor_Interface_t + USB_HID_Descriptor_HID_t +
                        USB_Descriptor_Endpoint_t)
device_size = calcsize(device_format)


class Header:
    """A data storage class for manipulating a USB_Descriptor_Header_t struct."""

    def __init__(self, args):
        self.Size = args[0]
        self.Type = args[1]

    def tolist(self):
        return [self.Size, self.Type]


class Config:
    """A data storage class for manipulating a USB_Descriptor_Configuration_Header_t struct."""

    def __init__(self, args):
        self.Header = Header(args[0:2])
        self.TotalConfigurationSize = args[2]
        self.TotalInterfaces = args[3]
        self.ConfigurationNumber = args[4]
        self.ConfigurationStrIndex = args[5]
        self.ConfigAttributes = args[6]
        self.MaxPowerConsumption = args[7]

    def tolist(self):
        return (self.Header.tolist() + [self.TotalConfigurationSize, self.TotalInterfaces,
                self.ConfigurationNumber, self.ConfigurationStrIndex, self.ConfigAttributes,
                self.MaxPowerConsumption])


class Interface:
    """A data storage class for manipulating a USB_Descriptor_Interface_t struct."""

    def __init__(self, args):
        self.Header = Header(args[0:2])
        self.InterfaceNumber = args[2]
        self.AlternateSetting = args[3]
        self.TotalEndpoints = args[4]
        self.Class = args[5]
        self.SubClass = args[6]
        self.Protocol = args[7]
        self.InterfaceStrIndex = args[8]

    def tolist(self):
        return (self.Header.tolist() + [self.InterfaceNumber, self.AlternateSetting,
                self.TotalEndpoints, self.Class, self.SubClass, self.Protocol,
                self.InterfaceStrIndex])


class HID:
    """A data storage class for manipulating a USB_HID_Descriptor_HID_t struct."""

    def __init__(self, args):
        self.Header = Header(args[0:2])
        self.HIDSpec = args[2]
        self.CountryCode = args[3]
        self.TotalReportDescriptors = args[4]
        self.HIDReportType = args[5]
        self.HIDReportLength = args[6]

    def tolist(self):
        return (self.Header.tolist() + [self.HIDSpec, self.CountryCode,
                self.TotalReportDescriptors, self.HIDReportType, self.HIDReportLength])


class Endpoint:
    """A data storage class for manipulating a USB_Descriptor_Endpoint_t struct."""

    def __init__(self, args):
        self.Header = Header(args[0:2])
        self.EndpointAddress = args[2]
        self.Attributes = args[3]
        self.EndpointSize = args[4]
        self.PollingIntervalMS = args[5]

    def tolist(self):
        return (self.Header.tolist() + [self.EndpointAddress, self.Attributes, self.EndpointSize,
                self.PollingIntervalMS])


class Device:
    """A data storage class for manipulating the 3 structs that define HID devices."""

    def __init__(self, args):
        self.Interface = Interface(args[0:9])
        self.HID = HID(args[9:16])
        self.Endpoint = Endpoint(args[16:22])

    def tolist(self):
        return (self.Interface.tolist() + self.HID.tolist() + self.Endpoint.tolist())


class ConfigurationDescriptor:
    """A data storage class for manipulating a USB_Descriptor_Configuration_t struct."""

    def __init__(self, args):
        self.Config = Config(args[0:8])
        self.HID1_Device = Device(args[8:30])
        self.HID2_Device = Device(args[30:52])
        self.HID3_Device = Device(args[52:74])
        self.HID4_Device = Device(args[74:96])

    def tolist(self):
        return (self.Config.tolist() + self.HID1_Device.tolist() + self.HID2_Device.tolist() +
                self.HID3_Device.tolist() + self.HID4_Device.tolist())


def update_descriptor(byte_array, opts):
    """Takes a bytes-like object `byte_array` and remove any HID endpoints that are False in the
    corresponding Opts namedtuple `opts`.  The `byte_array` array must be of length
    USB_Descriptor_Configuration_t.  Returns a bytes object.
    """
    cd = ConfigurationDescriptor(unpack(confdesc_format, byte_array))
    blank_device = Device([0] * 22)
    # HID1 (boot keyboard) never changes
    if opts.media is False:
        cd.Config.TotalInterfaces -= 1
        cd.Config.TotalConfigurationSize -= device_size
        cd.HID2_Device = blank_device
        cd.HID3_Device.Interface.InterfaceNumber -= 1
        cd.HID3_Device.Endpoint.EndpointAddress -= 1
        cd.HID4_Device.Interface.InterfaceNumber -= 1
        cd.HID4_Device.Endpoint.EndpointAddress -= 1
    if opts.nkro is False:
        cd.Config.TotalInterfaces -= 1
        cd.Config.TotalConfigurationSize -= device_size
        cd.HID3_Device = blank_device
        cd.HID4_Device.Interface.InterfaceNumber -= 1
        cd.HID4_Device.Endpoint.EndpointAddress -= 1
    if opts.mouse is False:
        cd.Config.TotalInterfaces -= 1
        cd.Config.TotalConfigurationSize -= device_size
        cd.HID4_Device = blank_device
    # move any "holes" to the end
    if cd.HID3_Device is blank_device:
        cd.HID3_Device = cd.HID4_Device
        cd.HID4_Device = blank_device
    if cd.HID2_Device is blank_device:
        cd.HID2_Device = cd.HID3_Device
        cd.HID3_Device = cd.HID4_Device
        cd.HID4_Device = blank_device
    return pack(confdesc_format, *cd.tolist())

# -*- coding : utf-8 -*-

# PyAX-12

# The MIT License
#
# Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This module contain the "StatusPacket" class which implements
"status packet" (the response packets from the Dynamixel units to the main
controller after receiving an instruction packet).
"""

__all__ = ['StatusPacket']

import pyax12.packet as pk
from pyax12 import utils

# EXCEPTION CLASSES ###########################################################

class StatusPacketError(Exception):
    """Base class for exceptions in the status_packet module."""
    pass

class InstructionError(StatusPacketError):
    """Exception raised if an undefined instruction is sent or an action
    instruction is sent without a Reg_Write instruction."""
    pass

class OverloadError(StatusPacketError):
    """Exception raised if the specified maximum torque can't control the
    applied load."""
    pass

class ChecksumError(StatusPacketError):
    """Exception raised if the checksum of the instruction packet is
    incorrect."""
    pass

class RangeError(StatusPacketError):
    """Exception raised if the instruction sent is out of the defined range."""
    pass

class OverheatingError(StatusPacketError):
    """Exception raised if the internal temperature of the Dynamixel unit is
    above the operating temperature range as defined in the control table."""
    pass

class AngleLimitError(StatusPacketError):
    """Exception raised if the goal position is set outside of the range
    between "CW Angle Limit" and "CCW Angle Limit"."""
    pass

class InputVoltageError(StatusPacketError):
    """Exception raised if the voltage is out of the operating voltage range as
    defined in the control table."""
    pass

# STATUS PACKET CLASS #########################################################

class StatusPacket(pk.Packet):
    """The Status Packet is the response packet from the Dynamixel units to the
    main controller after receiving an instruction packet.

    The structure of the status packet is as the following:

    +----+----+--+------+-----+----------+---+-----------+---------+
    |0XFF|0XFF|ID|LENGTH|ERROR|PARAMETER1|...|PARAMETER N|CHECK SUM|
    +----+----+--+------+-----+----------+---+-----------+---------+
    """

    def __init__(self, bytes_packet):
        """Create a status packet.

        StatusPacket is not intended to be instancied by users (except maybe
        for testing and debugging prupose). Under normal conditions of use,
        StatusPacket's instances are automatically created by the "Connection"
        class.

        Keyword arguments:
        bytes_packet -- a "bytes" instance containing the full status packet
                        returned by Dynamixel units.
        """

        # Check arguments type to make exception messages more explicit
        if not isinstance(bytes_packet, bytes):
            msg = 'A "bytes" type is required (got {}).'
            raise TypeError(msg.format(type(bytes_packet)))

        if len(bytes_packet) >= 6:

            self.dynamixel_id = bytes_packet[2]
            self.error = bytes_packet[4]
            self.parameters = tuple([byte for byte in bytes_packet[5:-1]])

            # Write error bits
            self.instruction_error = bool(self.error & (1 << 6))
            self.overload_error = bool(self.error & (1 << 5))
            self.checksum_error = bool(self.error & (1 << 4))
            self.range_error = bool(self.error & (1 << 3))
            self.overheating_error = bool(self.error & (1 << 2))
            self.angle_limit_error = bool(self.error & (1 << 1))
            self.input_voltage_error = bool(self.error & (1 << 0))

            # Check the header bytes
            header_tuple = tuple(bytes_packet[0:2])
            if header_tuple != (0xff, 0xff):
                msg = 'Wrong header: {} (should be in "ff ff")).'
                header_str = utils.int_seq_to_hex_str(header_tuple)
                raise ValueError(msg.format(header_str))

            # Verify the checksum (it should be the first byte to check to
            # avoid wrong error message in case of transmission error)
            byte_tuple = tuple(bytes_packet[2:-1])
            computed_checksum = pk.dynamixel_checksum(byte_tuple)
            if computed_checksum != bytes_packet[-1]:
                msg = 'Wrong checksum: {}.'
                packet_str = utils.int_seq_to_hex_str(tuple(bytes_packet))
                raise ValueError(msg.format(packet_str))

            # Check the ID byte
            if not (0x00 <= self.dynamixel_id <= 0xfe):
                msg = "Wrong dynamixel_id:"
                msg += " {:#x} (should be in range(0x00, 0xfe))."
                raise ValueError(msg.format(self.dynamixel_id))

            # Check length (length = num_params + 2 = full_packet_length - 4)
            measured_length = len(bytes_packet) - 4
            if measured_length != bytes_packet[3]:
                msg = 'Wrong length: {}.'
                packet_str = utils.int_seq_to_hex_str(tuple(bytes_packet))
                raise ValueError(msg.format(packet_str))

            # Check error bit flags
            if self.instruction_error:
                raise InstructionError()

            if self.overload_error:
                raise OverloadError()

            if self.checksum_error:
                raise ChecksumError()

            if self.range_error:
                raise RangeError()

            if self.overheating_error:
                raise OverheatingError()

            if self.angle_limit_error:
                raise AngleLimitError()

            if self.input_voltage_error:
                raise InputVoltageError()

            # Set self.data
            self.data = (self.error, ) + self.parameters
        else:
            msg = "Incomplete packet: ({})."
            packet_str = utils.int_seq_to_hex_str(bytes_packet)
            raise ValueError(msg.format(packet_str))


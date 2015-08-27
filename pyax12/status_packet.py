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
This module contain the `StatusPacket` class which implements
"status packets" (the response packets from the Dynamixel units to the main
controller after receiving an instruction packet).
"""

__all__ = ['StatusPacket']

import pyax12.packet as pk

# EXCEPTION CLASSES ###########################################################

class StatusPacketError(Exception):
    """Base class for exceptions in the `status_packet` module."""
    pass

class InstructionError(StatusPacketError):
    """Exception raised if an undefined instruction is sent or an action
    instruction is sent without a Reg_Write instruction."""
    pass

class OverloadError(StatusPacketError):
    """Exception raised if the specified maximum torque can't control the
    applied load."""
    pass

class InstructionChecksumError(StatusPacketError):
    """Exception raised if the checksum of the instruction packet is
    incorrect."""
    pass

class StatusChecksumError(StatusPacketError):
    """Exception raised if the checksum of the status packet is
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
    """The "status packet" is the response packet from the Dynamixel units to
    the main controller after receiving an "instruction packet".

    The structure of the status packet is as the following:

    +----+----+--+------+-----+----------+---+-----------+---------+
    |0XFF|0XFF|ID|LENGTH|ERROR|PARAMETER1|...|PARAMETER N|CHECK SUM|
    +----+----+--+------+-----+----------+---+-----------+---------+

    StatusPacket is not intended to be instancied by users (except maybe
    for testing and debugging prupose). Under normal conditions of use,
    `StatusPacket`'s instances are automatically created by the
    `Connection` class.

    :param bytes packet: a sequence of bytes containing the full status
        packet returned by Dynamixel units. It must be compatible with the
        "bytes" type.
    """

    def __init__(self, packet):

        # Check the argument and convert it to "bytes" if necessary.
        # Assert "packet" items are in range (0, 0xff).
        # "TypeError" and "ValueError" are sent by the "bytes" constructor if
        # necessary.
        # The statement "tuple(packet)" implicitely rejects integers (and all
        # non-iterable objects) to compensate the fact that the bytes
        # constructor doesn't reject them: bytes(6) is valid and returns
        # b'\x00\x00\x00'.
        self._bytes = bytes(tuple(packet))

        # Assert the argument is a sequence with at least 6 items.
        if len(self._bytes) < 6:
            raise ValueError("Incomplete packet.")

        # Check the header bytes.
        # Should be tested before the length and checksum because if the header
        # is wrong then the length and the checksum are wrong too (thus testing
        # the header first gives a more relevant information when its value is
        # wrong).
        if bytes(self.header) != b'\xff\xff':
            raise ValueError("Wrong header (should be b'\xff\xff').")

        # Check length (length = num_params + 2 = full_packet_length - 4).
        # Should be tested before the checksum because if the length is wrong
        # then the checksum is wrong too (thus testing the length first gives a
        # more relevant information when its value is wrong).
        if self.length != len(self._bytes) - 4:
            raise ValueError('Wrong length byte.')

        # Verify the checksum.
        computed_checksum = pk.compute_checksum(self._bytes[2:-1])
        if computed_checksum != self.checksum:
            raise StatusChecksumError('Wrong checksum.')

        # Check error bit flags.
        if self.instruction_error:
            raise InstructionError()

        if self.overload_error:
            raise OverloadError()

        if self.checksum_error:
            raise InstructionChecksumError()

        if self.range_error:
            raise RangeError()

        if self.overheating_error:
            raise OverheatingError()

        if self.angle_limit_error:
            raise AngleLimitError()

        if self.input_voltage_error:
            raise InputVoltageError()

        # Check the ID byte
        if not(0x00 <= self.dynamixel_id <= 0xfd):
            msg = "Wrong dynamixel_id, a value in range (0, 0xFD) is required."
            raise ValueError(msg)


    # READ ONLY PROPERTIES

    @property
    def error(self):
        """The byte representing errors sent from the Dynamixel unit.

        This member is a read-only property.
        """
        return self._bytes[4]

    @property
    def instruction_error(self):
        """A boolean which is set to True if an undefined instruction is sent
        or an action instruction is sent without a Reg_Write instruction.

        This member is a read-only property.
        """
        return bool(self.error & (1 << 6))

    @property
    def overload_error(self):
        """A boolean which is set to True if the specified maximum torque can't
        control the applied load.

        This member is a read-only property.
        """
        return bool(self.error & (1 << 5))

    @property
    def checksum_error(self):
        """A boolean which is set to True if the checksum of the instruction
        packet is incorrect.

        This member is a read-only property.
        """
        return bool(self.error & (1 << 4))

    @property
    def range_error(self):
        """A boolean which is set to True if the instruction sent is out of the
        defined range.

        This member is a read-only property.
        """
        return bool(self.error & (1 << 3))

    @property
    def overheating_error(self):
        """A boolean which is set to True if the internal temperature of the
        Dynamixel unit is above the operating temperature range as defined in
        the control table.

        This member is a read-only property.
        """
        return bool(self.error & (1 << 2))

    @property
    def angle_limit_error(self):
        """A boolean which is set to True if the goal position is set outside
        of the range between "CW Angle Limit" and "CCW Angle Limit".

        This member is a read-only property.
        """
        return bool(self.error & (1 << 1))

    @property
    def input_voltage_error(self):
        """A boolean which is set to True if the voltage is out of the
        operating voltage range as defined in the control table.

        This member is a read-only property.
        """
        return bool(self.error & (1 << 0))


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
This module contain the general "Packet" class which implements the either
"instruction packet" (the packets sent by the controller to the Dynamixel
actuators to send commands) or "status packet" (the response packets from
the Dynamixel units to the main controller after receiving an instruction
packet).
"""

__all__ = ['Packet',
           'dynamixel_checksum']

from pyax12 import utils

# GENERAL CONSTANTS

BROADCAST_ID = 0xfe
PACKET_HEADER = (0xff, 0xff)

# CONTROL TABLE (ADDRESSES)
# (see the official Dynamixel AX-12 User's manual p.12)

MODEL_NUMBER = 0x00
VERSION_OF_FIRMWARE = 0x02
ID = 0x03
BAUD_RATE = 0x04
RETURN_DELAY_TIME = 0x05
CW_ANGLE_LIMIT = 0x06
CCW_ANGLE_LIMIT = 0x08
HIGHEST_LIMIT_TEMPERATURE = 0x0b
LOWEST_LIMIT_VOLTAGE = 0x0c
HIGHEST_LIMIT_VOLTAGE = 0x0d
MAX_TORQUE = 0x0e
STATUS_RETURN_LEVEL = 0x10
ALARM_LED = 0x11
ALARM_SHUTDOWN = 0x12
DOWN_CALIBRATION = 0x14
UP_CALIBRATION = 0x16
TORQUE_ENABLE = 0x18
LED = 0x19
CW_COMPLIENCE_MARGIN = 0x1a
CCW_COMPLIENCE_MARGIN = 0x1b
CW_COMPLIENCE_SLOPE = 0x1c
CCW_COMPLIENCE_SLOPE = 0x1d
GOAL_POSITION = 0x1e
MOVING_SPEED = 0x20
TORQUE_LIMIT = 0x22
PRESENT_POSITION = 0x24
PRESENT_SPEED = 0x26
PRESENT_LOAD = 0x28
PRESENT_VOLTAGE = 0x2a
PRESENT_TEMPERATURE = 0x2b
REGISTRED_INSTRUCTION = 0x2c
MOVING = 0x2e
LOCK = 0x2f
PUNCH = 0x30

# CHECKSUM FUNCTION

def dynamixel_checksum(byte_seq):
    """Compute and return the checksum of the "byte_seq" packet.

    The checksum is the value of the last byte of each packet. It is used
    to prevent transmission errors of packets. Checksums are computed as
    follow:

    Checksum = ~(dynamixel_id + length + data1 + ... + dataN)
    where ~ represent the NOT logic operation.

    If the computed value is larger than 255, the lower byte is defined as
    the checksum value.

    Keyword arguments:
    byte_seq -- a byte sequence containing the packet's bytes involved in the
                computation of the checksum (i.e. from the third to the
                penultimate byte of the "full packet" considered).
    """

    # Check the argument and convert it to "bytes" if necessary.
    # Assert "byte_seq" items are in range (0, 0xff).
    # "TypeError" and "ValueError" are sent by the "bytes" constructor if
    # necessary.
    # The statement "tuple(byte_seq)" implicitely rejects integers (and all
    # non-iterable objects) to compensate the fact that the bytes constructor
    # doesn't reject them: bytes(3) is valid and returns b'\x00\x00\x00'
    byte_seq = bytes(tuple(byte_seq))

    # Check the argument's length
    if len(byte_seq) < 3:
        raise ValueError("At least three bytes are required.")

    # Check the ID byte
    if not (0x00 <= byte_seq[0] <= 0xfe):
        msg = "Wrong dynamixel_id, a byte in range(0x00, 0xfe) is required."
        raise ValueError(msg)

    # Check the "length" byte
    if byte_seq[1] != (len(byte_seq) - 1):
        raise ValueError('Wrong length, at least 3 bytes are required.')

    checksum = ~sum(byte_seq) & 0xff

    return checksum


# THE IMPLEMENTATION OF "PACKETS"

class Packet(object):
    """The general raw "Packet" class.

    It implements the either "instruction packet" (the packets sent by the
    controller to the Dynamixel actuators to send commands) or "status packet"
    (the response packets from the Dynamixel units to the main controller after
    receiving an instruction packet).

    The structure of a general Packet is as the following:

    +----+----+--+------+-------+---------+
    |0XFF|0XFF|ID|LENGTH|DATA...|CHECK SUM|
    +----+----+--+------+-------+---------+

    Instance variable:
    dynamixel_id -- the unique ID of a Dynamixel unit (from 0x00 to 0xFD),
                    0xFE is a broadcasting ID;
    data -- a tuple containing the packet's data: the instruction to perform or
            the status of the Dynamixel actuator.
    """

    def __init__(self, _id, _data):
        """Create a raw packet.

        This constructor has been made for debugging purpose and is not intended
        to be used widely to create packets.
        Instead, it is recommanded to use InstructionPacket or StatusPacket
        classes to build Packet instances.

        Keyword arguments:
        _id -- the unique ID of a Dynamixel unit (from 0x00 to 0xFD), 0xFE is a
               broadcasting ID;
        _data -- a tuple containing the packet's data: the instruction to
                 perform or the status of the Dynamixel actuator.
                 This "data" argument contains the fifth to the penultimate
                 byte of the built packet.
        """

        # Check arguments type to make exception messages more explicit
        if not isinstance(_id, int):
            msg = "Wrong dynamixel_id type: {} (an integer is required)."
            raise TypeError(msg.format(type(_id)))

        for byte in _data:
            if not isinstance(byte, int):
                msg = "Wrong data type: {} (an integer is required)."
                raise TypeError(msg.format(type(byte)))

        # Check the ID byte
        if 0x00 <= _id <= 0xfe:
            self.dynamixel_id = _id
        else:
            msg = "Wrong dynamixel_id: {:#x} (should be in range (0x00, 0xfe))."
            raise ValueError(msg.format(_id))

        # Check the data bytes
        for byte in _data:
            if not (0x00 <= byte <= 0xff):
                msg = "Wrong data value: ({})"
                msg += " (an integer in range (0x00, 0xff) is required)."
                data_str = utils.pretty_hex_str(_data)
                raise ValueError(msg.format(data_str))

        self.data = _data


    def length(self):
        """Return the length of the packet.

        This is not the actual length of the packet but the value of the fourth
        byte (called "LENGTH") of each packet computed as follow:
        length = data length + 1

        In other words, for a given packet, this "length" is the number of
        bytes after its fourth byte.
        """

        return len(self.data) + 1


    def checksum(self):
        """Compute and return the packet checksum.

        The checksum is the value of the last byte of each packet. It is used
        to prevent transmission errors of packets. Checksums are computed as
        follow:

        Checksum = ~(dynamixel_id + length + data1 + ... + dataN)
        where ~ represent the NOT logic operation.

        If the computed value is larger than 255, the lower byte is defined as
        the checksum value.
        """

        byte_seq = (self.dynamixel_id, self.length()) + self.data
        checksum = dynamixel_checksum(byte_seq)

        return checksum


    def to_integer_tuple(self):
        """Return the packet as a tuple of integers.

        Returns something like: (255, 255, 254, 4, 3, 3, 1, 246).
        """

        integer_tuple = PACKET_HEADER
        integer_tuple += (self.dynamixel_id, self.length())
        integer_tuple += self.data
        integer_tuple += (self.checksum(),)

        return integer_tuple


    def to_printable_string(self):
        """Return the packet as a string of hexadecimal values.

        Returns something like: ff ff fe 04 03 03 01 f6.
        """

        integer_tuple = self.to_integer_tuple()
        packet_str = ' '.join(['%02x' % integer for integer in integer_tuple])

        return packet_str


    def to_byte_array(self):
        """Return the packet as a bytearray (a mutable sequence of bytes).

        Returns something like: bytearray(b'\xff\xff\xfe\x04\x03\x03\x01\xf6').
        """

        return bytearray(self.to_integer_tuple())


    def to_bytes(self):
        """Return the packet as a bytes string (an immutable sequence of
        bytes).

        Returns something like: b'\xff\xff\xfe\x04\x03\x03\x01\xf6'.
        """

        return bytes(self.to_integer_tuple())


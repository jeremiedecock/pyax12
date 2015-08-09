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


# GENERAL CONSTANTS

BROADCAST_ID = 0xfe
PACKET_HEADER = bytes((0xff, 0xff))

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

    def __init__(self, id_byte, data_bytes):
        """Create a raw packet.

        This constructor has been made for debugging purpose and is not intended
        to be used widely to create packets.
        Instead, it is recommanded to use InstructionPacket or StatusPacket
        classes to build Packet instances.

        Keyword arguments:
        id_byte -- the unique ID of a Dynamixel unit (from 0x00 to 0xFD), 0xFE
                   is a broadcasting ID;
        data_bytes -- a sequence of byte containing the packet's data: the
                      instruction to perform or the status of the Dynamixel
                      actuator.
                      This "data" argument contains the fifth to the
                      penultimate byte of the full built packet.
        """

        self._dynamixel_id = None  # TODO ?
        self._data = None          # TODO ?

        self.dynamixel_id = id_byte
        self.data = data_bytes


    def get_dynamixel_id(self):
        """The unique ID of a Dynamixel unit affected by this packet.

        This byte either has a value between 0x00 and 0xFD to affect the
        corresponding Dynamixel unit or it has the value 0xFE to affect all
        connected units (0xFE is the "broadcasting" ID).
        """

        return self._dynamixel_id


    def set_dynamixel_id(self, id_byte):
        """Set the dynamixel_id property.

        An integer in range (0, 0xFE) is required.
        """

        # Check the ID byte
        if not isinstance(id_byte, int):
            raise TypeError("Wrong dynamixel_id type, an integer is required.")

        if 0x00 <= id_byte <= 0xfe:
            self._dynamixel_id = id_byte
        else:
            msg = "Wrong dynamixel_id, a value in range (0, 0xfe) is required."
            raise ValueError(msg)


    dynamixel_id = property(get_dynamixel_id, set_dynamixel_id,
                            get_dynamixel_id.__doc__)


    def get_data(self):
        """A sequence of byte containing the packet's data: the instruction to
        perform or the status of the Dynamixel actuator.

        The data property contains the fifth to the penultimate byte of the
        full built packet.
        """

        return self._data


    def set_data(self, data_bytes):
        """Set the data property.

        A sequence of byte or an integer is required.
        """

        # Check the data bytes and convert it to "bytes" if necessary.
        # This conversion assert "data_bytes" items are in range (0, 0xff).
        # "TypeError" and "ValueError" are sent by the "bytes" constructor if
        # necessary.
        if isinstance(data_bytes, int):
            data_bytes = bytes((data_bytes, ))
        else:
            data_bytes = bytes(data_bytes)

        self._data = data_bytes


    data = property(get_data, set_data, get_data.__doc__)


    @property
    def length(self):
        """Return the length of the packet.

        This is not the actual length of the packet but the value of the fourth
        byte (called "LENGTH") of each packet computed as follow:
        length = data length + 1

        In other words, for a given packet, this "length" is the number of
        bytes after its fourth byte.
        """

        return len(self.data) + 1


    @property
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

        byte_array = bytearray()
        byte_array.append(self.dynamixel_id)
        byte_array.append(self.length)
        byte_array.extend(self.data)

        checksum = dynamixel_checksum(byte_array)

        return checksum


    def to_byte_array(self):
        """Return the packet as a bytearray (a mutable sequence of bytes).

        Returns something like: bytearray(b'\xff\xff\xfe\x04\x03\x03\x01\xf6').
        """

        byte_array = bytearray(PACKET_HEADER)
        byte_array.append(self.dynamixel_id)
        byte_array.append(self.length)
        byte_array.extend(self.data)
        byte_array.append(self.checksum)

        return byte_array


    def to_bytes(self):
        """Return the packet as a bytes string (an immutable sequence of
        bytes).

        Returns something like: b'\xff\xff\xfe\x04\x03\x03\x01\xf6'.
        """

        return bytes(self.to_byte_array())


    def to_integer_tuple(self):
        """Return the packet as a tuple of integers.

        Returns something like: (255, 255, 254, 4, 3, 3, 1, 246).
        """

        return tuple(self.to_byte_array())


    def to_printable_string(self):
        """Return the packet as a string of hexadecimal values.

        Returns something like: ff ff fe 04 03 03 01 f6.
        """

        byte_array = self.to_byte_array()
        packet_str = ' '.join(['%02x' % byte for byte in byte_array])

        return packet_str


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
This module contains the general `Packet` class which implements the either
"instruction packet" (the packets sent by the controller to the Dynamixel
actuators to send commands) or "status packet" (the response packets from
the Dynamixel units to the main controller after receiving an instruction
packet).
"""

__all__ = ['Packet',
           'compute_checksum']


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

def compute_checksum(byte_seq):
    """Compute and return the checksum of the `byte_seq` packet.

    The checksum is the value of the last byte of each packet. It is used
    to prevent transmission errors of packets. Checksums are computed as
    follow::

        Checksum = ~(dynamixel_id + length + data1 + ... + dataN)

    where ~ represent the NOT logic operation.

    If the computed value is larger than 255, then only its lower byte is
    defined as the checksum value.

    :param bytes byte_seq: a byte sequence containing the packet's bytes
        involved in the computation of the checksum (i.e. from the third to the
        penultimate byte of the "full packet" considered).
    """

    # Check the argument and convert it to "bytes" if necessary.
    # Assert "byte_seq" items are in range (0, 0xff).
    # "TypeError" and "ValueError" are sent by the "bytes" constructor if
    # necessary.
    # The statement "tuple(byte_seq)" implicitely rejects integers (and all
    # non-iterable objects) to compensate the fact that the bytes constructor
    # doesn't reject them: bytes(3) is valid and returns b'\x00\x00\x00'.
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
    """The general raw `Packet` class.

    It implements the either "instruction packet" (the packets sent by the
    controller to the Dynamixel actuators to send commands) or "status packet"
    (the response packets from the Dynamixel units to the main controller after
    receiving an instruction packet).

    The structure of a general `Packet` is as the following:

    +----+----+--+------+-------+---------+
    |0xFF|0xFF|ID|LENGTH|DATA...|CHECK SUM|
    +----+----+--+------+-------+---------+

    This class has been made for debugging purpose and is not intended to be
    used widely to create packets.
    Instead, it is recommanded to use `InstructionPacket` or `StatusPacket`
    classes to build `Packet` instances.

    :param int dynamixel_id: the unique ID of a Dynamixel unit (from 0x00
        to 0xFD), 0xFE is a broadcasting ID.
    :param bytes data: a sequence of byte containing the packet's data: the
        instruction to perform or the status of the Dynamixel actuator.
        This `data` argument contains the fifth to the penultimate byte of
        the full built packet.
    """

    def __init__(self, dynamixel_id, data):

        # Check the data bytes.
        # "TypeError" and "ValueError" are raised by the "bytes" constructor if
        # necessary.
        if isinstance(data, int):
            data = bytes((data, )) # convert integers to a sequence
        else:
            data = bytes(data)

        # Add the header bytes.
        self._bytes = bytearray((0xff, 0xff))

        # Check and add the Dynamixel ID byte.
        # "TypeError" and "ValueError" are raised by the "bytearray.append()"
        # if necessary.
        if 0x00 <= dynamixel_id <= 0xfe:
            self._bytes.append(dynamixel_id)
        else:
            msg = "Wrong dynamixel_id: {:#x} (should be in range(0x00, 0xfe))."
            raise ValueError(msg.format(dynamixel_id))

        # Add the length byte.
        self._bytes.append(len(data) + 1)

        # Add the data bytes.
        self._bytes.extend(data)

        # Add the checksum byte.
        computed_checksum = compute_checksum(self._bytes[2:])
        self._bytes.append(computed_checksum)


    def to_byte_array(self):
        r"""Return the packet as a bytearray (a mutable sequence of bytes).

        This function returns something like::

            bytearray(b'\xff\xff\xfe\x04\x03\x03\x01\xf6')
        """

        return bytearray(self._bytes)


    def to_bytes(self):
        r"""Return the packet as a bytes string (an immutable sequence of
        bytes).

        This function returns something like::

            b'\xff\xff\xfe\x04\x03\x03\x01\xf6'
        """

        return bytes(self._bytes)


    def to_integer_tuple(self):
        """Return the packet as a tuple of integers.

        This function returns something like::

            (255, 255, 254, 4, 3, 3, 1, 246)
        """

        return tuple(self._bytes)


    def to_printable_string(self):
        """Return the packet as a string of hexadecimal values.

        This function returns something like::

            ff ff fe 04 03 03 01 f6
        """

        packet_str = ' '.join(['%02x' % byte for byte in self._bytes])

        return packet_str


    # READ ONLY PROPERTIES

    @property
    def header(self):
        r"""The header of the packet.

        This pair of byte should always be equals to ``b'\xff\xff'``.

        This member is a read-only property.
        """
        return self._bytes[0:2]

    @property
    def dynamixel_id(self):
        r"""The unique ID of a Dynamixel unit concerned with this packet.

        This byte either:

        - has a value between 0x00 and 0xFD to affect the corresponding
          Dynamixel unit
        - or has the value 0xFE to affect all connected units (0xFE is the
          "broadcasting" ID).

        This member is a read-only property.
        """
        return self._bytes[2]

    @property
    def length(self):
        """The so called "length" of the packet.

        This is not the actual length of the full packet (`self._bytes`) but
        its number of bytes after its fourth byte, i.e.::

            len(self._bytes[4:])

        or in other words::

            len(self._bytes) - 4

        This value (so called "LENGTH") defines the fourth byte of each packet.

        This member is a read-only property.
        """
        return self._bytes[3]

    @property
    def parameters(self):
        """A sequence of byte used if there is additional information needed
        to be read (other than the error itself).

        This member is a read-only property.
        """
        return self._bytes[5:-1]

    @property
    def data(self):
        """A sequence of byte containing the packet's data, i.e. from the fifth
        to the penultimate byte of the "full packet".

        It contains either:

        - the instruction to perform and its parameters if the packet is an
          "instruction packet";
        - or the status of the Dynamixel actuator (the "error" and "parameters"
          fields) if the packet is a "status packet".

        This member is a read-only property.
        """
        return self._bytes[4:-1]

    @property
    def checksum(self):
        """The packet checksum, used to prevent packet transmission error.

        This member is a read-only property.
        """
        return self._bytes[-1]

# -*- coding : utf-8 -*-

# PyAX12

# Copyright (c) 2010 Jeremie Decock (http://www.jdhp.org)

# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import warnings

BROADCAST_ID = 0xfe
PACKET_HEADER = (0xff, 0xff)

# Control table
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

class Packet(object):

    def __init__(self, _id, _data):
        """Create a raw packet.

        Instance variable:
        dynamixel_id -- the unique ID of a Dynamixel unit (from 0x00 to 0xFD),
                        0xFE is a broadcasting ID;
        data -- a tuple containing the packet's data;
        """
        if 0x00 <= _id <= 0xfe:
            self.dynamixel_id = _id
        else:
            warnings.warn('Wrong id')

        self.data = _data

    def length(self):
        """Return the length of the packet.

        Length = data length + 1
        """
        return len(self.data) + 1

    def checksum(self):
        """Compute packet checksum.
        
        Checksum = ~(dynamixel_id + length + instruction + parameter1 + ... + parameterN)
        where ~ represent the NOT logic operation.

        If calculated value is larger than 255, the lower byte is defined as
        the checksum value.
        """
        checksum_data_tuple = (self.dynamixel_id, self.length()) + self.data
        checksum = ~sum(checksum_data_tuple) & 0xff
        return checksum

    def to_integer_tuple(self):
        """Return the packet as a tuple of integers."""
        return PACKET_HEADER + (self.dynamixel_id, self.length()) + self.data + (self.checksum(),)

    def to_printable_string(self):
        """Return the packet as a string of hexadecimal values."""
        return ' '.join(['%02x' % integer for integer in self.to_integer_tuple()])

    def to_byte_array(self):
        """Return the packet as a bytearray (array of bytes)."""
        return bytearray(self.to_integer_tuple())


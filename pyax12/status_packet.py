# -*- coding : utf-8 -*-

# PyAX12

# Copyright (c) 2010,2015 Jeremie Decock (http://www.jdhp.org)

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

"""
This module contain the "StatusPacket" class which implements
"status packet" (the response packets from the Dynamixel units to the main
controller after receiving an instruction packet).
"""

__all__ = ['StatusPacket']

import pyax12.packet as pk
from pyax12 import utils

class StatusPacket(pk.Packet):
    """The Status Packet is the response packet from the Dynamixel units to the
    main controller after receiving an instruction packet.

    The structure of the status packet is as the following:

    +----+----+--+------+-----+----------+---+-----------+---------+
    |0XFF|0XFF|ID|LENGTH|ERROR|PARAMETER1|...|PARAMETER N|CHECK SUM|
    +----+----+--+------+-----+----------+---+-----------+---------+
    """

    def __init__(self, byte_array_packet):
        """Create a status packet.

        StatusPacket is not intended to be instancied by users (except maybe
        for debugging prupose). Under normal conditions of use, StatusPacket's
        instances are automatically created by the "Connection" class.

        Keyword arguments:
        byte_array_packet -- a bytearray containing the full status packet
                             returned by Dynamixel units.
        """

        if len(byte_array_packet) >= 6:

            self.dynamixel_id = byte_array_packet[2]
            self.error = byte_array_packet[4]
            self.parameters = tuple([byte for byte in byte_array_packet[5:-1]])

            # Write error bits
            self.instruction_error = bool(self.error & (1 << 6))
            self.overload_error = bool(self.error & (1 << 5))
            self.checksum_error = bool(self.error & (1 << 4))
            self.range_error = bool(self.error & (1 << 3))
            self.overheating_error = bool(self.error & (1 << 2))
            self.angle_limit_error = bool(self.error & (1 << 1))
            self.input_voltage_error = bool(self.error & (1 << 0))

            # Check the header bytes
            header_tuple = tuple(byte_array_packet[0:2])
            if header_tuple != (0xff, 0xff):
                msg = 'Wrong header: {} (should be in "ff ff")).'
                header_str = utils.int_seq_to_hex_str(header_tuple)
                raise ValueError(msg.format(header_str))

            # Verify the checksum (it should be the first byte to check to
            # avoid wrong error message in case of transmission error)
            byte_tuple = tuple(byte_array_packet[2:-1])
            computed_checksum = pk.dynamixel_checksum(byte_tuple)
            if computed_checksum != byte_array_packet[-1]:
                msg = 'Wrong checksum: {}.'
                packet_str = utils.int_seq_to_hex_str(tuple(byte_array_packet))
                raise ValueError(msg.format(packet_str))

            # Check the ID byte
            if not (0x00 <= self.dynamixel_id <= 0xfe):
                msg = "Wrong dynamixel_id:"
                msg += " {:#x} (should be in range(0x00, 0xfe))."
                raise ValueError(msg.format(self.dynamixel_id))

            # Check length (length = num_params + 2 = full_packet_length - 4)
            measured_length = len(byte_array_packet) - 4
            if measured_length != byte_array_packet[3]:
                msg = 'Wrong length: {}.'
                packet_str = utils.int_seq_to_hex_str(tuple(byte_array_packet))
                raise ValueError(msg.format(packet_str))

            # TODO: if an error bit flag is ON:
            #       check params length and value
            #       if ok, parse param
            #       raise exception on error bits (user defined exceptions)

            # Set self.data
            self.data = (self.error, ) + self.parameters
        else:
            msg = "Incomplete packet: ({})."
            packet_str = utils.int_seq_to_hex_str(byte_array_packet)
            raise ValueError(msg.format(packet_str))


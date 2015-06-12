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

from pyax12.packet import Packet

class StatusPacket(Packet):
    """The Status Packet is the response packet from the Dynamixel units to the main
    controller after receiving an instruction packet.
    
    The structure of the status packet is as the following.

    +----+----+--+------+-----+----------+---+-----------+---------+
    |0XFF|0XFF|ID|LENGTH|ERROR|PARAMETER1|...|PARAMETER N|CHECK SUM|
    +----+----+--+------+-----+----------+---+-----------+---------+
    """

    def __init__(self, byte_array_packet):
        """Create a status packet."""

        if len(byte_array_packet) >= 6:
            self.dynamixel_id = byte_array_packet[2]
            self.error = byte_array_packet[4]
            self.parameters = tuple([byte_value for byte_value in byte_array_packet[5:-1]])

            # Write error bits
            self.instruction_error = bool(self.error & (1 << 6)) 
            self.overload_error = bool(self.error & (1 << 5)) 
            self.checksum_error = bool(self.error & (1 << 4)) 
            self.range_error = bool(self.error & (1 << 3)) 
            self.overheating_error = bool(self.error & (1 << 2)) 
            self.angle_limit_error = bool(self.error & (1 << 1)) 
            self.input_voltage_error = bool(self.error & (1 << 0)) 

            # Check the ID byte
            if not 0x00 <= self.dynamixel_id <= 0xfe:
                warnings.warn('Wrong dynamixel_id')

            # TODO: check checksum, length and header

            self.data = (self.error, ) + self.parameters
        else:
            pass # TODO: warning/error
 

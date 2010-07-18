# -*- coding : utf-8 -*-

# PyDynamixel

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

BROADCAST_ID = 0xfe
PACKET_HEADER = (0xff, 0xff)

class Packet:

    id = 0x00
    data = ()

    def __init__(self, id=None, data=None):
        # TODO : check id and data value
        self.id = id
        self.data = data

    def length(self):
        """Return the length of the packet.

        Length = data length + 1"""

        return len(self.data) + 1

    def checksum(self):
        """Compute packet checksum.
        
        Checksum = ~(id + length + instruction + parameter1 + ... + parameterN)
        where ~ represent the NOT logic operation.

        If calculated value is larger than 255, the lower byte is defined as
        the checksum value."""
        
        sum = reduce(lambda x, y: x + y, (self.id,) + (self.length(),) + self.data)
        checksum = ~sum & 0xff
        return checksum

    def to_integer_list(self):
        "Return the packet as a tuple of integers."

        return PACKET_HEADER + (self.id,) + (self.length(),) + self.data + (self.checksum(),)

    def to_printable_string(self):
        "Return the packet as a string of hexadecimal values."
        return ' '.join(['%02x' % b for b in self.to_integer_list()])

    def to_raw_string(self):
        "Return the packet as a string of hexadecimal values."
        return ''.join(map(chr, self.to_integer_list()))


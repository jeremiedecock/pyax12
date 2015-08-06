#!/usr/bin/env python3
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
This module contains unit tests for the "StatusPacket" class.
"""

from pyax12.status_packet import StatusPacket

import unittest

class TestStatusPacket(unittest.TestCase):
    """
    Contains unit tests for the "StatusPacket" class.
    """

    def test_wrong_arg_type(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "byte_array_packet" has a wrong type."""

        # Wrong type (tuple instead bytearray)
        bytearray_packet = (0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb)

        with self.assertRaises(TypeError):
            StatusPacket(bytearray_packet)


    def test_bytearray_len(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "byte_array_packet" is too short: at least 6 bytes are required to make
        a valid packet (two for the header, one for the dynamixel ID, one for
        the packet "length", one for the error code, one for the checksum and
        the rest for parameters)."""

        # Wrong packet: too short (at least 6 bytes are required)
        bytearray_packet = bytearray((0xff, 0xff, 0x01, 0x03, 0x00))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)

        # Wrong packet: too short (at least 6 bytes are required)
        bytearray_packet = bytearray((0xff,))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)

        # Wrong packet: too short (at least 6 bytes are required)
        bytearray_packet = bytearray(())

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)


    def test_header_bytes(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "byte_array_packet" has a wrong header (when the two first bytes are
        not equal to "\xff\xff")."""

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        bytearray_packet = bytearray((0xff, 0, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        bytearray_packet = bytearray((0, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        bytearray_packet = bytearray((0, 0, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)


    def test_checksum_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "byte_array_packet" has a wrong "checksum" byte (the last byte)."""

        # Wrong packet: wrong "checksum" byte (the last byte)
        bytearray_packet = bytearray((0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)


    def test_id_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "byte_array_packet" has a wrong "id" byte (the third byte)."""

        # Wrong packet: wrong "id" byte (the third byte)
        bytearray_packet = bytearray((0xff, 0xff, 0xff, 0x03, 0x00, 0x20, 0))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)


    def test_lenth_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "byte_array_packet" has a wrong "length" byte (the fourth packet's byte
        must be equal to "len(byte_array_packet) - 4")."""

        # Wrong packet: wrong "length" byte (the fourth byte)
        bytearray_packet = bytearray((0xff, 0xff, 0x01, 0x02, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        bytearray_packet = bytearray((0xff, 0xff, 0x01, 0x00, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        bytearray_packet = bytearray((0xff, 0xff, 0x01, 0x04, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        bytearray_packet = bytearray((0xff, 0xff, 0x01, 0xff, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytearray_packet)


    def test_example2(self):
        """Check the example 2 from the Dynamixel user guide: "Reading the
        internal temperature of the Dynamixel actuator with an ID of 1"
        (p.20)."""

        # Return the internal temperature of the Dynamixel actuator #1
        bytearray_packet = bytearray((0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb))

        try:
            StatusPacket(bytearray_packet)
        except Exception:
            self.fail("Encountered an unexpected exception.")



if __name__ == '__main__':
    unittest.main()


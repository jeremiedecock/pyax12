#!/usr/bin/env python3
# -*- coding : utf-8 -*-

# PyAX12

# Copyright (c) 2015 Jeremie Decock (http://www.jdhp.org)

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
This module contain unit tests for the "Packet" class.
"""

import pyax12.packet as pk

import unittest

class TestPacket(unittest.TestCase):
    """
    Contains unit tests for the "packet" module.
    """

    # Tests for the dynamixel_checksum function ###############################

    def test_checksum_func_incomplete(self):
        """Check that the dynamixel_checksum function fails when the
        "byte_tuple" argument is incomplete (len(byte_tuple) < 3)."""

        byte_tuple = (0x01, 0x02)                      # incomplete packet

        with self.assertRaises(ValueError):
            pk.dynamixel_checksum(byte_tuple)


    def test_checksum_func_wrong_type(self):
        """Check that the dynamixel_checksum function fails when the
        "byte_tuple" argument has a wrong type (float)."""

        byte_tuple = 1.0                               # wrong type

        with self.assertRaises(TypeError):
            pk.dynamixel_checksum(byte_tuple)


    def test_checksum_func_wrong_byte_type(self):
        """Check that the dynamixel_checksum function fails when an item of the
        "byte_tuple" argument has a wrong type (float)."""

        byte_tuple = (0x01, 1.0, 0x02, 0x2b, 0x01)     # wrong type

        with self.assertRaises(TypeError):
            pk.dynamixel_checksum(byte_tuple)


    def test_checksum_func_wrong_byte_value_low(self):
        """Check that the dynamixel_checksum function fails when an item of the
        "byte_tuple" argument has a wrong value (too low value)."""

        byte_tuple = (0x01, -1, 0x02, 0x2b, 0x01)      # wrong value

        with self.assertRaises(ValueError):
            pk.dynamixel_checksum(byte_tuple)


    def test_checksum_func_wrong_byte_value_hi(self):
        """Check that the dynamixel_checksum function fails when an item of the
        "byte_tuple" argument has a wrong value (too high value)."""

        byte_tuple = (0x01, 0xffff, 0x02, 0x2b, 0x01)  # wrong value

        with self.assertRaises(ValueError):
            pk.dynamixel_checksum(byte_tuple)


    def test_checksum_func_wrong_id_value_hi(self):
        """Check that the dynamixel_checksum function fails when the "id" byte
        of the "byte_tuple" argument has a wrong value (too high value)."""

        byte_tuple = (0xff,)             # wrong id
        byte_tuple += (4,)               # length
        byte_tuple += (0x02, 0x2b, 0x01) # read the temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.dynamixel_checksum(byte_tuple)


    def test_checksum_func_wrong_length_value_low(self):
        """Check that the dynamixel_checksum function fails when the "length"
        byte of the "byte_tuple" argument has a wrong value (too low value).
        """

        byte_tuple = (1,)                # id
        byte_tuple += (1,)               # wrong length
        byte_tuple += (0x02, 0x2b, 0x01) # read the temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.dynamixel_checksum(byte_tuple)


    def test_checksum_func_wrong_length_value_hi(self):
        """Check that the dynamixel_checksum function fails when the "length"
        byte of the "byte_tuple" argument has a wrong value (too high value).
        """

        byte_tuple = (1,)                # id
        byte_tuple += (9,)               # wrong length
        byte_tuple += (0x02, 0x2b, 0x01) # read the temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.dynamixel_checksum(byte_tuple)


    def test_checksum_func_example1(self):
        """Check the "dynamixel_checksum" function using the example 2 of the
        Dynamixel user guide: "Reading the internal temperature of the
        Dynamixel actuator with an ID of 1" (p.20)."""

        byte_tuple = (1,)                # id
        byte_tuple += (4,)               # length
        byte_tuple += (0x02, 0x2b, 0x01) # read the temperature of the dynamixel

        checksum_byte = pk.dynamixel_checksum(byte_tuple)
        expected_checksum_byte = 0xcc

        self.assertEqual(checksum_byte, expected_checksum_byte)

    # Tests for the Packet class ##############################################

    def test_wrong_id_type_float(self):
        """Check that pk.Packet fails when the "_id" argument's type
        is wrong (float)."""

        dynamixel_id = 1.0        # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)


    def test_wrong_id_value_hi(self):
        """Check that pk.Packet fails when the "_id" argument's
        value is wrong (too high value)."""

        dynamixel_id = 1000       # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.Packet(dynamixel_id, data)


    def test_wrong_id_value_negative(self):
        """Check that pk.Packet fails when the "_id" argument's
        value is wrong (negative value)."""

        dynamixel_id = -1         # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.Packet(dynamixel_id, data)

    ###

    def test_wrong_params_type_int(self):
        """Check that pk.Packet fails when the "_data" argument's type is wrong
        (int)."""

        dynamixel_id = 1
        data = 0x00                 # wrong type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)


    def test_wrong_params_items_type_float(self):
        """Check that pk.Packet fails when the "_data" items argument's type is
        wrong (float)."""

        dynamixel_id = 1
        data = (0x02, 0x2b, 1.0)    # wrong item type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)


    def test_wrong_params_value(self):
        """Check that pk.Packet fails when the "_data" items value is wrong
        (too high value)."""

        dynamixel_id = 1
        data = (0x02, 0x2b, 0xffff) # wrong value

        with self.assertRaises(ValueError):
            pk.Packet(dynamixel_id, data)

    ###

    def test_to_integer_tuple_func(self):
        """Check the pk.to_integer_tuple() function.

        Based on the Dynamixel user guide, example 2: "Reading the internal
        temperature of the Dynamixel actuator with an ID of 1" (p.20).
        """

        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        raw_packet = pk.Packet(dynamixel_id, data)

        expected_str = (0xff, 0xff, 0x01, 0x04, 0x02, 0x2b, 0x01, 0xcc)
        self.assertEqual(raw_packet.to_integer_tuple(), expected_str)


    def test_to_printable_string_func(self):
        """Check the pk.to_printable_string() function.

        Based on the Dynamixel user guide, example 2: "Reading the internal
        temperature of the Dynamixel actuator with an ID of 1" (p.20).
        """

        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        raw_packet = pk.Packet(dynamixel_id, data)

        expected_str = "ff ff 01 04 02 2b 01 cc"
        self.assertEqual(raw_packet.to_printable_string(), expected_str)


    def test_to_byte_array_func(self):
        """Check the pk.to_byte_array() function.

        Based on the Dynamixel user guide, example 2: "Reading the internal
        temperature of the Dynamixel actuator with an ID of 1" (p.20).
        """

        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        raw_packet = pk.Packet(dynamixel_id, data)

        expected_str = bytearray(b'\xff\xff\x01\x04\x02\x2b\x01\xcc')
        self.assertEqual(raw_packet.to_byte_array(), expected_str)


if __name__ == '__main__':
    unittest.main()


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
This module contain unit tests for the "Packet" class.
"""

import pyax12.packet as pk

import unittest

class TestPacket(unittest.TestCase):
    """
    Contains unit tests for the "packet" module.
    """

    # Tests for the compute_checksum function ###############################

    def test_checksum_func_incomplete(self):
        """Check that the compute_checksum function fails when the
        "byte_seq" argument is incomplete (len(byte_seq) < 3)."""

        byte_seq = (0x01, 0x02)                      # incomplete packet

        with self.assertRaises(ValueError):
            pk.compute_checksum(byte_seq)


    def test_checksum_func_wrong_arg_type(self):
        """Check that the compute_checksum function fails when the
        "byte_seq" argument has a wrong type."""

        # Check with None
        byte_seq = None                              # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)

        # Check with an integer
        byte_seq = 0                                 # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)

        # Check with an integer
        byte_seq = 1                                 # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)

        # Check with an integer
        byte_seq = 3                                 # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)

        # Check with a float
        byte_seq = 1.0                               # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)

        # Check with a string
        byte_seq = "hello"                           # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)


    def test_checksum_func_good_arg_type(self):
        """Check the "compute_checksum" function using the example 2 of the
        Dynamixel user guide: "Reading the internal temperature of the
        Dynamixel actuator with an ID of 1" (p.20)."""

        # Check with a tuple
        byte_seq = (0x01, 0x04, 0x02, 0x2b, 0x01)

        checksum_byte = pk.compute_checksum(byte_seq)
        expected_checksum_byte = 0xcc

        self.assertEqual(checksum_byte, expected_checksum_byte)

        # Check with a list
        byte_seq = [0x01, 0x04, 0x02, 0x2b, 0x01]

        checksum_byte = pk.compute_checksum(byte_seq)
        expected_checksum_byte = 0xcc

        self.assertEqual(checksum_byte, expected_checksum_byte)

        # Check with a bytes string
        byte_seq = bytes((0x01, 0x04, 0x02, 0x2b, 0x01))

        checksum_byte = pk.compute_checksum(byte_seq)
        expected_checksum_byte = 0xcc

        self.assertEqual(checksum_byte, expected_checksum_byte)

        # Check with a bytearray
        byte_seq = bytearray((0x01, 0x04, 0x02, 0x2b, 0x01))

        checksum_byte = pk.compute_checksum(byte_seq)
        expected_checksum_byte = 0xcc

        self.assertEqual(checksum_byte, expected_checksum_byte)


    def test_checksum_func_wrong_byte_type(self):
        """Check that the compute_checksum function fails when an item of the
        "byte_seq" argument has a wrong type (float)."""

        # Check with None
        byte_seq = (0x01, None, 0x02, 0x2b, 0x01)    # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)

        # Check with float
        byte_seq = (0x01, 1.0, 0x02, 0x2b, 0x01)     # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)

        # Check with string
        byte_seq = (0x01, "hi", 0x02, 0x2b, 0x01)    # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)

        # Check with tuple
        byte_seq = (0x01, (), 0x02, 0x2b, 0x01)      # wrong type

        with self.assertRaises(TypeError):
            pk.compute_checksum(byte_seq)


    def test_checksum_func_wrong_byte_value(self):
        """Check that the compute_checksum function fails when an item of the
        "byte_seq" argument has a wrong value (too low or too high)."""

        # Too low value
        byte_seq = (0x01, -1, 0x02, 0x2b, 0x01)      # wrong value

        with self.assertRaises(ValueError):
            pk.compute_checksum(byte_seq)

        # Too high value
        byte_seq = (0x01, 0xffff, 0x02, 0x2b, 0x01)  # wrong value

        with self.assertRaises(ValueError):
            pk.compute_checksum(byte_seq)


    def test_checksum_func_wrong_id_byte(self):
        """Check that the compute_checksum function fails when the "id" byte
        of the "byte_seq" argument has a wrong value (too high value)."""

        byte_seq = (0xff,)             # wrong id
        byte_seq += (4,)               # length
        byte_seq += (0x02, 0x2b, 0x01) # read the temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.compute_checksum(byte_seq)


    def test_checksum_func_wrong_length_byte(self):
        """Check that the compute_checksum function fails when the "length"
        byte of the "byte_seq" argument has a wrong value (too low or too
        high).
        """

        # Too low value
        byte_seq = (1,)                # id
        byte_seq += (1,)               # wrong length
        byte_seq += (0x02, 0x2b, 0x01) # read the temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.compute_checksum(byte_seq)

        # Too high value
        byte_seq = (1,)                # id
        byte_seq += (9,)               # wrong length
        byte_seq += (0x02, 0x2b, 0x01) # read the temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.compute_checksum(byte_seq)


    def test_checksum_func_example1(self):
        """Check the "compute_checksum" function using the example 2 of the
        Dynamixel user guide: "Reading the internal temperature of the
        Dynamixel actuator with an ID of 1" (p.20)."""

        byte_seq = (1,)                # id
        byte_seq += (4,)               # length
        byte_seq += (0x02, 0x2b, 0x01) # read the temperature of the dynamixel

        checksum_byte = pk.compute_checksum(byte_seq)
        expected_checksum_byte = 0xcc

        self.assertEqual(checksum_byte, expected_checksum_byte)

    # Tests for the Packet class ##############################################

    # Test the "dynamixel_id" argument

    def test_wrong_id_type(self):
        """Check that the instanciation of Packet fails when the argument
        "dynamixel_id" has a wrong type."""

        # Check with None
        dynamixel_id = None       # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)

        # Check with float
        dynamixel_id = 1.0        # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)

        # Check with string
        dynamixel_id = "hi"       # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)

        # Check with tuple
        dynamixel_id = ()         # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)


    def test_wrong_id_value(self):
        """Check that the instanciation of Packet fails when the argument
        "dynamixel_id" has a wrong value (too low or too high)."""

        # Too low
        dynamixel_id = -1         # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.Packet(dynamixel_id, data)

        # Too high
        dynamixel_id = 1000       # wrong id
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        with self.assertRaises(ValueError):
            pk.Packet(dynamixel_id, data)

    # Test the "data" argument

    def test_wrong_data_type(self):
        """Check that the instanciation of Packet fails when the argument
        "data" has a wrong type."""

        # Check with None
        dynamixel_id = 1
        data = None                              # wrong type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)

        # Check with a float
        dynamixel_id = 1
        data = 1.0                               # wrong type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)

        # Check with a string
        dynamixel_id = 1
        data = "hello"                           # wrong type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)


    def test_good_data_type(self):
        """Check that the instanciation of Packet doesn't fail when the
        argument "data" has a right type."""

        # Check with a tuple
        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01)

        try:
            pk.Packet(dynamixel_id, data)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")

        # Check with a list
        dynamixel_id = 1
        data = [0x02, 0x2b, 0x01]

        try:
            pk.Packet(dynamixel_id, data)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")

        # Check with a bytes string
        dynamixel_id = 1
        data = bytes((0x02, 0x2b, 0x01))

        try:
            pk.Packet(dynamixel_id, data)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")

        # Check with a bytearray
        dynamixel_id = 1
        data = bytearray((0x02, 0x2b, 0x01))

        try:
            pk.Packet(dynamixel_id, data)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")

        # Check with an integer
        dynamixel_id = 1
        data = 0x01                 # Ping packet

        try:
            pk.Packet(dynamixel_id, data)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")


    def test_wrong_data_items_type(self):
        """Check that the instanciation of Packet fails when the "data"
        items type is wrong."""

        # Check with None
        dynamixel_id = 1
        data = (0x02, 0x2b, None)    # wrong item type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)

        # Check with float
        dynamixel_id = 1
        data = (0x02, 0x2b, 1.0)     # wrong item type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)

        # Check with string
        dynamixel_id = 1
        data = (0x02, 0x2b, "hi")    # wrong item type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)

        # Check with tuple
        dynamixel_id = 1
        data = (0x02, 0x2b, ())      # wrong item type

        with self.assertRaises(TypeError):
            pk.Packet(dynamixel_id, data)


    def test_wrong_data_items_value(self):
        """Check that the instanciation of Packet fails when the "data"
        items value is wrong (too high or too low)."""

        # Too high value
        dynamixel_id = 1
        data = (0x02, 0x2b, 0xffff) # wrong value

        with self.assertRaises(ValueError):
            pk.Packet(dynamixel_id, data)

        # Too low value
        dynamixel_id = 1
        data = (0x02, 0x2b, -1)     # wrong value

        with self.assertRaises(ValueError):
            pk.Packet(dynamixel_id, data)

    ###

    def test_to_integer_tuple_func(self):
        """Check the "to_integer_tuple()" function.

        Based on the Dynamixel user guide, example 2: "Reading the internal
        temperature of the Dynamixel actuator with an ID of 1" (p.20).
        """

        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        raw_packet = pk.Packet(dynamixel_id, data)

        expected_str = (0xff, 0xff, 0x01, 0x04, 0x02, 0x2b, 0x01, 0xcc)
        self.assertEqual(raw_packet.to_integer_tuple(), expected_str)


    def test_to_printable_string_func(self):
        """Check the "to_printable_string()" function.

        Based on the Dynamixel user guide, example 2: "Reading the internal
        temperature of the Dynamixel actuator with an ID of 1" (p.20).
        """

        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        raw_packet = pk.Packet(dynamixel_id, data)

        expected_str = "ff ff 01 04 02 2b 01 cc"
        self.assertEqual(raw_packet.to_printable_string(), expected_str)


    def test_to_byte_array_func(self):
        """Check the "to_byte_array()" function.

        Based on the Dynamixel user guide, example 2: "Reading the internal
        temperature of the Dynamixel actuator with an ID of 1" (p.20).
        """

        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        raw_packet = pk.Packet(dynamixel_id, data)

        expected_str = bytearray(b'\xff\xff\x01\x04\x02\x2b\x01\xcc')
        self.assertEqual(raw_packet.to_byte_array(), expected_str)


    def test_to_bytes_func(self):
        """Check the "to_bytes()" function.

        Based on the Dynamixel user guide, example 2: "Reading the internal
        temperature of the Dynamixel actuator with an ID of 1" (p.20).
        """

        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01) # read internal temperature of the dynamixel

        raw_packet = pk.Packet(dynamixel_id, data)

        expected_str = b'\xff\xff\x01\x04\x02\x2b\x01\xcc'
        self.assertEqual(raw_packet.to_bytes(), expected_str)


if __name__ == '__main__':
    unittest.main()


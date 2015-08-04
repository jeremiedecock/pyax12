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
This module contains some unit tests for the general purpose utility functions
implemented in the "utils" module.
"""

from pyax12 import utils

import unittest

class TestUtils(unittest.TestCase):
    """
    Contains some unit tests for the general purpose utility functions
    implemented in the "utils" module.
    """

    # Check int_to_little_endian_hex_tuple() ##################################

    def test_int_to_le_hex_tuple_func_type(self):
        """Check that the utils.int_to_little_endian_hex_tuple() function fails
        when the "integer" argument's type is wrong (float)."""

        with self.assertRaises(TypeError):
            utils.int_to_little_endian_hex_tuple(1.0)


    def test_int_to_le_hex_tuple_func_value_low(self):
        """Check that the utils.int_to_little_endian_hex_tuple() function fails
        when the "integer" argument's value is wrong (too low)."""

        with self.assertRaises(ValueError):
            utils.int_to_little_endian_hex_tuple(-1)       # too low


    def test_int_to_le_hex_tuple_func_value_hi(self):
        """Check that the utils.int_to_little_endian_hex_tuple() function fails
        when the "integer" argument's value is wrong (too high)."""

        with self.assertRaises(ValueError):
            utils.int_to_little_endian_hex_tuple(0xffffff) # too high


    def test_int_to_le_hex_tuple_func_1(self):
        """Check the returned value of utils.int_to_little_endian_hex_tuple().
        """

        hex_tuple = utils.int_to_little_endian_hex_tuple(0)
        expected_tuple = (0x00, 0x00)

        self.assertEqual(hex_tuple, expected_tuple)


    def test_int_to_le_hex_tuple_func_2(self):
        """Check the returned value of utils.int_to_little_endian_hex_tuple().
        """

        hex_tuple = utils.int_to_little_endian_hex_tuple(0xffff)
        expected_tuple = (0xff, 0xff)

        self.assertEqual(hex_tuple, expected_tuple)


    def test_int_to_le_hex_tuple_func_3(self):
        """Check the returned value of utils.int_to_little_endian_hex_tuple().
        """

        hex_tuple = utils.int_to_little_endian_hex_tuple(0x02bc)
        expected_tuple = (0xbc, 0x02)

        self.assertEqual(hex_tuple, expected_tuple)


    def test_int_to_le_hex_tuple_func_4(self):
        """Check the returned value of utils.int_to_little_endian_hex_tuple().
        """

        hex_tuple = utils.int_to_little_endian_hex_tuple(0xbc)
        expected_tuple = (0xbc, 0x00)

        self.assertEqual(hex_tuple, expected_tuple)


    def test_int_to_le_hex_tuple_func_5(self):
        """Check the returned value of utils.int_to_little_endian_hex_tuple().
        """

        hex_tuple = utils.int_to_little_endian_hex_tuple(1)
        expected_tuple = (0x01, 0x00)

        self.assertEqual(hex_tuple, expected_tuple)



    # Check int_seq_to_hex_str() ##############################################

    def test_int_seq_to_hex_str_func_type(self):
        """Check that the utils.int_seq_to_hex_str() function fails when the
        "tuple_of_integers" argument's type is wrong (int)."""

        with self.assertRaises(TypeError):
            utils.int_seq_to_hex_str(0)


    def test_int_seq_to_hex_str_func_items_type(self):
        """Check that the utils.int_seq_to_hex_str() function fails when the
        "tuple_of_integers" items have wrong type (float)."""

        tuple_of_integers = (1.0, 0, 10)       # wrong type (float)
        with self.assertRaises(TypeError):
            utils.int_seq_to_hex_str(tuple_of_integers)


    def test_int_seq_to_hex_str_func_items_value_low(self):
        """Check that the utils.int_seq_to_hex_str() function fails when the
        "integer_tuple" items's value is wrong (too low)."""

        tuple_of_integers = (-1, 0, 10)        # the first item is too low
        with self.assertRaises(ValueError):
            utils.int_seq_to_hex_str(tuple_of_integers)


    def test_int_seq_to_hex_str_func_items_value_hi(self):
        """Check that the utils.int_seq_to_hex_str() function fails when the
        "integer_tuple" items's value is wrong (too high)."""

        tuple_of_integers = (0xffff, 0, 10)    # the first item is too high
        with self.assertRaises(ValueError):
            utils.int_seq_to_hex_str(tuple_of_integers)


    def test_int_seq_to_hex_str_func_1(self):
        """Check the returned value of utils.int_seq_to_hex_str()."""

        tuple_of_integers = (0xff, 0, 0x0a)
        hex_str = utils.int_seq_to_hex_str(tuple_of_integers)
        expected_str = "ff,00,0a"

        self.assertEqual(hex_str, expected_str)


    def test_int_seq_to_hex_str_func_2(self):
        """Check the returned value of utils.int_seq_to_hex_str()."""

        tuple_of_integers = (0xff,)
        hex_str = utils.int_seq_to_hex_str(tuple_of_integers)
        expected_str = "ff"

        self.assertEqual(hex_str, expected_str)


    def test_int_seq_to_hex_str_func_3(self):
        """Check the returned value of utils.int_seq_to_hex_str()."""

        tuple_of_integers = (0xff,) * 10
        hex_str = utils.int_seq_to_hex_str(tuple_of_integers)
        expected_str = "ff," * 9 + "ff"

        self.assertEqual(hex_str, expected_str)


if __name__ == '__main__':
    unittest.main()


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
This module contain unit tests for the "pyax12.connection.Connection" class.
"""

from pyax12.connection import Connection
import serial

import unittest

class TestConnection(unittest.TestCase):
    """
    Contains unit tests for the "pyax12.connection.Connection" class.
    """

    def test_init_wrong_port_type(self):
        """Check that the pyax12.connection.Connection initialization fails
        when the "port" argument's type is wrong (bool)."""

        port = False           # wrong type (expected: str)
        baudrate = 57600
        timeout = 0.1

        with self.assertRaises(serial.serialutil.SerialException):
            serial_connection = Connection(port, baudrate, timeout)
            serial_connection.close()

    ###

    def test_init_wrong_port_value(self):
        """Check that the pyax12.connection.Connection initialization fails
        when the "port" argument's value is wrong (/dev/null)."""

        port = '/dev/null'  # wrong value
        baudrate = 57600
        timeout = 0.1

        with self.assertRaises(serial.serialutil.SerialException):
            serial_connection = Connection(port, baudrate, timeout)
            serial_connection.close()

    ###

#    def test_init_wrong_baudrate_type_float(self):
#        """Check that the pyax12.connection.Connection initialization fails
#        when the "baudrate" argument's type is wrong (float)."""
#
#        port = None
#        baudrate = 0.1      # wrong type
#        timeout = 0.1
#
#        with self.assertRaises(serial.serialutil.SerialException):
#            serial_connection = Connection(port, baudrate, timeout)
#            serial_connection.close()

    ###

#    def test_init_wrong_baudrate_value_negative(self):
#        """Check that the pyax12.connection.Connection initialization fails
#        when the "baudrate" argument's value is wrong (negative value)."""
#
#        port = None
#        baudrate = -1       # wrong value
#        timeout = 0.1
#
#        with self.assertRaises(serial.serialutil.SerialException):
#            serial_connection = Connection(port, baudrate, timeout)
#            serial_connection.close()


#    def test_init_wrong_baudrate_value_zero(self):
#        """Check that the pyax12.connection.Connection initialization fails
#        when the "baudrate" argument's value is wrong (zero)."""
#
#        port = None
#        baudrate = 0        # wrong value
#        timeout = 0.1
#
#        with self.assertRaises(serial.serialutil.SerialException):
#            serial_connection = Connection(port, baudrate, timeout)
#            serial_connection.close()

    ###

    def test_init_wrong_timeout_type_str(self):
        """Check that the pyax12.connection.Connection initialization fails
        when the "timeout" argument's type is wrong (string)."""

        port = None
        baudrate = 57600
        timeout = "0.1"     # wrong type

        with self.assertRaises(ValueError):
            serial_connection = Connection(port, baudrate, timeout)
            serial_connection.close()

    ###

#    def test_init_wrong_timeout_value_negative(self):
#        """Check that the pyax12.connection.Connection initialization fails
#        when the "timeout" argument's value is wrong (negative value)."""
#
#        port = None
#        baudrate = -1
#        timeout = 0.1       # wrong value
#
#        with self.assertRaises(serial.serialutil.SerialException):
#            serial_connection = Connection(port, baudrate, timeout)
#            serial_connection.close()


#    def test_init_wrong_timeout_value_zero(self):
#        """Check that the pyax12.connection.Connection initialization fails
#        when the "timeout" argument's value is wrong (zero)."""
#
#        port = None
#        baudrate = 0
#        timeout = 0.1       # wrong value
#
#        with self.assertRaises(serial.serialutil.SerialException):
#            serial_connection = Connection(port, baudrate, timeout)
#            serial_connection.close()


if __name__ == '__main__':
    unittest.main()


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
        when the "port" argument's type is wrong."""

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

#    def test_init_wrong_baud_rate_type(self):
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

#    def test_init_wrong_baud_rate_value(self):
#        """Check that the pyax12.connection.Connection initialization fails
#        when the "baudrate" argument's value is wrong."""
#
#        # negative
#        port = None
#        baudrate = -1       # wrong value
#        timeout = 0.1
#
#        with self.assertRaises(serial.serialutil.SerialException):
#            serial_connection = Connection(port, baudrate, timeout)
#            serial_connection.close()
#
#        # zero
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

#    def test_init_wrong_timeout_value(self):
#        """Check that the pyax12.connection.Connection initialization fails
#        when the "timeout" argument's value is wrong."""
#
#        # negative
#        port = None
#        baudrate = -1
#        timeout = 0.1       # wrong value
#
#        with self.assertRaises(serial.serialutil.SerialException):
#            serial_connection = Connection(port, baudrate, timeout)
#            serial_connection.close()
#
#        # zero
#        port = None
#        baudrate = 0
#        timeout = 0.1       # wrong value
#
#        with self.assertRaises(serial.serialutil.SerialException):
#            serial_connection = Connection(port, baudrate, timeout)
#            serial_connection.close()


if __name__ == '__main__':
    unittest.main()


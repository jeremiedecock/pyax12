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

from pyax12.status_packet import InstructionError
from pyax12.status_packet import OverloadError
from pyax12.status_packet import ChecksumError
from pyax12.status_packet import RangeError
from pyax12.status_packet import OverheatingError
from pyax12.status_packet import AngleLimitError
from pyax12.status_packet import InputVoltageError

from pyax12.packet import Packet
from pyax12.connection import Connection

import unittest

class TestStatusPacket(unittest.TestCase):
    """
    Contains unit tests for the "StatusPacket" class.
    """

    def test_wrong_arg_type(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "bytes_packet" has a wrong type."""

        # Wrong type (tuple instead bytes)
        bytes_packet = (0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb)

        with self.assertRaises(TypeError):
            StatusPacket(bytes_packet)


    def test_bytes_len(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "bytes_packet" is too short: at least 6 bytes are required to make
        a valid packet (two for the header, one for the dynamixel ID, one for
        the packet "length", one for the error code, one for the checksum and
        the rest for parameters)."""

        # Wrong packet: too short (at least 6 bytes are required)
        bytes_packet = bytes((0xff, 0xff, 0x01, 0x03, 0x00))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)

        # Wrong packet: too short (at least 6 bytes are required)
        bytes_packet = bytes((0xff,))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)

        # Wrong packet: too short (at least 6 bytes are required)
        bytes_packet = bytes(())

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)


    def test_header_bytes(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "bytes_packet" has a wrong header (when the two first bytes are
        not equal to "\xff\xff")."""

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        bytes_packet = bytes((0xff, 0, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        bytes_packet = bytes((0, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        bytes_packet = bytes((0, 0, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)


    def test_checksum_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "bytes_packet" has a wrong "checksum" byte (the last byte)."""

        # Wrong packet: wrong "checksum" byte (the last byte)
        bytes_packet = bytes((0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)


    def test_id_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "bytes_packet" has a wrong "id" byte (the third byte)."""

        # Wrong packet: wrong "id" byte (the third byte)
        bytes_packet = bytes((0xff, 0xff, 0xff, 0x03, 0x00, 0x20, 0))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)


    def test_lenth_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "bytes_packet" has a wrong "length" byte (the fourth packet's byte
        must be equal to "len(bytes_packet) - 4")."""

        # Wrong packet: wrong "length" byte (the fourth byte)
        bytes_packet = bytes((0xff, 0xff, 0x01, 0x02, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        bytes_packet = bytes((0xff, 0xff, 0x01, 0x00, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        bytes_packet = bytes((0xff, 0xff, 0x01, 0x04, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        bytes_packet = bytes((0xff, 0xff, 0x01, 0xff, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(bytes_packet)

    ###

    def test_instruction_error(self):
        """Check that the "InstructionError" exception is raised when the
        "instruction error" flag is ON on the StatusPacket's "error" byte.
        
        This test require to be connected to the Dynamixel number 1 using
        port "/dev/ttyUSB0" (thus it works on Unix systems only) at 57600
        baud."""

        # Connect to the serial port
        port = "/dev/ttyUSB0" # TODO
        baudrate = 57600      # TODO
        timeout = 0.1         # TODO
        serial_connection = Connection(port, baudrate, timeout)

        # Make a wrong instruction packet (based on the example 2 of the
        # Dynamixel user guide: "Reading the internal temperature of the
        # Dynamixel actuator with an ID of 1" (p.20))
        dynamixel_id = 1
        data = (0, 0x2b, 0x01)   # wrong instruction (the first byte)
        instruction_packet = Packet(dynamixel_id, data)

        # Send the wrong instruction packet and get the response
        with self.assertRaises(InstructionError):
            status_packet = serial_connection.send(instruction_packet)

    # TODO...

    ###

    def test_example2(self):
        """Check the example 2 from the Dynamixel user guide: "Reading the
        internal temperature of the Dynamixel actuator with an ID of 1"
        (p.20).
        
        In this test, status packet are made artificially, no connection to an
        actual Dynamixel actuator is required."""

        # Return the internal temperature of the Dynamixel actuator #1
        bytes_packet = bytes((0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb))

        try:
            StatusPacket(bytes_packet)
        except Exception:
            self.fail("Encountered an unexpected exception.")


    def test_example2_hard(self):
        """Check the example 2 from the Dynamixel user guide: "Reading the
        internal temperature of the Dynamixel actuator with an ID of 1"
        (p.20).
        
        This test require to be connected to the Dynamixel number 1 using
        port "/dev/ttyUSB0" (thus it works on Unix systems only) at 57600
        baud."""

        # Connect to the serial port
        port = "/dev/ttyUSB0" # TODO
        baudrate = 57600      # TODO
        timeout = 0.1         # TODO
        serial_connection = Connection(port, baudrate, timeout)

        # Make the instruction packet (based on the example 2 of the
        # Dynamixel user guide: "Reading the internal temperature of the
        # Dynamixel actuator with an ID of 1" (p.20))
        dynamixel_id = 1
        data = (0x02, 0x2b, 0x01)
        instruction_packet = Packet(dynamixel_id, data)

        try:
            status_packet = serial_connection.send(instruction_packet)
        except Exception:
            self.fail("Encountered an unexpected exception.")



if __name__ == '__main__':
    unittest.main()


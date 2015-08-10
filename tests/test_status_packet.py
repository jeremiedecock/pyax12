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

from pyax12.status_packet import StatusPacketError
from pyax12.status_packet import InstructionError
#from pyax12.status_packet import OverloadError
from pyax12.status_packet import InstructionChecksumError
from pyax12.status_packet import StatusChecksumError
from pyax12.status_packet import RangeError
#from pyax12.status_packet import OverheatingError
#from pyax12.status_packet import AngleLimitError
#from pyax12.status_packet import InputVoltageError

from pyax12.packet import Packet
from pyax12.connection import Connection

import unittest

class TestStatusPacket(unittest.TestCase):
    """
    Contains unit tests for the "StatusPacket" class.
    """

    def test_correct_arg_type(self):
        """Check that the instanciation of StatusPacket doesn't fail when the
        argument "packet" is correct.

        This test is based on the example 2 of the Dynamixel user guide:
        "Reading the internal temperature of the Dynamixel actuator with an ID
        of 1" (p.20).

        In this test, status packet are made artificially, no connection to any
        actual Dynamixel actuator is required."""

        # Test with a tuple of bytes
        packet = (0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb)

        try:
            StatusPacket(packet)
        except (TypeError, ValueError, StatusPacketError):
            self.fail("Encountered an unexpected exception.")

        # Test with a list of bytes
        packet = [0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb]

        try:
            StatusPacket(packet)
        except (TypeError, ValueError, StatusPacketError):
            self.fail("Encountered an unexpected exception.")

        # Test with a bytes string
        packet = bytes((0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb))

        try:
            StatusPacket(packet)
        except (TypeError, ValueError, StatusPacketError):
            self.fail("Encountered an unexpected exception.")

        # Test with a bytearray
        packet = bytearray((0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb))

        try:
            StatusPacket(packet)
        except (TypeError, ValueError, StatusPacketError):
            self.fail("Encountered an unexpected exception.")


    def test_wrong_arg_type(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "packet" has a wrong type."""

        # Wrong type: int
        packet = 1

        with self.assertRaises(TypeError):
            StatusPacket(packet)

        # Wrong type: int
        packet = 0

        with self.assertRaises(TypeError):
            StatusPacket(packet)

        # Wrong type: int
        # Trap to avoid: bytes(6) return a sequence of 6 bytes (equal to 0)
        # which could be seen as a valid packet. This error have to be properly
        # detected.
        packet = 6

        with self.assertRaises(TypeError):
            StatusPacket(packet)

        # Wrong type: None
        packet = None

        with self.assertRaises(TypeError):
            StatusPacket(packet)

        # Wrong type: float
        packet = 1.0

        with self.assertRaises(TypeError):
            StatusPacket(packet)

        # Wrong type: string
        packet = "hello world"

        with self.assertRaises(TypeError):
            StatusPacket(packet)


    def test_bytes_len(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "packet" is too short: at least 6 bytes are required to make
        a valid packet (two for the header, one for the dynamixel ID, one for
        the packet "length", one for the error code, one for the checksum and
        the rest for parameters).

        Note that the length of packets have to be tested before the checksum
        (thus the checksums in this test are wrong): this tests should raise a
        "ValueError" but not a "StatusChecksumError"."""

        # Wrong packet: too short (at least 6 bytes are required)
        packet = bytes((0xff, 0xff, 0x01, 0x03, 0x00))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

        # Wrong packet: too short (at least 6 bytes are required)
        packet = bytes((0xff,))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

        # Wrong packet: too short (at least 6 bytes are required)
        packet = bytes(())

        with self.assertRaises(ValueError):
            StatusPacket(packet)


    def test_header_bytes(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "packet" has a wrong header (when the two first bytes are
        not equal to "\xff\xff")."""

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        packet = bytes((0xff, 0, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        packet = bytes((0, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

        # Wrong packet: the two first bytes are not equal to "\xff\xff"
        packet = bytes((0, 0, 0x01, 0x03, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(packet)


    def test_checksum_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "packet" has a wrong "checksum" byte (the last byte)."""

        # Wrong packet: wrong "checksum" byte (the last byte)
        packet = bytes((0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0))

        with self.assertRaises(StatusChecksumError):
            StatusPacket(packet)


    def test_id_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "packet" has a wrong "id" byte (the third byte)."""

        # Wrong packet: wrong "id" byte (the third byte)
        packet = bytes((0xff, 0xff, 0xff, 0x03, 0x00, 0x20, 0xdd))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

        # Wrong packet: wrong "id" byte (the third byte)
        # The broadcast ID 0xFE is for instruction packets not for status
        # packets.
        packet = bytes((0xff, 0xff, 0xfe, 0x03, 0x00, 0x20, 0xde))

        with self.assertRaises(ValueError):
            StatusPacket(packet)


    def test_lenth_byte(self):
        """Check that the instanciation of StatusPacket fails when the argument
        "packet" has a wrong "length" byte (the fourth packet's byte
        must be equal to "len(packet) - 4")."""

        # Wrong packet: wrong "length" byte (the fourth byte)
        packet = bytes((0xff, 0xff, 0x01, 0x02, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        packet = bytes((0xff, 0xff, 0x01, 0x00, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        packet = bytes((0xff, 0xff, 0x01, 0x04, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

        # Wrong packet: wrong "length" byte (the fourth byte)
        packet = bytes((0xff, 0xff, 0x01, 0xff, 0x00, 0x20, 0xdb))

        with self.assertRaises(ValueError):
            StatusPacket(packet)

    ###

    def test_instruction_error(self):
        """Check that the "InstructionError" exception is raised when the
        "instruction error" flag is ON in the StatusPacket's "error" byte.

        This test requires to be connected to the Dynamixel number 1 using
        port "/dev/ttyUSB0" at 57600 baud (thus it only works on Unix systems
        with FTDI devices)."""

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
            serial_connection.send(instruction_packet)


    def test_checksum_error(self):
        """Check that the "InstructionChecksumError" exception is raised when
        the "checksum error" flag is ON in the StatusPacket's "error" byte.

        This test requires to be connected to the Dynamixel number 1 using
        port "/dev/ttyUSB0" at 57600 baud (thus it only works on Unix systems
        with FTDI devices)."""

        # Connect to the serial port
        port = "/dev/ttyUSB0" # TODO
        baudrate = 57600      # TODO
        timeout = 0.1         # TODO
        serial_connection = Connection(port, baudrate, timeout)

        # Make a wrong instruction packet (based on the example 2 of the
        # Dynamixel user guide: "Reading the internal temperature of the
        # Dynamixel actuator with an ID of 1" (p.20))
        packet = bytes((0xff, 0xff, 0x01, 0x04, 0x02, 0x2b, 0x01, 0))

        # Send the wrong instruction packet and get the response
        with self.assertRaises(InstructionChecksumError):
            serial_connection.send(packet)


    def test_range_error(self):
        """Check that the "RangeError" exception is raised when the
        "range error" flag is ON in the StatusPacket's "error" byte.

        This test requires to be connected to the Dynamixel number 1 using
        port "/dev/ttyUSB0" at 57600 baud (thus it only works on Unix systems
        with FTDI devices)."""

        # Connect to the serial port
        port = "/dev/ttyUSB0" # TODO
        baudrate = 57600      # TODO
        timeout = 0.1         # TODO
        serial_connection = Connection(port, baudrate, timeout)

        # Make a wrong instruction packet (set the LED byte in the control
        # table)
        dynamixel_id = 1
        data = (0x03, 0x19, 0xff)   # wrong parameter value (the last byte)
        instruction_packet = Packet(dynamixel_id, data)

        # Send the wrong instruction packet and get the response
        with self.assertRaises(RangeError):
            serial_connection.send(instruction_packet)

    # TODO...

    ###

    def test_example2(self):
        """Check the example 2 from the Dynamixel user guide: "Reading the
        internal temperature of the Dynamixel actuator with an ID of 1"
        (p.20).

        In this test, status packet are made artificially, no connection to an
        actual Dynamixel actuator is required."""

        # Return the internal temperature of the Dynamixel actuator #1
        packet = bytes((0xff, 0xff, 0x01, 0x03, 0x00, 0x20, 0xdb))

        try:
            StatusPacket(packet)
        except (TypeError, ValueError, StatusPacketError):
            self.fail("Encountered an unexpected exception.")


    def test_example2_hard(self):
        """Check the example 2 from the Dynamixel user guide: "Reading the
        internal temperature of the Dynamixel actuator with an ID of 1"
        (p.20).

        This test requires to be connected to the Dynamixel number 1 using
        port "/dev/ttyUSB0" at 57600 baud (thus it only works on Unix systems
        with FTDI devices)."""

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
            serial_connection.send(instruction_packet)
        except (TypeError, ValueError, StatusPacketError):
            self.fail("Encountered an unexpected exception.")



if __name__ == '__main__':
    unittest.main()


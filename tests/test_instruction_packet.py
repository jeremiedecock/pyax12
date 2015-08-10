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
This module contains unit tests for the "InstructionPacket" class.
"""

import pyax12.packet as pk
import pyax12.instruction_packet as ip

import unittest

class TestInstructionPacket(unittest.TestCase):
    """
    Contains unit tests for the "InstructionPacket" class.
    """

    def test_wrong_id_type_float(self):
        """Check that ip.InstructionPacket fails when the "dynamixel_id" argument's type
        is wrong (float)."""

        dynamixel_id = 1.0   # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_id_value_hi(self):
        """Check that ip.InstructionPacket fails when the "dynamixel_id" argument's
        value is wrong (too high value)."""

        dynamixel_id = 1000  # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_id_value_negative(self):
        """Check that ip.InstructionPacket fails when the "dynamixel_id" argument's
        value is wrong (negative value)."""

        dynamixel_id = -1    # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

    ###

    def test_wrong_instruction_type_float(self):
        """Check that ip.InstructionPacket fails when the "instruction"
        argument's type is wrong (float)."""

        dynamixel_id = 1
        instruction = 1.0    # wrong instruction
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_instruction_value(self):
        """Check that ip.InstructionPacket fails when the "instruction"
        argument's value is wrong."""

        dynamixel_id = 1
        instruction = 1000   # wrong instruction
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

    ###

    def test_wrong_params_type_int(self):
        """Check that ip.InstructionPacket fails when the "parameters"
        argument's type is wrong (int)."""

        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = 0x00                                 # wrong value

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_params_items_type_float(self):
        """Check that ip.InstructionPacket fails when the "parameters" items
        argument's type is wrong (float)."""

        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 1.0)       # wrong value

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_params_value(self):
        """Check that ip.InstructionPacket fails when the "parameters" items
        argument's value is wrong (too high value)."""

        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0xffff)     # wrong value

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

    ###

    def test_wrong_num_params_ping_hi(self):
        """Check that ip.InstructionPacket fails when the number of paramaters
        is wrong (greater than 0 for the PING instruction)."""

        dynamixel_id = 1
        instruction = ip.PING
        params = (0x00, )                             # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_hi(self):
        """Check that ip.InstructionPacket fails when the number of paramaters
        is wrong (too high)."""

        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01, 0x00) # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_low(self):
        """Check that ip.InstructionPacket fails when the number of paramaters
        is wrong (too low)."""

        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, )           # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

    ###

    def test_example1(self):
        """Check the example 1 from the Dynamixel user guide: "Setting the ID
        of a connected Dynamixel actuator to 1" (p.20)."""

        dxl_id = pk.BROADCAST_ID
        instruction = ip.WRITE_DATA
        params = (pk.ID, 1)

        instruction_packet = ip.InstructionPacket(dxl_id, instruction, params)

        expected_str = "ff ff fe 04 03 03 01 f6"
        self.assertEqual(instruction_packet.to_printable_string(), expected_str)


    def test_example2(self):
        """Check the example 2 from the Dynamixel user guide: "Reading the
        internal temperature of the Dynamixel actuator with an ID of 1"
        (p.20)."""

        dxl_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 1)

        instruction_packet = ip.InstructionPacket(dxl_id, instruction, params)

        expected_str = "ff ff 01 04 02 2b 01 cc"
        self.assertEqual(instruction_packet.to_printable_string(), expected_str)


    def test_example3(self):
        """Check the example 3 from the Dynamixel user guide: "Obtaining the
        status packet of the Dynamixel actuator with an ID of 1" (p.22) i.e.
        PING the Dynamixel #1."""

        dxl_id = 1
        instruction = ip.PING
        params = ()

        instruction_packet = ip.InstructionPacket(dxl_id, instruction, params)

        expected_str = "ff ff 01 02 01 fb"
        self.assertEqual(instruction_packet.to_printable_string(), expected_str)


if __name__ == '__main__':
    unittest.main()


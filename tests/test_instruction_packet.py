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

    # Test the "dynamixel_id" argument ########################################

    def test_wrong_id_type(self):
        """Check that the instanciation of InstructionPacket fails when the
        argument "dynamixel_id" has a wrong type."""

        # Check with None
        dynamixel_id = None       # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with float
        dynamixel_id = 1.0        # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with string
        dynamixel_id = "hi"       # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with tuple
        dynamixel_id = ()         # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_id_value(self):
        """Check that the instanciation of InstructionPacket fails when the
        argument "dynamixel_id" has a wrong value (too low or too high)."""

        # Too high
        dynamixel_id = 0xff  # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Too low
        dynamixel_id = -1    # wrong id
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


#    # TODO: should it be considered as an actual error or can it be neglected?
#    def test_wrong_id_value_sync_write(self):
#        """Check that the instanciation of InstructionPacket fails when the
#        argument "dynamixel_id" has a wrong value (the SYNC_WRITE
#        instruction expects the broadcast id)."""
#
#        dynamixel_id = 1                  # wrong id (must be 0xfe)
#        instruction = ip.SYNC_WRITE
#        params = (pk.LED, 1, 1, 1)
#
#        with self.assertRaises(ValueError):
#            ip.InstructionPacket(dynamixel_id, instruction, params)

    # Test the "instruction" argument #########################################

    def test_wrong_instruction_type(self):
        """Check that the instanciation of InstructionPacket fails when the
        argument "instruction" has a wrong type."""

        # Check with None
        dynamixel_id = 1
        instruction = None   # wrong instruction
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with float
        dynamixel_id = 1
        instruction = 1.0    # wrong instruction
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with string
        dynamixel_id = 1
        instruction = "hi"   # wrong instruction
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with tuple
        dynamixel_id = 1
        instruction = ()     # wrong instruction
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_instruction_value(self):
        """Check that the instanciation of InstructionPacket fails when the
        argument "instruction" has a wrong value."""

        dynamixel_id = 1
        instruction = 1000   # wrong instruction
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

    # Test the "parameters" argument ##########################################

    def test_wrong_params_type(self):
        """Check that the instanciation of InstructionPacket fails when the
        argument "parameters" has a wrong type."""

        # Check with a float.
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = 1.0                                  # wrong type

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with a string.
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = "hello world"                        # wrong type

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with an integer.
        # There is no instruction which take only one parameter (some take 0
        # parameters, some take 2 or more parameters but none take 1
        # parameter).
        dynamixel_id = 1
        instruction = ip.PING
        params = 1

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_good_params_type(self):
        """Check that the instanciation of InstructionPacket doesn't fail when
        the argument "parameters" has a right type."""

        # Check with None (some instructions like "PING" doesn't take any
        # parameter)
        dynamixel_id = 1
        instruction = ip.PING
        params = None                                 # wrong type

        try:
            ip.InstructionPacket(dynamixel_id, instruction, params)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")

        # Check with a tuple
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01)

        try:
            ip.InstructionPacket(dynamixel_id, instruction, params)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")

        # Check with a list
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = [pk.PRESENT_TEMPERATURE, 0x01]

        try:
            ip.InstructionPacket(dynamixel_id, instruction, params)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")

        # Check with a bytes string
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = bytes((pk.PRESENT_TEMPERATURE, 0x01))

        try:
            ip.InstructionPacket(dynamixel_id, instruction, params)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")

        # Check with a bytearray
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = bytearray((pk.PRESENT_TEMPERATURE, 0x01))

        try:
            ip.InstructionPacket(dynamixel_id, instruction, params)
        except (TypeError, ValueError):
            self.fail("Encountered an unexpected exception.")


    def test_wrong_params_items_type(self):
        """Check that the instanciation of InstructionPacket fails when the
        "parameters" items type is wrong."""

        # Check with None
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, None)      # wrong value

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with float
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 1.0)       # wrong value

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with string
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, "hi")      # wrong value

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Check with tuple
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, ())        # wrong value

        with self.assertRaises(TypeError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_params_items_value(self):
        """Check that the instanciation of InstructionPacket fails when the
        "parameters" items type is value."""

        # Too high value
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0xffff)     # wrong value

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Too low value
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, -1)         # wrong value

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_ping(self):
        """Check that the instanciation of InstructionPacket fails when the
        number of paramaters is wrong (greater than 0 for the PING
        instruction)."""

        # Too high
        dynamixel_id = 1
        instruction = ip.PING
        params = (0x00, )                             # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_read(self):
        """Check that the instanciation of InstructionPacket fails when the
        number of paramaters is wrong (for the READ_DATA instruction)."""

        # Too high
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, 0x01, 0x00) # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Too low
        dynamixel_id = 1
        instruction = ip.READ_DATA
        params = (pk.PRESENT_TEMPERATURE, )           # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_write(self):
        """Check that the instanciation of InstructionPacket fails when the
        number of paramaters is wrong (for the WRITE_DATA instruction)."""

        # Too low
        dynamixel_id = 1
        instruction = ip.WRITE_DATA
        params = (pk.LED, )                           # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_reg_write(self):
        """Check that the instanciation of InstructionPacket fails when the
        number of paramaters is wrong (for the REG_WRITE instruction)."""

        # Too low
        dynamixel_id = 1
        instruction = ip.REG_WRITE
        params = (pk.LED, )                           # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_action(self):
        """Check that the instanciation of InstructionPacket fails when the
        number of paramaters is wrong (greater than 0 for the ACTION
        instruction)."""

        # Too high
        dynamixel_id = 1
        instruction = ip.ACTION
        params = (0x00, )                             # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_reset(self):
        """Check that the instanciation of InstructionPacket fails when the
        number of paramaters is wrong (greater than 0 for the RESET
        instruction)."""

        # Too high
        dynamixel_id = 1
        instruction = ip.RESET
        params = (0x00, )                             # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)


    def test_wrong_num_params_sync_write(self):
        """Check that the instanciation of InstructionPacket fails when the
        number of paramaters is wrong (for the SYNC_WRITE instruction)."""

        # Too low (1)
        dynamixel_id = 0xfe
        instruction = ip.SYNC_WRITE
        params = (pk.LED, )                           # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Too low (2)
        dynamixel_id = 0xfe
        instruction = ip.SYNC_WRITE
        params = (pk.LED, 1)                          # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

        # Too low (3)
        dynamixel_id = 0xfe
        instruction = ip.SYNC_WRITE
        params = (pk.LED, 1, 1)                       # wrong nb of params

        with self.assertRaises(ValueError):
            ip.InstructionPacket(dynamixel_id, instruction, params)

    # Full examples ###########################################################

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


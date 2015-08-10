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
This module contain the "InstructionPacket" class which implements "instruction
packet" (the packets sent by the controller to the Dynamixel actuators to send
commands).
"""

__all__ = ['InstructionPacket']

import pyax12.packet as pk
from pyax12 import utils

# THE INSTRUCTION SET
# (see the official Dynamixel AX-12 User's manual p.19)

PING = 0x01
READ_DATA = 0x02
WRITE_DATA = 0x03
REG_WRITE = 0x04
ACTION = 0x05
RESET = 0x06
SYNC_WRITE = 0x83

INSTRUCTIONS = (PING, READ_DATA, WRITE_DATA, REG_WRITE, ACTION, RESET,
                SYNC_WRITE)

# THE NUMBER OF PARAMETERS EXPECTED FOR EACH INSTRUCTION
# (see the official Dynamixel AX-12 User's manual p.19)

MAX_NUM_PARAMS = 255 - 6 # TODO: what is the actual max value ?

NUMBER_OF_PARAMETERS = {
    PING:{
        'min': 0,
        'max': 0
    },
    READ_DATA:{
        'min': 2,
        'max': 2
    },
    WRITE_DATA:{
        'min': 2,
        'max': MAX_NUM_PARAMS
    },
    REG_WRITE:{
        'min': 2,
        'max': MAX_NUM_PARAMS
    },
    ACTION:{
        'min': 0,
        'max': 0
    },
    RESET:{
        'min': 0,
        'max': 0
    },
    SYNC_WRITE:{
        'min': 4,
        'max': MAX_NUM_PARAMS
    }
}


# THE IMPLEMENTATION OF "INSTRUCTION PACKETS"

class InstructionPacket(pk.Packet):
    """The Instruction Packet is the packet sent by the main controller to the
    Dynamixel units to send commands.

    The structure of the Instruction Packet is as the following:

    +----+----+--+------+-----------+----------+---+-----------+---------+
    |0XFF|0XFF|ID|LENGTH|INSTRUCTION|PARAMETER1|...|PARAMETER N|CHECK SUM|
    +----+----+--+------+-----------+----------+---+-----------+---------+

    Read only properties:
    dynamixel_id -- the unique ID of a Dynamixel unit (from 0x00 to 0xFD),
                    0xFE is a broadcasting ID.
    instruction -- the instruction for the Dynamixel actuator to perform.
    parameters -- a tuple of bytes used if there is additional information
                  needed to be sent other than the instruction itself.
    data -- a sequence of byte defining the packet's instruction and its
            parameters.
    checksum -- the packet checksum, used to prevent packet transmission error.
    """

    def __init__(self, dynamixel_id, instruction, parameters):
        """Create an instruction packet.

        Keyword arguments:
        dynamixel_id -- the the unique ID of the Dynamixel unit which have to
                        execute this instruction packet.
        instruction -- the instruction for the Dynamixel actuator to perform.
        parameters -- a sequence of bytes used if there is additional
                      information needed to be sent other than the instruction
                      itself.
        """

        # Add the header bytes.
        self._bytes = bytearray((0xff, 0xff))

        # Check and add the Dynamixel ID byte.
        # "TypeError" and "ValueError" are raised by the "bytearray.append()"
        # if necessary.
        if 0x00 <= dynamixel_id <= 0xfe:
            self._bytes.append(dynamixel_id)
        else:
            msg = "Wrong dynamixel_id: {:#x} (should be in range(0x00, 0xfe))."
            raise ValueError(msg.format(dynamixel_id))

        # Add the length byte.
        self._bytes.append(len(parameters) + 2)

        # Check and add the instruction byte.
        # "TypeError" and "ValueError" are raised by the "bytearray.append()"
        # if necessary.
        if instruction in INSTRUCTIONS:
            self._bytes.append(instruction)
        else:
            msg = "Wrong instruction, should be in ({})."
            raise ValueError(msg.format(utils.pretty_hex_str(INSTRUCTIONS)))

        # Check and add the parameter bytes.
        # "TypeError" and "ValueError" are raised by the "bytearray.append()"
        # or "bytearray.extend()" if necessary.
        if isinstance(parameters, int):
            parameters = bytes((parameters, )) # convert integers to a sequence
        else:
            parameters = bytes(parameters)

        nb_param_min = NUMBER_OF_PARAMETERS[self.instruction]['min']
        nb_param_max = NUMBER_OF_PARAMETERS[self.instruction]['max']

        if nb_param_min <= len(parameters) <= nb_param_max:
            self._bytes.extend(parameters)
        else:
            msg = "Wrong number of parameters: {} parameters"
            msg += " (min expected={}; max expected={})."
            nb_param = len(parameters)
            raise ValueError(msg.format(nb_param, nb_param_min, nb_param_max))

        # Add the checksum byte.
        computed_checksum = pk.compute_checksum(self._bytes[2:])
        self._bytes.append(computed_checksum)


    # READ ONLY PROPERTIES

    @property
    def instruction(self):
        """The instruction for the Dynamixel actuator to perform."""
        return self._bytes[4]


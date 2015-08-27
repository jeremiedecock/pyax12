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
This module contain the `InstructionPacket` class which implements "instruction
packets" (the packets sent by the controller to the Dynamixel actuators to send
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
    """The "instruction packet" is the packet sent by the main controller to
    the Dynamixel units to send commands.

    The structure of the instruction packet is as the following:

    +----+----+--+------+-----------+----------+---+-----------+---------+
    |0XFF|0XFF|ID|LENGTH|INSTRUCTION|PARAMETER1|...|PARAMETER N|CHECK SUM|
    +----+----+--+------+-----------+----------+---+-----------+---------+

    :param int dynamixel_id: the the unique ID of the Dynamixel unit which
        have to execute this instruction packet.
    :param int instruction: the instruction for the Dynamixel actuator to
        perform.
    :param bytes parameters: a sequence of bytes used if there is
        additional information needed to be sent other than the instruction
        itself.
    """

    def __init__(self, dynamixel_id, instruction, parameters=None):

        # Check the parameters byte.
        # "TypeError" and "ValueError" are raised by the "bytes" constructor if
        # necessary.
        # The statement "tuple(parameters)" implicitely rejects integers (and
        # all non-iterable objects) to compensate the fact that the bytes
        # constructor doesn't reject them: bytes(3) is valid and returns
        # b'\x00\x00\x00'.
        if parameters is None:
            parameters = bytes()
        else:
            parameters = bytes(tuple(parameters))

        # Add the header bytes.
        self._bytes = bytearray((0xff, 0xff))

        # Check and add the Dynamixel ID byte.
        # "TypeError" and "ValueError" are raised by the "bytearray.append()"
        # if necessary.
        if 0x00 <= dynamixel_id <= 0xfe:
            self._bytes.append(dynamixel_id)
        else:
            if isinstance(dynamixel_id, int):
                msg = ("Wrong dynamixel_id value, "
                       "an integer in range(0x00, 0xfe) is required.")
                raise ValueError(msg)
            else:
                raise TypeError("Wrong dynamixel_id type (integer required).")

        # Add the length byte.
        self._bytes.append(len(parameters) + 2)

        # Check and add the instruction byte.
        # "TypeError" and "ValueError" are raised by the "bytearray.append()"
        # if necessary.
        if instruction in INSTRUCTIONS:
            self._bytes.append(instruction)
        else:
            if isinstance(instruction, int):
                msg = "Wrong instruction, should be in ({})."
                instructions_str = utils.pretty_hex_str(INSTRUCTIONS)
                raise ValueError(msg.format(instructions_str))
            else:
                raise TypeError("Wrong instruction type (integer required).")

        # Check and add the parameter bytes.
        nb_param_min = NUMBER_OF_PARAMETERS[self.instruction]['min']
        nb_param_max = NUMBER_OF_PARAMETERS[self.instruction]['max']

        if nb_param_min <= len(parameters) <= nb_param_max:
            self._bytes.extend(parameters)
        else:
            msg = ("Wrong number of parameters: {} parameters "
                   "(min expected={}; max expected={}).")
            nb_param = len(parameters)
            raise ValueError(msg.format(nb_param, nb_param_min, nb_param_max))

        # Add the checksum byte.
        computed_checksum = pk.compute_checksum(self._bytes[2:])
        self._bytes.append(computed_checksum)


    # READ ONLY PROPERTIES

    @property
    def instruction(self):
        """The instruction for the Dynamixel actuator to perform.

        This member is a read-only property.
        """
        return self._bytes[4]


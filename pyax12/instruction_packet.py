# -*- coding : utf-8 -*-

# PyAX12

# Copyright (c) 2010,2015 Jeremie Decock (http://www.jdhp.org)

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
This module contain the "InstructionPacket" class which implements "instruction
packet" (the packets sent by the controller to the Dynamixel actuators to send
commands).
"""

__all__ = ['InstructionPacket']

from pyax12.packet import Packet
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
    PING:{'min': 0, 'max': 0},
    READ_DATA:{'min': 2, 'max': 2},
    WRITE_DATA:{'min': 2, 'max': MAX_NUM_PARAMS},
    REG_WRITE:{'min': 2, 'max': MAX_NUM_PARAMS},
    ACTION:{'min': 0, 'max': 0},
    RESET:{'min': 0, 'max': 0},
    SYNC_WRITE:{'min': 4, 'max': MAX_NUM_PARAMS}
}


# THE IMPLEMENTATION OF "INSTRUCTION PACKETS"

class InstructionPacket(Packet):
    """The Instruction Packet is the packet sent by the main controller to the
    Dynamixel units to send commands.

    The structure of the Instruction Packet is as the following:

    +----+----+--+------+-----------+----------+---+-----------+---------+
    |0XFF|0XFF|ID|LENGTH|INSTRUCTION|PARAMETER1|...|PARAMETER N|CHECK SUM|
    +----+----+--+------+-----------+----------+---+-----------+---------+

    Instance variable:
    dynamixel_id -- the unique ID of a Dynamixel unit (from 0x00 to 0xFD),
                    0xFE is a broadcasting ID;
    instruction -- the instruction for the Dynamixel actuator to perform;
    parameters -- a tuple of bytes used if there is additional information
                  needed to be sent other than the instruction itself.
    """

    def __init__(self, _id=None, _instruction=None, _parameters=()):
        """Create an instruction packet.

        Keyword arguments:
        _id -- the the unique ID of the Dynamixel unit which have to execute
               this instruction packet.
        _instruction -- the instruction for the Dynamixel actuator to perform.
        _parameters -- a tuple of bytes used if there is additional information
                       needed to be sent other than the instruction itself."""

        # Check arguments type to make exception messages more explicit
        if not isinstance(_id, int):
            msg = "Wrong dynamixel_id type: {} (an integer is required)."
            raise TypeError(msg.format(type(_id)))

        if not isinstance(_instruction, int):
            msg = "Wrong instruction type: {} (an integer is required)."
            raise TypeError(msg.format(type(_instruction)))

        for parameter in _parameters:
            if not isinstance(parameter, int):
                msg = "Wrong parameter type: {} (an integer is required)."
                raise TypeError(msg.format(type(parameter)))


        # Check the ID byte
        if 0x00 <= _id <= 0xfe:
            self.dynamixel_id = _id
        else:
            msg = "Wrong dynamixel_id: {:#x} (should be in range(0x00, 0xfe))."
            raise ValueError(msg.format(_id))

        # Check the instruction byte
        if _instruction in INSTRUCTIONS:
            self.instruction = _instruction
        else:
            msg = "Wrong instruction: {:#x} (should be in ({}))."
            instructions_str = utils.int_seq_to_hex_str(INSTRUCTIONS)
            raise ValueError(msg.format(_instruction, instructions_str))

        # Check the number of parameters and parameters value
        nb_param_min = NUMBER_OF_PARAMETERS[self.instruction]['min']
        nb_param_max = NUMBER_OF_PARAMETERS[self.instruction]['max']
        if nb_param_min <= len(_parameters) <= nb_param_max:
            if all([0x00 <= param <= 0xff for param in _parameters]):
                self.parameters = _parameters
            else:
                msg = "Wrong parameters value: ({})"
                msg += " (an integer in range(0x00, 0xff) is required)."
                params_str = utils.int_seq_to_hex_str(_parameters)
                raise ValueError(msg.format(params_str))
        else:
            msg = "Wrong number of parameters: {} parameters"
            msg += " (min expected={}; max expected={})."
            nb_param = len(_parameters)
            raise ValueError(msg.format(nb_param, nb_param_min, nb_param_max))

        self.data = (self.instruction, ) + self.parameters


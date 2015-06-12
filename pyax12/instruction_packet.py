# -*- coding : utf-8 -*-

# PyAX12

# Copyright (c) 2010 Jeremie Decock (http://www.jdhp.org)

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

from pyax12.packet import Packet
import warnings
import sys

PING = 0x01
READ_DATA = 0x02
WRITE_DATA = 0x03
REG_WRITE = 0x04
ACTION = 0x05
RESET = 0x06
SYNC_WRITE = 0x83

INSTRUCTIONS = (PING, READ_DATA, WRITE_DATA, REG_WRITE, ACTION, RESET,
                SYNC_WRITE)

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
        """Create an instruction packet."""

        # Check the ID byte
        if 0x00 <= _id <= 0xfe:
            self.dynamixel_id = _id
        else:
            warnings.warn('Wrong dynamixel_id')

        # Check the instruction byte
        if _instruction in INSTRUCTIONS:
            self.instruction = _instruction
        else:
            warnings.warn('Wrong instruction')

        # Check the number of parameters
        num_param_min = NUMBER_OF_PARAMETERS[self.instruction]['min']
        num_param_max = NUMBER_OF_PARAMETERS[self.instruction]['max']
        if num_param_min <= len(_parameters) <= num_param_max:
            self.parameters = _parameters
        else:
            warnings.warn('Wrong number of parameters')

        self.data = (self.instruction, ) + self.parameters


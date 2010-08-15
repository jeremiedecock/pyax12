# -*- coding : utf-8 -*-

# PyDynamixel

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

from pydynamixel.packet import Packet
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

NUMBER_OF_PARAMETERS = {
                        PING:{'min':0, 'max':0},
                        READ_DATA:{'min':2, 'max':2},
                        WRITE_DATA:{'min':2, 'max':sys.maxint},
                        REG_WRITE:{'min':2, 'max':sys.maxint},
                        ACTION:{'min':0, 'max':0},
                        RESET:{'min':0, 'max':0},
                        SYNC_WRITE:{'min':4, 'max':sys.maxint}
                       }

class InstructionPacket(Packet):

    id = 0x00
    instruction = 0x00
    parameters = ()

    def __init__(self, id=None, instruction=None, parameters=None):
        # Assert id
        if 0x00 <= id <= 0xfe:
            self.id = id
        else:
            warnings.warn('Wrong id')

        # Assert instruction
        if instruction in INSTRUCTIONS:
            self.instruction = instruction
        else:
            warnings.warn('Wrong instruction')

        # Assert number of parameters
        num_param_min = NUMBER_OF_PARAMETERS[instruction]['min']
        num_param_max = NUMBER_OF_PARAMETERS[instruction]['max']
        if num_param_min <= len(parameters) <= num_param_max:
            self.parameters = parameters
        else:
            warnings.warn('Wrong number of parameters')

        self.data = (instruction, ) + parameters


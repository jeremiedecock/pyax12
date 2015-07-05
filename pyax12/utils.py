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

import pyax12.packet as pk
import pyax12.instruction_packet as ip

def int_to_little_endian_hex_tuple(val):
    """Convert a two-bytes integer into a pair of one-byte integers using
    the little-endian notation (i.e. the less significant byte first).

    The "val" input must be a 2 bytes integer (i.e. val must be greater or
    equal to 0 and less or equal to 1024).

    For instance, with the input decimal value val=700 (0x02bc in hexadecimal
    notation) this function will return the tuple (0xbc, 0x02).
    """
    assert 0 <= val <= 1024
    hex_string = '%04x' % val
    hex_tuple = (int(hex_string[2:4], 16), int(hex_string[0:2], 16))
    return hex_tuple


def read_control_table(serial_connection, dynamixel_id, address, length):
    instruction_packet = ip.InstructionPacket(_id=dynamixel_id, _instruction=ip.READ_DATA, _parameters=(address, length))

    status_packet = serial_connection.send(instruction_packet)

    value_tuple = None
    if status_packet is not None:
        value_tuple = status_packet.parameters

    return value_tuple


def write_control_table(serial_connection, dynamixel_id, address, value_tuple):
    instruction_packet = ip.InstructionPacket(_id=dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(address, ) + value_tuple)

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        pass
        # TODO warning


def dump(serial_connection, dynamixel_id):
    pass


def scan(serial_connection, id_tuple):

    for dynamixel_id in id_tuple:
        if 0 <= dynamixel_id <= 254:
            instruction_packet = ip.InstructionPacket(_id=dynamixel_id, _instruction=ip.PING)

            status_packet = serial_connection.send(instruction_packet)

            value_tuple = None
            if status_packet is not None:
                value_tuple = status_packet.parameters
                # TODO check errors and print available IDs
        else:
            pass # TODO exception


def reset(serial_connection, dynamixel_id):
    pass

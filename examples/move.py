#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pydynamixel.packet as pk
import pydynamixel.connection
import pydynamixel.instruction_packet as ip

import time

def main():
    serial_connection = pydynamixel.connection.Connection()

    # Goto to 180°

    instruction_packet = ip.InstructionPacket(_id=pk.BROADCAST_ID, _instruction=ip.WRITE_DATA, _parameters=(pk.GOAL_POSITION, 0x00, 0x02, 0x00, 0x02))
    print('> ', instruction_packet.to_printable_string())

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        print('< ', status_packet.to_printable_string())

    # Wait 2 seconds

    time.sleep(1)

    # Go back to 0

    instruction_packet = ip.InstructionPacket(_id=pk.BROADCAST_ID, _instruction=ip.WRITE_DATA, _parameters=(pk.GOAL_POSITION, 0x00, 0x00, 0x00, 0x02))
    print('> ', instruction_packet.to_printable_string())

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        print('< ', status_packet.to_printable_string())

if __name__ == '__main__':
    main()

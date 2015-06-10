#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pydynamixel.packet as pk
import pydynamixel.connection
import pydynamixel.instruction_packet as ip

import time

def main():
    serial_connection = pydynamixel.connection.Connection()

    # Switch ON the LED

    #instruction_packet = ip.InstructionPacket(_id=pk.BROADCAST_ID, _instruction=ip.WRITE_DATA, _parameters=(pk.LED, 1))
    instruction_packet = ip.InstructionPacket(_id=0x02, _instruction=ip.WRITE_DATA, _parameters=(pk.LED, 1))
    print('> ', instruction_packet.to_printable_string())

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        print('< ', status_packet.to_printable_string())

    # Wait 2 seconds

    time.sleep(2)

    # Switch OFF the LED

    instruction_packet = ip.InstructionPacket(_id=pk.BROADCAST_ID, _instruction=ip.WRITE_DATA, _parameters=(pk.LED, 0))
    print('> ', instruction_packet.to_printable_string())

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        print('< ', status_packet.to_printable_string())

if __name__ == '__main__':
    main()

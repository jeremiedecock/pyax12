#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pydynamixel.packet as pk
import pydynamixel.connection
import pydynamixel.instruction_packet as ip

import argparse
import time

def main():

    # PARSE OPTIONS

    parser = argparse.ArgumentParser(description='A PyAX-12 demo.')

    parser.add_argument("--dynamixel_id", "-i",  help="The unique ID of a Dynamixel unit to work with (254 is a broadcasting ID)", metavar="INTEGER", type=int, default=pk.BROADCAST_ID)
    parser.add_argument("--baudrate", "-b",  help="The baudrate speed (e.g. 57600)", metavar="INTEGER", type=int, default=57600)
    parser.add_argument("--timeout", "-t",  help="The timeout value for the connection", metavar="FLOAT", type=float, default=0.1)
    parser.add_argument("--port", "-p",  help="The serial device to connect with (e.g. '/dev/ttyUSB0' for Unix users)", metavar="STRING", default="/dev/ttyUSB0")
    args = parser.parse_args()

    # CONNECT TO THE SERIAL PORT

    serial_connection = pydynamixel.connection.Connection(_port=args.port, _baudrate=args.baudrate, _timeout=args.timeout)

    # GOTO TO 180°

    instruction_packet = ip.InstructionPacket(_id=args.dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(pk.GOAL_POSITION, 0x00, 0x02, 0x00, 0x02))
    print('> ', instruction_packet.to_printable_string())

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        print('< ', status_packet.to_printable_string())

    # WAIT 2 SECONDS

    time.sleep(1)

    # GO BACK TO 0°

    instruction_packet = ip.InstructionPacket(_id=args.dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(pk.GOAL_POSITION, 0x00, 0x00, 0x00, 0x02))
    print('> ', instruction_packet.to_printable_string())

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        print('< ', status_packet.to_printable_string())

if __name__ == '__main__':
    main()

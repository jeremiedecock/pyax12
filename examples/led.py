#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import pyax12.packet as pk
import pyax12.connection
import pyax12.instruction_packet as ip

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

    serial_connection = pyax12.connection.Connection(_port=args.port, _baudrate=args.baudrate, _timeout=args.timeout)

    # SWITCH ON THE LED

    instruction_packet = ip.InstructionPacket(_id=args.dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(pk.LED, 1))
    print('> ', instruction_packet.to_printable_string())

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        print('< ', status_packet.to_printable_string())

    # WAIT 2 SECONDS

    time.sleep(2)

    # SWITCH OFF THE LED

    instruction_packet = ip.InstructionPacket(_id=args.dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(pk.LED, 0))
    print('> ', instruction_packet.to_printable_string())

    status_packet = serial_connection.send(instruction_packet)

    if status_packet is not None:
        print('< ', status_packet.to_printable_string())

if __name__ == '__main__':
    main()

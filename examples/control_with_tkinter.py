#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
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

import tkinter as tk

def int_to_hex_tuple(val):
    s = '%04x' % val
    t = (int(s[2:4], 16), int(s[0:2], 16))
    return t

def main():

    # PARSE OPTIONS

    parser = argparse.ArgumentParser(description='A PyAX-12 demo.')

    parser.add_argument("--dynamixel_id", "-i",  help="The unique ID of a Dynamixel unit to work with (254 is a broadcasting ID)", metavar="INTEGER", type=int, default=pk.BROADCAST_ID)
    parser.add_argument("--baudrate", "-b",  help="The baudrate speed (e.g. 57600)", metavar="INTEGER", type=int, default=57600)
    parser.add_argument("--timeout", "-t",  help="The timeout value for the connection (in seconds)", metavar="FLOAT", type=float, default=0.1)
    parser.add_argument("--port", "-p",  help="The serial device to connect with (e.g. '/dev/ttyUSB0' for Unix users)", metavar="STRING", default="/dev/ttyUSB0")
    args = parser.parse_args()

    # CONNECT TO THE SERIAL PORT

    serial_connection = pyax12.connection.Connection(_port=args.port, _baudrate=args.baudrate, _timeout=args.timeout)

    # TKINTER GUI

    root = tk.Tk()
    root.geometry("150x500")   # Set the size of the "root" window

    ###

    def scale_cb(ev=None):
        position = position_scale.get()    # Get the scale value (integer or float)
        position_byte_tuple = int_to_hex_tuple(position)

        speed = speed_scale.get()    # Get the scale value (integer or float)
        speed_byte_tuple = int_to_hex_tuple(speed)

        instruction_packet = ip.InstructionPacket(_id=args.dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(pk.GOAL_POSITION, position_byte_tuple[0], position_byte_tuple[1], speed_byte_tuple[0], speed_byte_tuple[1]))
        status_packet = serial_connection.send(instruction_packet)

    position_scale = tk.Scale(root, from_=0, to=1024, orient=tk.VERTICAL, command=scale_cb)  # Arguments "orient" and "command" are optional
    position_scale.pack(fill=tk.Y, expand=1, side=tk.LEFT)

    speed_scale = tk.Scale(root, from_=0, to=1024, orient=tk.VERTICAL, command=scale_cb)  # Arguments "orient" and "command" are optional
    speed_scale.pack(fill=tk.Y, expand=1, side=tk.RIGHT)

    position_scale.set(512)         # Set the scale value
    speed_scale.set(512)            # Set the scale value

    ###

    root.mainloop()

if __name__ == '__main__':
    main()

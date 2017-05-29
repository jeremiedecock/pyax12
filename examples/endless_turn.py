#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PyAX-12

# The MIT License
#
# Copyright (c) 2010,2015,2017 Jeremie DECOCK (http://www.jdhp.org)
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
A PyAX-12 demo.
"""

from pyax12.connection import Connection
from pyax12.argparse_default import common_argument_parser
import pyax12.packet as pk

import time

def main():
    """
    This is an *endless turn mode* demo.

    If both values for the *CW angle limit* and *CCW angle limit* are set to 0,
    an *endless turn mode* can be implemented by setting the *goal speed*.
    This feature can be used for implementing a continuously rotating wheel.
    """

    # Parse options
    parser = common_argument_parser(desc=main.__doc__)
    args = parser.parse_args()

    # Connect to the serial port
    serial_connection = Connection(port=args.port,
                                   baudrate=args.baudrate,
                                   timeout=args.timeout,
                                   rpi_gpio=args.rpi)

    dynamixel_id = args.dynamixel_id

    # Set the "wheel mode"
    serial_connection.set_cw_angle_limit(dynamixel_id, 0, degrees=False)
    serial_connection.set_ccw_angle_limit(dynamixel_id, 0, degrees=False)

    # Activate the actuator (speed=512)
    serial_connection.set_speed(dynamixel_id, 512)

    # Lets the actuator turn 5 seconds
    time.sleep(5)

    # Stop the actuator (speed=0)
    serial_connection.set_speed(dynamixel_id, 0)

    # Leave the "wheel mode"
    serial_connection.set_ccw_angle_limit(dynamixel_id, 1023, degrees=False)

    # Go to the initial position (0 degree)
    serial_connection.goto(dynamixel_id, 0, speed=512, degrees=True)

    # Close the serial connection
    serial_connection.close()

if __name__ == '__main__':
    main()

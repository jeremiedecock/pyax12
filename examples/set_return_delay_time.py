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

DEFAULT_VALUE = 500

def main():
    """
    Set the *return delay time* for the specified Dynamixel unit
    i.e. the time (in microsecond) for the status packets to return after the
    instruction packet is sent.
    """

    # Parse options
    parser = common_argument_parser(desc=main.__doc__)

    parser.add_argument("--return-delay-time",
                        "-r",
                        help="The new return delay time assigned to the "
                             "selected Dynamixel unit. It must be in range "
                             "(0, 500). The default value is {default}µs "
                             "({default} microseconds).".format(default=DEFAULT_VALUE),
                        type=int,
                        metavar="INT",
                        default=DEFAULT_VALUE)

    args = parser.parse_args()

    # Connect to the serial port
    serial_connection = Connection(port=args.port,
                                   baudrate=args.baudrate,
                                   timeout=args.timeout,
                                   rpi_gpio=args.rpi)

    serial_connection.set_return_delay_time(args.dynamixel_id, args.return_delay_time)

    # Close the serial connection
    serial_connection.close()

if __name__ == '__main__':
    main()

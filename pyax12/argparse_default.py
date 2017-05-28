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

"""
Common functions for PyAX-12 demos.
"""

__all__ = ['common_argument_parser']

import argparse

import pyax12.packet as pk


ID_HELP_STR = ("The unique ID of a Dynamixel unit to work with "
               "(254 is a broadcasting ID)")

BAUD_RATE_HELP_STR = "The baud rate speed (e.g. 57600)"

TIMEOUT_HELP_STR = "The timeout value for the connection"

PORT_HELP_STR = ("The serial device to connect with "
                 "(e.g. '/dev/ttyUSB0' for Unix users "
                 "or 'COM1' for Windows users)")

RPI_HELP_STR = "Use Raspberry Pi GPIO to connect Dynamixels"


def common_argument_parser(desc, id_arg=True, id_arg_mandatory=False):
    """Return a preconfigured `argparse` parser instance.

    :param str desc: the global description of the program (printed with -h or
        --help).
    :param bool id_arg: `argparse` ignores the `dynamixel_id` option if
        `id_arg` is ``False`` (`dynamixel_id` is not relevant for some programs
        e.g. examples/scan.py).
    :param bool id_arg_mandatory: the `dynamixel_id` option is mandatory if
        this parameter is ``True``. This parameter is ignored if `id_arg` is
        ``False``.
    """

    # Parse options
    parser = argparse.ArgumentParser(description=desc)

    if id_arg:
        if id_arg_mandatory:
            parser.add_argument("--dynamixel_id",
                                "-i",
                                help=ID_HELP_STR,
                                metavar="INTEGER",
                                type=int,
                                required=True,
                                default=pk.BROADCAST_ID)
        else:
            parser.add_argument("--dynamixel_id",
                                "-i",
                                help=ID_HELP_STR,
                                metavar="INTEGER",
                                type=int,
                                default=pk.BROADCAST_ID)

    parser.add_argument("--baudrate",
                        "-b",
                        help=BAUD_RATE_HELP_STR,
                        metavar="INTEGER",
                        type=int,
                        default=57600)

    parser.add_argument("--timeout",
                        "-t",
                        help=TIMEOUT_HELP_STR,
                        metavar="FLOAT",
                        type=float,
                        default=0.1)

    parser.add_argument("--port",
                        "-p",
                        help=PORT_HELP_STR,
                        metavar="STRING",
                        default="/dev/ttyUSB0")

    parser.add_argument("--rpi",
                        help=RPI_HELP_STR,
                        action="store_true")

    return parser


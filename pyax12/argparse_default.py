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


def common_argument_parser(desc, id_arg=True):
    """Return a preconfigured "argparse" parser instance.

    The "dynamixel_id" argument is ignored if "id_arg" is False."""

    # Parse options
    parser = argparse.ArgumentParser(description=desc)

    if id_arg:
        parser.add_argument("--dynamixel_id", "-i", help="The unique ID of a Dynamixel unit to work with (254 is a broadcasting ID)", metavar="INTEGER", type=int, default=pk.BROADCAST_ID)
    parser.add_argument("--baudrate", "-b", help="The baudrate speed (e.g. 57600)", metavar="INTEGER", type=int, default=57600)
    parser.add_argument("--timeout", "-t", help="The timeout value for the connection", metavar="FLOAT", type=float, default=0.1)
    parser.add_argument("--port", "-p", help="The serial device to connect with (e.g. '/dev/ttyUSB0' for Unix users or 'COM1' for Windows users)", metavar="STRING", default="/dev/ttyUSB0")

    return parser


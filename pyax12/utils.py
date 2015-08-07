# -*- coding : utf-8 -*-

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

"""This module contains some general purpose utility functions."""

__all__ = ['int_to_little_endian_bytes',
           'pretty_hex_str']

def int_to_little_endian_hex_tuple(integer):
    """Deprecated (kept to prevent compatibility issue)."""
    int_to_little_endian_bytes(integer)


def int_to_little_endian_bytes(integer):
    """Convert a two-bytes integer into a pair of one-byte integers using
    the little-endian notation (i.e. the less significant byte first).

    The "integer" input must be a 2 bytes integer (i.e. "integer" must be
    greater or equal to 0 and less or equal to 65535 (0xffff)).

    For instance, with the input decimal value integer=700 (0x02bc in
    hexadecimal notation) this function will return the tuple (0xbc, 0x02).
    """

    # Check argument type to make exception messages more explicit
    if not isinstance(integer, int):
        msg = "An integer in range(0x00, 0xffff) is required (got {})."
        raise TypeError(msg.format(type(integer)))

    # Check the argument value
    if not (0 <= integer <= 0xffff):
        msg = "An integer in range(0x00, 0xffff) is required (got {})."
        raise ValueError(msg.format(integer))

    hex_string = '%04x' % integer
    hex_tuple = (int(hex_string[2:4], 16), int(hex_string[0:2], 16))

    return hex_tuple


def int_seq_to_hex_str(bytes_seq, separator=","):
    """Deprecated (kept to prevent compatibility issue)."""
    pretty_hex_str(bytes_seq, separator)


def pretty_hex_str(bytes_seq, separator=","):
    """Convert a squence of bytes to a string of hexadecimal numbers.

    For instance, with the input tuple (255, 0, 10)
    this function will return the string "ff,00,0a".

    Keyword arguments:
    bytes_seq -- a sequence of bytes to process. It must be compatible with the
                 "bytes" type.
    """

    # Check the argument and convert it to "bytes" if necessary
    if isinstance(bytes_seq, int):
        bytes_seq = bytes((bytes_seq, ))
    else:
        bytes_seq = bytes(bytes_seq)

    return separator.join(['%02x' % byte for byte in bytes_seq])

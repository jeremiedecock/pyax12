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
           'little_endian_bytes_to_int',
           'pretty_hex_str']


def int_to_little_endian_bytes(integer):
    """Converts a two-bytes integer into a pair of one-byte integers using
    the little-endian notation (i.e. the less significant byte first).

    The `integer` input must be a 2 bytes integer, i.e. `integer` must be
    greater or equal to 0 and less or equal to 65535 (0xffff in hexadecimal
    notation).

    For instance, with the input decimal value ``integer=700`` (0x02bc in
    hexadecimal notation) this function will return the tuple ``(0xbc, 0x02)``.

    :param int integer: the 2 bytes integer to be converted. It must be in
        range (0, 0xffff).
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


def little_endian_bytes_to_int(little_endian_byte_seq):
    """Converts a pair of bytes into an integer.

    The `little_endian_byte_seq` input must be a 2 bytes sequence defined
    according to the little-endian notation (i.e. the less significant byte
    first).

    For instance, if the `little_endian_byte_seq` input is equals to
    ``(0xbc, 0x02)`` this function returns the decimal value ``700`` (0x02bc in
    hexadecimal notation).

    :param bytes little_endian_byte_seq: the 2 bytes sequence to be converted.
        It must be compatible with the "bytes" type and defined according to the
        little-endian notation.
    """

    # Check the argument and convert it to "bytes" if necessary.
    # Assert "little_endian_byte_seq" items are in range (0, 0xff).
    # "TypeError" and "ValueError" are sent by the "bytes" constructor if
    # necessary.
    # The statement "tuple(little_endian_byte_seq)" implicitely rejects
    # integers (and all non-iterable objects) to compensate the fact that the
    # bytes constructor doesn't reject them: bytes(2) is valid and returns
    # b'\x00\x00'
    little_endian_byte_seq = bytes(tuple(little_endian_byte_seq))

    # Check that the argument is a sequence of two items
    if len(little_endian_byte_seq) != 2:
        raise ValueError("A sequence of two bytes is required.")

    integer = little_endian_byte_seq[1] * 0x100 + little_endian_byte_seq[0]

    return integer


def pretty_hex_str(byte_seq, separator=","):
    """Converts a squence of bytes to a string of hexadecimal numbers.

    For instance, with the input tuple ``(255, 0, 10)``
    this function will return the string ``"ff,00,0a"``.

    :param bytes byte_seq: a sequence of bytes to process. It must be
        compatible with the "bytes" type.
    :param str separator: the string to be used to separate each byte in the
        returned string (default ",").
    """

    # Check the argument and convert it to "bytes" if necessary.
    # This conversion assert "byte_seq" items are in range (0, 0xff).
    # "TypeError" and "ValueError" are sent by the "bytes" constructor if
    # necessary.
    if isinstance(byte_seq, int):
        byte_seq = bytes((byte_seq, ))
    else:
        byte_seq = bytes(byte_seq)

    return separator.join(['%02x' % byte for byte in byte_seq])

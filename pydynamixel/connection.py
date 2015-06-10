# -*- coding : utf-8 -*-

# PyDynamixel

# Copyright (c) 2010 Jeremie Decock (http://www.jdhp.org)

# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import serial
from pydynamixel.status_packet import StatusPacket

class Connection(object):
    """Create a serial connection with dynamixel actuators."""
    
    def __init__(self, _port='/dev/ttyUSB0', _baudrate=57600, _timeout=0.1):
        """Create a serial connection with dynamixel actuators.

        Instance variable:
        serial_connection -- the serial connection object returned by pyserial;
        port -- the serial device to connect with (e.g. '/dev/ttyUSB0' for Unix users);
        baudrate -- the baudrate speed (e.g. 57600);
        timeout -- the timeout value for the connection.
        """

        self.port = _port
        self.baudrate = _baudrate
        self.timeout = _timeout
        self.serial_connection = serial.Serial(port=self.port,
                                               baudrate=self.baudrate,
                                               timeout=self.timeout,
                                               bytesize=serial.EIGHTBITS,
                                               parity=serial.PARITY_NONE,
                                               stopbits=serial.STOPBITS_ONE)

    def send(self, packet):
        """Send a packet."""

        # Send the packet #################################

        byte_array_instruction = packet.to_byte_array()
        self.serial_connection.write(byte_array_instruction)

        # Receive the reply (status packet) ###############

        #reply = self.serial_connection.read(int(self.baudrate / 8 * self.timeout))
        byte_array_status = self.serial_connection.read(120)
        #print(byte_array_status)

        status_packet = None
        if len(byte_array_status) > 0:
            status_packet = StatusPacket(byte_array_status)

        return status_packet

    def close(self):
        """Close the serial connection."""
        self.serial_connection.close()


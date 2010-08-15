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

class Connection():
    
    serial_connection = None
    port = None
    baudrate = None
    timeout = None

    def __init__(self, port='/dev/ttyUSB0', baudrate=57600, timeout=1):
        "Create a serial connection with dynamixel actuators."
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = serial.Serial(port=port,
                                               baudrate=baudrate,
                                               timeout=timeout,
                                               bytesize=serial.EIGHTBITS,
                                               parity=serial.PARITY_NONE,
                                               stopbits=serial.STOPBITS_ONE)

    def send(self, packet):
        "Send a packet."
        # Send the packet.
        raw_instruction = packet.to_raw_string()
        self.serial_connection.write(raw_instruction)
        print '> ', ' '.join(["%02x" % ord(char) for char in raw_instruction])

        # Receive the reply (status packet)
        #reply = self.serial_connection.read(int(self.baudrate / 8 * self.timeout))
        reply = self.serial_connection.read(120)
        print '< ', ' '.join(["%02x" % ord(char) for char in reply])

    def close(self):
        "Close the serial connection."
        self.serial_connection.close()


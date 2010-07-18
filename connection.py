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
from status_packet import StatusPacket

class Connection():
    
    serial_connection = None
    port = None
    baudrate = None
    timeout = None

    buffer = ''

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
        self.serial_connection.write(packet.to_raw_string())

    def receive(self):
        """Receive a packet.
        
        Return a tuple of status_packets."""
        # TODO
        self.buffer += self.serial_connection.read(self.baudrate * self.timeout)
        print self.buffer
        #packets_string = buffer.split('ffff')[1:]
        #print [StatusPacket(packet) for packet in packets_string]
        #return [StatusPacket(packet) for packet in packets_string]

    def close(self):
        "Close the serial connection."
        self.serial_connection.close()


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

"""
This module contain the "Connection" class communicate with Dynamixel units.
"""

__all__ = ['Connection']

import serial
import time

import pyax12.status_packet as sp
import pyax12.instruction_packet as ip

class Connection(object):
    """Create a serial connection with dynamixel actuators."""

    def __init__(self, _port='/dev/ttyUSB0', _baudrate=57600, _timeout=0.1):
        """Create a serial connection with dynamixel actuators.

        Instance variable:
        serial_connection -- the serial connection object returned by pyserial;
        port -- the serial device to connect with (e.g. '/dev/ttyUSB0' for Unix
                users);
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

    def send(self, instruction_packet):
        """Send an instruction packet.

        Keyword arguments:
        instruction_packet -- can be either a "Packet" instance or a "bytes"
                              string containing the full instruction packet to
                              be sent to Dynamixel units.
        """

        if isinstance(instruction_packet, bytes):
            # instruction_packet is a bytes instance
            instruction_packet_bytes = instruction_packet
        else:
            # instruction_packet is a Packet instance
            instruction_packet_bytes = instruction_packet.to_bytes()

        self.flush()

        # Send the packet #################################

        self.serial_connection.write(instruction_packet_bytes)

        # Receive the reply (status packet) ###############

        # WARNING:
        # If you use the USB2Dynamixel device, make sure its switch is set on
        # "TTL" (otherwise status packets won't be readable).

        time.sleep(0.01) # TODO
        num_bytes_available = self.serial_connection.inWaiting()

        # TODO: not robust...
        status_packet_bytes = self.serial_connection.read(num_bytes_available)

        # TODO: make the reading status more robust. See:
        # - ROS: http://docs.ros.org/diamondback/api/dynamixel_driver/html/dynamixel__io_8py_source.html#l00085
        # - PyDynamixel: https://github.com/richard-clark/PyDynamixel/blob/master/pydynamixel/dynamixel.py#L295
        # - PyPot: https://github.com/poppy-project/pypot/blob/master/pypot/dynamixel/io/abstract_io.py#L503
        status_packet = None
        if len(status_packet_bytes) > 0:
            status_packet = sp.StatusPacket(status_packet_bytes)

        return status_packet


    def close(self):
        """Close the serial connection."""

        # TODO: flush ?
        self.serial_connection.close()


    def flush(self):
        """Flush the connection buffers."""

        self.serial_connection.flushInput()
        #self.serial_connection.flushOutput()  # TODO ?


    ## HIGH LEVEL FUNCTIONS ####################################################

    def read_data(self, dynamixel_id, address, length):
        """Read bytes form the control table of the specified Dynamixel unit.

        Keyword arguments:
        dynamixel_id -- the unique ID of a Dynamixel unit (in range (0, 0xfe)).
        address -- starting address of the location where the data is to be
                   read.
        length -- length of the data to be read.
        """

        instruction = ip.READ_DATA
        params = (address, length)
        inst_packet = ip.InstructionPacket(dynamixel_id, instruction, params)

        status_packet = self.send(inst_packet)

        data_bytes = None
        if status_packet is not None:
            if status_packet.dynamixel_id == dynamixel_id:
                data_bytes = status_packet.parameters
            else:
                pass # TODO: exception ?
        # TODO: manage the special case with dxl_id = 0xFE
        # TODO: manage the special case where length cover multiples items
        # TODO: manage the case where items coded on only one byte are returned

        return data_bytes


    def write_data(self, dynamixel_id, address, data):
        """Write bytes to the control table of the specified Dynamixel unit.

        Keyword arguments:
        dynamixel_id -- the unique ID of a Dynamixel unit (in range (0, 0xfe)).
        address -- starting address of the location where the data is to be
                   written.
        data -- bytes of the data to be written (can be an integer, a sequence
                of integer, a bytes or a bytearray).
        """

        bytes_address = bytes((address, ))

        if isinstance(data, int):
            bytes_to_write = bytes((data, ))
        else:
            bytes_to_write = bytes(data)

        instruction = ip.WRITE_DATA
        params = bytes_address + bytes_to_write
        inst_packet = ip.InstructionPacket(dynamixel_id, instruction, params)

        self.send(inst_packet)


    def ping(self, dynamixel_id):
        """Ping the specified Dynamixel unit.

        Keyword arguments:
        dynamixel_id -- the unique ID of a Dynamixel unit (in range (0, 0xfe)).
        """

        instruction = ip.PING
        inst_packet = ip.InstructionPacket(dynamixel_id, instruction)

        status_packet = self.send(inst_packet)

        is_available = False
        if status_packet is not None:
            if status_packet.dynamixel_id == dynamixel_id:
                is_available = True
            else:
                pass # TODO: exception ?
        # TODO: manage the special case with dxl_id = 0xFE

        return is_available


    #def reset(self, dynamixel_id):
    #
    #    status_packet = self.send(instruction_packet)
    #
    #    if status_packet is not None:
    #        pass
    #        # TODO warning


    ## HIGHEST LEVEL FUNCTIONS #################################################

    #def dump_control_table(self, dynamixel_id):
    #    pass


    #def print_control_table(self, dynamixel_id):
    #    pass


    def scan(self, dynamixel_id_bytes=None):
        """Return the ID sequence of available Dynamixel units.

        Keyword arguments:
        dynamixel_id_bytes -- a sequence of unique ID of the Dynamixel units to
                              be ping.
        """

        available_ids = bytearray()

        if dynamixel_id_bytes is None:
            dynamixel_id_bytes = bytes(range(0xfe)) # bytes in range (0, 0xfd)

        for dynamixel_id in dynamixel_id_bytes:
            if 0 <= dynamixel_id <= 0xfd:
                if self.ping(dynamixel_id):
                    available_ids.append(dynamixel_id)
            else:
                pass # TODO exception

        return available_ids

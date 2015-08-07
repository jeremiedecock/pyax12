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

__all__ = ['Connection']

import serial
import time
from pyax12.status_packet import StatusPacket

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

    def send(self, instruction_packet):
        """Send an instruction packet.
        
        Keyword arguments:
        instruction_packet -- can be either a "Packet" instance or a "bytes"
                  string containing the full instruction packet to be sent to
                  Dynamixel units.
        """

        if isinstance(instruction_packet, bytes):
            instruction_packet_bytes = instruction_packet
        else:
            instruction_packet_bytes = instruction_packet.to_bytes()

        self.flush()

        # Send the packet #################################

        self.serial_connection.write(instruction_packet_bytes)

        # Receive the reply (status packet) ###############
        
        # WARNING:
        # If you use the USB2Dynamixel device, make sure its switch is set on
        # "TTL" (otherwise status packets won't be readable).

        time.sleep(0.01) # TODO
        num_bytes_in_read_buffer = self.serial_connection.inWaiting()

        byte_array_status = self.serial_connection.read(num_bytes_in_read_buffer) # TODO: not robust...

        # TODO: make the reading status more robust. See:
        # - ROS: http://docs.ros.org/diamondback/api/dynamixel_driver/html/dynamixel__io_8py_source.html#l00085
        # - PyDynamixel: https://github.com/richard-clark/PyDynamixel/blob/master/pydynamixel/dynamixel.py#L295
        # - PyPot: https://github.com/poppy-project/pypot/blob/master/pypot/dynamixel/io/abstract_io.py#L503
        status_packet = None
        if len(byte_array_status) > 0:
            status_packet = StatusPacket(byte_array_status)

        return status_packet


    def close(self):
        """Close the serial connection."""
        self.serial_connection.close()


    def flush(self):
        """Close the serial connection."""

        self.serial_connection.flushInput()
        #self.serial_connection.flushOutput()  # TODO ?

    ## HIGH LEVEL FUNCTIONS ####################################################

    #def ping(self, dynamixel_id):
    #    instruction_packet = ip.InstructionPacket(_id=dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(address, ) + value_tuple)
    #
    #    status_packet = serial_connection.send(instruction_packet)
    #
    #    if status_packet is not None:
    #        pass
    #        # TODO warning


    #def read_control_table(self, dynamixel_id, address, length):
    #    instruction_packet = ip.InstructionPacket(_id=dynamixel_id, _instruction=ip.READ_DATA, _parameters=(address, length))
    #
    #    status_packet = serial_connection.send(instruction_packet)
    #
    #    value_tuple = None
    #    if status_packet is not None:
    #        value_tuple = status_packet.parameters
    #
    #    return value_tuple


    #def write_control_table(self, dynamixel_id, address, bytes_to_write):
    #    instruction_packet = ip.InstructionPacket(_id=dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(address, ) + value_tuple)
    #
    #    status_packet = serial_connection.send(instruction_packet)
    #
    #    if status_packet is not None:
    #        pass
    #        # TODO warning


    #def reset(self, dynamixel_id):
    #    instruction_packet = ip.InstructionPacket(_id=dynamixel_id, _instruction=ip.WRITE_DATA, _parameters=(address, ) + value_tuple)
    #
    #    status_packet = serial_connection.send(instruction_packet)
    #
    #    if status_packet is not None:
    #        pass
    #        # TODO warning

    ## HIGHEST LEVEL FUNCTIONS #################################################

    #def dump_control_table(self, dynamixel_id):
    #    pass


    #def scan(self, dynamixel_id_bytes=None):
    #    available_ids = bytearray()
    #
    #    for dynamixel_id in dynamixel_id_bytes:
    #        if 0 <= dynamixel_id <= 0xfe:
    #            if self.ping(dynamixel_id):
    #               available_ids.append(dynamixel_id)
    #        else:
    #            pass # TODO exception
    #
    #    return available_ids

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
This module contain the `Connection` class communicate with Dynamixel units.
"""

__all__ = ['Connection']

import math
import serial
import time

import pyax12.packet as pk
import pyax12.status_packet as sp
import pyax12.instruction_packet as ip

from pyax12 import utils

class Connection(object):
    """Create a serial connection with dynamixel actuators.

    :param str port: the serial device to connect with (e.g. '/dev/ttyUSB0'
        for Unix users or 'COM1' for windows users).
    :param int baudrate: the baudrate speed (e.g. 57600).
    :param float timeout: the timeout value for the connection.
    """

    def __init__(self, port='/dev/ttyUSB0', baudrate=57600, timeout=0.1):

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = serial.Serial(port=self.port,
                                               baudrate=self.baudrate,
                                               timeout=self.timeout,
                                               bytesize=serial.EIGHTBITS,
                                               parity=serial.PARITY_NONE,
                                               stopbits=serial.STOPBITS_ONE)

    def send(self, instruction_packet):
        """Send an instruction packet.

        :param instruction_packet: can be either a `Packet` instance or a
            "bytes" string containing the full instruction packet to be sent to
            Dynamixel units.
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

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFE).
        :param int address: the starting address of the location where the data
            is to be read.
        :param int length: the length of the data to be read.
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

        return data_bytes


    def write_data(self, dynamixel_id, address, data):
        """Write bytes to the control table of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFE).
        :param int address: the starting address of the location where the data
            is to be written.
        :param bytes data: the bytes of the data to be written (it can be an
            integer, a sequence of integer, a bytes or a bytearray).
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

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFE).
        :returns: ``True`` if the specified unit is available, ``False``
            otherwise.
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

    def dump_control_table(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, 0, 50)
        return byte_seq


    def print_control_table(self, dynamixel_id):
        byte_seq = self.dump_control_table(dynamixel_id)
        print(utils.pretty_hex_str(byte_seq, ' '))


    def pretty_print_control_table(self, dynamixel_id):
        print("{:.<24}{}".format("model_number", self.get_model_number(dynamixel_id)))
        print("{:.<24}{}".format("firmware_version", self.get_firmware_version(dynamixel_id)))
        print("{:.<24}{}".format("id", self.get_id(dynamixel_id)))
        print("{:.<24}{}".format("baud_rate", self.get_baud_rate(dynamixel_id)))
        print("{:.<24}{}".format("return_delay_time", self.get_return_delay_time(dynamixel_id)))
        print("{:.<24}{}".format("cw_angle_limit", self.get_cw_angle_limit(dynamixel_id)))
        print("{:.<24}{}".format("ccw_angle_limit", self.get_ccw_angle_limit(dynamixel_id)))
        print("{:.<24}{}".format("max_temperature", self.get_max_temperature(dynamixel_id)))
        print("{:.<24}{}".format("min_voltage", self.get_min_voltage(dynamixel_id)))
        print("{:.<24}{}".format("max_voltage", self.get_max_voltage(dynamixel_id)))
        print("{:.<24}{}".format("max_torque", self.get_max_torque(dynamixel_id)))
        print("{:.<24}{}".format("status_return_level", self.get_status_return_level(dynamixel_id)))
        print("{:.<24}{}".format("alarm_led", self.get_alarm_led(dynamixel_id)))
        print("{:.<24}{}".format("alarm_shutdown", self.get_alarm_shutdown(dynamixel_id)))
        print("{:.<24}{}".format("down_calibration", self.get_down_calibration(dynamixel_id)))
        print("{:.<24}{}".format("up_calibration", self.get_up_calibration(dynamixel_id)))
        print("{:.<24}{}".format("torque_enable", self.get_torque_enable(dynamixel_id)))
        print("{:.<24}{}".format("led", self.get_led(dynamixel_id)))
        print("{:.<24}{}".format("cw_compliance_margin", self.get_cw_compliance_margin(dynamixel_id)))
        print("{:.<24}{}".format("ccw_compliance_margin", self.get_ccw_compliance_margin(dynamixel_id)))
        print("{:.<24}{}".format("cw_compliance_slope", self.get_cw_compliance_slope(dynamixel_id)))
        print("{:.<24}{}".format("ccw_compliance_slope", self.get_ccw_compliance_slope(dynamixel_id)))
        print("{:.<24}{}".format("goal_position", self.get_goal_position(dynamixel_id)))
        print("{:.<24}{}".format("moving_speed", self.get_moving_speed(dynamixel_id)))
        print("{:.<24}{}".format("torque_limit", self.get_torque_limit(dynamixel_id)))
        print("{:.<24}{}".format("present_position", self.get_present_position(dynamixel_id)))
        print("{:.<24}{}".format("present_speed", self.get_present_speed(dynamixel_id)))
        print("{:.<24}{}".format("present_load", self.get_present_load(dynamixel_id)))
        print("{:.<24}{}".format("present_voltage", self.get_present_voltage(dynamixel_id)))
        print("{:.<24}{}".format("present_temperature", self.get_present_temperature(dynamixel_id)))
        print("{:.<24}{}".format("registred_instruction", self.get_registred_instruction(dynamixel_id)))
        print("{:.<24}{}".format("moving", self.get_moving(dynamixel_id)))
        print("{:.<24}{}".format("lock", self.get_lock(dynamixel_id)))
        print("{:.<24}{}".format("punch", self.get_punch(dynamixel_id)))


    def scan(self, dynamixel_id_bytes=None):
        """Return the ID sequence of available Dynamixel units.

        :param bytes dynamixel_id_bytes: a sequence of unique ID of the
            Dynamixel units to be pinged.
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


    def get_model_number(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.MODEL_NUMBER, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_firmware_version(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.VERSION_OF_FIRMWARE, 1)
        return byte_seq[0]


    def get_id(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.ID, 1)
        return byte_seq[0]


    def get_baud_rate(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.BAUD_RATE, 1)
        return byte_seq[0]


    def get_return_delay_time(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.RETURN_DELAY_TIME, 1)
        return byte_seq[0]


    def get_cw_angle_limit(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.CW_ANGLE_LIMIT, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_ccw_angle_limit(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.CCW_ANGLE_LIMIT, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_max_temperature(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.HIGHEST_LIMIT_TEMPERATURE, 1)
        return byte_seq[0]


    def get_min_voltage(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.LOWEST_LIMIT_VOLTAGE, 1)
        return byte_seq[0]


    def get_max_voltage(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.HIGHEST_LIMIT_VOLTAGE, 1)
        return byte_seq[0]


    def get_max_torque(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.MAX_TORQUE, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_status_return_level(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.STATUS_RETURN_LEVEL, 1)
        return byte_seq[0]


    def get_alarm_led(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.ALARM_LED, 1)
        return byte_seq[0]


    def get_alarm_shutdown(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.ALARM_SHUTDOWN, 1)
        return byte_seq[0]


    def get_down_calibration(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.DOWN_CALIBRATION, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_up_calibration(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.UP_CALIBRATION, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_torque_enable(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.TORQUE_ENABLE, 1)
        return byte_seq[0]


    def get_led(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.LED, 1)
        return byte_seq[0]


    def get_cw_compliance_margin(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.CW_COMPLIENCE_MARGIN, 1)
        return byte_seq[0]


    def get_ccw_compliance_margin(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.CCW_COMPLIENCE_MARGIN, 1)
        return byte_seq[0]


    def get_cw_compliance_slope(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.CW_COMPLIENCE_SLOPE, 1)
        return byte_seq[0]


    def get_ccw_compliance_slope(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.CCW_COMPLIENCE_SLOPE, 1)
        return byte_seq[0]


    def get_goal_position(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.GOAL_POSITION, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_moving_speed(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.MOVING_SPEED, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_torque_limit(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.TORQUE_LIMIT, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_present_position(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_POSITION, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_present_speed(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_SPEED, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_present_load(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_LOAD, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_present_voltage(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_VOLTAGE, 1)
        return byte_seq[0]


    def get_present_temperature(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_TEMPERATURE, 1)
        return byte_seq[0]


    def get_registred_instruction(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.REGISTRED_INSTRUCTION, 1)
        return byte_seq[0]


    def get_moving(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.MOVING, 1)
        return byte_seq[0]


    def get_lock(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.LOCK, 1)
        return byte_seq[0]


    def get_punch(self, dynamixel_id):
        byte_seq = self.read_data(dynamixel_id, pk.PUNCH, 2)
        return utils.little_endian_bytes_to_int(byte_seq)

    ###

    def goto(self, dynamixel_id, position, speed=None, degrees=False):
        # TODO: check ranges

        if degrees:
            position = math.ceil(position / 300. * 1023.)

        params = utils.int_to_little_endian_bytes(position)

        if speed is not None:
            params += utils.int_to_little_endian_bytes(speed)

        self.write_data(dynamixel_id, pk.GOAL_POSITION, params)

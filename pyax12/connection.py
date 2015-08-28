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
    :param float waiting_time: the waiting time (in seconds) between sending
        the instruction packet and the receiving the status packet.
    """

    def __init__(self, port='/dev/ttyUSB0', baudrate=57600, timeout=0.1,
                 waiting_time=0.02):

        self.waiting_time = waiting_time

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

        time.sleep(self.waiting_time)
        num_bytes_available = self.serial_connection.inWaiting()

        # TODO: not robust...
        status_packet_bytes = self.serial_connection.read(num_bytes_available)

        # TODO: make the reading status more robust?
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
            in range (0, 0xFD).
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
        # TODO: exception if dxl_id = 0xFE

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
            in range (0, 0xFD).
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
        # TODO: exception if dxl_id = 0xFE

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
        """Dump the *control table* of the specified Dynamixel unit.

        This function can be used to backup the current configuration of the
        given Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        :returns: the sequence of all bytes in currently the *control table*.
        """

        byte_seq = self.read_data(dynamixel_id, 0, 50)
        return byte_seq


    def print_control_table(self, dynamixel_id):
        """Print the *control table* of the specified Dynamixel unit in an
        "raw" format.

        To get the same output in a more easily human readable format, use the
        `pretty_print_control_table` function.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """

        byte_seq = self.dump_control_table(dynamixel_id)
        control_table_str = utils.pretty_hex_str(byte_seq, ' ')

        print(control_table_str)


    def get_control_table_tuple(self, dynamixel_id):
        """Return the *control table* of the specified Dynamixel unit in an
        easily human readable tuple.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """

        dxl_id = dynamixel_id   # use a shorter alias...

        ####

        def angle_to_str(dxl_angle):
            angle_degrees = dxl_angle_to_degrees(dxl_angle)
            angle_str = "{} ({}°)".format(dxl_angle, angle_degrees)
            return angle_str

        ####

        model_number = self.get_model_number(dxl_id)
        if model_number == 12:
            model_number_str = "AX-12+" 
        elif model_number == 13:
            model_number_str = "AX-S1"
        else:
            model_number_str = "Unknown (%i)" % model_number

        baud_rate_str = "%s bps" % self.get_baud_rate(dxl_id)
        return_delay_time_str = "%s µs" % self.get_return_delay_time(dxl_id)

        cw_angle_limit_str = angle_to_str(self.get_cw_angle_limit(dxl_id))
        ccw_angle_limit_str = angle_to_str(self.get_ccw_angle_limit(dxl_id))

        max_temperature_str = "%s°C" % self.get_max_temperature(dxl_id)
        min_voltage_str = "%sV" % self.get_min_voltage(dxl_id)
        max_voltage_str = "%sV" % self.get_max_voltage(dxl_id)

        torque_enable_str = "yes" if self.is_torque_enable(dxl_id) else "no"
        led_str = "on" if self.is_led_enabled(dxl_id) else "off"

        goal_position_str = angle_to_str(self.get_goal_position(dxl_id))
        position_str = angle_to_str(self.get_present_position(dxl_id))

        voltage_str = "%sV" % self.get_present_voltage(dxl_id)
        temperature_str = "%s°C" % self.get_present_temperature(dxl_id)

        if self.has_registred_instruction(dxl_id):
            registred_inst_str = "yes"
        else:
            registred_inst_str = "no"

        moving_str = "yes" if self.is_moving(dxl_id) else "no"
        locked_str = "yes" if self.is_locked(dxl_id) else "no"

        ####

        ctrl_table_tuple = (
            ("model_number", model_number_str),
            ("firmware_version", self.get_firmware_version(dxl_id)),
            #("id", self.get_id(dxl_id)), # TODO: stupide...
            ("id", dxl_id),
            ("baud_rate", baud_rate_str),
            ("return_delay_time", return_delay_time_str),
            ("cw_angle_limit", cw_angle_limit_str),
            ("ccw_angle_limit", ccw_angle_limit_str),
            ("max_temperature", max_temperature_str),
            ("min_voltage", min_voltage_str),
            ("max_voltage", max_voltage_str),
            ("max_torque", self.get_max_torque(dxl_id)),
            ("status_return_level", self.get_status_return_level(dxl_id)),
            ("alarm_led", self.get_alarm_led(dxl_id)),
            ("alarm_shutdown", self.get_alarm_shutdown(dxl_id)),
            ("down_calibration", self.get_down_calibration(dxl_id)),
            ("up_calibration", self.get_up_calibration(dxl_id)),
            ("torque_enabled", torque_enable_str),
            ("led", led_str),
            ("cw_compliance_margin", self.get_cw_compliance_margin(dxl_id)),
            ("ccw_compliance_margin", self.get_ccw_compliance_margin(dxl_id)),
            ("cw_compliance_slope", self.get_cw_compliance_slope(dxl_id)),
            ("ccw_compliance_slope", self.get_ccw_compliance_slope(dxl_id)),
            ("goal_position", goal_position_str),
            ("moving_speed", self.get_moving_speed(dxl_id)),
            ("torque_limit", self.get_torque_limit(dxl_id)),
            ("present_position", position_str),
            ("present_speed", self.get_present_speed(dxl_id)),
            ("present_load", self.get_present_load(dxl_id)),
            ("present_voltage", voltage_str),
            ("present_temperature", temperature_str),
            ("registred_instruction", registred_inst_str),
            ("moving", moving_str),
            ("locked", locked_str),
            ("punch", self.get_punch(dxl_id)),
        )

        return ctrl_table_tuple


    def pretty_print_control_table(self, dynamixel_id):
        """Print the *control table* of the specified Dynamixel unit in an
        easily human readable format.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """

        ctrl_table_tuple = self.get_control_table_tuple(dynamixel_id)

        for key, value in ctrl_table_tuple:
            print("{:.<24} {}".format(key, value))


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
        """Return the model number of the specified Dynamixel unit.

        For AX-12, this value should be 12 (0x000C).

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.MODEL_NUMBER, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_firmware_version(self, dynamixel_id):
        """Return the firmware version of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.VERSION_OF_FIRMWARE, 1)
        return byte_seq[0]


#    # TODO: stupide...
#    def get_id(self, dynamixel_id):
#        """Return the ID of the specified Dynamixel unit.
#
#        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
#            in range (0, 0xFD).
#        """
#        byte_seq = self.read_data(dynamixel_id, pk.ID, 1)
#        return byte_seq[0]


    # TODO: add the data value table (cf. p. 13)
    # baud_rate = 2000000 / (address_4 + 1)
    def get_baud_rate(self, dynamixel_id):
        """Return the communication speed (baud rate) of the specified
        Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.BAUD_RATE, 1)
        raw_value = byte_seq[0]

        baudrate = 2000000 / (raw_value + 1)

        return round(baudrate, 1)


    def get_return_delay_time(self, dynamixel_id):
        """Return the return delay time of the specified Dynamixel unit.

        The return delay time is the time it takes (in uSec) for the status
        packet to return after the instruction packet is sent.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.RETURN_DELAY_TIME, 1)
        raw_value = byte_seq[0]

        delay_time = 2 * raw_value

        return delay_time


    def get_cw_angle_limit(self, dynamixel_id):
        """Return the *clock wise angle limit* of the specified Dynamixel unit.

        The goal position should be higher or equal than this value, otherwise
        the *Angle Limit Error Bit* (the second error bit of Status Packets)
        will be set to ``1``.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.CW_ANGLE_LIMIT, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_ccw_angle_limit(self, dynamixel_id):
        """Return the *counter clock wise angle limit* of the specified
        Dynamixel unit.

        The goal position should be lower or equal than this value, otherwise
        the *Angle Limit Error Bit* (the second error bit of Status Packets)
        will be set to ``1``.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.CCW_ANGLE_LIMIT, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_max_temperature(self, dynamixel_id):
        """Return the maximum tolerated internal temperature for the specified
        Dynamixel unit.

        If the internal temperature of the Dynamixel actuator gets higher than
        this value, the *Over Heating Error Bit* (the third error bit of
        Status Packets) will be set to ``1``.
        The values are in degrees Celsius.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.HIGHEST_LIMIT_TEMPERATURE, 1)
        return byte_seq[0]


    def get_min_voltage(self, dynamixel_id):
        """Return the minimum tolerated operating voltage for the specified
        Dynamixel unit.

        If the present voltage of the Dynamixel actuator gets lower than
        this value, the *Voltage Range Error Bit* (the first error bit of
        Status Packets) will be set to ``1``.
        The values are in Volts.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.LOWEST_LIMIT_VOLTAGE, 1)
        raw_value = byte_seq[0]

        min_voltage = raw_value / 10.
        return min_voltage


    def get_max_voltage(self, dynamixel_id):
        """Return the maximum tolerated operating voltage for the specified
        Dynamixel unit.

        If the present voltage of the Dynamixel actuator gets higher than
        this value, the *Voltage Range Error Bit* (the first error bit of
        Status Packets) will be set to ``1``.
        The values are in Volts.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.HIGHEST_LIMIT_VOLTAGE, 1)
        raw_value = byte_seq[0]

        max_voltage = raw_value / 10.
        return max_voltage


    def get_max_torque(self, dynamixel_id):
        """Return the initial maximum torque output of the specified Dynamixel
        unit.

        This value, written in EEPROM, is copied to the *torque limit* bytes
        (in RAM) when the power is turned ON. Thus, *max torque* is just an
        initialization value for the actual *max torque*.

        If this value is equal to ``0``, the Dynamixel unit is configured in
        *free run mode*.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.MAX_TORQUE, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_status_return_level(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.STATUS_RETURN_LEVEL, 1)
        return byte_seq[0]


    def get_alarm_led(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.ALARM_LED, 1)
        return byte_seq[0]


    def get_alarm_shutdown(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.ALARM_SHUTDOWN, 1)
        return byte_seq[0]


    def get_down_calibration(self, dynamixel_id):
        """Return the "down calibration" value of the specified Dynamixel unit.

        The calibration value is used to compensate the differences between the
        potentiometers used in the Dynamixel units.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.DOWN_CALIBRATION, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_up_calibration(self, dynamixel_id):
        """Return the "up calibration" value of the specified Dynamixel unit.

        The calibration value is used to compensate the differences between the
        potentiometers used in the Dynamixel units.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.UP_CALIBRATION, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def is_torque_enable(self, dynamixel_id):
        """Return ``True`` if the torque of the specified Dynamixel unit is
        enabled; otherwise return ``False``.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.TORQUE_ENABLE, 1)
        return byte_seq[0] == 1


    def is_led_enabled(self, dynamixel_id):
        """Return ``True`` if the LED of the specified Dynamixel unit is ON;
        otherwise return ``False``.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.LED, 1)
        return byte_seq[0] == 1


    def get_cw_compliance_margin(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.CW_COMPLIENCE_MARGIN, 1)
        return byte_seq[0]


    def get_ccw_compliance_margin(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.CCW_COMPLIENCE_MARGIN, 1)
        return byte_seq[0]


    def get_cw_compliance_slope(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.CW_COMPLIENCE_SLOPE, 1)
        return byte_seq[0]


    def get_ccw_compliance_slope(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.CCW_COMPLIENCE_SLOPE, 1)
        return byte_seq[0]


    def get_goal_position(self, dynamixel_id):
        """Return the requested goal angular position of the specified
        Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.GOAL_POSITION, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_moving_speed(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.MOVING_SPEED, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_torque_limit(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.TORQUE_LIMIT, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_present_position(self, dynamixel_id, degrees=False):
        """Return the current angular position of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        :param bool degrees: defines the returned `position` unit. If `degrees`
            is ``True``, `position` corresponds to the goal rotation angle *in
            degrees* with respect to the original position and is defined in
            range (0, 300). Otherwise, `position` is a unit free angular position
            to the origin, defined in range (0, 1023) i.e. (0, 0x3FF) in
            hexadecimal notation.
        """
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_POSITION, 2)
        position = utils.little_endian_bytes_to_int(byte_seq)

        if degrees:
            position = dxl_angle_to_degrees(position)

        return position


    def get_present_speed(self, dynamixel_id):
        """Return the current angular velocity of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_SPEED, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_present_load(self, dynamixel_id):
        """Return the  of the specified Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_LOAD, 2)
        return utils.little_endian_bytes_to_int(byte_seq)


    def get_present_voltage(self, dynamixel_id):
        """Return the voltage currently applied to the specified Dynamixel
        unit (in Volts).

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_VOLTAGE, 1)
        raw_value = byte_seq[0]

        voltage = raw_value / 10.
        return voltage


    def get_present_temperature(self, dynamixel_id):
        """Return the internal temperature of the specified Dynamixel unit (in
        Degrees Celsius).

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.PRESENT_TEMPERATURE, 1)
        return byte_seq[0]


    # TODO: stupid ?
    def has_registred_instruction(self, dynamixel_id):
        """Return ``True`` if the specified Dynamixel unit is currently
        processing a REG_WRITE command; otherwise, return ``False``.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.REGISTRED_INSTRUCTION, 1)
        return byte_seq[0] == 1


    def is_moving(self, dynamixel_id):
        """Return ``True`` if the specified Dynamixel unit is moving by its own
        power; return ``False`` otherwise.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.MOVING, 1)
        return byte_seq[0] == 1


    def is_locked(self, dynamixel_id):
        """Return ``True`` if the specified Dynamixel unit is locked; return
        ``False`` otherwise.

        When a Dynamixel unit is locked, only addresses 0x18 to 0x23 can be
        written.
        Once locked, it can only be unlocked by turning the power off.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.LOCK, 1)
        return byte_seq[0] == 1


    def get_punch(self, dynamixel_id):
        """Return the minimum current supplied to the motor of the specified
        Dynamixel unit during operation.

        The initial value is set to 0x20 and its maximum value is 0x3FF.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFD).
        """
        byte_seq = self.read_data(dynamixel_id, pk.PUNCH, 2)
        return utils.little_endian_bytes_to_int(byte_seq)

    ###

    def goto(self, dynamixel_id, position, speed=None, degrees=False):
        """Set the *goal position* and *moving speed* for the specified
        Dynamixel unit.

        :param int dynamixel_id: the unique ID of a Dynamixel unit. It must be
            in range (0, 0xFE).
        :param int position: the new goal position. If `degrees` is ``True``,
            `position` corresponds to the goal rotation angle *in degrees* with
            respect to the original position and must be in range (0, 300).
            Otherwise, `position` is a unit free rotation angle to the origin,
            defined in range (0, 1023) i.e. (0, 0x3FF) in hexadecimal notation.
        :param int speed: the new moving speed. It must be in range (0, 1023)
            i.e. (0, 0x3FF) in hexadecimal notation. This parameter is
            optional; if `speed` is not specified, the *moving speed* present
            in the Dynamixel control table is kept and used to reach the goal
            position.
        :param bool degrees: defines the `position` unit. If `degrees` is
            ``True``, `position` corresponds to the goal rotation angle *in
            degrees* with respect to the original position and must be in range
            (0, 300). Otherwise, `position` is a unit free angular position,
            defined in range (0, 1023) i.e. (0, 0x3FF) in hexadecimal notation.
        """
        # TODO: check ranges

        if degrees:
            position = degrees_to_dxl_angle(position)

        params = utils.int_to_little_endian_bytes(position)

        if speed is not None:
            params += utils.int_to_little_endian_bytes(speed)

        self.write_data(dynamixel_id, pk.GOAL_POSITION, params)

####

# TODO: move it to utils
def dxl_angle_to_degrees(dxl_angle):
    angle_degrees = round(dxl_angle / 1023. * 300., 1)
    return angle_degrees


# TODO: move it to utils
def degrees_to_dxl_angle(angle_degrees):
    dxl_angle = math.floor(angle_degrees / 300. * 1023.)
    return dxl_angle


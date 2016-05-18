.. image:: https://readthedocs.org/projects/pyax-12/badge/?version=latest
    :target: https://readthedocs.org/projects/pyax-12/?badge=latest
    :alt: Documentation Status

==========
`PyAX-12`_
==========

Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)


* Web site: http://www.jdhp.org/projects_en.html#pyax12
* Online documentation: http://pyax-12.readthedocs.org
* Source code: https://github.com/jeremiedecock/pyax12
* Issue tracker: https://github.com/jeremiedecock/pyax12/issues
* PyAX-12 on PyPI: https://pypi.python.org/pypi/pyax12

In collaboration with http://www.vorobotics.com


Description
===========

`PyAX-12`_ is an open source lightweight Python library to control
`Dynamixel AX-12+`_ actuators.

|Watch a demo on youtube|_

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

-  Python >= 3.0
-  `Python-serial`_

PyAX-12 is tested to work with Python 3.4 under Gnu/Linux Debian 8 and Windows
7.
It should also work with Python 3.X under recent Gnu/Linux and Windows systems.
It hasn't been tested (yet) on MacOSX and BSD systems.

`Python-serial`_ is required to install PyAX-12.

Note:

    If you use ``pip`` to install PyAX-12, Python-serial will be automatically
    downloaded and installed (see the following install_ section).


.. _install:

Installation
============

Gnu/Linux
---------

You can install, upgrade, uninstall PyAX-12 with these commands (in a
terminal)::

    pip install --pre pyax12
    pip install --upgrade pyax12
    pip uninstall pyax12

Or, if you have downloaded the PyAX-12 source code::

    python3 setup.py install

.. There's also a package for Debian/Ubuntu::
.. 
..     sudo apt-get install pyax12

Windows
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.4 under Windows 7.
..     It should also work with recent Windows systems.

You can install, upgrade, uninstall PyAX-12 with these commands (in a
`command prompt`_)::

    py -m pip install --pre pyax12
    py -m pip install --upgrade pyax12
    py -m pip uninstall pyax12

Or, if you have downloaded the PyAX-12 source code::

    py setup.py install

MacOSX
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.5 under MacOSX 10.9 (*Mavericks*).
..     It should also work with recent MacOSX systems.

You can install, upgrade, uninstall PyAX-12 with these commands (in a
terminal)::

    pip install --pre pyax12
    pip install --upgrade pyax12
    pip uninstall pyax12

Or, if you have downloaded the PyAX-12 source code::

    python3 setup.py install


Documentation
=============

.. PyAX-12 documentation is available on the following page:
.. 
..     http://pyax-12.rtfd.org/

- Online Documentation: http://pyax-12.readthedocs.org
- API Documentation: http://pyax-12.readthedocs.org/en/latest/api.html


Example usage
=============

.. Please check whether the serial port, the baudrate and the
.. Dynamixel IDs defined in the following examples fits with your hardware.

In the following examples, the ``dynamixel_id``, ``port`` and ``baudrate``
values should be adapted depending on your configuration:

- for **Linux** users:
  
  - the ``port`` value should be something like
  
    - "/dev/ttyS0", "/dev/ttyS1", ... if you use an actual serial port
    - "/dev/ttyUSB0", "/dev/ttyUSB1", ... if you use an `USB to serial` adapter
      (like the USB2Dynamixel_ adapter)

  - the ``baudrate`` value should be the same than the one configured in
    Dynamixel units

- for **Windows** users:

  - the ``port`` value should be something like "COM2", "COM3", ... (see the
    *COM port* configuration in the Windows `device manager`_)
  - the ``baudrate`` value should be the same than the one configured in
    the Dynamixel units *and* the Windows `device manager`_ (i.e. check the
    *COM port* configuration in the Windows `device manager`_)

- for **MacOSX** users:
  
  - the ``port`` value should be something like "/dev/tty.usbserial-XXX" if you
    use an `USB to serial` adapter like the USB2Dynamixel_ adapter
  - the ``baudrate`` value should be the same than the one configured in
    Dynamixel units

If you use the USB2Dynamixel_ device, make sure its switch is set on "TTL".

Some other examples are available in the examples_ directory.

Ping a Dynamixel
----------------

This snippet prints ``True`` if the specified Dynamixel unit is connected and
available at the given `baudrate`; otherwise it prints ``False``.

::

    from pyax12.connection import Connection

    # Connect to the serial port
    serial_connection = Connection(port="/dev/ttyUSB0", baudrate=57600)

    dynamixel_id = 3

    # Ping the third dynamixel unit
    is_available = serial_connection.ping(dynamixel_id)

    print(is_available)

    # Close the serial connection
    serial_connection.close()


Scan (search available Dynamixel units)
---------------------------------------

This snippet prints the ID list of connected and available Dynamixel units (at
the given `baudrate`).

::

    from pyax12.connection import Connection

    # Connect to the serial port
    serial_connection = Connection(port="/dev/ttyUSB0", baudrate=57600)

    # Ping the dynamixel unit(s)
    ids_available = serial_connection.scan()

    for dynamixel_id in ids_available:
        print(dynamixel_id)

    # Close the serial connection
    serial_connection.close()


Print the control table of the first Dynamixel unit
---------------------------------------------------

This snippet prints the control table of the specified Dynamixel unit (i.e. the
internal state information of the Dynamixel unit).

::

    from pyax12.connection import Connection

    # Connect to the serial port
    serial_connection = Connection(port="/dev/ttyUSB0", baudrate=57600)

    dynamixel_id = 1

    # Print the control table of the specified Dynamixel unit
    serial_connection.pretty_print_control_table(dynamixel_id)

    # Close the serial connection
    serial_connection.close()

This snippet should print something like that::

    model_number................. AX-12+
    firmware_version............. 24
    id........................... 1
    baud_rate.................... 57142.9 bps
    return_delay_time............ 500 µs
    cw_angle_limit............... -150.0° (0)
    ccw_angle_limit.............. 150.0° (1023)
    max_temperature.............. 70°C
    min_voltage.................. 6.0V
    max_voltage.................. 14.0V
    max_torque................... 1023
    status_return_level.......... 2 (respond to all instructions)
    input_voltage_alarm_led...... off
    angle_limit_alarm_led........ off
    overheating_alarm_led........ on
    range_alarm_led.............. off
    checksum_alarm_led........... off
    overload_alarm_led........... on
    instruction_alarm_led........ off
    input_voltage_alarm_shutdown. off
    angle_limit_alarm_shutdown... off
    overheating_alarm_shutdown... on
    range_alarm_shutdown......... off
    checksum_alarm_shutdown...... off
    overload_alarm_shutdown...... on
    instruction_alarm_shutdown... off
    down_calibration............. 46
    up_calibration............... 972
    torque_enabled............... yes
    led.......................... off
    cw_compliance_margin......... 0.3° (1)
    ccw_compliance_margin........ 0.3° (1)
    cw_compliance_slope.......... 9.4° (32)
    ccw_compliance_slope......... 9.4° (32)
    goal_position................ -0.1° (511)
    moving_speed................. 512
    torque_limit................. 1023
    present_position............. -0.1° (511)
    present_speed................ 0
    present_load................. 0
    present_voltage.............. 12.1V
    present_temperature.......... 43°C
    registred_instruction........ no
    moving....................... no
    locked....................... no
    punch........................ 32

Move the first Dynamixel unit to various position angles
--------------------------------------------------------

This snippet moves the first Dynamixel unit to 0°, then -45°, -90°, -135°,
-150° (the maximum CW angle), +150° (the maximum CCW angle), +135°, +90°, +45°
and finally goes back to 0°.

::

    from pyax12.connection import Connection
    import time

    # Connect to the serial port
    serial_connection = Connection(port="/dev/ttyUSB0", baudrate=57600)

    dynamixel_id = 1

    # Go to 0°
    serial_connection.goto(dynamixel_id, 0, speed=512, degrees=True)
    time.sleep(1)    # Wait 1 second

    # Go to -45° (45° CW)
    serial_connection.goto(dynamixel_id, -45, speed=512, degrees=True)
    time.sleep(1)    # Wait 1 second

    # Go to -90° (90° CW)
    serial_connection.goto(dynamixel_id, -90, speed=512, degrees=True)
    time.sleep(1)    # Wait 1 second

    # Go to -135° (135° CW)
    serial_connection.goto(dynamixel_id, -135, speed=512, degrees=True)
    time.sleep(1)    # Wait 1 second

    # Go to -150° (150° CW)
    serial_connection.goto(dynamixel_id, -150, speed=512, degrees=True)
    time.sleep(1)    # Wait 1 second

    # Go to +150° (150° CCW)
    serial_connection.goto(dynamixel_id, 150, speed=512, degrees=True)
    time.sleep(2)    # Wait 2 seconds

    # Go to +135° (135° CCW)
    serial_connection.goto(dynamixel_id, 135, speed=512, degrees=True)
    time.sleep(1)    # Wait 1 second

    # Go to +90° (90° CCW)
    serial_connection.goto(dynamixel_id, 90, speed=512, degrees=True)
    time.sleep(1)    # Wait 1 second

    # Go to +45° (45° CCW)
    serial_connection.goto(dynamixel_id, 45, speed=512, degrees=True)
    time.sleep(1)    # Wait 1 second

    # Go back to 0°
    serial_connection.goto(dynamixel_id, 0, speed=512, degrees=True)

    # Close the serial connection
    serial_connection.close()


Bug reports
===========

To search for bugs or report them, please use the PyAX-12 Bug Tracker at:

    https://github.com/jeremiedecock/pyax12/issues


.. _related-libraries:

Related libraries
=================

Other libraries to control `Dynamixel AX-12+`_ actuators are referenced in the
following (non comprehensive) list:

- PyPot_ by Inria (FLOWERS team)
- PyDynamixel_ by Richard Clark
- Pydyn_ by Fabien Benureau and Olivier Mangin (Inria FLOWER team)
- Dynamixel_ by Ian Danforth
- dynamixel_hr_ by Romain Reignier
- python_dynamixels_ by Jesse Merritt
- ax12_ by Thiago Hersan
- `Dynamixel Monitor`_ by Christian Balkenius
- DynamixelMonitor_ by Slavik


License
=======

The ``PyAX-12`` library is provided under the terms and conditions of the
`MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT

.. _PyAX-12: http://www.jdhp.org/projects_en.html#pyax12
.. _Dynamixel AX-12+: http://www.robotis.com/xe/dynamixel_en
.. _examples: https://github.com/jeremiedecock/pyax12/tree/master/examples
.. _USB2Dynamixel: http://support.robotis.com/en/product/auxdevice/interface/usb2dxl_manual.htm
.. _Python-serial: http://pyserial.sourceforge.net
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe
.. _device manager: http://windows.microsoft.com/en-us/windows/open-device-manager

.. _PyPot: https://github.com/poppy-project/pypot
.. _Pydyn: https://github.com/humm/pydyn
.. _PyDynamixel: https://github.com/richard-clark/PyDynamixel
.. _Python-serial: http://pyserial.sourceforge.net
.. _Dynamixel : https://pypi.python.org/pypi/dynamixel/1.0.1
.. _dynamixel_hr : https://github.com/HumaRobotics/dynamixel_hr
.. _python_dynamixels : https://github.com/jes1510/python_dynamixels
.. _ax12 : https://github.com/thiagohersan/memememe/tree/master/Python/ax12
.. _Dynamixel Monitor : http://robosavvy.com/forum/viewtopic.php?p=42991
.. _DynamixelMonitor : https://github.com/slavikshen/DynamixelMonitor

.. |Watch a demo on youtube| image:: http://download.tuxfamily.org/jdhp/image/pyax12_demo_youtube.jpeg
.. _Watch a demo on youtube: http://youtu.be/5r0mNPhpf04

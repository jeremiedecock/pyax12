.. image:: https://readthedocs.org/projects/pyax-12/badge/?version=latest
    :target: https://readthedocs.org/projects/pyax-12/?badge=latest
    :alt: Documentation Status

=========================================================
`PyAX-12 <http://www.jdhp.org/projects_en.html#pyax12>`__
=========================================================

Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)


* Web site: http://www.jdhp.org/projects_en.html#pyax12
* Online documentation: http://pyax-12.readthedocs.org
* Source code: https://github.com/jeremiedecock/pyax12
* Issue tracker: https://github.com/jeremiedecock/pyax12/issues
* PyAX-12 on PyPI: https://pypi.python.org/pypi/pyax12


Description
===========

PyAX-12 is an open source lightweight Python library to control
`Dynamixel AX-12+ <http://www.robotis.com/xe/dynamixel_en>`__ actuators.

|Watch a demo on youtube|_


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

Note:

    The following installation procedure has been tested to work with Python
    3.4 under Windows 7.
    It should also work with recent Windows systems.

You can install, upgrade, uninstall PyAX-12 with these commands (in a
`command prompt`_)::

    py -m pip install --pre pyax12
    py -m pip install --upgrade pyax12
    py -m pip uninstall pyax12

Or, if you have downloaded the PyAX-12 source code::

    py setup.py install


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

- for Linux users the `port` value should be something like
  
  - "/dev/ttyS0", "/dev/ttyS1", ... if you use an actual serial port
  - "/dev/ttyUSB0", "/dev/ttyUSB1", ... if you use an `USB to serial` adapter
    (like the USB2Dynamixel_ adapter)

- for Windows users the `port` value should be something like "COM2", "COM3",
  ...

If you use the USB2Dynamixel_ device, make sure its switch is set on
"TTL".

Some other examples are available in the examples_ directory.

Ping a Dynamixel
----------------

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


Print the control table of the third Dynamixel unit
---------------------------------------------------

::

    from pyax12.connection import Connection

    # Connect to the serial port
    serial_connection = Connection(port="/dev/ttyUSB0", baudrate=57600)

    dynamixel_id = 3

    # Print the control table of the specified Dynamixel unit
    serial_connection.pretty_print_control_table(dynamixel_id)

    # Close the serial connection
    serial_connection.close()


Move the first Dynamixel unit to 0° then go to 300° and finally go back to 150°
-------------------------------------------------------------------------------

::

    from pyax12.connection import Connection
    import time

    # Connect to the serial port
    serial_connection = Connection(port="/dev/ttyUSB0", baudrate=57600)

    dynamixel_id = 1

    # Goto to 0°
    serial_connection.goto(dynamixel_id, 0, degrees=True)

    # Wait 2 seconds
    time.sleep(2)

    # Go back to 300°
    serial_connection.goto(dynamixel_id, 300, degrees=True)

    # Wait 2 seconds
    time.sleep(2)

    # Go back to 150°
    serial_connection.goto(dynamixel_id, 150, degrees=True)

    # Close the serial connection
    serial_connection.close()


Bug reports
===========

To search for bugs or report them, please use the PyAX-12 Bug Tracker at:

    https://github.com/jeremiedecock/pyax12/issues


.. _related-libraries:

Related libraries
=================

Other libraries to control
`Dynamixel AX-12+ <http://www.robotis.com/xe/dynamixel_en>`__
actuators are referenced in the following (non comprehensive) list:

- PyPot_ by Inria (FLOWERS team)
- PyDynamixel_ by Richard Clark
- Pydyn_ by Fabien Benureau and Olivier Mangin (Inria FLOWER team)
- Dynamixel_ by Ian Danforth
- dynamixel_hr_ by Romain Reignier
- python_dynamixels_ by Jesse Merritt
- ax12_ by Thiago Hersan


License
=======

The ``PyAX-12`` library is provided under the terms and conditions of the
`MIT License <http://opensource.org/licenses/MIT>`__.


.. _Dynamixel AX-12+ actuators: http://www.robotis.com/xe/dynamixel_en
.. _examples: https://github.com/jeremiedecock/pyax12/tree/master/examples
.. _USB2Dynamixel: http://support.robotis.com/en/product/auxdevice/interface/usb2dxl_manual.htm
.. _Python-serial: http://pyserial.sourceforge.net
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe

.. _PyPot: https://github.com/poppy-project/pypot
.. _Pydyn: https://github.com/humm/pydyn
.. _PyDynamixel: https://github.com/richard-clark/PyDynamixel
.. _Python-serial: http://pyserial.sourceforge.net
.. _Dynamixel : https://pypi.python.org/pypi/dynamixel/1.0.1
.. _dynamixel_hr : https://github.com/HumaRobotics/dynamixel_hr
.. _python_dynamixels : https://github.com/jes1510/python_dynamixels
.. _ax12 : https://github.com/thiagohersan/memememe/tree/master/Python/ax12

.. |Watch a demo on youtube| image:: http://download.tuxfamily.org/jdhp/image/pyax12_demo_youtube.jpeg
.. _Watch a demo on youtube: https://youtu.be/sXrEGmjz-S4

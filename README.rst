`PyAX-12 <http://www.jdhp.org/projects_en.html#pyax12>`__
=========================================================

Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)

Description
-----------

PyAX-12 is an open source lightweight Python library to control
`Dynamixel AX-12+ <http://www.robotis.com/xe/dynamixel_en>`__ actuators.

|Watch a demo on youtube|_

Dependencies
------------

-  Python >= 3.0
-  `Python-serial <http://pyserial.sourceforge.net>`__

Install
-------

PyAX-12 can be installed with Python Distutils by entering the following
command in a terminal::

    python setup.py install

Warning
-------

If you use the USB2Dynamixel device, make sure its switch is set on
"TTL" (otherwise status packets won't be readable).

Also, please check whether the serial port, the baudrate and the
Dynamixel IDs defined in PyAX-12 fits with your hardware.

License
-------

The ``PyAX-12`` library is provided under the terms and conditions of the
`MIT License <http://opensource.org/licenses/MIT>`__.

.. |Watch a demo on youtube| image:: http://download.tuxfamily.org/jdhp/image/pyax12_demo_youtube.jpeg
.. _Watch a demo on youtube: https://youtu.be/sXrEGmjz-S4

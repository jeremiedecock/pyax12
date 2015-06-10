# [PyAX-12](http://www.jdhp.org/projects_en.html#pydynamixel)

Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)

## Description

PyAX-12 is a Python library to control Dynamixel AX-12+ servos.

## Dependencies

* Python >= 3.0
* [Python-serial](http://pyserial.sourceforge.net)

## Install

Pyarm can be installed with Python Distutils by entering the following command
in a terminal:

```
python setup.py install
```

## Warning

If you use the USB2Dynamixel device, make sure its switch is set on "TTL"
(otherwise status packets won't be readable).

Also, please check whether the serial port, the baudrate and the Dynamixel IDs
defined in PyAX-12 fits with your hardware.

## License

PyAX-12 is distributed under the [MIT License](http://opensource.org/licenses/MIT).

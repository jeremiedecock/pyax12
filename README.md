# [PyAX-12](http://www.jdhp.org/projects_en.html#pyax12)

Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)

## Description

PyAX-12 is an open source lightweight Python library to control
[Dynamixel AX-12+](http://www.robotis.com/xe/dynamixel_en) actuators.

<iframe width="560" height="315" src="https://www.youtube.com/embed/sXrEGmjz-S4" frameborder="0" allowfullscreen></iframe>

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

# TODO

## Version 0.3

- [x] Change the package name (from `pydynamixel` to `pyax12`): the project
      now focus on Dynamixel AX-12 actuators.

## Version 0.4

- [ ] Check/fix the setup.py file.
- [x] Publish PyAX-12 on PyPI.
- [x] Check the PyAX-12 installation (with pip) and examples on Windows 7.
- [ ] Write unit tests.
- [ ] Improve docstrings.
- [ ] Clean all modules with pylint.
- [ ] Use exceptions instead warnings.
- [ ] Create a user documentation with Sphinx.
- [ ] Publish the documentation on readthedocs.org
- [ ] Write "high level" functions in Connection: Connection.dump(),
  Connection.scan(), Connection.reset(), ...
- [ ] Test arguments in all functions (type, value, ...)

## Version 0.5

- [ ] Write a test suite to launch all unit tests.
- [ ] Add some examples.
- [ ] Improve the README file.
    - [ ] Description.
    - [ ] Installation procedure.
- [x] Add a demonstration video in the README file.

## Version 0.6

- [ ] Fix remaining "TODO" tags.
- [ ] Improve the reliability of Connection.send()

## Version 1.0

- [ ] Fix missing data and tests:
    - [ ] Error table (Dynamixel User Manual p.11)
    - [ ] Access RD/WD (p.12)
    - [ ] Addr/labels (p.12)
    - [ ] Baudrates (p.13)
    - [ ] Status return level (p.14)
    - [ ] Alarm led (p.15)
    - [ ] Alarm shutdown (p.15)
    - [ ] Compliance margin and slope (p.16)
    - [ ] Present load (p.17)
    - [ ] Goal speed setting (p.18)
    - [ ] Range (p.18)
    - [ ] Instruction set labels (p.19)
    - [ ] UART p.30 and 31
- [ ] Complete the sphinx documentation to contain all the "Dynamixel User
  Manual" (the documentation should help users to connect dynamixels,
  understand how it works, ...).
- [ ] Add a "Features" section in the README.rst and sphinx docs.
- [ ] Add a "Troubleshooting" section in the README.rst and sphinx docs (should
  contain installation instructions relative to specific
  platforms/configurations).
- [ ] Add a "FAQ" section in the README.rst and sphinx docs.
- [ ] Use Tox (http://tox.testrun.org/) to run tests ?
- [ ] Implement `__str__` in Packet.
- [ ] Implement `__iter__` and `next` in Packet to make it iterable.
- [ ] Implement the `with` context manager in the Connection class (to
  automatically close serial connections).
- [ ] Check the "debian-dist.sh" script and build/publish a Debian packet.
- [ ] Add a RPM package.
- [ ] Check the PyAX-12 installation (with pip) and examples on Windows
  XP/Vista/8/10.
- [ ] Check the PyAX-12 installation (with pip) and examples on MacOSX.
- [ ] Write functions "Packet.print_info()" and "Connection.print_info()" to
  print "human readable" informations (e.g. "position=...°\nspeed=..." ;
  "baudrate=...\nport=...\n...") ?
- [ ] Some unit tests "requires to be connected to the Dynamixel number 1 using
  port "/dev/ttyUSB0" (thus it works on Unix systems only) at 57600 baud." ->
  fix it... (especially in test_status_packet)

## Misc

- [ ] Write a MSI installer for Windows.
- [ ] Create a "pyax12gui" repository: a set of graphic tools (tkinter) on top
  of PyAX-12 to handle Dynamixels servos.
- [ ] Write a tutorial to explain how to use PyAX-12 on a RaspberryPi using
  GPIOs (i.e. without the usbdynamixel adapter) and without the CM-5 (i.e. using
  a batteries, a LiPo or a DC lab power supply instead).


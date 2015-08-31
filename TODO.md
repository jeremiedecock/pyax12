# TODO

## Version 0.3

- [x] Change the package name (from `pydynamixel` to `pyax12`): the project
      now focus on Dynamixel AX-12 actuators.

## Version 0.4

- [x] Check/fix the setup.py file.
- [x] Publish PyAX-12 on PyPI.
- [x] Check the PyAX-12 installation (with pip) and examples on Windows 7.
- [x] Put an argparse default instance in "argparse_default.py".
- [ ] Write unit tests.
    - [x] argparse_default.py
    - [ ] connection.py
    - [ ] instruction_packet.py
    - [x] packet.py
    - [x] status_packet.py
    - [x] utils.py
- [ ] Improve docstrings.
    - [x] argparse_default.py
    - [ ] connection.py
    - [x] instruction_packet.py
    - [x] packet.py
    - [x] status_packet.py
    - [x] utils.py
- [ ] Check how docstrings are printed with the "help()" function (is it
  readable ?).
- [ ] Clean all modules with pylint.
    - [x] argparse_default.py
    - [ ] connection.py
    - [x] instruction_packet.py
    - [x] packet.py
    - [x] status_packet.py
    - [x] utils.py
- [x] Use exceptions instead warnings.
- [x] Create a user documentation with Sphinx.
- [x] Publish the documentation on readthedocs.org
- [x] Add a demonstration video in the README file.
- [ ] Write "high level" functions in Connection: Connection.dump(),
  Connection.scan(), Connection.reset(), ...
- [x] Fix issue #1: https://github.com/jeremiedecock/pyax12/issues/1
- [ ] Test arguments in all functions (type, value, ...)
    - [x] argparse_default.py
    - [ ] connection.py
    - [x] instruction_packet.py
    - [x] packet.py
    - [x] status_packet.py
    - [x] utils.py
- [ ] Add the following warning in the documentation: the baudrate value given
  to the Connection class should be the same than the one in dynamixel units
  (and also the same than the one of the COM port used for Windows).
- [ ] How to avoid the "--pre" option when installing on Linux with pip ?
- [ ] Cite the *Vor12 project* in the documentation (in the examples section).
- [ ] Update the CHANGES.rst file.

## Version 0.5

- [ ] Write a test suite to launch all unit tests.
- [ ] Add some examples.
- [ ] Improve the README file:
    - [ ] Description;
    - [ ] Installation procedure: see http://www.pylint.org/ (and add more
      details in the Troubleshooting/FAQ sections)
- [ ] Clean all modules with pep8.
    - [ ] argparse_default.py
    - [ ] connection.py
    - [ ] instruction_packet.py
    - [ ] packet.py
    - [ ] status_packet.py
    - [ ] utils.py
- [ ] Clean all modules with pyflakes.
    - [ ] argparse_default.py
    - [ ] connection.py
    - [ ] instruction_packet.py
    - [ ] packet.py
    - [ ] status_packet.py
    - [ ] utils.py
- [ ] Get a table with border in sphinx (to write clean packet data frame in
  the documentation), i.e. something like this:
  https://docs.python.org/3/library/itertools.html

## Version 1.0

- [ ] Update "Connection.get_control_table_tuple()" such that only one
  Instruction Packet is send to the Dynamixel unit and only one (big) Status
  Packet is returned by the Dynamixel Unit.
- [ ] Add a "Connection.scan_multiple_baudrate()" function (or
  "Connection.discover_devices()") (it probably won't work under Windows
  because of the COM port configuration in the Device Manager)
- [ ] Make Connection.send() method more robust? See:
    - ROS: http://docs.ros.org/diamondback/api/dynamixel_driver/html/dynamixel__io_8py_source.html#l00085
    - PyDynamixel: https://github.com/richard-clark/PyDynamixel/blob/master/pydynamixel/dynamixel.py#L295
    - PyPot: https://github.com/poppy-project/pypot/blob/master/pypot/dynamixel/io/abstract_io.py#L503
- [ ] Check how famous open source Python projects write:
    - [ ] setup.py
    - [ ] MANIFEST.in
    - [ ] sphinx documentation
    - [ ] docstrings (e.g. Sphinx style, Google/Numpy "Napoleon" sytle, ...)
- [ ] Fix remaining "TODO" tags.
- [ ] Improve the reliability of "Connection.send()".
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
- [ ] Use the following services and add webbadges ?
    - [ ] https://travis-ci.org/
    - [ ] https://coveralls.io/
    - [ ] https://landscape.io/
    - [ ] https://ci.appveyor.com/
    - [ ] ...
- [ ] Clone the git repository in the following forges ?
    - [ ] https://git.framasoft.org/
    - [ ] https://bitbucket.org/
    - [ ] https://about.gitlab.com/gitlab-com/ (https://about.gitlab.com)
          "(Gitorious was acquired by GitLab B.V., who announced service
          through gitorious.org will be discontinued on 1 June 2015 and
          encouraged Gitorious users to make use of its import tools to migrate
          projects to Gitlab)"
    - [ ] http://savannah.nongnu.org/
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
- [ ] On Windows, how to automatically update the PATH variable (for
  C:\PYTHON34\Scripts) from pip or from a .bat ?
- [ ] Say somewhere in the documentation that (by default), with pip, the
  package is installed in C:\PYTHON34\libs\site-packages\
- [ ] Add a RPM package.
- [ ] Check the PyAX-12 installation (with pip and dedicated packages) and
  examples:
    - [ ] on Windows XP/Vista/8/10;
    - [ ] on MacOSX;
    - [ ] on Ubuntu/Fedora/SuSE/Arch/Mint/...;
    - [ ] on Raspbian/...;
    - [ ] with Python 3.0/3.1/3.2/3.3;
    - [ ] with PySerial 2.5/2.4/...
- [ ] Write functions "Packet.print_info()" and "Connection.print_info()" to
  print "human readable" informations (e.g. "position=...°\nspeed=..." ;
  "baudrate=...\nport=...\n...") ?
- [ ] Some unit tests "requires to be connected to the Dynamixel number 1 using
  port "/dev/ttyUSB0" (thus it works on Unix systems only) at 57600 baud." ->
  fix it... (especially in test_status_packet)
- [ ] Write a tutorial to explain how to use PyAX-12 on a RaspberryPi using
  GPIOs (i.e. without the usbdynamixel adapter) and without the CM-5 (i.e. using
  a batteries, a LiPo or a DC lab power supply instead).
  - See: www.instructables.com/id/How-to-drive-Dynamixel-AX-12A-servos-with-a-Raspbe/?ALLSTEPS
  - See: www.oppedijk.com/robotics/control-dynamixel-with-raspberrypi
- [ ] Annoucements: raspberrypi.org, linuxfr, ...

## Misc

- [ ] Conform to google.github.io/styleguide/pyguide.html ?
- [ ] Write a MSI installer for Windows.
- [ ] Test "setup.py bdist_rpm ..." (create an RPM distribution)
- [ ] Test "setup.py bdist_wininst ..." (create an executable installer for MS Windows)
- [ ] Create a "pyax12gui" repository: a set of graphic tools (tkinter) on top
  of PyAX-12 to handle Dynamixels servos.


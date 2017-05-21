# Bugs

## Missing return packages using Raspberry Pi's GPIO (issue #3)

https://github.com/jeremiedecock/pyax12/issues/3

### Warning message

    RuntimeWarning: This channel is already in use, continuing anyway.

### Raspberry Pi Coockbook (Siomon Monk), recipe 8.7 "Freeing the serial port"

"By default, the serial port acts as a console, through which you can Raspberry Pi with sudo reboot.
To disable this so that you can use the serial port to connect to peripherals such as GPS ( Recipe 11.10 ), comment out a line in /etc/inittab:

    $ sudo nano /etc/inittab

Scroll down to the end of the file to find the line:

    T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100

Comment it out by placing a # in front of it:

    #T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100

Save the file with Ctrl-X followed by Y. For the changes to take effect, you need to reboot your Raspberry Pi with sudo reboot."

### UART issues with Raspberry Pi 3

See http://www.framboise314.fr/le-port-serie-du-raspberry-pi-3-pas-simple/ (in French).


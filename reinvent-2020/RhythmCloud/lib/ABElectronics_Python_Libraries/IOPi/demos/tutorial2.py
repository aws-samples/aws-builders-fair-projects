#!/usr/bin/env python
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tutorial 1

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python tutorial2.py
================================================

This example uses the write_pin and write_port methods to switch pin 1 on
and off on the IO Pi.
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    """
    Main program function
    """
    bus = IOPi(0x20)

    bus.set_pin_direction(1, 1)  # set pin 1 as an input

    bus.set_pin_direction(8, 0)  # set pin 8 as an output

    bus.write_pin(8, 0)  # turn off pin 8

    bus.set_pin_pullup(1, 1)  # enable the internal pull-up resistor on pin 1

    bus.invert_pin(1, 1)  # invert pin 1 so a button press will register as 1

    while True:

        if bus.read_pin(1) == 1:  # check to see if the button is pressed
            print('button pressed')  # print a message to the screen
            bus.write_pin(8, 1)  # turn on the led on pin 8
            time.sleep(2)  # wait 2 seconds
        else:
            bus.write_pin(8, 0)  # turn off the led on pin 8

if __name__ == "__main__":
    main()

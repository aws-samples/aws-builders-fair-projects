#!/usr/bin/env python

"""
================================================
ABElectronics IO Pi | Digital I/O Read Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_ioread.py
================================================

This example reads from all 16 pins on both buses on the IO Pi.
The internal pull-up resistors are enabled so each pin will read
as 1 unless the pin is connected to ground.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os

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
    iobus1 = IOPi(0x20)
    iobus2 = IOPi(0x21)

    # We will read the inputs 1 to 16 from the I/O bus so set port 0 and
    # port 1 to be inputs and enable the internal pull-up resistors
    iobus1.set_port_direction(0, 0xFF)
    iobus1.set_port_pullups(0, 0xFF)

    iobus1.set_port_direction(1, 0xFF)
    iobus1.set_port_pullups(1, 0xFF)

    # Repeat the steps above for the second bus
    iobus2.set_port_direction(0, 0xFF)
    iobus2.set_port_pullups(0, 0xFF)

    iobus2.set_port_direction(1, 0xFF)
    iobus2.set_port_pullups(1, 0xFF)

    while True:
        # clear the console
        os.system("clear")

        # read the pins 1 to 16 on both buses and print the results
        print("Bus 1                   Bus 2")
        print("Pin 1:  " + str(iobus1.read_pin(1)) +
              "               Pin 1:  " + str(iobus2.read_pin(1)))
        print("Pin 2:  " + str(iobus1.read_pin(2)) +
              "               Pin 2:  " + str(iobus2.read_pin(2)))
        print("Pin 3:  " + str(iobus1.read_pin(3)) +
              "               Pin 3:  " + str(iobus2.read_pin(3)))
        print("Pin 4:  " + str(iobus1.read_pin(4)) +
              "               Pin 4:  " + str(iobus2.read_pin(4)))
        print("Pin 5:  " + str(iobus1.read_pin(5)) +
              "               Pin 5:  " + str(iobus2.read_pin(5)))
        print("Pin 6:  " + str(iobus1.read_pin(6)) +
              "               Pin 6:  " + str(iobus2.read_pin(6)))
        print("Pin 7:  " + str(iobus1.read_pin(7)) +
              "               Pin 7:  " + str(iobus2.read_pin(7)))
        print("Pin 8:  " + str(iobus1.read_pin(8)) +
              "               Pin 8:  " + str(iobus2.read_pin(8)))
        print("Pin 9:  " + str(iobus1.read_pin(9)) +
              "               Pin 9:  " + str(iobus2.read_pin(9)))
        print("Pin 10: " + str(iobus1.read_pin(10)) +
              "               Pin 10: " + str(iobus2.read_pin(10)))
        print("Pin 11: " + str(iobus1.read_pin(11)) +
              "               Pin 11: " + str(iobus2.read_pin(11)))
        print("Pin 12: " + str(iobus1.read_pin(12)) +
              "               Pin 12: " + str(iobus2.read_pin(12)))
        print("Pin 13: " + str(iobus1.read_pin(13)) +
              "               Pin 13: " + str(iobus2.read_pin(13)))
        print("Pin 14: " + str(iobus1.read_pin(14)) +
              "               Pin 14: " + str(iobus2.read_pin(14)))
        print("Pin 15: " + str(iobus1.read_pin(15)) +
              "               Pin 15: " + str(iobus2.read_pin(15)))
        print("Pin 16: " + str(iobus1.read_pin(16)) +
              "               Pin 16: " + str(iobus2.read_pin(16)))

        # wait 0.5 seconds before reading the pins again
        time.sleep(0.1)

if __name__ == "__main__":
    main()

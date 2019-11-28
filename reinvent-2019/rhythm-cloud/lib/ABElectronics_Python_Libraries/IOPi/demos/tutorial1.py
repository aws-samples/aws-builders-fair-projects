#!/usr/bin/env python
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tutorial 1

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python tutorial1.py
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
    bus = IOPi(0x21)

    bus.set_port_direction(0, 0x00)
    bus.write_port(0, 0x00)

    while True:
        bus.write_pin(1, 1)
        time.sleep(1)
        bus.write_pin(1, 0)
        time.sleep(1)

if __name__ == "__main__":
    main()

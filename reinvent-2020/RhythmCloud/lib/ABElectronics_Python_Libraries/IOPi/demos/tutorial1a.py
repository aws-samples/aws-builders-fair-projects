#!/usr/bin/env python
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tutorial 1a

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python tutorial1a.py
================================================

This example uses the write_port method to count in binary using 8 LEDs
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

    bus.set_port_direction(0, 0x00)
    bus.write_port(0, 0x00)

    while True:
        for count in range(0, 255):
            bus.write_port(0, count)
            time.sleep(0.5)

        bus.write_port(0, 0x00)

if __name__ == "__main__":
    main()

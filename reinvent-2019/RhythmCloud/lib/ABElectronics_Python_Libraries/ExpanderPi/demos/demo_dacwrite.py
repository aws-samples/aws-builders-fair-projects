#!/usr/bin/env python
"""
================================================
ABElectronics Expander Pi | DAC Write Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_dacwrite.py
================================================

this demo will generate a 1.5V p-p square wave at 1Hz on channel 1
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

try:
    import ExpanderPi
except ImportError:
    print("Failed to import ExpanderPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        import ExpanderPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    '''
    Main program function
    '''
    dac = ExpanderPi.DAC(1)  # create a dac instance with  the gain set to 1

    while True:
        dac.set_dac_voltage(1, 1.5)  # set the voltage on channel 1 to 1.5V
        time.sleep(1)  # wait 1 seconds
        dac.set_dac_voltage(1, 0)  # set the voltage on channel 1 to 0V
        time.sleep(1)  # wait 1 seconds

if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
================================================
ABElectronics ADC Pi ACS712 30 Amp current sensor demo

Requires python smbus to be installed
run with: python demo_acs712_30.py
================================================

Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os

try:
    from ADCPi import ADCPi
except ImportError:
    print("Failed to import ADCPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCPi import ADCPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def calc_current(inval):
    '''
    change the 2.5 value to be half of the supply voltage.
    '''
    return ((inval) - 2.5) / 0.066


def main():
    '''
    Main program function
    '''

    adc = ADCPi(0x68, 0x69, 14)

    while True:

        # clear the console
        os.system('clear')

        # read from adc channels and print to screen
        print("Current on channel 1: %02f" % calc_current(adc.read_voltage(1)))

        # wait 0.5 seconds before reading the pins again
        time.sleep(0.5)

if __name__ == "__main__":
    main()

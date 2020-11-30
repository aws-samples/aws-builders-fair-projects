#!/usr/bin/env python
"""
================================================
ABElectronics ADC Differential Pi 8-Channel ADC Read Raw demo

Requires python smbus to be installed
run with: python demo_readraw.py
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
    from ADCDifferentialPi import ADCDifferentialPi
except ImportError:
    print("Failed to import ADCDifferentialPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCDifferentialPi import ADCDifferentialPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    '''
    Main program function
    '''

    adc = ADCDifferentialPi(0x68, 0x69, 18)

    while True:

        # clear the console
        os.system('clear')

        # read the raw value from adc channels and print to screen
        print("Channel 1: %d" % adc.read_raw(1))
        print("Channel 2: %d" % adc.read_raw(2))
        print("Channel 3: %d" % adc.read_raw(3))
        print("Channel 4: %d" % adc.read_raw(4))
        print("Channel 5: %d" % adc.read_raw(5))
        print("Channel 6: %d" % adc.read_raw(6))
        print("Channel 7: %d" % adc.read_raw(7))
        print("Channel 8: %d" % adc.read_raw(8))

        # wait 0.5 seconds before reading the pins again
        time.sleep(0.5)

if __name__ == "__main__":
    main()

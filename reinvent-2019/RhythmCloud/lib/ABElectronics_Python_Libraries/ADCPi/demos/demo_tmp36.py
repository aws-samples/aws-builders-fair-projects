#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
================================================
ABElectronics ADC Pi TMP36 temperature sensor demo

Requires python smbus to be installed
run with: python demo_tmp36.py
================================================

Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

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


def main():
    '''
    Main program function
    '''

    adc = ADCPi(0x68, 0x69, 18)

    while True:
        # Calculate the temperature
        # TMP36 returns 0.01 volts per C - -40C to +125C
        # 750mV = 25C and 500mV = 0C.  The temperature is (voltage / 0.01) - 50

        temperature = (adc.read_voltage(1)/0.01)-50

        # read from adc channels and print to screen
        print("Temperature on channel 1: %0.02f°C" % temperature)

        # wait 0.5 seconds before reading the pins again
        time.sleep(0.5)

if __name__ == "__main__":
    main()

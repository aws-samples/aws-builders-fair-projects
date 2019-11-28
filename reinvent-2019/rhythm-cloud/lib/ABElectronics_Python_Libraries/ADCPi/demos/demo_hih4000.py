#!/usr/bin/env python
"""
================================================
ABElectronics ADC Pi HIH4000 humidity sensor demo

Requires python smbus to be installed
run with: python demo_hih4000.py
================================================

The HIH4000 humidity sensor needs a load of at least 80K between the output
and ground pin so add a 100K resistor between the sensor output and the
ADC Pi input pin to make the sensor work correctly

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

RESISTOR_MULTIPLIER = 6.95225  # use 100K resistor in series with the input
ZERO_OFFSET = 0.826  # zero offset value from calibration data printout
SLOPE = 0.031483  # slope value from calibration data printout


def calc_humidity(inval):
    '''
    Calculate the humidity
    '''
    voltage = inval * RESISTOR_MULTIPLIER
    humidity = (voltage - ZERO_OFFSET) / SLOPE
    return humidity


def main():
    '''
    Main program function
    '''

    adc = ADCPi(0x68, 0x69, 14)

    while True:

        # clear the console
        os.system('clear')

        # read from adc channels and print to screen
        print("Humidity on channel 1: %0.1f%%" %
              calc_humidity(adc.read_voltage(1)))

        # wait 0.5 seconds before reading the pins again
        time.sleep(0.5)

if __name__ == "__main__":
    main()

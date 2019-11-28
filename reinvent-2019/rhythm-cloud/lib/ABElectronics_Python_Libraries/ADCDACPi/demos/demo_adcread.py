#!/usr/bin/env python

"""
================================================
ABElectronics ADC-DAC Pi 2-Channel ADC, 2-Channel DAC | ADC Read Demo

run with: python demo_adcread.py
================================================

this demo reads the voltage from channel 1 on the ADC inputs
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import time
import os

try:
    from ADCDACPi import ADCDACPi
except ImportError:
    print("Failed to import ADCDACPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCDACPi import ADCDACPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    '''
    Main program function
    '''

    # create an instance of the ADCDAC Pi with a DAC gain set to 1
    adcdac = ADCDACPi(1)

    # set the reference voltage.  this should be set to the exact voltage
    # measured on the raspberry pi 3.3V rail.
    adcdac.set_adc_refvoltage(3.3)

    while True:
        # clear the console
        os.system('clear')

        # read the voltage from channel 1 in single ended mode
        # and display on the screen

        print(adcdac.read_adc_voltage(1, 0))

        time.sleep(0.1)

if __name__ == "__main__":
    main()

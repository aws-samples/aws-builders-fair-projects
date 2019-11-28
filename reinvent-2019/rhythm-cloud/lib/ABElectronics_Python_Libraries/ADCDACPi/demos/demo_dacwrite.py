#!/usr/bin/env python
"""
================================================
ABElectronics ADCDAC Pi 2-Channel ADC, 2-Channel DAC | DAC Write Demo

run with: python demo_dacwrite.py
================================================

this demo will generate a 1.5V p-p square wave at 1Hz
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time

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

    while True:
        adcdac.set_dac_voltage(1, 1.5)  # set the voltage on channel 1 to 1.5V
        time.sleep(0.5)  # wait 0.5 seconds
        adcdac.set_dac_voltage(1, 0)  # set the voltage on channel 1 to 0V
        time.sleep(0.5)  # wait 0.5 seconds

if __name__ == "__main__":
    main()

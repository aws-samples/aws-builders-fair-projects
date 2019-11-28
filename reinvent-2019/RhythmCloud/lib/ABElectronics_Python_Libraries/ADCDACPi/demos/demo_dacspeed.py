#!/usr/bin/env python
"""
================================================
ABElectronics ADCDAC Pi 2-Channel ADC, 2-Channel DAC | DAC Speed Demo

run with: python demo_dacspeed.py
================================================

this demo will output a 3.3V square wave, testing the maximum speed of the DAC
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

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

    # create an instance of the ADCDAC Pi with a DAC gain set to 2
    adcdac = ADCDACPi(2)

    while True:
        adcdac.set_dac_raw(1, 4095)  # set the voltage on channel 1 to 3.3V
        adcdac.set_dac_raw(1, 0)  # set the voltage on channel 1 to 0V

if __name__ == "__main__":
    main()

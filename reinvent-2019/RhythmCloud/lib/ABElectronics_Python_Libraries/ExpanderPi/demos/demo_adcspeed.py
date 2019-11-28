#!/usr/bin/env python

"""
================================================
# ABElectronics Expander Pi | ADC Speed Demo
#
# Requires python smbus to be installed
# For Python 2 install with: sudo apt-get install python-smbus
# For Python 3 install with: sudo apt-get install python3-smbus
#
# run with: python demo_adcspeed.py
================================================

this demo tests the maximum sample speed for the ADC
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import numpy as N

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

    adc = ExpanderPi.ADC()  # create an instance of the ADC

    # set the reference voltage.  this should be set to the exact voltage
    # measured on the Expander Pi Vref pin.
    adc.set_adc_refvoltage(4.096)

    counter = 1
    totalsamples = 100000

    readarray = N.zeros(totalsamples)

    starttime = datetime.datetime.now()
    print("Start: " + str(starttime))

    while counter < totalsamples:
        # read the voltage from channel 1 and display on the screen
        readarray[counter] = adc.read_adc_voltage(1, 0)

        counter = counter + 1

    endtime = datetime.datetime.now()

    print("End: " + str(endtime))
    totalseconds = (endtime - starttime).total_seconds()

    samplespersecond = totalsamples / totalseconds

    print("%.2f samples per second" % samplespersecond)


if __name__ == "__main__":
    main()

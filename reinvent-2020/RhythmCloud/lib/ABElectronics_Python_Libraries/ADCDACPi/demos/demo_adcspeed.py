#!/usr/bin/env python

"""
================================================
ABElectronics ADC-DAC Pi 2-Channel ADC, 2-Channel DAC | ADC Speed Demo

run with: python demo_adcspeed.py
================================================

this demo tests the maximum sample speed for the ADC
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import numpy as N

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

    counter = 1
    totalsamples = 100000

    readarray = N.zeros(totalsamples)

    starttime = datetime.datetime.now()
    print("Start: " + str(starttime))

    while counter < totalsamples:
        # read the voltage from channel 1 and display on the screen
        readarray[counter] = adcdac.read_adc_voltage(1, 0)

        counter = counter + 1

    endtime = datetime.datetime.now()

    print("End: " + str(endtime))
    totalseconds = (endtime - starttime).total_seconds()

    samplespersecond = totalsamples / totalseconds

    print("%.2f samples per second" % samplespersecond)


if __name__ == "__main__":
    main()

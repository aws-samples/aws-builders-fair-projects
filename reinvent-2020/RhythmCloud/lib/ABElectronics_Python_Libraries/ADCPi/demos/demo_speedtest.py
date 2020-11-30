#!/usr/bin/env python
"""
================================================
ABElectronics ADC Pi 8-Channel ADC speed test demo

Requires python smbus to be installed
run with: python demo_speedtest.py
================================================

Initialise the ADC device using the default addresses and test the
samples per second at each bit rate

"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import datetime
import numpy as N


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


def sampleratecheck(adc, rate, samples):
    """
    This function calls read_adc_voltage for a specified
    number of samples and measures how long it takes to complete the task
    """
    # create a counter and array to store the sampled voltages
    counter = 1
    readarray = N.zeros(samples)

    # set the bit rate of the ADC to the specified rate
    adc.set_bit_rate(rate)

    starttime = datetime.datetime.now()

    while counter < samples:
        # read the voltage from channel 1
        readarray[counter] = adc.read_voltage(1)
        counter = counter + 1

    # stop the timer
    endtime = datetime.datetime.now()

    # calculate the samples per second and the average voltage
    totalseconds = (endtime - starttime).total_seconds()
    samplespersecond = samples / totalseconds

    print("Bit Rate: %i - %.2f samples per second" % (rate, samplespersecond))


def main():
    '''
    Main program function
    '''

    # create an instance of the ADCPi class
    adc = ADCPi(0x68, 0x69, 12)

    adc.set_conversion_mode(1)

    print("Testing ---- This may take some time")

    # 12 bit test - 100 samples
    sampleratecheck(adc, 12, 100)

    # 14 bit test - 100 samples
    sampleratecheck(adc, 14, 100)

    # 16 bit test - 100 samples
    sampleratecheck(adc, 16, 100)

    # 18 bit test - 100 samples
    sampleratecheck(adc, 18, 100)

if __name__ == "__main__":
    main()

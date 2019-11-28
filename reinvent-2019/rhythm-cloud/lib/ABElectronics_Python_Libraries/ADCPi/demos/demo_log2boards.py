#!/usr/bin/env python
"""
================================================
ABElectronics ADC Pi 8-Channel ADC data-logger demo

Requires python smbus to be installed
run with: python demo_log2boards.py
================================================

Initialise two ADC Pi boards using the  addresses 0x6A to 0x6D 
and sample rate to 12 bits

Sample rate can be 12,14, 16 or 18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import datetime

logtofile = True  # set to false if you want to log to the console

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


def writetofile(texttowrtite):
    '''
    Open the log file, write the value and close the file.
    '''
    if logtofile is True:
        file = open('adclog.txt', 'a')
        file.write(str(datetime.datetime.now()) + " " + texttowrtite)
        file.close()
    else:
        print(str(datetime.datetime.now()) + " " + texttowrtite)


def main():
    '''
    Main program function
    '''

    adc1 = ADCPi(0x6A, 0x6B, 12)
    adc2 = ADCPi(0x6C, 0x6D, 12)

    print("Logging...")

    while True:

        # read from adc channels on board 1 and write to the log file
        writetofile("Board 1 - Channel 1: %02f\n" % adc1.read_voltage(1))
        writetofile("Board 1 - Channel 2: %02f\n" % adc1.read_voltage(2))
        writetofile("Board 1 - Channel 3: %02f\n" % adc1.read_voltage(3))
        writetofile("Board 1 - Channel 4: %02f\n" % adc1.read_voltage(4))
        writetofile("Board 1 - Channel 5: %02f\n" % adc1.read_voltage(5))
        writetofile("Board 1 - Channel 6: %02f\n" % adc1.read_voltage(6))
        writetofile("Board 1 - Channel 7: %02f\n" % adc1.read_voltage(7))
        writetofile("Board 1 - Channel 8: %02f\n" % adc1.read_voltage(8))

        # read from adc channels on board 2 and write to the log file
        writetofile("Board 2 - Channel 1: %02f\n" % adc2.read_voltage(1))
        writetofile("Board 2 - Channel 2: %02f\n" % adc2.read_voltage(2))
        writetofile("Board 2 - Channel 3: %02f\n" % adc2.read_voltage(3))
        writetofile("Board 2 - Channel 4: %02f\n" % adc2.read_voltage(4))
        writetofile("Board 2 - Channel 5: %02f\n" % adc2.read_voltage(5))
        writetofile("Board 2 - Channel 6: %02f\n" % adc2.read_voltage(6))
        writetofile("Board 2 - Channel 7: %02f\n" % adc2.read_voltage(7))
        writetofile("Board 2 - Channel 8: %02f\n" % adc2.read_voltage(8))

        # wait 1 second before reading the pins again
        time.sleep(1)

if __name__ == "__main__":
    main()

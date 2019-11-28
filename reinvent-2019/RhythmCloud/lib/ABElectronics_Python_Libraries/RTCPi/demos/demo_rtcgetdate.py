#!/usr/bin/env python

"""
================================================
ABElectronics RTC Pi | Get Time Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_rtcgetdate.py
===============================================

This demo shows how to read the current time on the 
RTC Pi real-time clock at 1 second intervals
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import time

try:
    from RTCPi import RTC
except ImportError:
    print("Failed to import RTCPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from RTCPi import RTC
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    '''
    Main program function
    '''
    rtc = RTC()  # create a new instance of the RTC class

    while True:
        # read the date from the RTC in ISO 8601 format and print it
        print(rtc.read_date())
        time.sleep(1)  # wait 1 second

if __name__ == "__main__":
    main()

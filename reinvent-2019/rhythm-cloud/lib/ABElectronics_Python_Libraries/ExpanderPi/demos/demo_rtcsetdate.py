#!/usr/bin/env python

"""
================================================
ABElectronics Expander Pi | Set Time Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_rtcsetdate.py
===============================================

This demo shows how to set the time on the Expander Pi real-time clock
and then read the current time at 1 second intervals
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import time

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
    rtc = ExpanderPi.RTC()  # create a new instance of the RTC class

    # set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS
    rtc.set_date("2013-04-23T12:32:11")

    while True:
        # read the date from the RTC in ISO 8601 format and print it
        print(rtc.read_date())
        time.sleep(1)  # wait 1 second

if __name__ == "__main__":
    main()

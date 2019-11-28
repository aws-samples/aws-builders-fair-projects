#!/usr/bin/env python

"""
================================================
ABElectronics Expander Pi | RTC clock output demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_rtcout.py
================================================

This demo shows how to enable the clock square wave output on the
Expander Pi real-time clock and set the frequency
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

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

    # set the frequency of the output square-wave, options are: 1 = 1Hz, 2 =
    # 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
    rtc.set_frequency(3)
    rtc.enable_output()  # enable the square-wave

if __name__ == "__main__":
    main()

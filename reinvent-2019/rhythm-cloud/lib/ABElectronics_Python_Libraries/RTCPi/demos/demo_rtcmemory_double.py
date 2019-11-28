#!/usr/bin/env python

"""
================================================
ABElectronics RTC Pi | RTC memory double demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_rtcmemory_double.py
================================================

This demo shows how to write to and read from the internal battery
backed memory on the DS1307 RTC chip
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import struct

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


def double_to_array(val):
    '''
    convert a double into an eight byte array
    '''
    buf = bytearray(struct.pack('d', val))
    arraybytes = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 8):
        arraybytes[i] = buf[i]
    return arraybytes


def array_to_double(val):
    '''
    convert an eight byte array into a double
    '''
    dval, = struct.unpack('d', bytearray(val))
    return dval


def main():
    '''
    Main program function
    '''

    # create a new instance of the RTC class
    rtc = RTC()

    # number to be written to the RTC memory
    value = 0.0005
    print("Writing to memory: ", value)

    # convert the number into an array of bytes
    writearray = double_to_array(value)

    # write the array to the RTC memory
    rtc.write_memory(0x08, writearray)

    # read eight bytes from the RTC memory into an array
    read_array = rtc.read_memory(0x08, 8)

    # combine the array values into an number and print it
    print("Reading from memory: ", array_to_double(read_array))

if __name__ == "__main__":
    main()

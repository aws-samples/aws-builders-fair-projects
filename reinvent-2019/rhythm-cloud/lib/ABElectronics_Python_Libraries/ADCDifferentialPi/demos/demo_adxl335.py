#!/usr/bin/env python
"""
================================================
ABElectronics ADC Differential Pi 8-Channel ADC read ADXL335
SparkFun Triple Axis Accelerometer Breakout

The ADXL335 outputs are connected to inputs 1, 2 and 3 on
the ADC Differential Pi and the negative inputs are connected to GND

The inputs must run via a voltage divider to avoid damaging the ADC chips
inputs. The demo uses a 18K and 27K divider with the 18K connected to the
sensor board and the lower side of the 27K connected to GND

Requires python smbus to be installed
run with: python demo_adxl335.py
================================================

Initialise the ADC device using the default addresses and 12 bit sample rate,
change this value if you have changed the address selection jumpers
Bit rate can be 12,14, 16 or 18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os

try:
    from ADCDifferentialPi import ADCDifferentialPi
except ImportError:
    print("Failed to import ADCDifferentialPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCDifferentialPi import ADCDifferentialPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    '''
    Main program function
    '''

    adc = ADCDifferentialPi(0x68, 0x69, 14)

    # the conversion factor is the ratio of the voltage divider on the inputs
    conversionfactor = 1.666

    # setup these static values when the sensor is not moving
    x_static = 0.0
    y_static = 0.0
    z_static = 0.0

    x_max = 0.0
    x_min = 0.0
    y_max = 0.0
    y_min = 0.0
    z_max = 0.0
    z_min = 0.0

    # get 50 samples from each adc channel and use that to get an
    # average value for 0G.
    # Keep the accelerometer still while this part of the code is running
    for _ in range(0, 50):
        x_static = x_static + adc.read_voltage(1)
        y_static = y_static + adc.read_voltage(2)
        z_static = z_static + adc.read_voltage(3)
    x_static = (x_static / 50) * conversionfactor
    y_static = (y_static / 50) * conversionfactor
    z_static = (z_static / 50) * conversionfactor

    # loop forever reading the values and printing them to screen
    while True:
        # read from adc channels and print to screen

        x_force = ((adc.read_voltage(1) * conversionfactor) - x_static) / 0.3
        y_force = ((adc.read_voltage(2) * conversionfactor) - y_static) / 0.3
        z_force = ((adc.read_voltage(3) * conversionfactor) - z_static) / 0.3

        # Check values against max and min and update if needed
        if x_force >= x_max:
            x_max = x_force

        if x_force <= x_min:
            x_min = x_force

        if y_force >= y_max:
            y_max = y_force

        if y_force <= y_min:
            y_min = y_force

        if z_force >= z_max:
            z_max = z_force

        if z_force <= z_min:
            z_min = z_force

        # clear the console
        os.system('clear')

        # print values to screen
        print("X: %02f" % x_force)
        print("Y: %02f" % y_force)
        print("Z: %02f" % z_force)
        print("Max X: %02f" % x_max)
        print("Min X: %02f" % x_min)

        print("Max Y: %02f" % y_max)
        print("Min Y: %02f" % y_min)

        print("Max Z: %02f" % z_max)
        print("Min Z: %02f" % z_min)

        print("X Static Voltage: %02f" % x_static)
        print("Y Static Voltage: %02f" % y_static)
        print("Z Static Voltage: %02f" % z_static)

        # wait 0.05 seconds before reading the pins again
        time.sleep(0.05)

if __name__ == "__main__":
    main()

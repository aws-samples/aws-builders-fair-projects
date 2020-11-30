#!/usr/bin/env python
"""
================================================
ABElectronics Servo Pi pwm controller | PWM output demo

run with: python demo_pwm.py
================================================

This demo shows how to set a 1KHz output frequency and change the pulse width
between the minimum and maximum values
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

try:
    from ServoPi import PWM
except ImportError:
    print("Failed to import ServoPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from ServoPi import PWM
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    """
    Main program function
    """

    # create an instance of the PWM class on i2c address 0x40
    pwm = PWM(0x40)

    # Set PWM frequency to 1 Khz and enable the output
    pwm.set_pwm_freq(1000)
    pwm.output_enable()

    while True:
        for count in range(1, 4095, 5):
            pwm.set_pwm(1, 0, count)
        for count in range(4095, 1, -5):
            pwm.set_pwm(1, 0, count)

if __name__ == "__main__":
    main()

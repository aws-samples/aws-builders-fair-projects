#!/usr/bin/env python
"""
================================================
ABElectronics Servo Pi pwm controller | PWM all call i2c address demo

run with: python demo_setallcalladdress.py
================================================

This demo shows how to set the I2C address for the All Call function
All Call allows you to control several Servo Pi boards simultaneously
on the same I2C address
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

    # Set the all call address to 0x30
    pwm.set_allcall_address(0x30)

    # Disable the all call address
    #  pwm.disable_allcall_address()

    # Enable the all call address
    #  pwm.enable_allcall_address()

if __name__ == "__main__":
    main()

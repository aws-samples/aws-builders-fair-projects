#!/usr/bin/env python
"""
================================================
ABElectronics IO Pi | - Tutorial 3

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python tutorial3.py
================================================

This tutorial shows how to use interrupts on the IO Pi Plus.
Port 0 on Bus 1 is set as inputs with pull-ups enabled and the pins inverted.
Port 0 on Bus 2 is set as outputs.
When a button is pressed on port 0 on bus 1 an interrupt is triggered.
The interrupt value is read and the value is used to set the output bus 2.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    '''
    Main program function
    '''
    # Create two instances of the IOPi class with
    # I2C addresses of 0x20 and 0x21
    busin = IOPi(0x20)
    busout = IOPi(0x21)

    # Set port 0 on the busin bus to be inputs with internal pull-ups enabled.

    busin.set_port_pullups(0, 0xFF)
    busin.set_port_direction(0, 0xFF)

    # Invert the port so pins will show 1 when grounded
    busin.invert_port(0, 0xFF)

    # Set port 0 on busout to be outputs and set the port to be off
    busout.set_port_direction(0, 0x00)
    busout.write_port(0, 0x00)

    # Set the interrupts default value for port 0 to 0x00 so the interrupt
    # will trigger when any pin registers as true
    busin.set_interrupt_defaults(0, 0x00)

    # Set the interrupt type to be 1 on each pin for port 0 so an interrupt is
    # fired when the pin matches the default value
    busin.set_interrupt_type(0, 0xFF)

    # Enable interrupts for all pins on port 0
    busin.set_interrupt_on_port(0, 0xFF)

    # Reset the interrupts
    busin.reset_interrupts()

    while True:

        # read the interrupt status for each port.

        if (busin.read_interrupt_status(0) != 0):
            # If the status is not 0 then an interrupt has occured
            # on one of the pins so read the value from the interrupt capture
            value = busin.read_interrupt_capture(0)

            # write the value to port 0 on the busout bus
            busout.write_port(0, value)

        # sleep 200ms before checking the pin again
        time.sleep(0.2)


if __name__ == "__main__":
    main()

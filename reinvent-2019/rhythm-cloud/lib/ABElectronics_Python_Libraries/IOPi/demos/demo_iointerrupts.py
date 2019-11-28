#!/usr/bin/env python
"""
================================================
ABElectronics IO Pi | - IO Interrupts Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_iointerrupts.py
================================================

This example shows how to use the interrupt methods on the IO port.
Both ports will be set as inputs with pull-ups enabled and the 
pins inverted so they will show as on when connected to ground
The interrupts will be enabled and set so that 
ports 0 and 1 will trigger INT A and B respectively.
Using the read_interrupt_capture or read_port methods will
reset the interrupts.

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
    # Create an instance of the IOPi class with an I2C address of 0x20
    iobus = IOPi(0x20)

    # Set all pins on the IO bus to be inputs with internal pull-ups enabled.

    iobus.set_port_pullups(0, 0xFF)
    iobus.set_port_pullups(1, 0xFF)
    iobus.set_port_direction(0, 0xFF)
    iobus.set_port_direction(1, 0xFF)

    # Invert both ports so pins will show 1 when grounded
    iobus.invert_port(0, 0xFF)
    iobus.invert_port(1, 0xFF)

    # Set the interrupt polarity to be active high and mirroring disabled, so
    # pins 1 to 8 trigger INT A and pins 9 to 16 trigger INT B
    iobus.set_interrupt_polarity(1)
    iobus.mirror_interrupts(0)

    # Set the interrupts default value to 0x00 so the interrupt will trigger when any pin registers as true
    iobus.set_interrupt_defaults(0, 0x00)
    iobus.set_interrupt_defaults(1, 0x00)

    # Set the interrupt type to be 1 for ports A and B so an interrupt is
    # fired when the pin matches the default value
    iobus.set_interrupt_type(0, 0xFF)
    iobus.set_interrupt_type(1, 0xFF)

    # Enable interrupts for all pins
    iobus.set_interrupt_on_port(0, 0xFF)
    iobus.set_interrupt_on_port(1, 0xFF)

    while True:

        # read the interrupt status for each port.  
        # If the status is not 0 then an interrupt has occured on one of the pins 
        # so read the value from the interrupt capture.

        if (iobus.read_interrupt_status(0) != 0):
            print("Port 0: " + str(iobus.read_interrupt_capture(0)))
        if (iobus.read_interrupt_status(1) != 0):
            print("Port 1: " + str(iobus.read_interrupt_capture(1)))

        time.sleep(2)


if __name__ == "__main__":
    main()

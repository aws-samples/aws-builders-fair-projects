#!/usr/bin/env python
"""
================================================
ABElectronics Expander Pi | - IO Interrupts Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_iointerrupts.py
================================================

This example shows how to use the interrupt methods on the Expander Pi IO port.
The interrupts will be enabled and set so that a voltage applied
to pins 1 and 16 will trigger INT A and B respectively.
Using the read_interrupt_capture or read_port methods will
reset the interrupts.

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
    # Create an instance of the IO class called iobus.
    iobus = ExpanderPi.IO()

    # Set all pins on the IO bus to be inputs with internal pull-ups disabled.

    iobus.set_port_pullups(0, 0x00)
    iobus.set_port_pullups(1, 0x00)
    iobus.set_port_direction(0, 0xFF)
    iobus.set_port_direction(1, 0xFF)

    # Set the interrupt polarity to be active high and mirroring disabled, so
    # pins 1 to 8 trigger INT A and pins 9 to 16 trigger INT B
    iobus.set_interrupt_polarity(1)
    iobus.mirror_interrupts(0)

    # Set the interrupts default value to trigger when 5V is applied to pins 1
    # and 16
    iobus.set_interrupt_defaults(0, 0x01)
    iobus.set_interrupt_defaults(0, 0x80)

    # Set the interrupt type to be 1 for ports A and B so an interrupt is
    # fired when the pin matches the default value
    iobus.set_interrupt_type(0, 1)
    iobus.set_interrupt_type(1, 1)

    # Enable interrupts for pins 1 and 16
    iobus.set_interrupt_on_pin(1, 1)
    iobus.set_interrupt_on_pin(16, 1)

    while True:

        # read the port value from the last capture for ports 0 and 1.
        # This will reset the interrupts
        print(iobus.read_interrupt_capture(0))
        print(iobus.read_interrupt_capture(1))
        time.sleep(2)


if __name__ == "__main__":
    main()

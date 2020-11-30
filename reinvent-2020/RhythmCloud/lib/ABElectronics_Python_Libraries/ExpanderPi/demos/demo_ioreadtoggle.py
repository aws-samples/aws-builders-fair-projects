#!/usr/bin/env python

"""
================================================
ABElectronics Expander Pi | Digital I/O Read Toggle Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_ioreadtoggle.py
================================================

This example reads the input from pin 1 and toggles an output variable
on each button press.
The internal pull-up resistors are enabled so the input pin can be toggled
by connecting it to ground.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os

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
    iobus = ExpanderPi.IO()

    # We will read the input on pin 1 on the I/O bus so set pin 1 as an input
    # and enable the internal pull-up resistors
    iobus.set_pin_direction(1, 1)
    iobus.set_pin_pullup(1, 1)

    # Invert pin 1 so pressing the button will be read as 1 instead of 0
    iobus.invert_pin(1, 1)

    # create a variable to store the toggle state of the input

    pin1_toggle_state = 0

    # to stop the value from toggling on every loop we will set
    # a variable to store the state from the previous loop
    pin1_last_state = 0

    # clear the console
    os.system('clear')

    while True:
        # read the value from pin 1 into a temporary variable
        pin1_val = iobus.read_pin(1)

        # check to see if the pin state has changed since the last loop
        if pin1_val != pin1_last_state:

            if pin1_val == 1:  # pin has been pressed

                pin1_toggle_state = not pin1_toggle_state  # invert the value
                print("Button state changed to " + str(pin1_toggle_state))

            pin1_last_state = pin1_val

        # wait 0.1 seconds before reading the pins again
        time.sleep(0.1)

if __name__ == "__main__":
    main()

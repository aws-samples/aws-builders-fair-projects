#!/usr/bin/env python
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tkinter GUI Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_guiwrite.py
================================================

This example creates a GUI using Tkinter with 16 buttons and uses
the write_pin method to switch the pins on Bus 2 on the IO Pi on and off.

Initialises the IOPi device using the default address
for Bus 2, you will need to change the addresses if you have changed
the jumpers on the IO Pi
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

# check the python version and import the correct version of tkinter
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        sys.path.append('..')
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


class App:
    """
    Application Class
    """

    bus2 = None

    def __init__(self, master):
        """
        __init__ is called at startup
        """

        # create an instance of Bus 2 which is on I2C address 0x21 by default
        self.bus2 = IOPi(0x21)

        # set pins 1 to 8 to be outputs and turn them off
        self.bus2.set_port_direction(0, 0x00)
        self.bus2.write_port(0, 0x00)

        # set pins 9 to 16 to be outputs and turn them off
        self.bus2.set_port_direction(1, 0x00)
        self.bus2.write_port(1, 0x00)

        self.build_ui(master)

    def build_ui(self, master):
        """
        Build the UI using tkinter components
        """
        frame = tk.Frame(master)  # create a frame for the GUI
        frame.pack()

        # create 16 buttons which run the toggle function when pressed
        self.button = tk.Button(frame,
                                text="Pin 1", command=lambda: self.toggle(1))
        self.button.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 2", command=lambda: self.toggle(2))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 3", command=lambda: self.toggle(3))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 4", command=lambda: self.toggle(4))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 5", command=lambda: self.toggle(5))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 6", command=lambda: self.toggle(6))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 7", command=lambda: self.toggle(7))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 8", command=lambda: self.toggle(8))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 9", command=lambda: self.toggle(9))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 10", command=lambda: self.toggle(10))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 11", command=lambda: self.toggle(11))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 12", command=lambda: self.toggle(12))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 13", command=lambda: self.toggle(13))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 14", command=lambda: self.toggle(14))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 15", command=lambda: self.toggle(15))
        self.slogan.pack(side=tk.LEFT)

        self.slogan = tk.Button(frame,
                                text="Pin 16", command=lambda: self.toggle(16))
        self.slogan.pack(side=tk.LEFT)

    def toggle(self, pin):
        """
        read the status from the selected pin, invert it and write it
        back to the pin
        """
        pinstatus = self.bus2.read_pin(pin)
        if pinstatus == 1:
            pinstatus = 0
        else:
            pinstatus = 1
        self.bus2.write_pin(pin, pinstatus)

ROOT = tk.Tk()
APP = App(ROOT)
ROOT.mainloop()

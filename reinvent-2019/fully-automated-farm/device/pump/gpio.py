#!/usr/bin/python3
# -*- Coding: utf-8 -*-

import pigpio
from time import sleep

gpio = pigpio.pi()

class Output:
    def __init__(self, pin):
        self.pin = pin
        gpio.set_mode(pin, pigpio.OUTPUT)
        
    def high(self):
        gpio.write(self.pin, 1)
        print(f"Output high {self.pin}")

    def low(self):
        gpio.write(self.pin, 0)
        print(f"Output low {self.pin}")

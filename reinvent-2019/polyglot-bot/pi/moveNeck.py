"""Just for namaste"""
import time
from adafruit_servokit import ServoKit
import os
import RPi.GPIO as GPIO




# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)




#Move hand
time.sleep(1)
kit.servo[0].angle = 120
time.sleep(3)
kit.servo[0].angle = 90
time.sleep(1)
kit.servo[0].angle = 60
time.sleep(1)
kit.servo[0].angle = 90
time.sleep(1)
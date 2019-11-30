"""Just for namaste"""

import time
from adafruit_servokit import ServoKit
import os
import RPi.GPIO as GPIO




# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)


#Move hands
kit.servo[15].angle = 130
time.sleep(2)
kit.servo[12].angle = 110
time.sleep(2)
kit.servo[13].angle = 150

time.sleep(2)
kit.servo[13].angle = 90
time.sleep(2)
kit.servo[13].angle = 150
time.sleep(2)
kit.servo[13].angle = 90
time.sleep(2)
#back to original position

kit.servo[2].angle = 0
kit.servo[13].angle = 0
time.sleep(2)
kit.servo[12].angle = 15
kit.servo[3].angle = 180
kit.servo[15].angle = 145
GPIO.cleanup()
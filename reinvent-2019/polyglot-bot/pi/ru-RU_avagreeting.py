"""Hi or Hola"""
import time
from adafruit_servokit import ServoKit
import os


# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

kit = ServoKit(channels=16)
kit.servo[12].angle = 0 #Servo right elbow initial position

time.sleep(0.5)

kit.servo[12].angle = 30  #Servo right shoulder up
time.sleep(0.5)
kit.servo[12].angle = 60
time.sleep(0.5)
kit.servo[12].angle = 180
time.sleep(1)
kit.servo[15].angle = 120
time.sleep(1)
kit.servo[15].angle = 145
time.sleep(1)

kit.servo[12].angle = 90
time.sleep(0.5)
kit.servo[12].angle = 60
time.sleep(0.5)
kit.servo[12].angle = 30
kit.servo[12].angle = 15 #Servo right elbow initial position
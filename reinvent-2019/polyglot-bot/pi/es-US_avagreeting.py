"""Hi or Hola"""
import time
from adafruit_servokit import ServoKit
import os
import RPi.GPIO as GPIO
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.

kit = ServoKit(channels=16)
kit.servo[12].angle = 0 #Servo right elbow initial position

time.sleep(0.5)

kit.servo[12].angle = 30  #Servo right shoulder up
time.sleep(0.5)
kit.servo[12].angle = 60
time.sleep(0.5)
kit.servo[12].angle = 150
time.sleep(3)
kit.servo[12].angle = 90
time.sleep(0.5)
kit.servo[12].angle = 30
time.sleep(0.5)
kit.servo[12].angle = 30
kit.servo[12].angle = 15 #Servo right elbow initial position
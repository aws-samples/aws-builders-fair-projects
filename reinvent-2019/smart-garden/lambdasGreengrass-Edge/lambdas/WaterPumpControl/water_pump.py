import sys
import time
import os
import logging
import RPi.GPIO as GPIO

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vendored/'))

import greengrasssdk

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class WaterPumpControl:
    WATER_PUMP_PIN = 3
    RELEASE_DURATION = 4 # seconds

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup([self.WATER_PUMP_PIN], GPIO.OUT, initial=GPIO.HIGH)

    def on(self):
        logging.info('Turning on pump')
        GPIO.output([self.WATER_PUMP_PIN], GPIO.LOW)

    def off(self):
        logging.info('Turning off pump')
        GPIO.output([self.WATER_PUMP_PIN], GPIO.HIGH)

    def release(self, duration=None):
        if not duration:
            duration = self.RELEASE_DURATION

        logging.info('Releasing water for {} seconds'.format(duration))
        self.on()
        time.sleep(duration)
        self.off()

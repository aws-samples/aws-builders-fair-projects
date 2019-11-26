from .actuator import Actuator
import RPi.GPIO as GPIO

class GrowLight(Actuator):
    def __init__(self):
        Actuator.__init__(self)
        
        self.gpio = int(self.config["gpio"]["light"]) 

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio, GPIO.HIGH)

    def on(self):
        super().on()
        GPIO.output(self.gpio, GPIO.LOW)

    def off(self):
        super().off()
        GPIO.output(self.gpio, GPIO.HIGH)

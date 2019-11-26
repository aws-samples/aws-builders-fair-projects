from .actuator import Actuator
import RPi.GPIO as GPIO

class Pump(Actuator):
    def __init__(self, no):
        Actuator.__init__(self)

        self.gpio = int(self.config["gpio"]["pump" + str(no)])

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio, GPIO.HIGH)

    def on(self):
        super().on()
        GPIO.output(self.gpio, GPIO.LOW)

    def off(self):
        super().off()
        GPIO.output(self.gpio, GPIO.HIGH)

import os
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()

channel = int(os.environ['LED_CHANNEL'])

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT) # green
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

if __name__ == "__main__":
  try:
    while True:
      print('red')
      GPIO.output(21, 1)
      GPIO.output(20, 1)
      GPIO.output(16, 1)
      time.sleep(2)
      print('testing led...setting low')

      GPIO.output(21, 0)
      GPIO.output(20, 0)
      GPIO.output(16, 0)

      time.sleep(1)
  except KeyboardInterrupt:
    GPIO.cleanup()

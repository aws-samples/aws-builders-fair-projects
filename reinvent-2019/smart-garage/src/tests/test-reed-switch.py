import os
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()

switchChannel = int(os.environ['SWITCH_CHANNEL'])

class ReedSwitch:
  def __init__(self, channel):
    self.lastState = ''
    self.state = ''
    self.channel = channel
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  def getState(self):
    return GPIO.input(self.channel)

  def _setState(self):
    self.state = self.getState()

  def monitor(self):
    print('monitoring for new state')

    while True:
      self._setState()
      if self.state != self.lastState:
        print('new state ', self.state)
        self.lastState = self.state
      time.sleep(1)

if __name__ == "__main__":
  reedSwitch = ReedSwitch(switchChannel)
  reedSwitch.monitor()

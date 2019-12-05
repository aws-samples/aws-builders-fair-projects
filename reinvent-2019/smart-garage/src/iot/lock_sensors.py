import time
import RPi.GPIO as GPIO
import coloredlogs
import logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)


class LockSensors:
  def __init__(self, lockChannel, relayChannel):
    self.lastState = ''
    self.state = ''
    self.lockChannel = lockChannel
    self.relayChannel = relayChannel

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.lockChannel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.relayChannel, GPIO.OUT)

    self._init()

  def _init(self):
    GPIO.output(self.relayChannel, GPIO.HIGH)
    self.setState()
    self.syncState()
    logger.info('Reset initial lock state to: {}'.format(self.state))

  def stateChanged(self):
    return self.state != self.lastState

  def syncState(self):
    self.lastState = self.state

  def getState(self):
    return GPIO.input(self.lockChannel)

  def setState(self):
    self.state = self.getState()

  def _toggleLock(self):
    GPIO.output(self.relayChannel, not GPIO.input(self.relayChannel))
    time.sleep(0.5)
    GPIO.output(self.relayChannel, GPIO.HIGH)

  def lock(self):
    logger.info('Locking...')
    self._toggleLock()

  def unlock(self):
    logger.info('Unlocking...')
    self._toggleLock()

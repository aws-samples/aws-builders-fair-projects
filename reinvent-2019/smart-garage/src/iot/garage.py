import coloredlogs
import logging
import os
import time
import json
import watchtower
from dotenv import load_dotenv
from iot_client import IoTClient
from lock_sensors import LockSensors

load_dotenv()
PROJECT_NAME = "smart-garage"
iotThingName = os.environ['IOT_THING_NAME']
iotEndpoint = os.environ['IOT_ENDPOINT']
lockChannel = int(os.environ['LOCK_SENSOR_CHANNEL'])
relayChannel = int(os.environ['RELAY_CHANNEL'])
topic = "dt/{}/{}/control".format(PROJECT_NAME, iotThingName)

logging.basicConfig(filename='garage.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(iotThingName)
coloredlogs.install(level='INFO', logger=logger)
logger.addHandler(watchtower.CloudWatchLogHandler(log_group="/{}/{}".format(PROJECT_NAME, iotThingName), stream_name="{logger_name}-{strftime:%Y-%m-%d}"))

class Garage:
  def __init__(self):
    self.iot = IoTClient(thingName=iotThingName, iotEndpoint=iotEndpoint)
    self.lock = LockSensors(lockChannel=lockChannel, relayChannel=relayChannel)
    self.lockStateMapping = {}
    self.lockStateMapping[0] = "locked"
    self.lockStateMapping[1] = "unlocked"

  def onDeviceControl(self, client, userdata, message):
    print('Received control data on topic: {}'.format(message.topic))
    payload = json.loads(message.payload)
    if payload['device_name'] == iotThingName:

      lockStatus = self.lockStateMapping[self.lock.getState()]

      if payload['desired_state'] == 'unlock' and lockStatus == 'locked':
        self.lock.unlock()
      elif payload['desired_state'] == 'lock' and lockStatus == 'unlocked':
        self.lock.lock()

  def monitor(self):
    logger.info('Monitoring for new lock state')
    self.iot.subscribe(topic, qos=0, callback=self.onDeviceControl)

    while True:
      try:
        self.lock.setState()
        if self.lock.stateChanged():
          isUnlocked = self.lock.getState()
          lockStatus = self.lockStateMapping[isUnlocked]
          logger.info('New state: {}'.format(lockStatus))
          self.lock.syncState()

          logger.info("Update shadow with is_open: {}".format(bool(isUnlocked)))
          self.iot.updateShadow(isOpen=isUnlocked)
      except Exception as e:
        logger.error(e)

      time.sleep(1)

if __name__ == "__main__":
  garage = Garage()
  garage.monitor()

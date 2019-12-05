import json
import coloredlogs
import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from pathlib import Path

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)

certsPath = Path.cwd().joinpath('src', 'iot', 'certs')
rootCA = str(certsPath.joinpath("AmazonRootCA1.pem"))
privateKey = str(certsPath.joinpath("64321ad229-private.pem.key"))
certFile = str(certsPath.joinpath("64321ad229-certificate.pem.crt"))

class IoTClient:
  def __init__(self, thingName, iotEndpoint, rootCA=rootCA, privateKey=privateKey, certFile=certFile):
    self.rootCA = rootCA
    self.privateKey = privateKey
    self.certFile = certFile
    self.iotEndpoint = iotEndpoint
    self.thingName = thingName
    self.shadowClient = AWSIoTMQTTShadowClient(self.thingName)
    self.deviceShadow = None
    self.mqttClient = None
    self.connect()

  def connect(self):
    self.shadowClient.configureEndpoint(self.iotEndpoint, 8883)
    self.shadowClient.configureCredentials(self.rootCA, self.privateKey, self.certFile)
    self.shadowClient.configureConnectDisconnectTimeout(10)
    self.shadowClient.configureMQTTOperationTimeout(5)
    self.shadowClient.connect()

  def getShadowClient(self):
    return self.shadowClient

  def getDeviceShadow(self):
    if self.deviceShadow:
      return self.deviceShadow

    self.deviceShadow = self.shadowClient.createShadowHandlerWithName(self.thingName, True)

    return self.deviceShadow

  def getMQTT(self):
    if self.mqttClient:
      return self.mqttClient

    self.mqttClient = self.shadowClient.getMQTTConnection()

    return self.mqttClient

  def onShadowUpdate(self, payload, responseStatus, token):
    if (responseStatus != "accepted"):
      logger.error("Problem with shadow update: {}".format(responseStatus))

  def publish(self, topic, payload):
    self.getMQTT().publish(topic, json.dumps(payload), 1)

  def subscribe(self, topic, qos, callback):
    self.getMQTT().subscribe(topic, qos, callback)

  def updateShadow(self, isOpen):
    payload = {
      "state": {
        "reported": {
          "is_open": bool(isOpen),
          "device_name": self.thingName
        }
      }
    }
    self.getDeviceShadow().shadowUpdate(json.dumps(payload), self.onShadowUpdate, 5)

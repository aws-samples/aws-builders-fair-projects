import json
import logging
import os
import sys
import uuid

from AWSIoTPythonSDK.core.greengrass.discovery.providers import \
    DiscoveryInfoProvider
from AWSIoTPythonSDK.exception.AWSIoTExceptions import \
    DiscoveryInvalidRequestException
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

GROUP_CA_PATH = "./groupCA/"

logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


class GGDiscovery():
    def checkfile(self, f):
        if not os.path.exists(f):
            print("{} is not found.".format(f))
        
    def __init__(self, host, rootCAPath, certificatePath, privateKeyPath, thingName, gropCaDeleteOnExit=True):

        self.checkfile(rootCAPath)
        self.checkfile(certificatePath)
        self.checkfile(privateKeyPath)

        self.discoveryInfoProvider = DiscoveryInfoProvider()
        self.discoveryInfoProvider.configureEndpoint(host)
        self.discoveryInfoProvider.configureCredentials(
            rootCAPath, certificatePath, privateKeyPath)
        self.discoveryInfoProvider.configureTimeout(10)
        self.certificatePath = certificatePath
        self.privateKeyPath = privateKeyPath
        self.thingName = thingName
        self.discovered = False
        self.gropCaDeleteOnExit = gropCaDeleteOnExit

    def discover(self):
        try:
            discoveryInfo = self.discoveryInfoProvider.discover(self.thingName)
            caList = discoveryInfo.getAllCas()
            coreList = discoveryInfo.getAllCores()

            self.groupId, self.ca = caList[0]
            self.coreInfo = coreList[0]
            self.groupCA = GROUP_CA_PATH + self.groupId + \
                "_CA_" + str(uuid.uuid4()) + ".crt"
            if not os.path.exists(GROUP_CA_PATH):
                os.makedirs(GROUP_CA_PATH)
            groupCAFile = open(self.groupCA, "w")
            groupCAFile.write(self.ca)
            groupCAFile.close()
            self.discovered = True
        except DiscoveryInvalidRequestException as e:
            print("Invalid discovery request detected!")
            print("Type: %s" % str(type(e)))
            print("Error message: %s" % e.message)
            raise e
        except BaseException as e:
            print("Error in discovery!")
            print("Type: %s" % str(type(e)))
            print("Error message: %s" % e.message)

    def remove_group_ca(self):
        if self.gropCaDeleteOnExit and self.discovered:
            os.remove(self.groupCA)


class MQTTClient():
    def __init__(self, groupCA, privateKeyPath, certificatePath, thingName, customOnMessage=None):
        self.mqttClient = AWSIoTMQTTClient(thingName)
        self.mqttClient.configureCredentials(
            groupCA, privateKeyPath, certificatePath)
        self.customOnMessage = customOnMessage
        self.mqttClient.onMessage = self.onMessage
        self.connected = False

    def onMessage(self, message):
        if self.customOnMessage:
            self.customOnMessage(message)

    def connect(self, host, port):
        self.mqttClient.configureEndpoint(host, port)
        try:
            self.mqttClient.connect()
            self.connected = True
        except BaseException as e:
            raise e

    def subscribe(self, topic):
        self.mqttClient.subscribe(topic, 0, None)

    def publish(self, topic, obj, qos=0):
        messageJson = json.dumps(obj)
        self.mqttClient.publish(topic, messageJson, qos)


class GGThing(MQTTClient, object):
    def __init__(self, ggDiscovery, customOnMessage=None):
        super(GGThing, self).__init__(ggDiscovery.groupCA, ggDiscovery.privateKeyPath,
                         ggDiscovery.certificatePath, ggDiscovery.thingName, customOnMessage)
        self.ggDiscovery = ggDiscovery

    def connect(self):
        for connectivityInfo in self.ggDiscovery.coreInfo.connectivityInfoList:
            currentHost = connectivityInfo.host
            currentPort = connectivityInfo.port
            print("Trying to connect to core at %s:%d" %
                  (currentHost, currentPort))
            try:
                super().connect(currentHost, currentPort)
                break
            except BaseException as e:
                print("Error in connect!")
                print("Type: %s" % str(type(e)))
                print("Error message: %s" % e)

        if not self.connected:
            print("Cannot connect to core %s. Exiting..." %
                  self.ggDiscovery.coreInfo.coreThingArn)
            sys.exit(-2)

#!/usr/bin/python3
# -*- Coding: utf-8 -*-

import argparse
import json
import os
import sys
import threading
import time
import uuid

from AWSIoTPythonSDK.core.greengrass.discovery.providers import \
    DiscoveryInfoProvider
from AWSIoTPythonSDK.exception.AWSIoTExceptions import \
    DiscoveryInvalidRequestException
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


GROUP_CA_PATH = "./groupCA/"
GG_DISCOVERY_HOST = "greengrass-ats.iot.us-west-2.amazonaws.com"


class GgDiscovery():
    def __init__(self, host, rootCAPath, certificatePath, privateKeyPath, thingName, gropCaDeleteOnExit=True):
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
            print("Error message: %s" % e)

    def __del__(self):
        if self.gropCaDeleteOnExit and self.discovered:
            os.remove(self.groupCA)


class MqttClient():
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

    def publish(self, topic, obj):
        messageJson = json.dumps(obj)
        self.mqttClient.publish(topic, messageJson, 0)


class GGThing(MqttClient):
    def __init__(self, ggDiscovery, customOnMessage=None):
        super().__init__(ggDiscovery.groupCA, ggDiscovery.privateKeyPath,
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


SENSOR_PORT = 0


def analogRead():
    try:
        return grovepi.analogRead(SENSOR_PORT)
    except IOError:
        print("Sensor IOError")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", action="store",
                        default=GG_DISCOVERY_HOST, dest="host", help="Your GG discovery Endpoint")
    parser.add_argument("-r", "--rootCA", action="store",
                        default="./root.pem", dest="rootCAPath", help="Root CA file path")
    parser.add_argument("-c", "--cert", action="store",
                        dest="certificatePath", default="./cert.pem", help="Certificate file path")
    parser.add_argument("-k", "--key", action="store",
                        dest="privateKeyPath", default="./private.pem", help="Private key file path")
    parser.add_argument("-n", "--thingName", action="store",
                        dest="thingName", default="MoistureSensor1", help="Targeted thing name")
    parser.add_argument("-t", "--topic", action="store", dest="topic",
                        default="moisture/sensor1", help="Targeted topic")

    args = parser.parse_args()

    discovery = GgDiscovery(args.host, args.rootCAPath,
                            args.certificatePath, args.privateKeyPath, args.thingName)
    discovery.discover()
    thing = GGThing(discovery)
    thing.connect()

    while(True):
        message = {}
        message['moisture'] = analogRead()
        thing.publish(args.topic, message)
        time.sleep(3)

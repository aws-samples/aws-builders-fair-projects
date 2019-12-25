#!/usr/bin/env python3

import argparse
import json
import logging
import os
import random
import signal
import time

import netifaces as ni

import grovepi
import mqtt
from lcd import *

discovery = None

GG_DISCOVERY_HOST = "greengrass-ats.iot.us-west-2.amazonaws.com"

logger = logging.getLogger('moisture')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def analogRead(sensor_port = 0):
    try:
        return grovepi.analogRead(sensor_port)
    except Exception as e:
        logger.exception(f'{e}')

def term(signum, frame):
    global discovery
    if discovery is not None:
        discovery.remove_group_ca()       
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", action="store",
                        default=GG_DISCOVERY_HOST, dest="host", help="Your GG discovery Endpoint")
    parser.add_argument("-r", "--rootCA", action="store",
                        default="./certs/root.pem", dest="rootCAPath", help="Root CA file path")
    parser.add_argument("-t", "--topic", action="store", dest="topic",
                        default="data/agri/", help="Targeted topic")

    parser.add_argument("-n", "--thingName", action="store",
                        dest="thingName", required=True, help="Targeted thing name")
    parser.add_argument("-a", "--area", action="store", dest="area",
                        required=True, help="Area where sensor is placed")

    parser.add_argument("-c", "--cert", action="store",
                        dest="certificatePath", help="Certificate file path")
    parser.add_argument("-k", "--key", action="store",
                        dest="privateKeyPath", help="Private key file path")
    parser.add_argument("-p", "--port", action="store",
                        dest="sensorPort", help="Moisture Sensor port", type=int, default=0)

    args = parser.parse_args()

    topic = args.topic + args.area + '/moisture/' + args.thingName
    certs = args.certificatePath if args.certificatePath is not None else "./certs/{}/cert.pem".format(args.thingName)
    private_key = args.privateKeyPath if args.privateKeyPath is not None else "./certs/{}/private.key".format(args.thingName)

    discovery = mqtt.GGDiscovery(args.host, args.rootCAPath,
                            certs, private_key, args.thingName)
    discovery.discover()
    thing = mqtt.GGThing(discovery)
    thing.connect()

    signal.signal(signal.SIGTERM, term)

    ip_status_message = {
        'hostname': os.uname()[1],
        'ip_address': ni.ifaddresses('eth0')[2][0]['addr']
    }
    thing.publish('state/agri/ip/' + args.thingName, ip_status_message)

    while(True):
        try:
            message = {}
            time.sleep(random.uniform(0.01,0.1))
            m = analogRead(args.sensorPort)
            message['moisture'] = m
            thing.publish(topic, message)
            time.sleep(2)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.exception(f'{e}')

    discovery.remove_group_ca()  

#!/usr/bin/python3
# -*- Coding: utf-8 -*-

import json
import os
from threading import Timer
from time import sleep

import netifaces as ni
from args import Args
from gpio import Output
from greengrass import GgDiscovery, GGThing


def publish_message_based_on(state):
    message = { 'state': state }
    thing.publish(published_topic, message)
    print(f"Published {message} to {published_topic}")


def on():
    pump.low()
    publish_message_based_on('ON')


def off():
    pump.high()
    publish_message_based_on('OFF')


def water(duration):
    on()
    timer = Timer(duration, off)
    timer.start()
    

def recieve_message(message):
    topic = message.topic
    payload = json.loads(message.payload)
    print(f"Recieved {payload} from {topic}")
    return payload


def control_pump_based_on(message):
    try:
        payload = recieve_message(message)
        state = payload.get('set')
        duration = payload.get('duration')
        duration = int(duration)

        if state == 'ON':
            water(duration)
        elif state == 'OFF':
            off()
        else:
            publish_message_based_on("Error: publish 'ON' or 'OFF' as value in your message")
    except:
        print("Recieved invalid message, cannot control pump")



file_path = 'args.json'
parser = Args()
args = parser.set_args_of(file_path)

endpoint = f"greengrass-ats.iot.{args.region}.amazonaws.com"

discovery = GgDiscovery(
    endpoint,
    args.rootCA,
    args.cert,
    args.key,
    args.thing_name
)

base_topic = f"agri/{args.area}/pump"
subscribed_topic = f"cmd/{base_topic}"
published_topic = f"state/{base_topic}/{args.thing_name}"

discovery.discover()
thing = GGThing(discovery, customOnMessage=control_pump_based_on)
thing.connect()
thing.subscribe(subscribed_topic)
print(f"Subscribed {subscribed_topic}")

ip_status_message = {
    'hostname': os.uname()[1],
    'ip_address': ni.ifaddresses('enxb827eb9c25d8')[2][0]['addr']
}
thing.publish('state/agri/ip/' + args.thing_name, ip_status_message)

pump_pin = int(args.pin)
pump = Output(pump_pin)
pump.high()

while(True):
    sleep(100)

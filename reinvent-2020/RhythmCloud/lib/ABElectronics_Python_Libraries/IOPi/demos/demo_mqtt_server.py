#!/usr/bin/env python3
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - MQTT Server Demo
Requires mosquitto & paho-mqtt to be installed
Install mosquitto with: sudo apt-get install mosquitto

Install pip: sudo apt-get install python3-pip
Install paho-mqtt: sudo pip3 install paho-mqtt

run with: python3 demo_mqtt_server.py
================================================
This example uses MQTT to communicate with a Raspberry Pi and IO Pi Plus
to switch the pins on the IO Pi on and off.

Command to turn pin on or off using client "topic/iopi" 
With message of pin number,state i.e  5,1 turns pin 5 on
The second bus on the IO Pi Plus is accesses using pins 17 to 32
"""

import paho.mqtt.client as mqtt
import time

# Create client instance and connect to localhost
client = mqtt.Client()
client.connect("localhost",1883,60)

# Publish message to topic/iopi and set pin 1 on bus 1 to on
client.publish("topic/iopi", "1,1");
time.sleep(2)

# Publish message to topic/iopi and set pin 1 on bus 1 to off
client.publish("topic/iopi", "1,0");
time.sleep(2)
# Publish message to topic/iopi and set pin 1 on bus 2 to on
client.publish("topic/iopi", "17,1");
time.sleep(2)
# Publish message to topic/iopi and set pin 1 on bus 2 to off
client.publish("topic/iopi", "17,0");
client.disconnect();
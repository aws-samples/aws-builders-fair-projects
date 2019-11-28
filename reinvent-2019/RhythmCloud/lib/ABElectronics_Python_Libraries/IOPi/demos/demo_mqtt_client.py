#!/usr/bin/env python3
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - MQTT Client Demo
Requires python smbus & mosquitto to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus
Install mosquitto with: sudo apt-get install mosquitto
run with: python demo_mqtt_client.py
================================================
This example uses MQTT to communicate with a Raspberry Pi and IO Pi Plus
to switch the pins on the IO Pi on and off.
Initialises the IOPi device using the default addresses
Command to turn pin on or off using client "topic/iopi" 
With message of pin number,state i.e  5,1 turns pin 5 on
The second bus on the IO Pi Plus is accesses using pins 17 to 32

Run with: python3 demo_mqtt_client.py
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import paho.mqtt.client as mqtt
try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")
# Setup IOPi I2C addresses            
iobus = IOPi(0x20)
iobusb = IOPi(0x21)

# Set all pins as outputs and set to off
iobus.set_port_direction(0, 0x00)
iobus.write_port(0, 0x00)

iobus.set_port_direction(1, 0x00)
iobus.write_port(1, 0x00)

iobusb.set_port_direction(0, 0x00)
iobusb.write_port(0, 0x00)

iobusb.set_port_direction(1, 0x00)
iobusb.write_port(1, 0x00)

# This is the Subscriber Client

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/iopi")

def on_message(client, userdata, msg):
  p,s = msg.payload.decode().split(",")
  if (int(p) <= 16):
    print("IO Bus 0 Pin: " + p)
    print("IO Bus 0 mode: " + s)
    iobus.write_pin(int(p), int(s))
  else:
    print("IO Bus 1 Pin: " + p)
    print("IO Bus 1 mode: " + s)
    iobusb.write_pin((int(p) -16), int(s))
  # print(msg.payload.decode())
 
 
# Connect to the broker/server 
client = mqtt.Client()
client.connect("10.0.0.49",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()

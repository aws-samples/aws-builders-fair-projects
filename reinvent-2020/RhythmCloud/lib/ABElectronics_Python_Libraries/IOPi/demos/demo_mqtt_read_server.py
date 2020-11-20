#!/usr/bin/env python3
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - MQTT Server Read Demo
Requires python smbus & mosquitto to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus
Install mosquitto with: sudo apt-get install mosquitto
run with: python3 demo_mqtt_read_server.py
================================================
This example uses MQTT to communicate with a Raspberry Pi and IO Pi Plus
to read the pins on the IO Pi.
Initialises the IOPi device using the default addresses
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
iobus1 = IOPi(0x20)
iobus2 = IOPi(0x21)

# We will read the inputs 1 to 16 from the I/O bus so set port 0 and
# port 1 to be inputs and enable the internal pull-up resistors
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)

iobus1.set_port_direction(1, 0xFF)
iobus1.set_port_pullups(1, 0xFF)

# Repeat the steps above for the second bus
iobus2.set_port_direction(0, 0xFF)
iobus2.set_port_pullups(0, 0xFF)

iobus2.set_port_direction(1, 0xFF)
iobus2.set_port_pullups(1, 0xFF)


############### MQTT section ##################


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("sensor/iopi/ports")

# when receiving a mqtt message;

def on_message(client, userdata, msg):
  message = str(msg.payload)
  print(msg.topic+" "+message)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

# setup client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.0.0.49", 1883, 60)
client.loop_start()


while True:
  sensor_data = [iobus1.read_port(0),iobus1.read_port(1), iobus2.read_port(0),iobus2.read_port(1)]
  client.publish("sensor/iopi/ports", str(sensor_data))
  time.sleep(10)

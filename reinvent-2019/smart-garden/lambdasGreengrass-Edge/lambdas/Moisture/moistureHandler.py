import sys
import os
import logging
import time
import json

# os.environ['PYTHON_EGG_CACHE'] = '/tmp'

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vendored/'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import Adafruit_DHT
import RPi.GPIO as GPIO
import greengrasssdk

logger.info('Initializing moistureHandler')

#setup moisture
channel_moisture = 17    
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel_moisture, GPIO.IN)

#setup temperature
channel_temperature = 4
sensor_temperature = Adafruit_DHT.DHT11

#setup greengrasssdk
iotData = greengrasssdk.client('iot-data')

payload = {"water_level": 0, "temperature": 0, "humidity":0, "deviceId": "" }

serial = ""
def __init__(self):
    global serial   
    serial = getserial()

def getserial():
    logger.info('getserial called')
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    logger.info('serial {}'.format(cpuserial))
    return cpuserial   

def publish_metrics():
    shallow = payload.copy()
    shallow['water_level'] = collect_moisture()
    shallow['deviceId'] = getserial()
    shallow['humidity'], shallow['temperature'] = collect_temperature()
    iotData.publish(topic='SmartGarden/MoistureLevel', payload=json.dumps(shallow))

def collect_moisture():
    if GPIO.input(channel_moisture):
        logger.info('no water detected on channel {}'.format(channel_moisture))
        return 0
    else:
        logger.info('water detected on channel {}'.format(channel_moisture))
        return 1

def collect_temperature():    
    humidity, temperature = Adafruit_DHT.read_retry(sensor_temperature, channel_temperature)
    logger.info("humidity: {} temperature: {}".format(humidity, temperature))
    if humidity is not None and temperature is not None:
        return humidity, temperature
    logger.error("Falha ao ler dados do DHT11")
    return 0, 0
    

#GPIO.add_event_detect(channel, GPIO.BOTH)
#GPIO.add_event_callback(channel, collect_moisture)

def pinned_handler(event, context):
    """
    Mock function for pinned/long-lived Lambda
    """
    pass

while True:
    publish_metrics()    
    time.sleep(20)

import sys
import os
import logging
import time
import json
import glob

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vendored/'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import Adafruit_DHT
import RPi.GPIO as GPIO
import greengrasssdk

logger.info('Initializing temperatureHandler')
logger.info('RPI info {}'.format(GPIO.RPI_INFO))

#setup io
channel = 23
sensor = Adafruit_DHT.DHT11
# GPIO.setmode(GPIO.BCM)

#setup greengrasssdk
iotData = greengrasssdk.client('iot-data')

payload = { "temperature": 0, "humidity": 0 }

def publishTemperature(temperature, humidity):   
    temp = payload.copy()
    temp['temperature'] = temperature
    temp['humidity'] = humidity
    iotData.publish(topic='PlantWatering/Temperature', payload=json.dumps(temp))    

def collect_moisture(channel):
    # Efetua a leitura do sensor
    umid, temp = 0,0
    #umid, temp = Adafruit_DHT.read_retry(sensor, 4)    
    # Caso leitura esteja ok, mostra os valores na tela
    if umid is not None and temp is not None:
        print ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}n").format(temp, umid)
        print ("Aguarda 5 segundos para efetuar nova leitura...n")
        publishTemperature(temp, umid)
    else:
        # Mensagem de erro de comunicacao com o sensor
        print("Falha ao ler dados do DHT11 !!!")

#GPIO.add_event_detect(channel, GPIO.BOTH)
#GPIO.add_event_callback(channel, collect_moisture)

def pinned_handler(event, context):
    """
    Mock function for pinned/long-lived Lambda
    """
    pass

while True:
    collect_moisture(channel)
    time.sleep(30)

#!/usr/bin/env python


from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os
import sys
import random
import json
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
from datetime import datetime
import pytz
from tzlocal import get_localzone
from pytz import timezone
import subprocess

# set global colors
WHITE = (255, 255, 255)
GREEN = (0, 0, 255)
BLUE = (0, 255, 0)
PURPLE = (75, 130, 0)
RED = (255, 0, 0)
YELLOW = (255, 0, 255)
ORANGE = (255, 0, 102)
PINK = (255, 180, 105)


class Drum():

    startLED = 0
    endLED = 0
    color = WHITE
    name = 'name'
    pitches = [50]
    def __init__(self, startLED, endLED, color, pitches, name):
        self.startLED = startLED
        self.endLED = endLED
        self.color = color
        self.name = name
        self.pitches = pitches

PIXEL_COUNT = 191

smallTom = Drum(0, 22, PINK, [50],'smallTom')
largeTom = Drum(22, 50, ORANGE,[47,48],'largeTom')
snareDrum = Drum(50, 84, YELLOW,[37,38,40,91,93],'snareDrum')
kickDrum = Drum(84, 134, RED,[35,36],'kickDrum')
floorTom = Drum(134, 173, BLUE,[41,43,45],'floorTom')
#rideCymbal = Drum(173, 179, WHITE)
rideCymbal = Drum(173, 179, WHITE,[51,52,55,59],'rideCymbal')
highHat = Drum(179, 184, GREEN,[42,46,44],'highHat')
#crashCymbal = Drum(184, 191, GREEN)
crash = Drum(184, 191, GREEN,[49,57],'crash') 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("recordDrum")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint("a3lka4ud7kfmrw-ats.iot.us-east-1.amazonaws.com", 8883)
# For Websocket
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
# For TLS mutual authentication with TLS ALPN extension
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
myMQTTClient.configureCredentials("/greengrass/certs/AmazonRootCA1.pem", "/greengrass/certs/6acf979319.private.key", "/greengrass/certs/6acf979319.cert.pem")
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 s
myMQTTClient.connect()
topicValue = "/song/userHit"

def blink_drums(pixels, drumList, sessionId = "none", voltageDict = {}, stageName = "Guest"):
        pixels.clear()
        tz = pytz.timezone('America/Chicago')
        epoch = datetime.fromtimestamp(0, tz)

        for drum in drumList:
            for k in range(drum.startLED, drum.endLED):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( drum.color[0], drum.color[1], drum.color[2] ))
            payloadData = {}
            payloadData['drum'] = drum.name
            payloadData['timestamp'] = time.time_ns()
            payloadData['sessionId'] = sessionId
            payloadData['stageName'] = stageName
            print("voltageDict:",voltageDict)
            if (drum.name in voltageDict.keys()):
               payloadData['voltage'] = voltageDict[drum.name]
            else:
               continue

            result = myMQTTClient.publish(
                 topicValue,
                 json.dumps(payloadData), 0)

        pixels.show()
        pixels.clear()
        pixels.show()

def blink_drum(pixels, drumList, color=(255, 255, 255)):
    return
#        pixels.clear()
#        for drum in drumList:
#            for k in range(drum[0], drum[1]):
#                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
#        pixels.show()
#        pixels.clear()
#        pixels.show()

try:
    from ADCPi import ADCPi
except ImportError:
    print("Failed to import ADCPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCPi import ADCPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    '''
    Main program function
    '''
    subprocess.call(["/usr/bin/supervisorctl", "stop idlemode"])
    adc = ADCPi(0x68, 0x69, 12)
    #adc1 = ADCPi(0x6A, 0x6B, 12)
    sessionId = sys.argv[3]
    stageName = sys.argv[4]
    print("SessionId:",sessionId)
    print("StageName:",stageName)
    drumList =[]
    drumList.append(smallTom)
    blink_drums(pixels, drumList,sessionId,{"smallTom":0.0666},stageName)
    duration = sys.argv[1]
    song = sys.argv[2]
    startTime = time.time()    
    while True:

        # clear the console
        os.system('clear')

        drumList = []
        voltageDict = {}

        try:
           voltage1 = adc.read_voltage(1)
           if(voltage1 > 0.05):
              drumList.append(highHat)
              voltageDict[highHat.name] = voltage1
              print("Channel 1 (hihat): %02f" % voltage1)
           else:
              print("Channel 1 (hihat): no hit")
        except:
           print("Error reading voltage channel 1!")
        try:
           voltage2 = adc.read_voltage(2)
           if(voltage2 > 0.05):
              drumList.append(crash)
              voltageDict[crash.name] = voltage2
              print("Channel 2 (Crash Cymbal): %02f" % voltage2)
           else:
              print("Channel 2 (Crash Cymbal): no hit")
        except:
           print("Error reading voltage channel 2!") 
        try:
           voltage3 = adc.read_voltage(3)
           if(voltage3 > 0.05):
              drumList.append(rideCymbal)
              voltageDict[rideCymbal.name] = voltage3
              print("Channel 3 (Ride Cymbal): %02f" % voltage3)
           else:
              print("Channel 3 (Ride Cymbal): no hit")
        except:
           print("Error reading voltage channel 3!")
        try:
           voltage4 = adc.read_voltage(4)
           if(voltage4 > 0.05):
              drumList.append(smallTom)
              voltageDict[smallTom.name] = voltage4
              print("Channel 4 (Small Tom): %02f" % voltage4)
           else:
              print("Channel 4 (Small Tom): no hit")
        except:
           print("Error reading voltage channel 4!")

        try: 
           voltage5 = adc.read_voltage(5)
           if(voltage5 > 0.05):
              drumList.append(largeTom)
              voltageDict[largeTom.name] = voltage5
              print("Channel 5 (Large Tom): %02f" % voltage5)
           else:
              print("Channel 5 (Large Tom): no hit")
        except:
           print("Error reading voltage channel 5!")
        try:
          voltage6 = adc.read_voltage(6)
          if(voltage6 > 0.05):
             drumList.append(snareDrum)
             voltageDict[snareDrum.name] = voltage6
             print("Channel 6 (Snare Drum): %02f" % voltage6)
          else:
             print("Channel 6 (Snare Drum): no hit")
        except:
           print("Error reading voltage channel 6!")
        try:
           voltage7 = adc.read_voltage(7)
           if(voltage7 > 0.05):
              drumList.append(kickDrum)
              voltageDict[kickDrum.name] = voltage7
              print("Channel 7 (Kick Drum): %02f" % voltage7)
           else:
              print("Channel 7 (Kick Drum): no hit")
        except:
           print("Error reading voltage channel 7!")
        try:
           voltage8 = adc.read_voltage(8)
           if(voltage8 > 0.05):
              drumList.append(floorTom)
              voltageDict[floorTom.name] = voltage8
              print("Channel 8 (Floor Tom): %02f" % voltage8)
           else:
              print("Channel 8 (Floor Tom): no hit")
        except:
           print("Error reading voltage channel 8!")
        # wait 0.2 seconds before reading the pins again
        blink_drums(pixels, drumList,sessionId,voltageDict,stageName)

        currentDuration = time.time() - startTime
        print ("currentDuration:",currentDuration)
        print("duration limit:",duration)
        if (currentDuration > float(duration)):
            print("end")
#            myMQTTClient.disconnect()
            subprocess.call(["/usr/bin/supervisorctl", "start idlemode"])
            sys.exit(0) 

        time.sleep(0.1)


if __name__ == "__main__":
    main()

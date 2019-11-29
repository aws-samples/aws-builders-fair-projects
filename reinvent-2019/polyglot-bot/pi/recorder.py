#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  recorder.py
#  
#  Copyright 2019  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
from random import randint
# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
host = 'a6zwxk9vm9bfa-ats.iot.us-west-2.amazonaws.com'
rootCAPath = 'root-CA.crt'
certificatePath = 'pi.cert.pem'
privateKeyPath = 'pi.private.key'
port = 8883

clientId = 'basicPubSub'
topic = 'sdk/test/Python'
myAWSIoTMQTTClient = None
fileId= ''

def recordAudio(filename, key):
    print ("Starting Recorder")
    cmd  ='arecord /home/pi/Desktop/'+filename + ' -t wav -D sysdefault:CARD=1  -d 3 -r 48000;aws s3 cp /home/pi/Desktop/'+filename+' s3://bdfairdev/'+key+'/'+filename
    os.system(cmd)
    print ("Recording complete and sent to S3")
    if key == 'greetings':
        cmd = "ffplay -nodisp -autoexit /home/pi/PolyglotRobot/generalIntro1.mp3 >/dev/null 2>&1 &"
        os.system(cmd)
        cmd1 = " python3 /home/pi/PolyglotRobot/avainitialgreetings.py &"
        os.system(cmd1)
 
def recordRawAudio(filename, key):
    print ("Starting Recorder")
    cmd  ='arecord /home/pi/Desktop/'+filename + ' -c 2 -f S16_LE -r 22050 -t wav -D sysdefault:CARD=1 -d 3;aws s3 cp /home/pi/Desktop/'+filename+' s3://bdfairdev/'+key+'/'+filename
    os.system(cmd)
    print ("Recording complete and sent to S3")

 
# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    payload = json.loads(message.payload)
    
    langDetected = payload["language"]
    output=payload["s3output"]
    outputType=payload["type"]
    print(output)
    cmd  ='aws s3 cp ' + output + ' /home/pi/Desktop/output.mp3'
    os.system(cmd)
    if outputType == 'weather':
        cmd='python3 ' + langDetected+'_avagreeting.py & >/dev/null 2>&1'
        print(cmd)
        os.system(cmd)
        time.sleep(2)
    cmd='ffplay -nodisp -autoexit /home/pi/Desktop/output.mp3 >/dev/null 2>&1'
    os.system(cmd)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    fileId = str(randint(123456,234532))
    fileId= fileId +'.wav'
    if outputType == 'goodbye':
        main(None)
    recordRawAudio(langDetected+'_'+fileId, outputType)


def waitForResponse():
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    myAWSIoTMQTTClient.connect()
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(2)

    # Publish to the same topic in a loop forever
    loopCount = 0
    while True:
        time.sleep(2)


    
def main(args):
    time.sleep(2)
    fileId = str(randint(123456,234532))
    key='greetings'
    fileId= fileId +'.wav'
    recordAudio(fileId, key)
    waitForResponse()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

####    CREDITS    #################################################################
#
# This script creates a confidence level of a person being present and reports that
# into AWS IoT. LED outputs provided for visual feedback of operation (optional).
#
#  For Python 3
#
#  This is not production - it is Proof-of-Concept (PoC) only
#
####################################################################################
#
#  Created by Ian Fayers, with extra special thanks to Alex Fayers for his
#  implementation of the confidence algorithm and to Thiha Soe for his easy IoT
#  reporting. Thanks to Richard Westby-Nunn for the inspiration.
#
#
#  November 2019 - created as part of the re:Invent Builders Fair
#
####################################################################################

# import RPi.GPIO as GPIO
import datetime
import time
import json
import requests
import sys
from gpiozero import MotionSensor
from gpiozero import LED

####    VARIABLES     ###############################################################

loopDelay = 2         # time to wait between movement checks
minConfidence = 0     # minimum value of confidence that there is a person
maxConfidence = 50    # maximum value of confidence that there is a person

startConfidence = 0   # value of confidence to start the script with

highThreshold = 30    # value of confidence that will indicate there is a person
lowThreshold= 10      # value of confidence that will indicate there is no person

addValue = 5          # value to add to confidence upon movement
subValue = 3          # value to remove from confidence when there is no movement

personPresent = 0     # 0 if person not there, 1 if person there
reminderAnnounce = 270 # number of second to re-announce status (to ensure continuous presence is shown correctly)

path = "/home/pi/iot/"   # base path for the certificate files
client_cert = path + "6b148d4216-certificate.pem.crt"  # obtained from AWS IoT - note this ID will be different for you
client_key = path + "6b148d4216-private.pem.key"    # obtained from AWS IoT - note this ID will be different for you
root_cert = path + "AmazonRootCA1.pem"  # Amazon root-cert obained from https://www.amazontrust.com/repository/
url = "https://OVERTYPETHIS-ats.iot.us-east-2.amazonaws.com:8443/topics/sensorupdate" # URL for this Sensor - change OVERTYPETHIS, in fact, change the whole string to the one from your follow-along in the tutorial pack

#####     FUNCTIONS   ################################################################

def update_iot(sn, available):
    current_time = datetime.datetime.now()
    timestamp = current_time.isoformat()
    ddb_ttl = int((current_time + datetime.timedelta(minutes=5)).timestamp())
    payload = {"sn": sn, "updated_time": timestamp, "ddb_ttl": ddb_ttl, "available": available }
    headers = {'content-type': 'application/json'}
    print("Posting: " + sn + " - " + str(timestamp) + " - " + str(ddb_ttl) + " - " + str(available))
    try:
        r = requests.post(url, data=json.dumps(payload), verify=root_cert, headers=headers, cert=(client_cert, client_key))
        print(r)
    except Exception as e:
        print(e)
        print("Post to AWS failed")

# we'll reverse the serial number to increase the randomness - irrelevent for this small PoC, but useful for scale to mitigate hot-keys
def reversestring(s):
  str = ""
  for i in s:
    str = i + str
  return str

# get the serial number of each Pi progframmatically; we'll use that as the identifiers for desks/rooms and fix-up on the GUI
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
        cpuserial = 'ID' + reversestring(cpuserial) # flip the serial number to increase the entropy
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial

#####    DECISION FUNCTIONS    #####################################################

def active(sn): # what to do when movement is detected past the threshold
    update_iot(sn, 1)
    personPresent = 1
    LEDr.on()

def notactive(sn): # what to do when no movement has been detected for the set amount
    update_iot(sn, 0)
    personPresent = 0
    LEDr.off()

####   MAIN FUNCTION    ############################################################

def main(debug=1):
    if debug:
        print("Debug mode")
    else:
        print("Production mode")
    confidence = startConfidence
    prevActive = 0

    sn = getserial()

    if debug: ## DEBUG
        print("SERIAL : " + sn)

    reminderTick = 0
    active(sn)
    LEDg.on()
    time.sleep(2)

    processing = True # in case we need to exit, can just flip to false
    while processing:

        triggertime = datetime.datetime.now().isoformat() + ' : '

        # ensure we announce a status regularly, even if no status change (to prevent continuous use of a space showing as unused)
        if reminderTick <= 0:
            print(triggertime + 'Reminder announce = ' + str(personPresent))
            if personPresent:
                active(sn)
            else:
                notactive(sn)
            update_iot(sn, personPresent)
            reminderTick = reminderAnnounce
        reminderTick = reminderTick - loopDelay

        currentMovement = PIR.value # update motion sensor value

        percentageConfidence = round((confidence/highThreshold)*100)
        if debug: ### DEBUG
            print(triggertime + "confidence: "+str(confidence)+" ("+str(percentageConfidence)+"% to active)")

        if currentMovement == 1: # movement but not active yet
            LEDg.on()
            if confidence < (maxConfidence-addValue):
                confidence += addValue # increase confidence if it's not at max already

            if debug: ### DEBUG
                print(triggertime + "movement! (confidence += "+str(addValue)+")")

        else: # no movement detected
            LEDg.off()
            if confidence > (minConfidence+subValue):
                confidence -= subValue # decrease confidence if it's not at min already

            if debug: ### DEBUG
                print(triggertime +"(confidence -= "+str(subValue)+")")

        if confidence >= highThreshold and prevActive == 0: # person
            active(sn)
            prevActive = 1

            if debug: ### DEBUG
                print(triggertime + " PERSON +++++")

        elif confidence <= lowThreshold and prevActive == 1: # no person
            notactive(sn)
            prevActive = 0

            if debug: ### DEBUG
                print(triggertime +"NO PERSON -----")

        sys.stdout.flush()
        time.sleep(loopDelay) # wait a bit for next check

try:
    if (sys.version_info < (3, 0)):
        print("This script relies upon Python 3, nothing less\n")
        exit()

    pinLEDred = "BCM26"   # Red LED shows if sensor detects a perso
    pinLEDgreen = "BCM14" # Green LED shows if sensor detects motion
    pinSensor = "BCM4"    # Sensor LED is input from PIR

    PIR = MotionSensor(pinSensor) # init a Motion Sensor object on the GPIO you've connected it to
    LEDr = LED(pinLEDred)
    LEDg = LED(pinLEDgreen)
    main(debug=(len(sys.argv) - 1) > 0) # start monitoring - if any parameters then assume debug mode, otherwise it's prod!

except Exception as e:
        print(e)
        print("IR control script just failed!")

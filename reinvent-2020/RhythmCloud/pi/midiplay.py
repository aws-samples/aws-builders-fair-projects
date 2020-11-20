# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
from mido import MidiFile
#import greengrasssdk
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import time
import serial
import random
import re
import RPi.GPIO as GPIO
import mido
import json
from datetime import datetime
import pytz
import csv
from tzlocal import get_localzone
from pytz import timezone

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import yaml
import subprocess

# set global colors
# set global colors
WHITE = (255, 255, 255)
GREEN = (0, 0, 255)
BLUE = (0, 255, 0)
PURPLE = (75, 130, 0)
RED = (255, 0, 0)
YELLOW = (255, 0, 255)
ORANGE = (255, 0, 102)
PINK = (255, 180, 105)
DRKGREEN = (16, 3, 138)
CYAN = (0, 255, 255)
#open serial ports
ser1 = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200
)
ser2 = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=115200
)
ser3 = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=115200
)
ser4 = serial.Serial(
    port='/dev/ttyUSB3',
    baudrate=115200
)
ser5 = serial.Serial(
    port='/dev/ttyUSB4',
    baudrate=115200
)
ser6 = serial.Serial(
    port='/dev/ttyUSB5',
    baudrate=115200
)
ser7 = serial.Serial(
    port='/dev/ttyUSB6',
    baudrate=115200
)
ser8 = serial.Serial(
    port='/dev/ttyUSB7',
    baudrate=115200
)

class Drum():

    startLED = 0
    endLED = 0
    color = WHITE
    pitches = [50]
    name = 'name'
    serialport = ser1
    counter = 0
    drumA = 131
    drumB = 132
    def __init__(self, startLED, endLED, color, pitches,name,drumA,drumB):
        self.startLED = startLED
        self.endLED = endLED
        self.color = color
        self.pitches = pitches
        self.name = name
        self.drumA = drumA
        self.drumB = drumB

# Configure the count of pixels:
PIXEL_COUNT = 195

smalltom = Drum(0, 22, PINK, [50],'smalltom',131,132)
largetom = Drum(22, 50, ORANGE,[47,48],'largetom',131,132)
snaredrum = Drum(50, 84, YELLOW,[37,38,40,91,93],'snaredrum',131,132)
kickdrum = Drum(84, 134, RED,[35,36],'kickdrum',131,131)
floortom = Drum(134, 173, BLUE,[41,43,45],'floortom',131,132)
ridecymbal = Drum(173, 179, WHITE,[51,52,55,59],'ridecymbal',131,131)
highhat = Drum(179, 184, CYAN,[42,46,44],'highhat',131,132)
crashcymbal = Drum(184, 191, GREEN, [], 'crashcymbal',131,132)
metronome = Drum(191,195, DRKGREEN, [],'metronome',131,132)


# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)


drums=((0, 22), (22, 50), (50,89), (89,123), (123,173), (173,179), (179,184))
SMALLTOM=0
BIGTOM=1
FLOORTOM=2
SNARE=3
KICKDRUM=4

#client = greengrasssdk.client('iot-data')
# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("myClientID")
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
myMQTTClient.configureMQTTOperationTimeout(6)  # 5 s
myMQTTClient.connect()
print("Connected to IOT core")


if not ser1.isOpen():
  print("Error opening port /dev/ttyUSB0")
if not ser2.isOpen():
  print("Error opening port /dev/ttyUSB1")
if not ser3.isOpen():
  print("Error opening port /dev/ttyUSB2")
if not ser4.isOpen():
  print("Error opening port /dev/ttyUSB3")
if not ser5.isOpen():
  print("Error opening port /dev/ttyUSB4")
if not ser6.isOpen():
  print("Error opening port /dev/ttyUSB5")
if not ser7.isOpen():
  print("Error opening port /dev/ttyUSB6")
if not ser8.isOpen():
  print("Error opening port /dev/ttyUSB7")




def startidlemode():
   subprocess.call(["/usr/bin/supervisorctl","start idlemode"])

def drumFromName(name):
        name = name.lower()
        print("lookup drum:",name)

	if (smalltom.name == name):
		return smalltom
        if (floortom.name == name):
                return floortom
        if (largetom.name == name):
		return largetom
        if (snaredrum.name == name):
		return snaredrum
        if (kickdrum.name == name):
		return kickdrum
	if (ridecymbal.name == name):
		return ridecymbal
        if (highhat.name == name):
		return highhat
        if (crashcymbal.name == name):
                return crashcymbal



def playYaml(yamlFile, sessionId, overrideTempo = 0, duration = 30.0):
#    start_count(pixels, blink_times = 1, color=GREEN)
    with open(yamlFile, 'r') as stream:
        try:
            yaml_loaded = yaml.safe_load(stream)
            tempo = float(yaml_loaded.get("tempo"))
            print ("tempo from file: ", tempo)
            print ("overridden tempo: ", overrideTempo)
            if (overrideTempo > 0):
               tempo = float(overrideTempo)

            song = yaml_loaded.get("song")
            beatCount = 0
            startTime = time.time()
            print("Song tempo: ", tempo)
            start_count(pixels, blink_times = 1, color=GREEN, tempo=tempo, sessionId=sessionId)
            for songPart in song:
                for songPartKey, songPartElement in songPart.items():
                    if(songPartKey == "loop"):
                        for item in songPartElement:
                            repeatItem = item.get("repeat")
                            print(repeatItem)
                            for x in range(repeatItem):
                                barItem = item.get("bar")
                                for hit in barItem:
                                    processBar((beatCount % 8) + 1, hit, sessionId,tempo,duration,startTime)
                                    beatCount += 1
                    elif(songPartKey == "bar"):
                        for item in songPartElement:
                            processBar((beatCount % 8) + 1, item, sessionId,tempo,duration,startTime)
                            beatCount += 1

        except yaml.YAMLError as exc:
            print(exc)

def processBar(beatCount = 1, item=[], sessionId="123", tempo = 120, duration = 30.0, startTime = 0):
    hit = item.get("hit")
    combo = item.get("combo")
    sleep = float(float(60) / float(tempo))
    print("sleep=",str(sleep))
    drumList = []
    if hit is not None:
        blink_drums(pixels,[drumFromName(hit),metronome], sessionId)
        print("%d:  %s" % (beatCount, hit))
    else:
        comboString = ""
        for drumHit in combo:
            comboString = comboString + drumHit.get("hit") + " "
            drumList.append(drumFromName(drumHit.get("hit")))
            drumList.append(metronome) # blink metronome to the tempo
            blink_drums(pixels,drumList,sessionId)
            print("%d:  %s" % (beatCount, comboString))
    currentDuration = time.time() - startTime
    print ("currentDuration:",currentDuration)
    print("duration limit:",duration)
    if (currentDuration > float(duration) and duration > 0):
        print("end")
#        myMQTTClient.disconnect()
        #startidlemode()
        closeSerials()
        sys.exit(0)

    time.sleep(sleep)

def readfile(file, sessionid, tempo = 0.0, duration = 30.0):
    startTime = time.time()
    beat = float(float(60) / float(120)) #set a default of 120 beats a minute
    if (tempo > 0.0):
        beat = float(float(60.0) / float(tempo))
    mid = MidiFile(file)
    print("ticks per beat:"+format(mid.ticks_per_beat))
    print("beat=",beat)
    drumcheck = re.compile('drum|percussion|snare')
    firstHit = True
    for i, track in enumerate(mid.tracks):
        if (firstHit == True):
            print('starting countdown beat=',beat)
            start_count(pixels, 1, GREEN, tempo, sessionid)
            firstHit = False
            print("finished start count")
            
        mo = drumcheck.search(track.name.lower())
        print(mo)
        if (mo != None):
            #drumList =[]
            print("found a drum track!")
            print('Track {}: {}'.format(i, track.name))
            for msg in track:
               drumList = []
               print(msg)
               if (msg.type == 'note_on'):
               	if (msg.velocity > 0 and msg.note in smalltom.pitches):
			print('smalltom')
                	drumList.append(smalltom)
                if (msg.velocity > 0 and msg.note in floortom.pitches):
                        print('floortom')
                	drumList.append(floortom)
                if (msg.velocity > 0 and msg.note in largetom.pitches):
                        print('largetom')
                	drumList.append(largetom)
        	if (msg.velocity > 0 and msg.note in snaredrum.pitches):
                        print('snaredrum')
               	        drumList.append(snaredrum)
                if (msg.velocity > 0 and msg.note in ridecymbal.pitches):
                        print('ridecymbal')
                        drumList.append(ridecymbal)
                if (msg.velocity > 0 and msg.note in highhat.pitches):
                        print('highhat')
                        drumList.append(highhat)
                if (msg.velocity > 0 and msg.note in kickdrum.pitches):
                        print('kickdrum')
                        drumList.append(kickdrum)
                        drumList.append(highhat)
                if (msg.velocity > 0 and msg.note in crashcymbal.pitches):
                        print('crashcymbal')
                        drumList.append(crashcymbal)



                drumList.append(metronome) # blink metronome to the tempo
                blink_drums(pixels,drumList,sessionid)
                #time.sleep(mido.tick2second(msg.time,mid.ticks_per_beat,mido.bpm2tempo(120)))
                currentDuration = time.time() - startTime
                print ("currentDuration:",currentDuration)
                print("duration limit:",duration)
                if (currentDuration > float(duration) and duration > 0):
                    print("end")
#                    myMQTTClient.disconnect()
                    startidlemode()
                    closeSerials()
                    sys.exit(0)

                print ("************************* end beat ********************")
                time.sleep(beat)
            break

def blink_drum(pixels, drumList, sessionid, color=(255, 255, 255)):
        pixels.clear()
        for drum in drumList:
            for k in range(drum[0], drum[1]):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
        pixels.show()
        pixels.clear()
        pixels.show()

def sendReferenceData(sessionid, voltage, tz, epoch, drum):
        topicValue = "/song/reference"
        payloadData = {}
        payloadData['drum'] = drum.name
        payloadData['timestamp'] = (datetime.now(timezone('America/Chicago')) - epoch).total_seconds() * 1000.0
        #payloadData['timestamp'] = time.time.time_ns()
        payloadData['sessionId'] = sessionid
        payloadData['voltage'] = voltage
        result = myMQTTClient.publish(
              topicValue,
              json.dumps(payloadData), 0)
        print("send message to queue result:")
        print(result)

def blinkDrum(drum):
        for k in range(drum.startLED, drum.endLED):
            pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( drum.color[0], drum.color[1], drum.color[2] ))

def hitDrum(drum):
        fireDrumstick(drum.counter,drum.serialport,0.25,drum.drumA,drum.drumB)
        if drum.counter == 0:
           drum.counter = 1
        else:
           drum.counter = 0
        print("drum "+drum.name+" counter="+str(drum.counter))

def blink_drums(pixels, drumList, sessionid, voltage = 0.0):
        pixels.clear()
        tz = pytz.timezone('America/Chicago')
        epoch = datetime.fromtimestamp(0, tz)
        for drum in drumList:
            sendReferenceData(sessionid, voltage, tz, epoch, drum)
            blinkDrum(drum)
            if(drum.name != 'metronome'):
                hitDrum(drum)

        pixels.show()
        pixels.clear()
        pixels.show()

def start_count(pixels, blink_times=1, color=(255,255,255),tempo = 120.0, sessionId = "abc123"):
    if (tempo > 0.0):
       beat = float(float(60.0) / float(tempo))
    else:
       beat = float(float(60.0) / float(120))
    print("The beat is: {:.4f}".format(beat))
    for i in range(8):
        if(i % 4 == 0):
            currentColor = RED
        else:
            currentColor = BLUE
        for k in range(191):
            pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( currentColor[0], currentColor[1], currentColor[2] ))
        pixels.show()
        pixels.clear()
        pixels.show()
        #blink_drums(pixels, [metronome], sessionId)
        time.sleep(beat)

#def start_count(pixels, blink_times=1, sessionid, color=(255,255,255)):
#    beat = 60.0 / float(sys.argv[1])
#    print("The beat is: {:.4f}".format(beat))
#    for i in range(8):
#        if(i % 4 == 0):
#            currentColor = RED
#        else:
#            currentColor = WHITE
#        drumList = drums
#        blink_drum(pixels, drums, currentColor, sessionid)
#        time.sleep(beat)

def mapDrums(filename):
   with open(filename, mode="r") as file:
   	csvFile = csv.DictReader(file, fieldnames=['drum','port'])
        for row in csvFile:
           eval(row['drum']).serialport = eval(row['port'])
           print("Mapped "+row['drum']+" to port "+row['port'])

def fireStickOne(ser, delay,drumA):
        print("Firing Motor A")
        ser.write(chr(drumA))
        out = ''
        time.sleep(delay)
        while ser.inWaiting() > 0:
                out += ser.read(1)
        if out != '':
                print ">>" + out
        return

def fireStickTwo(ser, delay,drumB):
        print("Firing Motor B")
        ser.write(chr(drumB))
        out = ''
        time.sleep(delay)
        while ser.inWaiting() > 0:
                out += ser.read(1)
        if out != '':
                print ">>" + out
        return

def fireDrumstick(counter, ser, delay, drumA, drumB):
        print("counter for serial port "+str(ser)+" is "+str(counter))
        if(counter % 2 == 0):
                fireStickOne(ser, delay, drumA)
        else:
                fireStickTwo(ser, delay, drumB)
        return

def closeSerials():
    ser1.close()
    ser2.close()
    ser3.close()
    ser4.close()
    ser5.close()
    ser6.close()
    ser7.close()
    ser8.close()

if __name__ == "__main__":

    fileToPlay = sys.argv[1]
    sessionId = sys.argv[2]
    duration = float(sys.argv[3])
    overrideTempo = float(sys.argv[4])
   
    # Clear all the pixels to turn them off.
    #subprocess.call(["/usr/bin/supervisorctl", "stop idlemode"])
    time.sleep(1)
       
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    #start_count(pixels, blink_times = 1, color=GREEN)
    mapDrums("drum-map.csv")
    if (fileToPlay.endswith(".mid")):
       readfile(fileToPlay,sessionId,overrideTempo,duration)

    if (fileToPlay.endswith('.yaml')):
       playYaml(fileToPlay,sessionId,overrideTempo,duration)

    #for i in range(10):
    #subprocess.call(["/usr/bin/supervisorctl","start idlemode"])
    closeSerials()

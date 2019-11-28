# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
from mido import MidiFile
#import greengrasssdk
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import time
import random
import re
import RPi.GPIO as GPIO
import mido
import json
from datetime import datetime
import pytz
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

class Drum():

    startLED = 0
    endLED = 0
    color = WHITE
    pitches = [50]
    name = 'name'
    def __init__(self, startLED, endLED, color, pitches,name):
        self.startLED = startLED
        self.endLED = endLED
        self.color = color
        self.pitches = pitches
        self.name = name

# Configure the count of pixels:
PIXEL_COUNT = 195

smallTom = Drum(0, 22, PINK, [50],'smalltom')
largeTom = Drum(22, 50, ORANGE,[47,48],'largetom')
snareDrum = Drum(50, 84, YELLOW,[37,38,40,91,93],'snaredrum')
kickDrum = Drum(84, 134, RED,[35,36],'kickdrum')
floorTom = Drum(134, 173, BLUE,[41,43,45],'floortom')
rideCymbal = Drum(173, 179, WHITE,[51,52,55,59],'ridecymbal')
highHat = Drum(179, 184, CYAN,[42,46,44],'highhat')
crashCymbal = Drum(184, 191, GREEN, [], 'crashcymbal')
metronome = Drum(191,195, DRKGREEN, [],'metronome')


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
myMQTTClient.configureCredentials("/greengrass/certs/root.ca.pem", "/home/pi/.ssh/6acf979319.private.key", "/greengrass/certs/6acf979319.cert.pem")
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(6)  # 5 s
myMQTTClient.connect()
print("Connected to IOT core")

def startidlemode():
   subprocess.call(["/usr/bin/supervisorctl","start idlemode"])

def drumFromName(name):
        name = name.lower()
        print("lookup drum:",name)

	if (smallTom.name == name):
		return smallTom
        if (floorTom.name == name):
                return floorTom
        if (largeTom.name == name):
		return largeTom
        if (snareDrum.name == name):
		return snareDrum
        if (kickDrum.name == name):
		return kickDrum
	if (rideCymbal.name == name):
		return rideCymbal
        if (highHat.name == name):
		return highHat



def playYaml(yamlFile, sessionId, overrideTempo = 0, duration = 30.0):
#    start_count(pixels, blink_times = 1, color=GREEN)
    with open(yamlFile, 'r') as stream:
        try:
            yaml_loaded = yaml.safe_load(stream)
            tempo = float(yaml_loaded.get("tempo"))
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
        startidlemode()
        sys.exit(0)

    time.sleep(sleep)

def readfile(file, sessionid, tempo = 0, duration = 30.0):
    startTime = time.time()
    beat = float(float(60.0) / float(tempo))
    if (tempo < 1):
        beat = float(float(60) / float(120)) 
    mid = MidiFile(file)
    print("ticks per beat:"+format(mid.ticks_per_beat))
    print("beat=",beat)
    drumcheck = re.compile('drum|percussion|snare')
    firstHit = True
    for i, track in enumerate(mid.tracks):
        if (firstHit == True):
            print('starting countdown beat=',beat)
            start_count(pixels, blink_times = 1, color=GREEN, tempo = tempo, sessionId = sessionid)
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
               	if (msg.velocity > 0 and msg.note in smallTom.pitches):
			print('smalltom')
                	drumList.append(smallTom)
                if (msg.velocity > 0 and msg.note in floorTom.pitches):
                        print('floortom')
                	drumList.append(floorTom)
                if (msg.velocity > 0 and msg.note in largeTom.pitches):
                        print('largetom')
                	drumList.append(largeTom)
	        	if (msg.velocity > 0 and msg.note in snareDrum.pitches):
                           print('snaredrum')
                	   drumList.append(snareDrum)
                if (msg.velocity > 0 and msg.note in rideCymbal.pitches):
                        print('ridecymbal')
                        drumList.append(rideCymbal)
                if (msg.velocity > 0 and msg.note in highHat.pitches):
                        print('highHat')
                        drumList.append(highHat)
                if (msg.velocity > 0 and msg.note in kickDrum.pitches):
                        print('kickDrum')
                        drumList.append(kickDrum)


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
                    sys.exit(0)

                time.sleep(beat)
            break
# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)

def blink_drum(pixels, drumList, sessionid, color=(255, 255, 255)):
        pixels.clear()
        for drum in drumList:
            for k in range(drum[0], drum[1]):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
        pixels.show()
        pixels.clear()
        pixels.show()


def blink_drums(pixels, drumList, sessionid, voltage = 0.0):
        pixels.clear()
#        epoch = datetime.utcfromtimestamp(0)
        tz = pytz.timezone('America/Chicago')
        epoch = datetime.fromtimestamp(0, tz)
        for drum in drumList:
            topicValue = "/song/reference"
            payloadData = {}
            payloadData['drum'] = drum.name
            payloadData['timestamp'] = (datetime.now(timezone('America/Chicago')) - epoch).total_seconds() * 1000.0
            payloadData['sessionId'] = sessionid
            payloadData['voltage'] = voltage
            result = myMQTTClient.publish(
                  topicValue,
                  json.dumps(payloadData), 0)
            print("send message to queue result:")
            print(result)
            for k in range(drum.startLED, drum.endLED):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( drum.color[0], drum.color[1], drum.color[2] ))

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
        blink_drums(pixels,[metronome], sessionId)
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


if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    subprocess.call(["/usr/bin/supervisorctl", "stop idlemode"])
    time.sleep(1)
       
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    #start_count(pixels, blink_times = 1, color=GREEN)
    if (sys.argv[2].endswith(".mid")):
       readfile(sys.argv[2],sys.argv[3],sys.argv[4],float(sys.argv[1]))

    if (sys.argv[2].endswith('.yaml')):
        playYaml(sys.argv[2],sys.argv[3],sys.argv[4],float(sys.argv[1]))
    #for i in range(10):
    subprocess.call(["/usr/bin/supervisorctl","start idlemode"])

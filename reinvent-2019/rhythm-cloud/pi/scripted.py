# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import sys
import time
import random
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# set global colors
ORANGE = (255, 0, 102)

WHITE = (255, 255, 255)
PURPLE = (255, 255, 0)
YELLOW = (255, 0, 255)
CYAN = (0, 255, 255)

RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)

class Drum():

    startLED = 0
    endLED = 0
    color = WHITE
    def __init__(self, startLED, endLED, color):
        self.startLED = startLED
        self.endLED = endLED
        self.color = color
 
# Configure the count of pixels:
PIXEL_COUNT = 191

smallTom = Drum(0, 22, PURPLE)
largeTom = Drum(22, 50, ORANGE)
snareDrum = Drum(50, 84, YELLOW)
kickDrum = Drum(84, 134, RED)
floorTom = Drum(134, 173, BLUE)
rideCymbal = Drum(173, 179, WHITE)
highHat = Drum(179, 184, CYAN)
crashCymbal = Drum(184, 191, GREEN)

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)


drums=((0, 22), (22, 50), (50,89), (89,123), (123,173), (173,179), (179,184), (184, 191))
SMALLTOM=0
BIGTOM=1
FLOORTOM=2
SNARE=3
KICKDRUM=4

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
 
def blink_drum(pixels, drumList, color=(255, 255, 255)):
        pixels.clear()
        for drum in drumList:
            for k in range(drum[0], drum[1]):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
        pixels.show()
        pixels.clear()
        pixels.show()


def blink_drums(pixels, drumList):
        pixels.clear()
        for drum in drumList:
            for k in range(drum.startLED, drum.endLED):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( drum.color[0], drum.color[1], drum.color[2] ))
        pixels.show()
        pixels.clear()
        pixels.show()

def start_count(pixels, blink_times=1, color=(255,255,255)):
    beat = 60.0 / 120
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
        time.sleep(beat)

def start_song(pixels, blink_times=1, color=WHITE):
    beat = 60.0 / 120
    print("The beat is: {:.4f}".format(beat))
    for i in range(8):
        drumList =[]
        drumList.append(smallTom)
        if(i % 8 == 0):
            drumList.append(floorTom)
        if(i % 8 == 1):
            drumList.append(rideCymbal)
        if(i % 8 == 2):
            drumList.append(snareDrum) 
        if(i % 8 == 3):
            drumList.append(crashCymbal)
        if(i % 8 == 4):
            drumList.append(kickDrum)
        if(i % 8 == 5):
            drumList.append(highHat)
        if(i % 8 == 6):
            drumList.append(largeTom)
        blink_drums(pixels, drumList)
        time.sleep(beat)

 
if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    start_count(pixels, blink_times = 1, color=WHITE)
    for i in range(10):
        start_song(pixels, blink_times = 1, color=GREEN)


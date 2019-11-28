# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
 
# Configure the count of pixels:
PIXEL_COUNT = 191
 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
 
 
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
 
 
def rainbow_cycle(pixels, wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
 
 
 
if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    while True: 
        rainbow_cycle(pixels, wait=0.001)
 
    
    
    
    
     

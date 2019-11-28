# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
# Will color all the lights different primary colors.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


# Configure the count of pixels:
PIXEL_COUNT = 10

# The WS2801 library makes use of the BCM pin numbering scheme. See the README.md for details.

# Specify a software SPI connection for Raspberry Pi on the following pins:
PIXEL_CLOCK = 18
PIXEL_DOUT  = 23
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=PIXEL_CLOCK, do=PIXEL_DOUT)

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
#SPI_PORT   = 0
#SPI_DEVICE = 0
#pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Clear all the pixels to turn them off.
pixels.clear()
pixels.show()  # Make sure to call show() after changing any pixels!

# Set the first third of the pixels red.
for i in range(PIXEL_COUNT//3):
    pixels.set_pixel_rgb(i, 255, 0, 0)  # Set the RGB color (0-255) of pixel i.

# Set the next third of pixels green.
for i in range(PIXEL_COUNT//3, PIXEL_COUNT//3*2):
    pixels.set_pixel_rgb(i, 0, 255, 0)

# Set the last third of pixels blue.
for i in range(PIXEL_COUNT//3*2, PIXEL_COUNT):
    pixels.set_pixel_rgb(i, 0, 0, 255)

# Now make sure to call show() to update the pixels with the colors set above!
pixels.show()

# Not used but you can also read pixel colors with the get_pixel_rgb function:
#r, g, b = pixels.get_pixel_rgb(0)  # Read pixel 0 red, green, blue value.

# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI


def RGB_to_color(r, g, b):
    """Convert three 8-bit red, green, blue component values to a single 24-bit
    color value.
    """
    return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

def color_to_RGB(color):
    """Convert a 24-bit color value to 8-bit red, green, blue components.
    Will return a 3-tuple with the color component values.
    """
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)


class WS2801Pixels(object):
    """WS2801/SPI interface addressable RGB LED lights."""

    def __init__(self, count, clk=None, do=None, spi=None, gpio=None):
        """Initialize set of WS2801/SPI-like addressable RGB LEDs.  Must
        specify the count of pixels, and either an explicit clk (clokc) and do
        (data output) line for software SPI or a spi instance for hardware SPI.
        """
        self._spi = None
        if spi is not None:
            # Handle hardware SPI.
            self._spi = spi
        elif clk is not None and do is not None:
            # Handle software SPI.
            # Default to platform GPIO if not provided.
            if gpio is None:
                import Adafruit_GPIO as GPIO
                gpio = GPIO.get_platform_gpio()
            self._spi = SPI.BitBang(gpio, clk, do, None, None)
        else:
            raise ValueError('Must specify either spi for for hardware SPI or clk, and do for softwrare SPI!')
        # Setup SPI interface with up to 20mhz speed.
        self._spi.set_clock_hz(1000000)
        self._spi.set_mode(0)
        self._spi.set_bit_order(SPI.MSBFIRST)
        # Setup buffer for pixel RGB data.
        self._count = count
        self._pixels = [0]*(count*3)

    def show(self):
        """Push the current pixel values out to the hardware.  Must be called to
        actually change the pixel colors.
        """
        self._spi.write(self._pixels)
        time.sleep(0.002)

    def count(self):
        """Return the count of pixels."""
        return self._count

    def set_pixel(self, n, color):
        """Set the specified pixel n to the provided 24-bit RGB color.  Note you
        MUST call show() after setting pixels to see the LEDs change color!"""
        r = color >> 16
        g = color >> 8
        b = color
        # Note the color components will be truncated to 8-bits in the
        # set_pixel_rgb function call.
        self.set_pixel_rgb(n, r, g, b)

    def set_pixel_rgb(self, n, r, g, b):
        """Set the specified pixel n to the provided 8-bit red, green, blue
        component values.  Note you MUST call show() after setting pixels to
        see the LEDs change color!
        """
        assert n >= 0 and n < self._count, 'Pixel n outside the count of pixels!'
        self._pixels[n*3]   = r & 0xFF
        self._pixels[n*3+1] = g & 0xFF
        self._pixels[n*3+2] = b & 0xFF

    def get_pixel(self, n):
        """Retrieve the 24-bit RGB color of the specified pixel n."""
        r, g, b = self.get_pixel_rgb(n)
        return (r << 16) | (g << 8) | b

    def get_pixel_rgb(self, n):
        """Retrieve the 8-bit red, green, blue component color values of the
        specified pixel n.  Will return a 3-tuple of red, green, blue data.
        """
        assert n >= 0 and n < self._count, 'Pixel n outside the count of pixels!'
        return (self._pixels[n*3], self._pixels[n*3+1], self._pixels[n*3+2])

    def set_pixels(self, color=0):
        """Set all pixels to the provided 24-bit RGB color value.  Note you
        MUST call show() after setting pixels to see the LEDs change!"""
        for i in range(self._count):
            self.set_pixel(i, color)

    def set_pixels_rgb(self, r, g, b):
        """Set all pixels to the provided 8-bit red, green, blue component color
        value.  Note you MUST call show() after setting pixels to see the LEDs
        change!
        """
        for i in range(self._count):
            self.set_pixel(i, r, g, b)

    def clear(self):
        """Clear all the pixels to black/off.  Note you MUST call show() after
        clearing pixels to see the LEDs change!
        """
        self.set_pixels(0)
#
# def colorwipe(pixels, c, delay):
#     for i in range(len(pixels)):
#         setpixelcolor(pixels, i, c)
#         writestrip(pixels)
#         time.sleep(delay)
#
# def Wheel(WheelPos):
#     if (WheelPos < 85):
#            return Color(WheelPos * 3, 255 - WheelPos * 3, 0)
#     elif (WheelPos < 170):
#            WheelPos -= 85;
#            return Color(255 - WheelPos * 3, 0, WheelPos * 3)
#     else:
#         WheelPos -= 170;
#         return Color(0, WheelPos * 3, 255 - WheelPos * 3)
#
# def rainbowCycle(pixels, wait):
#     for j in range(256): # one cycle of all 256 colors in the wheel
#            for i in range(len(pixels)):
# # tricky math! we use each pixel as a fraction of the full 96-color wheel
# # (thats the i / strip.numPixels() part)
# # Then add in j which makes the colors go around per pixel
# # the % 96 is to make the wheel cycle around
#               setpixelcolor(pixels, i, Wheel( ((i * 256 / len(pixels)) + j) % 256) )
#        writestrip(pixels)
#        time.sleep(wait)
#
# colorwipe(ledpixels, Color(255, 0, 0), 0.05)
# colorwipe(ledpixels, Color(0, 255, 0), 0.05)
# colorwipe(ledpixels, Color(0, 0, 255), 0.05)
# while True:
#     rainbowCycle(ledpixels, 0.00)

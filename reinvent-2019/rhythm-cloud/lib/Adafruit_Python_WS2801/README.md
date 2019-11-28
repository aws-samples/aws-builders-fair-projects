# Adafruit Python WS2801
Python code to control WS2801 and similar SPI interface addressable RGB LED strips on a Raspberry Pi &amp; BeagleBone Black.

## Installation

To install the library from source (recommended) run the following commands on a Raspberry Pi or other Debian-based OS system:

    sudo apt-get install git build-essential python-dev
    cd ~
    git clone https://github.com/adafruit/Adafruit_Python_WS2801.git
    cd Adafruit_Python_WS2801
    sudo python setup.py install

Alternatively you can install from pip with:

    sudo pip install adafruit-ws2801

Note that the pip install method **won't** install the example code.

## Pin numbering

The library (and the sample code) use the Broadcom BCM GPIO pin numbering scheme, rather than the physical pin numbering scheme. The [Adafruit T-Cobbler breakout board](https://www.adafruit.com/products/1754), for example, uses the BCM scheme. See [https://pinout.xyz](https://pinout.xyz/) for a quick-reference image.

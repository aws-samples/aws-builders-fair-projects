# Autoponics: Happier Plants

## Overview

This is the Python 3 app for controlling the sensors and actuators of the Autoponics thing.

## Installation

Download [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) and follow the [installation guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) to write the image to an SD card.

Enable [SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/) so you can connect to the Raspberry Pi from your computer. And connect to the device via SSH.

Update the Raspbian:
```sh
$ sudo apt update
````

Download this project to the Raspberry Pi:
```sh
$ mkdir autoponics
$ cd autoponics
$ git init
$ git config core.sparsecheckout true
$ echo autoponics/thing-app/ >> .git/info/sparse-checkout
$ git remote add -f origin https://github.com/mikeapted/aws-builders-fair-projects
$ git pull origin master
```

Install Python dependencies:
```sh
$ cd autoponics/thing-app
$ pip3 install -r requirements.txt
```

Enable [SPI](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md) as well.

## Running

To manually run the app, run the commands below:

```sh
$ cd autoponics/thing-app/
$ python3 app.py
```

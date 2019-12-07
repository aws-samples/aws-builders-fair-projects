# smart-garage

Control your garage using Alexa using Raspberry Pi. You can say thing like: Alexa, lock garage. Alexa, unlock garage (Alexa will ask for a 4 digit pin).

## Required Hardwares

1) [Raspberry Pi Zero W for about $5](https://www.microcenter.com/product/486575/zero-w)
2) [Relay switch for about $10](https://www.amazon.com/s?k=relay+switch+arduino)
3) [Reed Switch for about $15](https://www.amazon.com/gp/product/B00LYCUSBY)

## How does this work?

User talk to Alexa: Alexa, lock the garage. This will trigger a smart home lock skill that trigger a lambda. This Lambda will publish its desired state to AWS IoT to update device and shadow state. The raspi is also subscribe to the same IoT topic, it will trigger its GPIO pin which open / close the garage.

## Install

```shell
npm i
```

Copy env-sample file to .env

```shell
cp env-sample .env
```

## Enable as service

```shell
  # modify crontab to start the Python service after reboot
  crontab -e
  @reboot cd /home/pi/garage && /home/pi/garage/env/bin/python /home/pi/garage/src/iot/switch.py

  # enable cron
  systemctl enable cron.service
```

## Setup Raspi

```shell
  # download Raspbian Buster Lite (~500MB):
  https://www.raspberrypi.org/downloads/raspbian/

  # download etcher to burn Raspbian OS to your SD card:
  https://www.balena.io/etcher

  # enable SSH by default by creating an empty ssh file in the boot partition of the SD card
  touch ssh

  # copy your public key to raspi
  ssh-copy-id pi@raspi_zero_ip

  # update
  sudo apt update

  # install Nodejs LTS
  sudo wget -O - https://raw.githubusercontent.com/sdesalas/node-pi-zero/master/install-node-v.last.sh | bash

  # install required services
  sudo apt install yarn git vim htop python3-pip wiringpi -y

  # clone this repo
  git clone https://github.com/kienpham2000/garage.git

  # Disable the ACT LED on the Pi Zero, edit file: /boot/config.txt
  dtparam=act_led_trigger=none
  dtparam=act_led_activelow=on
```

## Raspi GPIO Pinout

![gpio](docs/raspi-0w-gpio-pinout.png)

#!/bin/sh
sudo service amazon-ssm-agent start

sudo apt-get update
sudo apt-get -y upgrade &

cd /home/pi/iot
# force the log folder to exist, ignore any error
mkdir logs
# launch the sensor - pass a paramter for debug mode. Log all console output to a log file (cleared each reboot)
sudo python3 app.py D >/home/pi/iot/logs/cronlog 2>&1
cd /

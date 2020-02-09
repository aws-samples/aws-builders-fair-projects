#!/bin/bash

echo_string="Cerebro Quick Start script - Starting ..."
echo $'\n'$echo_string$'\n'

echo_string="0. first, turnon screen & reset the local dirs ..."
echo $'\n'$echo_string$'\n'
echo_string="./turnon-display.sh && rm -rf /tmp/project_cerebro && mkdir -p /tmp/project_cerebro/logs && mkdir -p /tmp/project_cerebro/media && mkdir -p /tmp/project_cerebro/system && mkdir -p /tmp/project_cerebro/profiles"
echo $echo_string
eval "$echo_string"

echo_string="1. next, announce that we will initiate the Cerebro Startup sequence now ..."
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 generate_audio.py --text 'Cerebro Quick Start - All the backend will be retained as is. The local directories will be reset.' --filename 'cerebro_starting_up_qs.mp3' "
echo $echo_string
eval "$echo_string"

echo_string="3a. Get the Device ID"
echo $'\n'$echo_string$'\n'
echo_string='read -p "Enter Device ID: " deviceID'
echo $echo_string
eval "$echo_string"
echo "Your DeviceID was registered as: $deviceID"

echo_string="3b. now start up the cerebro downloader app"
echo $'\n'$echo_string$'\n'
echo_string="python3 cerebro_processor.py '$deviceID' --interval 10 --clean 2>&1 &"
echo $echo_string
eval "$echo_string"

echo_string="4. now, announce that the Cerebro Startup sequence is completed now ..."
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 generate_audio.py --text 'Cerebro is now completely started. Please follow along the prompts that you will hear shortly ...' --filename 'cerebro_started_new.mp3' "
echo $echo_string
eval "$echo_string"

echo_string="5. next, announce that we will initiate the Cerebro Startup sequence now ..."
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 generate_audio.py --text 'Alexa, Open Image Cerebro' --filename 'cerebro_trigger_alexa.mp3' "
echo $echo_string
eval "$echo_string"

echo_string="Cerebro Quick Start script - Completed!"
echo $'\n'$echo_string$'\n'

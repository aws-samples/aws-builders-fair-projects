#!/bin/bash

echo_string="Cerebro Startup script - Starting ..."
echo $'\n'$echo_string$'\n'

# First copy the system file into a temp folder
echo_string="1a. create the temp dir and copy the system file"
echo $'\n'$echo_string$'\n'
echo_string="mkdir -p /tmp/cerebro_start_dir && cp ../assets/system/*.jpg /tmp/cerebro_start_dir"
echo $echo_string
eval "$echo_string"

# Next, display the system files as a slideshow from the temp folder
echo_string="1b. start the slideshow"
echo $'\n'$echo_string$'\n'
echo_string="./start-picture-frame.sh /tmp/cerebro_start_dir &"
echo $echo_string
eval "$echo_string"

echo_string="2. next, announce that we will initiate the Cerebro Startup sequence now ..."
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 generate_audio.py --text 'Cerebro Cleanup starting now - Deleting S 3 entries, Dynamo DB and Recognition entries as well. The local directories will be reset as well.' --filename 'cerebro_starting_up.mp3' "
echo $echo_string
eval "$echo_string"

echo_string="3a. start the raw cleanup - to delete s3 content, recreate reko collection"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 ./cerebro_cleanup.py"
echo $echo_string
eval "$echo_string"

echo_string="3b. now, confirm that Cerebro cleanup was completed ..."
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 generate_audio.py --text 'Cerebro Cleanup completed now.' --filename 'cerebro_cleanup_complete.mp3' "
echo $echo_string
eval "$echo_string"

#echo_string="4. seed the stock profiles to baseline celebrities available"
#echo $'\n'$echo_string$'\n'
#echo_string="python3 media_uploader.py --imagedir ../assets/profiles --scan && python3 media_uploader.py --imagedir ../assets/profiles --retry"
#echo $echo_string
#eval "$echo_string"
#echo_string="cd ../py_client && python3 generate_audio.py --text 'Created the stock profiles for Cerebro.' --filename 'cerebro_stock_profiles.mp3' "
#echo $echo_string
#eval "$echo_string"

#echo_string="5. now, confirm that Cerebro stock profiles was uploaded ..."
#echo $'\n'$echo_string$'\n'
#echo_string="cd ../py_client && python3 generate_audio.py --text 'Uploaded stock profiles into Cerebro now.' --filename 'cerebro_stock_profiles_uploaded.mp3' "
#echo $echo_string
#eval "$echo_string"

#echo_string="6. seed the stock photos to baseline content"
#echo $'\n'$echo_string$'\n'
#echo_string="sleep 120 && python3 media_uploader.py --imagedir ../assets/stock --scan && python3 media_uploader.py --imagedir ../assets/stock --retry"
#echo $echo_string
#eval "$echo_string"
#echo_string="cd ../py_client && python3 generate_audio.py --text 'Added the stock photos for Cerebro.' --filename 'cerebro_stock_photos.mp3' "
#echo $echo_string
#eval "$echo_string"

echo_string="7a. Get the Device ID"
echo $'\n'$echo_string$'\n'
echo_string='read -p "Enter Device ID: " deviceID'
echo $echo_string
eval "$echo_string"
echo "Your DeviceID was registered as: $deviceID"

echo_string="7b. now start up the cerebro downloader app"
echo $'\n'$echo_string$'\n'
echo_string="python3 cerebro_processor.py '$deviceID' --interval 10 --clean 2>&1 &"
echo $echo_string
eval "$echo_string"

echo_string="cd ../py_client && python3 generate_audio.py --text 'Cerebro is now completely started. Please follow along the prompts that you will hear shortly ...' --filename 'cerebro_started_new.mp3' "
echo $echo_string
eval "$echo_string"

echo_string="8. next, announce that we will initiate the Cerebro Startup sequence now ..."
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 generate_audio.py --text 'Alexa, Open Image Cerebro' --filename 'cerebro_alexa.mp3' "
echo $echo_string
eval "$echo_string"

echo_string="XX. stop the slideshow"
echo $'\n'$echo_string$'\n'
echo_string="./stop-picture-frame.sh"
echo $echo_string
eval "$echo_string"

echo_string="------------------- Cleanup tmp dirs --------------------"
echo $'\n'$echo_string$'\n'
echo_string="rm -rf /tmp/cerebro_start_dir"
eval "$echo_string"

echo_string="Cerebro Startup script - Completed!"
echo $'\n'$echo_string$'\n'

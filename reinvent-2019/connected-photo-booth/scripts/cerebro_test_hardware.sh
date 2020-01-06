#!/bin/bash

echo_string="Cerebro Hardware Test script - Starting ..."
echo $'\n'$echo_string$'\n'

echo_string="Testing for AWS CLI:"
echo $'\n'$echo_string$'\n'
echo_string="aws --version"
eval "$echo_string"

echo_string="Testing for apply_image_effects:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 apply_image_effects.py --help"
eval "$echo_string"

echo_string="Testing for cerebro_cleanup:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 cerebro_cleanup.py --help"
eval "$echo_string"

echo_string="Testing for cerebro_processor:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 cerebro_processor.py --help"
eval "$echo_string"

echo_string="Testing for cerebro_utils:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 cerebro_utils.py"
eval "$echo_string"

echo_string="Testing for generate_audio:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 generate_audio.py --help"
eval "$echo_string"

echo_string="Testing for handle_push_button:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 handle_push_button.py --help"
eval "$echo_string"

echo_string="Testing for media_uploader:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 media_uploader.py --help"
eval "$echo_string"

echo_string="Testing for selfie_with_filters:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 selfie_with_filters.py --help"
eval "$echo_string"

echo_string="Testing for take_photo:"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 take_photo.py --help"
eval "$echo_string"

echo_string="------------------- Creating tmp dirs first --------------------"
echo $'\n'$echo_string$'\n'
echo_string="mkdir -p /tmp/project_cerebro/media && mkdir -p /tmp/project_cerebro/logs"
eval "$echo_string"

echo_string="------------------- Now, Testing for audio function --------------------"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 generate_audio.py --text 'This is just a test of the underlying audio subsystem'"
eval "$echo_string"

echo_string="------------------- Now, Testing for camera & led function --------------------"
echo $'\n'$echo_string$'\n'
echo_string="cd ../py_client && python3 cerebro_test_camera_led.py"
eval "$echo_string"

echo_string="------------------- Cleanup tmp dirs --------------------"
echo $'\n'$echo_string$'\n'
echo_string="rm -rf /tmp/project_cerebro"
eval "$echo_string"

echo_string="Cerebro Hardware Test script - Completed!"
echo $'\n'$echo_string$'\n'

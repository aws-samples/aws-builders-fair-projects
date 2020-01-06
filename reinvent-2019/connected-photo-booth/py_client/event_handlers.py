try:
    #from picamera import PiCamera
    from gpiozero import LED, Button
    #from gpiozero import LED
    test_environment = False
except (ImportError, RuntimeError):
    #import cv2
    test_environment = True

import boto3
import botocore

import os
import glob
import json
import requests

from datetime import datetime
from time import sleep
from time import gmtime, strftime

import sys, getopt

import argparse

import subprocess

from cerebro_utils import *
from take_photo import process_take_photo
from button_utils import *

from shutil import copyfile, rmtree

import logging

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

from config import Configuration

# --------- Module- Level Globals ---------------
kill_request = False
#global variables
image_dir = None
debug_mode = None
sqs_interval = None
initialize_logger = None
device_id = "Ronan"

config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

'''
# AWS RESOURCE: Switch
__QUEUE_URL__ = "https://queue.amazonaws.com/456038447595/cerebro_client"
__SQS_QUEUE_NAME__ = 'cerebro_client'
__SQS_BACKEND_QUEUE__ = 'cerebro_backend'

__APIGW_X_API_KEY__ = "2YSoTXerhD4u3iat9CWUM9kn756MTJIp4c4Tgfqk"
__APIGW_X_API_KEY_QR_CODE__ = "aLCOemQkKa6EzcOQU6xjI8T2hRzD4Cf050EwWdb1"

__APIGW_API__ = "https://lqhvtjhlsc.execute-api.us-east-1.amazonaws.com/production/Cerebro_GetImages_S3List"
__APIGW_API_QR_CODE__ = "https://lqhvtjhlsc.execute-api.us-east-1.amazonaws.com/production/Cerebro_GetQRCode"

__S3_BUCKET__ = "project-cerebro"
__CEREBRO_TEMP_DIR__ = "/tmp/project_cerebro"
__CEREBRO_MEDIA_DIR__ = "/tmp/project_cerebro/media"
__CEREBRO_LOGS_DIR__ = "/tmp/project_cerebro/logs"
__CEREBRO_PROFILES_DIR__ = "/tmp/project_cerebro/profiles"
__CEREBRO_SYSTEM_DIR__ = "/tmp/project_cerebro/system"
__IMAGE_MAX_COUNT__ = 10

__GREEN_LED__ = 27
__GREEN_BUTTON__ = 17
__YELLOW_LED__ = 26
__YELLOW_BUTTON__ = 16
'''

def process_download_or_print_request(accept_led=None, choice_led=None, user_request_type="download", image_dir=config.__CEREBRO_MEDIA_DIR__):

	process_download_or_print_request_logger = logging.getLogger('cerebro_processor.process_download_or_print_request')

	speech_text="Processing request for %sing images ..." % user_request_type
	speech_file_path = generate_audio(speech_text=speech_text)
	play_audio(file_path=speech_file_path)

	# 0. show default loading image first
	show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__)
	sleep(1)
	
	delete_local_files(image_dir=image_dir)

	# 1. download all images into staging dir
	#create the staging dir
	staging_dir = "%s/staging" % config.__CEREBRO_TEMP_DIR__
	os.makedirs(staging_dir, mode=0o777)

	process_download_or_print_request_logger.info("Getting media now ....")
	media_count = download_media(profile_name="", media_dir=staging_dir, ignore_stock_profiles=True)
	process_download_or_print_request_logger.info("Media Count retrieved: %d" % media_count)

	# 2. show first image and then check for button input
	chosen_image_id = ""
	files = glob.glob('%s/*' % staging_dir)
	for file in files:
		process_download_or_print_request_logger.info("Displaying image: %s for download ..." % file)
		# now copy in file to main image_dir
		copyfile(file, "%s/%s" % (image_dir, os.path.basename(file)))

		process_download_or_print_request_logger.info("Completed the copy of the file into mediadir: %s" % file)
		# display image
		show_images(media_dir=image_dir)

		# now wait for button press
		if not test_environment:
			accept_led.blink()
			choice_led.blink()

		process_download_or_print_request_logger.info("Setting up for the button input choice for this image ...")

		# button handler for accepting photo
		btn_input = button_handler(accept_led=accept_led, choice_led=choice_led, \
			green_button_text="to select this image", \
			yellow_button_text="to choose a different image")

		# now call the method to takephoto
		process_download_or_print_request_logger.info("push button input received as: %d" % btn_input)

		if btn_input == 1:
			profile_prompt = "Congratulations, you want to select this image!"
		elif btn_input == 2:
			profile_prompt = "Sure, we can look at the next image!"
		else:
			profile_prompt = "Default text"

		speech_file_path = generate_audio(speech_text=profile_prompt)
		process_download_or_print_request_logger.info("Generated Audio now. Playing audio next: ")
		play_audio(file_path=speech_file_path)
		process_download_or_print_request_logger.info("Audio played. Done!")

		# turn off the led
		process_download_or_print_request_logger.info("Turning off the LED now - TBD")
		if not test_environment:
			accept_led.off()
			choice_led.off()

		process_download_or_print_request_logger.info("Now sorting out based on buttons selected")
		if btn_input == 1:
			process_download_or_print_request_logger.info("Image chosen: %s" % file)
			# now get out of the loop with the chosen_image_id
			chosen_image_path = file
			chosen_image_id = os.path.basename(file)
			break
		elif btn_input == 2:
			show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__)
			sleep(1)
			
			delete_local_files(image_dir=image_dir)

	# 3. if image chosen, then request for qrcode with this imageid and display this message for 1 minute
	# 4. go to next image and display
	# 5. if all images were chosen, play message that all were shown and since no choice was made, quitting
	# 6. send sqs to display default slideshow and return

	if chosen_image_id:
		# playback a placeholder message for downloading the qrcode
		process_download_or_print_request_logger.info("ImageID: %s" % chosen_image_id)
		if user_request_type == "download":
			speech_text = "Retrieving the QRCode for the image chosen earlier ... "
		elif user_request_type == "print":
			speech_text = "Printing the image chosen earlier ..."
	else:
		# playback a placeholder message for abandoning downloads
		speech_text = "Thats unfortunate, looks like none of the images were suitable for a %s." % user_request_type 
		speech_text += " Now, abandoning the %s request. " % user_request_type
		
	speech_file_path = generate_audio(speech_text=speech_text)
	play_audio(file_path=speech_file_path)

	if not chosen_image_id:
		# delete the staging dir
		rmtree(staging_dir)

		# reset to default slideshow
		sqs_msg = {}
		sqs_msg["action"] = "show_profile"
		sqs_msg["profile"] = ""
		send_iot_message(iot_msg=sqs_msg, device_id=device_id, delay=60)

		return

	if user_request_type == "print":
		# now call the print function
		print_image(fileName=chosen_image_path)
		profile_prompt="Image was now printed. Hope you like it."
		speech_file_path = generate_audio(speech_text=profile_prompt)
		play_audio(file_path=speech_file_path)
	elif user_request_type == "download":

		process_download_or_print_request_logger.info("Now retrieving the QR Code ...")

		# just a temp - to allow for the deletes and downloads to happen in peace
		show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__)
		sleep(1)
		
		delete_local_files(image_dir=image_dir)

		process_download_or_print_request_logger.info("Getting QRCode now ....")
		download_qrcode(image_id=chosen_image_id)
		process_download_or_print_request_logger.info("QRCode retrieved")

		process_download_or_print_request_logger.info("execute the slideshow")

		show_images(media_dir=image_dir)

		speech_text="Direct your phone camera to the qr code displayed and displayed on the link that pops up. For your safety, this link will expire in 5 minutes."
		speech_file_path = generate_audio(speech_text=speech_text)
		play_audio(file_path=speech_file_path)

		sqs_msg = {}
		sqs_msg["action"] = "cleanup_qrcode"
		send_sqs_message(sqs_queue=config.__SQS_BACKEND_QUEUE__, sqs_msg=sqs_msg, device_id="lambda-only", delay=300)

	# delete the staging dir
	rmtree(staging_dir)

	sqs_msg = {}
	sqs_msg["action"] = "show_profile"
	sqs_msg["profile"] = ""
	send_iot_message(iot_msg=sqs_msg, device_id=device_id, delay=60)

	return

def process_kill_request(debug_mode=None, image_dir=""):

	process_logger = logging.getLogger('cerebro_processor.process_kill_request')

	#slideshow_util_stop = "../scripts/stop-picture-frame.sh"
	slideshow_util_stop = "../scripts/stop-slideshow-only.sh"
	slideshow_log_stop = "%s/picframe.stop.log" % config.__CEREBRO_LOGS_DIR__

	if debug_mode:
		process_logger.info("Killing the monitor process now. ignore all other parameters.")
		return True

	else:
		process_logger.info("Killing the monitor process now. Breaking out of the loop now ...")
		delete_local_files(image_dir=image_dir)
		status = subprocess.call(
			'%s > %s 2>&1 &' % 
			(slideshow_util_stop, slideshow_log_stop), 
			shell=True)
		return True

	process_logger.error("Error! Invalid DebugMode!!")
	return False

def process_photo_captured(debug_mode=None, sqs_msg=None, accept_led=None, choice_led=None, device_id=None):
	process_logger = logging.getLogger('cerebro_processor.process_photo_captured')
	process_logger.info("Entered process_photo_captured")

	if not test_environment:
		accept_led.blink()
		choice_led.blink()

	# audio out
	picture_text = "picture"
	selfie_mode = None
	if "selfie_mode" in sqs_msg.keys():
		if int(sqs_msg["selfie_mode"]):
			picture_text = "selfie"
			selfie_mode = True
		else:
			picture_text = "profile picture"
			selfie_mode = False

	green_button_text = "to accept this %s" % picture_text
	yellow_button_text = "to take a new %s" % picture_text

	# button handler for accepting photo
	btn_input = button_handler(accept_led=accept_led, choice_led=choice_led, \
		green_button_text=green_button_text, yellow_button_text=yellow_button_text)

	# now call the method to takephoto
	process_logger.info("push button input received as: %d" % btn_input)

	# results in redundant messages , lets try and avoid
	if btn_input == 1:
		#profile_prompt = "Congratulations, Your %s was taken." % picture_text
		profile_prompt = "Excellent, You liked your %s ." % picture_text
	elif btn_input == 2:
		profile_prompt = "Sure, we can take your %s again!" % picture_text
	else:
		profile_prompt = "Default text"

	fname = profile_prompt.replace(" ", "_")
	fname = fname.replace(".", "")

	speech_file_path = generate_audio(speech_text=profile_prompt, filename=fname+".mp3")
	process_logger.info("Generated Audio now. Playing audio next: ")
	play_audio(file_path=speech_file_path)
	process_logger.info("Audio played. Done!")

	# turn off the led
	process_logger.info("Turning off the LED now - TBD")
	if not test_environment:
		accept_led.off()
		choice_led.off()

	# now, if choice button , set a message for choosing a photo i.e. selfie
	# else, if accept button, set a message for applying filters						
	if btn_input == 2:
		sqs_msg_choice = {}
		sqs_msg_choice["choose_again"] = "1"
		if selfie_mode:
			sqs_msg_choice["action"] = "selfie"
		else:
			sqs_msg_choice["action"] = "register"
			if "profile_chosen" in sqs_msg.keys():
				sqs_msg_choice["profile"] = sqs_msg["profile_chosen"]
			else:
				sqs_msg_choice["profile"] = "noprofilefound"
		send_iot_message(iot_msg=sqs_msg_choice, device_id=device_id)
	elif btn_input == 1:
		sqs_msg_accept = {}
		if selfie_mode:
			sqs_msg_accept["action"] = "apply_filter"
		else:
			sqs_msg_accept["action"] = "upload_request"
			sqs_msg_accept["selfie_mode"] = str(int(selfie_mode))
			sqs_msg_accept["image_path"] = sqs_msg["image_path"]
		send_iot_message(iot_msg=sqs_msg_accept, device_id=device_id)

def process_filters_applied(debug_mode=None, sqs_msg=None, accept_led=None, choice_led=None, device_id=None):
	process_logger = logging.getLogger('cerebro_processor.process_filters_applied')
	process_logger.info("Entered process_filters_applied")

	if not test_environment:
		accept_led.blink()
		choice_led.blink()

	# button handler for accepting photo
	green_button_text = "to select this filter"
	yellow_button_text = "to choose a new filter"
	btn_input = button_handler(green_button_text=green_button_text, yellow_button_text=yellow_button_text)

	# turn on the LED
	if not test_environment:
		if btn_input == 1:
			accept_led.on()
			choice_led.off()
		elif btn_input == 2:
			accept_led.off()
			choice_led.on()
	process_logger.info("Turning on the LED now - TBD")

	# now call the method to takephoto
	process_logger.info("push button input received as: %d" % btn_input)

	# audio out
	picture_text = "picture"
	if "selfie_mode" in sqs_msg.keys():
		if int(sqs_msg["selfie_mode"]):
			picture_text = "selfie"
		else:
			picture_text = "profile picture"

	if btn_input == 1:
		profile_prompt = "Excellent, You liked the filter applied!"
	elif btn_input == 2:
		profile_prompt = "Sure, we can applying the filters again ..."
	else:
		profile_prompt = "Default text"

	fname = profile_prompt.replace(" ", "_")
	fname = fname.replace(".", "")

	speech_file_path = generate_audio(speech_text=profile_prompt, filename=fname+".mp3")
	process_logger.info("Generated Audio now. Playing audio next: ")
	play_audio(file_path=speech_file_path)
	process_logger.info("Audio played. Done!")

	# turn off the led
	process_logger.info("Turning off the LED now - TBD")
	if not test_environment:
		accept_led.off()
		choice_led.off()

	# now, if choice button , set a message for choosing a photo i.e. selfie
	# else, if accept button, set a message for applying filters						
	if btn_input == 2:
		sqs_msg_choice = {}
		sqs_msg_choice["action"] = "apply_filter"
		send_iot_message(iot_msg=sqs_msg_choice, device_id=device_id)
	elif btn_input == 1:
		# reset the filters applied setting to be ready for the next selfie
		persist_setting(setting_name='image_filter_applied', setting_value='')

		sqs_msg_accept = {}
		sqs_msg_accept["action"] = "apply_effect"
		send_iot_message(iot_msg=sqs_msg_accept, device_id=device_id)

def process_effects_applied(debug_mode=None, sqs_msg=None, accept_led=None, choice_led=None, device_id=None):
	process_logger = logging.getLogger('cerebro_processor.process_effects_applied')
	process_logger.info("Entered process_effects_applied")

	if not test_environment:
		accept_led.blink()
		choice_led.blink()

	# button handler for accepting photo
	green_button_text = "to select this image effect"
	yellow_button_text = "to choose a new image effect"
	btn_input = button_handler(green_button_text=green_button_text, yellow_button_text=yellow_button_text)

	# turn on the LED
	if not test_environment:
		if btn_input == 1:
			accept_led.on()
			choice_led.off()
		elif btn_input == 2:
			accept_led.off()
			choice_led.on()
	process_logger.info("Turning on the LED now - TBD")

	# now call the method to takephoto
	process_logger.info("push button input received as: %d" % btn_input)

	# audio out
	picture_text = "picture"
	if "selfie_mode" in sqs_msg.keys():
		if int(sqs_msg["selfie_mode"]):
			picture_text = "selfie"
		else:
			picture_text = "profile picture"

	if btn_input == 1:
		profile_prompt = "Excellent, You liked the effect applied!"

	elif btn_input == 2:
		profile_prompt = "Sure, we can apply the effects again ..."
	else:
		profile_prompt = "Default text"
		
	fname = profile_prompt.replace(" ", "_")
	fname = fname.replace(".", "")
	speech_file_path = generate_audio(speech_text=profile_prompt, filename=fname+".mp3")
	process_logger.info("Generated Audio now. Playing audio next: ")
	play_audio(file_path=speech_file_path)
	process_logger.info("Audio played. Done!")

	# turn off the led
	process_logger.info("Turning off the LED now - TBD")
	if not test_environment:
		accept_led.off()
		choice_led.off()

	# now, if choice button , set a message for choosing a photo i.e. selfie
	# else, if accept button, set a message for applying filters						
	if btn_input == 2:
		sqs_msg_choice = {}
		sqs_msg_choice["action"] = "apply_effect"
		send_iot_message(iot_msg=sqs_msg_choice, device_id=device_id)
	elif btn_input == 1:
		# reset the effects applied setting to be ready for the next selfie
		persist_setting(setting_name='image_effect_applied', setting_value='')

		# send out the upload request
		sqs_msg_accept = {}
		sqs_msg_accept["action"] = "upload_request"
		send_iot_message(iot_msg=sqs_msg_accept, device_id=device_id)

def process_upload_request(debug_mode=None, sqs_msg=None, accept_led=None, choice_led=None, device_id=None):
	process_logger = logging.getLogger('cerebro_processor.process_upload_request')
	process_logger.info("Entered process_upload_request")

	# audio out
	picture_text = "picture"
	if "selfie_mode" in sqs_msg.keys():
		if int(sqs_msg["selfie_mode"]):
			picture_text = "selfie"
		else:
			picture_text = "profile picture"

	profile_prompt = "Would you like to upload this %s ?" % picture_text
	fname = profile_prompt.replace(" ", "_")
	fname = fname.replace(".", "")
	fname = fname.replace("?", "")
	speech_file_path = generate_audio(speech_text=profile_prompt, filename=fname+".mp3")
	process_logger.info("Generated Audio now. Playing audio next: ")
	play_audio(file_path=speech_file_path)
	process_logger.info("Audio played. Done!")

	if not test_environment:
		accept_led.blink()
		choice_led.blink()

	# button handler for accepting photo
	green_button_text = "to upload this %s" % picture_text
	yellow_button_text = "to not upload this %s" % picture_text
	btn_input = button_handler(green_button_text=green_button_text, yellow_button_text=yellow_button_text)

	# turn on the LED
	if not test_environment:
		if btn_input == 1:
			accept_led.on()
			choice_led.off()
		elif btn_input == 2:
			accept_led.off()
			choice_led.on()
	process_logger.info("Turning on the LED now - TBD")

	# now call the method to takephoto
	process_logger.info("push button input received as: %d" % btn_input)

	if btn_input == 1:
		profile_prompt = "Excellent, You would like to upload the %s taken!" % picture_text
	elif btn_input == 2:
		profile_prompt = "Sure, we will not upload the %s!" % picture_text
	else:
		profile_prompt = "Default text"

	fname = profile_prompt.replace(" ", "_")
	fname = fname.replace(".", "")
	speech_file_path = generate_audio(speech_text=profile_prompt, filename=fname+".mp3")
	process_logger.info("Generated Audio now. Playing audio next: ")
	play_audio(file_path=speech_file_path)
	process_logger.info("Audio played. Done!")

	# turn off the led
	process_logger.info("Turning off the LED now - TBD")
	if not test_environment:
		accept_led.off()
		choice_led.off()

	# now, if choice button , set a message for showing default slideshow - profile=all
	# else, if accept button, upload the image and send confirmation
	if btn_input == 2:
		sqs_msg_choice = {}
		sqs_msg_choice["action"] = "show_profile"
		sqs_msg_choice["profile"] = ""
		send_iot_message(iot_msg=sqs_msg_choice, device_id=device_id)
	elif btn_input == 1:
		# first do the uploads
		if "image_path" in sqs_msg.keys():
			image_path = sqs_msg["image_path"]
		else:
			image_path = "/tmp/project_cerebro/media/filtered_image_effects.jpg"

		upload_image(image_path=image_path, device_id=device_id)
		# now send the completed msg
		sqs_msg_accept = {}
		sqs_msg_accept["action"] = "upload_completed"
		send_iot_message(iot_msg=sqs_msg_accept, device_id=device_id)

		profile_prompt = "Image was successfully uploaded !"
		fname = profile_prompt.replace(" ", "_")
		fname = fname.replace(".", "")
		speech_file_path = generate_audio(speech_text=profile_prompt, filename=fname+".mp3")
		process_logger.info("Generated Audio now. Playing audio next: ")
		play_audio(file_path=speech_file_path)
		process_logger.info("Audio played. Done!")

	return

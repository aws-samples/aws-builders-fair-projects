#!/usr/bin/python3

import boto3
from time import sleep
import argparse
import subprocess
import logging
import os
import json
from shutil import copyfile

from rpi_utils import *
from aws_utils import *
from cerebro_utils import *

from time import gmtime, strftime

try:
	from picamera import PiCamera
	#from gpiozero import LED, Button
	from gpiozero import LED
	test_environment = False
except (ImportError, RuntimeError):
	import cv2
	test_environment = True

from config import Configuration

# --------- Module- Level Globals ---------------
config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

'''
__PROFILE_PATH__ = "/tmp/project_cerebro/profiles"
__CEREBRO_LOGS_DIR__ = "/tmp/project_cerebro/logs"
__CEREBRO_TEMP_DIR__ = "/tmp/project_cerebro"
__CEREBRO_MEDIA_DIR__ = "/tmp/project_cerebro/media"
__CEREBRO_SYSTEM_DIR__ = "/tmp/project_cerebro/system"
__QUEUE_URL__ = "https://queue.amazonaws.com/456038447595/cerebro_client"
__SQS_QUEUE_NAME__ = 'cerebro_client'

__GREEN_LED__ = 27
__GREEN_BUTTON__ = 17
__YELLOW_LED__ = 26
__YELLOW_BUTTON__ = 16

__PUSHBUTTON_DELAY__ = 300
'''

def capture_image(profile_name='', selfie_mode=False):

	capture_image_logger = logging.getLogger('take_profile_photo.capture_image')
	capture_image_logger.info("Entered the capture_image handler ...")

	if profile_name:
		image_path = "%s/profile_%s.jpg" % (config.__CEREBRO_PROFILES_DIR__, profile_name.lower())
	else:
		image_path = "%s/image.jpg" % config.__CEREBRO_PROFILES_DIR__

	capture_image_logger.info("image_path: %s" % image_path)
	capture_image_logger.info("Starting the camera...")

	while True:

		# now enabling the display
		control_display(enable_display=True)
		sleep(1)

		# try and take the picture

		if not test_environment:
			# This assumes its a Pi platform
			camera = PiCamera()

			camera.rotation = 180

			camera.start_preview()
			#camera.start_recording('/home/pi/Desktop/video.h264')

			sleep(5)

			camera.capture(image_path)

			#camera.stop_recording()
			camera.stop_preview()

			capture_image_logger.info("Image is now captured and available in: %s" % image_path)

			camera.close()
			
		else:
			# this assumes that opencv is installed and a webcam exists
			# Loading Camera and Nose image and Creating mask

			cap = cv2.VideoCapture(0)

			print("start ...")
			while True:
				_, frame = cap.read()

				#rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

				cv2.imshow("Frame", frame)

				#sleep(2)

				key = cv2.waitKey(1)
				if key == 27:
					break

				#print("Take %d" % (i+1))

			cap.release()
			cv2.destroyAllWindows()
			sleep(5)
			#cv2.imwrite("captured.jpg", frame)
			cv2.imwrite(image_path, frame)
			capture_image_logger.info("Image is now captured and available in: %s" % image_path)

		capture_image_logger.info("Image captured, turning off display now ...")
		# disabling the display immediately
		control_display(enable_display=False)

		capture_image_logger.info("Retrieving Facial Landmarks now ...")
		# Now check if the image captured contains a face
		face_detected = get_facial_landmarks(image_path=image_path)
		if face_detected:
			break

		capture_image_logger.info("No Face detected, so announce this and retry")
		# This means no face was detected so continue the attempt to capture an image
		# disabling the display immediately
		control_display(enable_display=True)
		sleep(5)

		speech_text="No Face detected so please try again ..."
		speech_file_path = generate_audio(speech_text=speech_text)
		play_audio(file_path=speech_file_path)

	# now the common path top copy the file and start the slideshow ...
	capture_image_logger.info("And now, copying in the new profile taken ...")
	basename = os.path.basename(image_path)
	target = "%s/media/%s" % (config.__CEREBRO_TEMP_DIR__, basename)
	copyfile(image_path, target)

	return image_path

def initialize():

	parser = argparse.ArgumentParser()
	parser.add_argument("device_id", help="Device ID (string of characters is ok)")	
	parser.add_argument("--logfile", help="Logfile for all INFO/DEBUG level logs")
	parser.add_argument("--register", help="Register a profile - Profile can be provided (sachin, deeksha, etc.)" )
	parser.add_argument("--selfie", help="Selfie Mode to just take pictures in general", action='store_true' )
	parser.add_argument("--accept_picture", help="Mostly a debug helper - to indicate photo was accepted" )
	parser.add_argument("--debug", help="debug mode to not run scripts", action='store_true')
	parser.add_argument("--iot", help="IOT button mode", action='store_true')
	args = parser.parse_args()
	#print(args)

	# and now setup the logging profile
	# set up logging to file - see previous section for more details
	if args.logfile:
		logFile = args.logfile
	else:
		current_time = strftime("%Y_%m_%dT%H_%M_%S", gmtime())
		logFile = '%s/take_photo_%s.log' % (config.__CEREBRO_LOGS_DIR__, current_time)

	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
						datefmt='%m-%d %H:%M',
						filename=logFile,
						filemode='w')
	
	# define a Handler which writes INFO messages or higher to the sys.stderr
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	# set a format which is simpler for console use
	formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
	# tell the handler to use this format
	console.setFormatter(formatter)

	# Now, define a couple of other loggers which might represent areas in your
	# application:
	initialize_logger = logging.getLogger('take_profile_photo.initialize')

	initialize_logger.info(args)

	device_id = "default_device"
	if args.device_id:
		# tokenize if needed
		device_id_tokens = args.device_id.split()
		if len(device_id_tokens) > 0:
			device_id = device_id_tokens[0]


	profile_name = ''

	if args.register:
		profile_name = args.register
		if not profile_name:
			initialize_logger.info("Profile Name needs to be provided to register.")
			exit(1)
	
		initialize_logger.info("Profile to be registered: %s" % profile_name)

	selfie_mode = None

	if args.selfie:
		selfie_mode = args.selfie
		initialize_logger.info("Selfie Mode triggered.")
	else:
		selfie_mode = False
		initialize_logger.info("Register Mode triggered.")

	if args.accept_picture:
		accept_picture = args.accept_picture
	else:
		accept_picture = ''

	if args.iot:
		iot_mode = True
	else:
		iot_mode = False

	return profile_name, selfie_mode, accept_picture, iot_mode, device_id

def process_take_photo(profile_name='', selfie_mode=False, iot_mode=True, device_id=None):

	process_take_photo_logger = logging.getLogger('take_photo.process_take_photo')

	image_path = ''

	process_take_photo_logger.info("BEFORE capture_image: profile_name: %s , selfie_mode: %s" % (profile_name, selfie_mode) )
	if profile_name:
		process_take_photo_logger.info(profile_name)
		process_take_photo_logger.info("Profile pic to be taken ...")
		image_path = capture_image(profile_name=profile_name)
		picture_text = "Profile picture"
	elif selfie_mode:
		process_take_photo_logger.info(profile_name)
		process_take_photo_logger.info("Selfies to be taken ...")
		image_path = capture_image(selfie_mode=selfie_mode)
		picture_text = "Selfie"
	else:
		process_take_photo_logger.info("No valid option provided at cmdline")
		return image_path

	# now display those images
	show_images()

	process_take_photo_logger.info("ADTER: picture_text: %s" % picture_text )
	profile_prompt = "Your %s was taken successfully." % picture_text

	fname = profile_prompt.replace(" ", "_")
	fname = fname.replace(".", "")
	process_take_photo_logger.info("fname calculated to be: %s" % fname)

	speech_file_path = generate_audio(speech_text=profile_prompt, filename=fname+".mp3")
	process_take_photo_logger.info("Speech Text:'%s', file: %s.mp3 " % (profile_prompt, fname))
	play_audio(file_path=speech_file_path)
	process_take_photo_logger.info("Audio played. Done!")

	'''
	# setup for the IOT button press now
	if selfie_mode:
		iot_button_event = "selfie_picture_accept"
	else:
		iot_button_event = "profile_picture_accept"

	if iot_mode:
		iot_button_attributes = update_button_attributes(ready_for_event=iot_button_event, 
								image_path=image_path, selfie_mode=selfie_mode)
	else:
	'''

	# now setup the sqs to indicate ready for button input
	sqs_msg = {}
	sqs_msg["action"] = "photo_captured"
	sqs_msg["selfie_mode"] = str(int(selfie_mode))
	sqs_msg["image_path"] = image_path
	sqs_msg["profile_chosen"] = profile_name
	sqs_msg["device_id"] = device_id

	send_iot_message(iot_msg=sqs_msg, delay=0, device_id=device_id)

	return image_path

if __name__ == "__main__":

	profile_name, selfie_mode, accept_picture, iot_mode, device_id = initialize()

	main_logger = logging.getLogger('take_profile_photo.main')

	main_logger.info("In main thread ...")

	if accept_picture:
		image_path = accept_picture
		process_accept_picture(selfie_mode=selfie_mode, image_path=image_path)
		main_logger.info("Photo was accepted!")

	else:
		# lets turn shutdown the slideshow and then delete the local files

		show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__)
		delete_local_files()
		sleep(1)
		
		# purpose of this method is to 
		#	take the photo , 
		#	show the image captured, and then 
		#	pass a message back saying: ready for button input

		image_path = process_take_photo(profile_name=profile_name, selfie_mode=selfie_mode, iot_mode=iot_mode, device_id=device_id)

		main_logger.info("Photo was taken and button was setup for a trigger. No failsafe currently!")
		main_logger.info("Profile pic taken and available in: %s" % image_path)

		main_logger.info("Now the images should be displayed")

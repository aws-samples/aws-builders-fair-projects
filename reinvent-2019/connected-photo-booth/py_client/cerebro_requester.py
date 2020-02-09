#!../venv/bin/python3

import boto3
import botocore
import os
import json

import requests
from datetime import datetime
from time import sleep
from time import gmtime, strftime
import sys, getopt
import argparse
import subprocess
import logging
from cerebro_utils import send_sqs_message
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

from cerebro_utils import send_sqs_message

from config import Configuration

# --------- Module- Level Globals ---------------
image_dir = "/tmp"
debug_mode = False

myAWSIoTMQTTClient = None

config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

def initialize_mqtt_client(clientId=''):

	initialize_mqtt_client_logger = logging.getLogger('cerebro_requester.initialize_mqtt_client')
	initialize_mqtt_client_logger.info("In initialize_mqtt_client ...")

	if not clientId:
		initialize_mqtt_client_logger.error("Error! No clientId provided - cannot init IOTCore without this!")
		return None

	host = config.__IOT_HOST__
	rootCAPath = config.__IOT_ROOT_CA_PATH__
	certificatePath = config.__IOT_CERTIFICATE_PATH__
	privateKeyPath = config.__IOT_PRIVATE_KEY_PATH__

	topic = config.__IOT_TOPIC__

	port = 443

	# Init AWSIoTMQTTClient
	myAWSIoTMQTTClient = None

	myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
	myAWSIoTMQTTClient.configureEndpoint(host, port)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

	# AWSIoTMQTTClient connection configuration
	myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
	myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
	myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
	myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

	# Connect and subscribe to AWS IoT
	myAWSIoTMQTTClient.connect()

	initialize_mqtt_client_logger.info("Completed initialize_mqtt_client!")

	return myAWSIoTMQTTClient

def send_iot_message(iot_msg={}, delay=0, device_id="default_device", topic=config.__IOT_TOPIC__):
    send_iot_message_logger = logging.getLogger('take_profile_photo.send_iot_message')
    send_iot_message_logger.info("Entered send_iot_message ...")
    message = {}
    message['message'] = iot_msg
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    return True

def initialize():
	parser = argparse.ArgumentParser()

	parser.add_argument("device_id", help="Device ID (string of characters is ok)")
	parser.add_argument("--logfile", help="Logfile for all INFO/DEBUG level logs")
	parser.add_argument("--profile", help="Start the Slideshow - Profile to be provided (all, sachin, deeksha, etc.)")
	parser.add_argument("--stop", help="Stop The Slideshow", action='store_true')
	parser.add_argument("--kill", help="Kill The Monitoring script", action='store_true')
	parser.add_argument("--register", help="Register a profile - Profile can be provided (sachin, deeksha, etc.)" )
	parser.add_argument("--selfie", help="Take a selfie", action='store_true')
	parser.add_argument("--end_session", help="End the cerebro session", action='store_true')
	parser.add_argument("--photo_capture", help="Photo Captured", action='store_true')
	parser.add_argument("--button_click", help="Simulate an IOT button click - parameters can be 'single', 'double', 'longpress'" )
	parser.add_argument("--debug", help="debug mode to not run scripts", action='store_true')
	parser.add_argument("--download_image", help="Download My Image", action='store_true')
	parser.add_argument("--command", help="Provide the command to send over to the Cerebro ('cleanup_qrcode')")
	args = parser.parse_args()

	# 1. setup env. vars

	device_id = "default_device"
	if args.device_id:
		# tokenize if needed
		device_id_tokens = args.device_id.split()
		if len(device_id_tokens) > 0:
			device_id = device_id_tokens[0]

	if args.debug:
		debug_mode = True
	else:
		debug_mode = False

	# and now setup the logging profile
	# set up logging to file - see previous section for more details
	if args.logfile:
		logFile = args.logfile
	else:
		current_time = strftime("%Y_%m_%dT%H_%M_%S", gmtime())
		logFile = '%s/cerebro_requester_%s.log' % (config.__CEREBRO_LOGS_DIR__, current_time)

	if args.profile:
		if args.profile == "all":
			profile_name = ""
		else:
			profile_name = args.profile
		show_profile_requested = True
	else:
		profile_name = ""
		show_profile_requested = False

	if args.stop:
		stop_request = True
	else:
		stop_request = False

	if args.kill:
		kill_request = True
	else:
		kill_request = False

	if args.register:
		register_request = True
		profile_name = args.register
	else:
		register_request = False

	if args.selfie:
		selfie_request = True
	else:
		selfie_request = False

	if args.end_session:
		end_session_request = True
	else:
		end_session_request = False

	if args.button_click:
		button_click_request = True
		click_type = args.button_click
	else:
		button_click_request = False
		click_type = None

	if args.photo_capture:
		photo_captured = True
	else:
		photo_captured = False

	if args.download_image:
		download_image_request = True
	else:
		download_image_request = False

	if args.command:
		action_request = args.command.strip()
	else:
		action_request = ""

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

	media_requester_logger = logging.getLogger('media_requester.initialize')

	media_requester_logger.info("Image Dir: %s, Debug Mode: %d" % (image_dir, debug_mode))

	return profile_name, stop_request, kill_request, \
			register_request, selfie_request, \
			end_session_request, button_click_request, click_type, show_profile_requested, \
			photo_captured, device_id, download_image_request, action_request

if __name__ == "__main__":

    profile_name, stop_request, kill_request, \
    register_request, selfie_request, end_session_request, \
    button_click_request, click_type, show_profile_requested, \
    photo_captured, device_id, download_image_request, action_request = initialize()

    media_requester_logger = logging.getLogger('media_requester.main')
    media_requester_logger.info("Finished initialize.")

    # set up the MQTT Client now
    myAWSIoTMQTTClient = initialize_mqtt_client(clientId=config.__IOT_CLIENT_ID_REQUESTER__)

    media_requester_logger.info("Sending an IoT message ...")
    media_request = {}

    media_request["device_id"] = device_id
    media_request["profile"] = profile_name

    if action_request:
        media_request["action"] = action_request
    elif show_profile_requested:
        media_request["action"] = "show_profile"
    elif register_request:
        media_request["action"] = "register"
    elif selfie_request:
        media_request["action"] = "selfie"
    elif stop_request:
        media_request["action"] = "stop"
    elif kill_request:
        media_request["action"] = "kill"    
    elif end_session_request:
        media_request["action"] = "end_session"
    elif photo_captured:
        media_request["action"] = "photo_captured"
    elif button_click_request:
        media_request["action"] = "button_clicked"
        media_request["clickType"] = click_type
    elif download_image_request:
        media_request["action"] = "download_image"

    media_requester_logger.info(media_request)

    if action_request == "cleanup_qrcode":
        send_sqs_message(sqs_msg=media_request, sqs_queue=config.__SQS_BACKEND_QUEUE_NAME__)
    else:
        send_iot_message(media_request)

    media_requester_logger.info("Media Requested now. Exiting!")

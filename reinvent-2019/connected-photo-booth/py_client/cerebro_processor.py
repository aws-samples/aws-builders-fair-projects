#!../venv/bin/python3

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
from event_handlers import *
from config import Configuration

from shutil import copyfile, rmtree

import logging

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

# --------- Module- Level Globals ---------------
myAWSIoTMQTTClient = None

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

def initialize_mqtt_client(clientId=''):

    initialize_mqtt_client_logger = logging.getLogger('cerebro_processor.initialize_mqtt_client')
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

def initialize():

    parser = argparse.ArgumentParser()
    parser.add_argument("device_id", help="Device ID (string of characters is ok)") 
    parser.add_argument("--logfile", help="Logfile for all INFO/DEBUG level logs")
    parser.add_argument("--imagedir", help="directory to host all images")
    parser.add_argument("--interval", help="Interval to check SQS for command requests (in seconds)", type=int)
    parser.add_argument("--debug", help="debug mode to not run scripts", action='store_true')
    parser.add_argument("--clean", help="clean start - delete all old files", action='store_true')
    args = parser.parse_args()

    device_id = "default_device"
    if args.device_id:
        # tokenize if needed
        device_id_tokens = args.device_id.split()
        if len(device_id_tokens) > 0:
            device_id = device_id_tokens[0]

    # first setup the dirs
    setup_dirs(dir_to_create=config.__CEREBRO_PROFILES_DIR__, clean_mode=args.clean)
    setup_dirs(dir_to_create=config.__CEREBRO_LOGS_DIR__, clean_mode=args.clean)
    setup_dirs(dir_to_create=config.__CEREBRO_MEDIA_DIR__, clean_mode=args.clean)
    setup_dirs(dir_to_create=config.__CEREBRO_SYSTEM_DIR__, clean_mode=args.clean)
    
    # and now setup the logging profile
    # set up logging to file - see previous section for more details
    if args.logfile:
        logFile = args.logfile
    else:
        current_time = strftime("%Y_%m_%dT%H_%M_%S", gmtime())
        logFile = '%s/cerebro_processor_%s.log' % (config.__CEREBRO_LOGS_DIR__, current_time)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=logFile,
                        filemode='w')
    
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)

    # Now, define a couple of other loggers which might represent areas in your application:
    initialize_logger = logging.getLogger('cerebro_processor.initialize')

    initialize_logger.info(args)

    # 1. setup env. vars
    if args.imagedir:
        initialize_logger.info("image dir is available: %s" % args.imagedir)
        image_dir = args.imagedir
    else:
        initialize_logger.info("Dumping to tmp dir")
        image_dir = "%s/media" % config.__CEREBRO_TEMP_DIR__

    initialize_logger.info("Imagedir is: %s" % image_dir)

    if args.debug:
        debug_mode = True
    else:
        debug_mode = False

    copyfile("../assets/system/Loading_Please_Wait.jpg", "%s/Loading_Please_Wait.jpg" % config.__CEREBRO_SYSTEM_DIR__)
    show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__, debug_mode=debug_mode)

    if args.interval:
        sqs_interval = args.interval
    else:
        sqs_interval = 60

    initialize_logger.info("Image Dir: %s, Debug Mode: %d" % (image_dir, debug_mode))

    # also reset the image effects applied setting to start over
    persist_setting(setting_name='image_effect_applied', setting_value='')
    persist_setting(setting_name='image_filter_applied', setting_value='')

    return image_dir, debug_mode, sqs_interval, initialize_logger, device_id

#def sqs_monitor(image_dir='', debug_mode=None, sqs_interval=60, device_id=None):
def customCallback(client, userdata, message):

    global kill_request

    print(message)
    print("\n\nReceived a new message: (message.payload) ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    # first establish the logger object
    iot_monitor_logger = logging.getLogger('cerebro_processor.sqs_monitor')
    iot_json = json.loads(message.payload)
    device_id = iot_json['message']['device_id']
    print(device_id)
    if not device_id:
        iot_monitor_logger.error("Error! No Device ID found! Exiting !")
        return

    # and slideshow vars
    slideshow_util = "../scripts/start-picture-frame.sh"
    slideshow_util_stop = "../scripts/stop-picture-frame.sh"
    slideshow_dir = image_dir
    slideshow_log = "%s/picframe.start.log" % config.__CEREBRO_LOGS_DIR__
    slideshow_log_stop = "%s/picframe.stop.log" % config.__CEREBRO_LOGS_DIR__
    register_util = "python3 take_photo.py"
    register_util_log = "take_photo.log"

    selfie_util = "python3 take_photo.py"
    selfie_util_params = "--selfie"
    if device_id:
        selfie_util_params += " '%s'" % device_id
        
    selfie_util_log = "take_photo.log"

    iot_monitor_logger.info("Going to start on the sqs monitoring for Device ID: %s ......." % device_id)

    # setup the leds also
    if not test_environment:
        accept_led = LED(config.__GREEN_LED__)
        choice_led = LED(config.__YELLOW_LED__)

    # 2. setup a loop to monitor the queues every 60 secs perhaps

    message = message.payload
    #iot_monitor_logger.info(message)
    iot_monitor_logger.info(message)

    iot_msg = json.loads(message)
    iot_msg = iot_msg['message']
    print('iot_msg: ' + str(iot_msg))
    if "device_id" not in iot_msg.keys():
        print("\n\n==== Device ID is not inside IoT message. ====\n\n")
        return None
    if iot_msg["device_id"] != device_id:
        print("\n\n==== Device ID in message: " + iot_msg["device_id"] + " does not match local ID: " + device_id + " ====\n\n")
        return None
    

    iot_monitor_logger.info(iot_msg)
        # check if the request is to stop the slideshow
    if "action" in iot_msg.keys():
        iot_monitor_logger.info("IoT Action: " + iot_msg["action"])
        if "kill" == iot_msg["action"].lower():
            kill_request = process_kill_request(debug_mode=debug_mode, image_dir=image_dir)

            return None

        if "register" == iot_msg["action"].lower():
            if "profile" in iot_msg.keys():
                profile_name = iot_msg["profile"]
                if not profile_name:
                    iot_monitor_logger.error("Error! Empty Profile name found! No registration possible")
                    exit(1)
            else:
                iot_monitor_logger.error("Error!No Profile name found! No registration possible")
                exit(1)

            iot_monitor_logger.info("Registration requested for profile: %s." % profile_name)

            if debug_mode:
                iot_monitor_logger.info("Registration requested. In debug mode so do nothing.")
                return None
            else:
                iot_monitor_logger.info("Now normally will trigger the registration process")
                register_cmd_params = "--register %s" % profile_name
                device_id = iot_msg["device_id"]
                if device_id:
                    register_cmd_params += " '%s'" % device_id

                if "choose_again" in iot_msg.keys():
                	first_attempt = False
                else:
                	first_attempt = True

                iot_monitor_logger.info("Now normally will trigger the register process - inprocess")
                process_choose_photo(first_attempt=first_attempt, selfie_mode=False, image_path='', device_id=device_id, led=choice_led, profile_name=profile_name)
                iot_monitor_logger.info("Now normally will trigger the register process - inprocess - completed!")


                # normally will continue after register request but for now exit
                return None
                #exit(0)

        # This will trigger the take_photo script, capture the image
        # and confirm via a different sqs message
        if "selfie" == iot_msg["action"].lower():
            iot_monitor_logger.info("Selfie requested...")

            if debug_mode:
                iot_monitor_logger.info("Selfie requested. In debug mode so do nothing.")
                return None
            else:
                iot_monitor_logger.info("Now normally will trigger the selfie process")

                iot_monitor_logger.info("Now normally will trigger the selfie process - inprocess")
                process_choose_photo(first_attempt=True, selfie_mode=True, image_path='', device_id=device_id, led=choice_led)
                iot_monitor_logger.info("Now normally will trigger the selfie process - inprocess - completed!")

                # now call the method to takephoto
                iot_monitor_logger.info("Returned from selfie util.")                       
                return None

        # This will trigger the take_photo script, capture the image
        # and confirm via a different sqs message
        if "apply_filter" == iot_msg["action"].lower():
            iot_monitor_logger.info("Filters requested...")

            if debug_mode:
                iot_monitor_logger.info("Filters requested. In debug mode so do nothing.")
                return None
            else:
                iot_monitor_logger.info("Triggering filters util ...")
                selfie_mode=True
                image_path="/tmp/project_cerebro/profiles/image.jpg"
                if not test_environment:
                    accept_led.close()
                    choice_led.close()
                process_accept_picture(selfie_mode=selfie_mode, image_path=image_path, device_id=device_id)

                # now call the method to takephoto
                iot_monitor_logger.info("Returned from selfie util.")
                if not test_environment:
                    accept_led = LED(config.__GREEN_LED__)
                    choice_led = LED(config.__YELLOW_LED__)
                
                # normally will continue after register request but for now exit
                return None
                #exit(0)

        # This will trigger the take_photo script, capture the image
        # and confirm via a different sqs message
        if "apply_effect" == iot_msg["action"].lower():
            iot_monitor_logger.info("Effects requested...")

            if debug_mode:
                iot_monitor_logger.info("Effects requested. In debug mode so do nothing.")
                return None
            else:                       
                iot_monitor_logger.info("Triggering Effects util ...")
                selfie_mode=True
                image_path="/tmp/project_cerebro/media/filtered_image.jpg"
                if not test_environment:
                    accept_led.close()
                    choice_led.close()

                process_accept_filters(selfie_mode=selfie_mode, image_path=image_path, device_id=device_id)

                # now call the method to takephoto
                iot_monitor_logger.info("Returned from image effects util.")
                if not test_environment:
                    accept_led = LED(config.__GREEN_LED__)
                    choice_led = LED(config.__YELLOW_LED__)
                
                # normally will continue after register request but for now exit
                return None
                #exit(0)

        # ----- push button mgmt ---- START:
        if "upload_request" == iot_msg["action"].lower():
            iot_monitor_logger.info("upload request recieved. Now to see of this is acceptable or not ...")

            if debug_mode:
                iot_monitor_logger.info("upload request recieved. In debug mode so do nothing.")
                return None
            else:
                iot_monitor_logger.info("upload request recieved")

                process_upload_request(debug_mode=debug_mode, sqs_msg=iot_msg, accept_led=accept_led, choice_led=choice_led, device_id=device_id)

                return None

        if "effects_applied" == iot_msg["action"].lower():
            iot_monitor_logger.info("Applying effects complete. Now to see of this is acceptable or not ...")

            if debug_mode:
                iot_monitor_logger.info("Applying effects complete. In debug mode so do nothing.")
                return None
            else:
                iot_monitor_logger.info("Applying effects complete")
                process_effects_applied(debug_mode=debug_mode, sqs_msg=iot_msg, accept_led=accept_led, choice_led=choice_led, device_id=device_id)
                return None

        if "filters_applied" == iot_msg["action"].lower():
            iot_monitor_logger.info("Applying filters complete. Now to see of this is acceptable or not ...")

            if debug_mode:
                iot_monitor_logger.info("Applying filters complete. In debug mode so do nothing.")
                return None
            else:
                iot_monitor_logger.info("Applying filters complete")
                process_filters_applied(debug_mode=debug_mode, sqs_msg=iot_msg, accept_led=accept_led, choice_led=choice_led, device_id=device_id)
                return None

        if "photo_captured" == iot_msg["action"].lower():
            iot_monitor_logger.info("Image capture complete. Now to see of this is acceptable or not ...")

            if debug_mode:
                iot_monitor_logger.info("Image capture complete. In debug mode so do nothing.")
                return None
            else:
                iot_monitor_logger.info("Image capture complete")
                process_photo_captured(debug_mode=debug_mode, sqs_msg=iot_msg, accept_led=accept_led, choice_led=choice_led, device_id=device_id)
                return None

        # ----- push button mgmt ---- END!

        if "stop" == iot_msg["action"].lower():
            if debug_mode:
                iot_monitor_logger.info("stopping the slideshow now. ignore all other parameters.")
                return None
            else:
                iot_monitor_logger.info("execute the slideshow-stop")
                delete_local_files(image_dir=image_dir)
                status = subprocess.call(
                    '%s > %s 2>&1 &' % 
                    (slideshow_util_stop, slideshow_log_stop), 
                    shell=True)
                return None

        if "download_image" == iot_msg["action"].lower():
            iot_monitor_logger.info("Detected download_image request ...")
            if debug_mode:
                iot_monitor_logger.info("In Debug Mode. Ignore Now.")
                return None
            else:
                iot_monitor_logger.info("Will be processing the download_image request now.")
                process_download_or_print_request(accept_led=accept_led, choice_led=choice_led, user_request_type="download")
                return None

        if "print_image" == iot_msg["action"].lower():
            iot_monitor_logger.info("Detected print_image request ...")
            if debug_mode:
                iot_monitor_logger.info("In Debug Mode. Ignore Now.")
                return None
            else:
                iot_monitor_logger.info("Will be processing the print_image request now.")
                process_download_or_print_request(accept_led=accept_led, choice_led=choice_led, user_request_type="print")
                return None

        if "end_session" == iot_msg["action"].lower():
            if debug_mode:
                iot_monitor_logger.info("Ending the session now. In debug so just a message!")
                return None
            else:
                iot_monitor_logger.info("Ending the session. Calling the delete data now ...")

                show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__)
                sleep(1)

                # now call the delete data method
                delete_data()
                iot_monitor_logger.info("Data all deleted now. Resetting local dirs and stopping slideshow!")
                delete_local_files(image_dir=image_dir)

                audio_prompt = "Ended the Cerebro Session. All custom profiles and associated selfies were deleted! Reverting to the stock slideshow now. Thanks for using the Cerebro!"
                fname = audio_prompt.replace(" ", "_")
                fname = fname.replace(".", "")
                speech_file_path = generate_audio(speech_text=audio_prompt, filename=fname+".mp3")
                iot_monitor_logger.info("Generated Audio now. Playing audio next ...")
                play_audio(file_path=speech_file_path, delay_to_start=0)
                iot_monitor_logger.info("Audio played. Done!")

                # reset to default slideshow
                sqs_msg = {}
                sqs_msg["action"] = "show_profile"
                sqs_msg["profile"] = ""
                send_iot_message(iot_msg=sqs_msg, device_id=device_id, delay=0)

                # Change - on 11/28/2019 - by Sachin - End

                return None

        if "show_profile" == iot_msg["action"].lower():
            if "profile" in iot_msg.keys():
                if debug_mode:
                    iot_monitor_logger.info("In Debug mode - so no showing of images!")
                    return None

                # just a temp - to allow for the deletes and downloads to happen in peace
                show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__)
                sleep(1)
                
                delete_local_files(image_dir=image_dir)
                
                iot_monitor_logger.info(iot_msg["profile"])

                if debug_mode:
                    iot_monitor_logger.info("play the audio regarding switch over")
                else:
                    iot_monitor_logger.info("execute the audio regarding switch over")

                iot_monitor_logger.info("Getting media now ....")
                media_count = download_media(profile_name=iot_msg["profile"])
                iot_monitor_logger.info("Media Count retrieved: %d" % media_count)

                if not media_count:
                    # skip the display attempt if there were no images found
                    iot_monitor_logger.info("No images found so trying the next message/wait for one!")

                    audio_prompt = "Sorry, No images found for this profile named: %s. Try taking a selfie!" % iot_msg["profile"]
                    speech_file_path = generate_audio(speech_text=audio_prompt, filename="no_images_for_"+iot_msg["profile"]+"_try_taking.mp3")

                    iot_monitor_logger.info("Generated Audio now. Playing audio next ...")
                    play_audio(file_path=speech_file_path)
                    iot_monitor_logger.info("Audio played. Done!")

                    return None

                if debug_mode:
                    iot_monitor_logger.info("start the slideshow")
                else:
                    
                    iot_monitor_logger.info("execute the slideshow")

                    show_images(media_dir=image_dir)

                if media_count:
                    if media_count == 1:
                        audio_prompt = "Beware: There was only one image found for profile: %s." % iot_msg["profile"]
                        audio_prompt += " The slideshow will be static with a single image!"
                    else:
                        audio_prompt = "Found %d images. Will be displaying on the screen shortly!" % media_count
                else:
                    audio_prompt = "Sorry, no images found for profile: %s." % iot_msg["profile"]
                    audio_prompt += " Please try again!"

                fname = audio_prompt.replace(" ", "_")
                fname = fname.replace(".", "")
                speech_file_path = generate_audio(speech_text=audio_prompt, filename=fname+".mp3")
                iot_monitor_logger.info("Generated Audio now. Playing audio next ...")
                play_audio(file_path=speech_file_path, delay_to_start=5)
                iot_monitor_logger.info("Audio played. Done!")
    #
    # 4. sleep for 5 mins now and continue loop
    sleep(sqs_interval)

    iot_monitor_logger.info("Completed the monitoring!")

    # 3. return from function now
    return

if __name__ == "__main__":

    image_dir, debug_mode, sqs_interval, initialize_logger, device_id = initialize()
    main_logger = logging.getLogger('cerebro_processor.main')
    main_logger.info("After Initialize, parameters returned were: %s, %s, %s, %s" % (image_dir, str(debug_mode), str(sqs_interval), device_id))

    # set up the MQTT Client now
    myAWSIoTMQTTClient = initialize_mqtt_client(clientId=config.__IOT_CLIENT_ID_PROCESSOR__)

    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

    while not kill_request:
    	#main_logger.info("No Kill Request yet: sleeping for a second ...")
        time.sleep(1)

    main_logger.info("Exited the Cerebro Monitor now!")

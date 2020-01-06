#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
try:
	#from picamera import PiCamera
	from gpiozero import LED, Button
	#from gpiozero import LED
	test_environment = False
except (ImportError, RuntimeError):
	#import cv2
	test_environment = True

from time import sleep
import logging
import argparse
import subprocess
from cerebro_utils import *

from time import gmtime, strftime

from config import Configuration

# --------- Module- Level Globals ---------------

button_input_received = 0
selfie_mode = False
image_path = ""
trigger_mode = "accept"

config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

'''
# global vars, consts
__CEREBRO_TEMP_DIR__ = "/tmp/project_cerebro"
__CEREBRO_LOGS_DIR__ = "/tmp/project_cerebro/logs"
__CEREBRO_MEDIA_DIR__ = "/tmp/project_cerebro/media"

__GREEN_LED__ = 27
__GREEN_BUTTON__ = 17
__YELLOW_LED__ = 26
__YELLOW_BUTTON__ = 16

__ACCEPT_INPUT__ = 1
__CHOOSE_AGAIN__ = 2
'''

def accept_button_callback():
	global button_input_received

	accept_button_callback_logger = logging.getLogger('button_utils.accept_button_callback')

	accept_button_callback_logger.info("$$$$$$$$$$$$$$ Accept Button was pushed! $$$$$$$$$$$$$$")
	button_input_received = config.__ACCEPT_INPUT__
	accept_button_callback_logger.info("All done with the button callback!")

	return

def choice_button_callback():
	global button_input_received

	choice_button_callback_logger = logging.getLogger('button_utils.choice_button_callback')

	choice_button_callback_logger.info("############### Choice Button was pushed! #################")
	button_input_received = config.__CHOOSE_AGAIN__

	choice_button_callback_logger.info("All done with the button callback!")

	return

def button_handler(wait_delay=60, accept_led=None, choice_led=None, green_button_text="for Accept", yellow_button_text="for more choice"):

	global button_input_received

	button_utils_logger = logging.getLogger('button_.button_handler')
	button_input_received = False

	if not test_environment:
		accept_button = Button(config.__GREEN_BUTTON__)
		accept_button.when_pressed = accept_button_callback
		choice_button = Button(config.__YELLOW_BUTTON__)
		choice_button.when_pressed = choice_button_callback

	button_utils_logger.info("Go ahead and press the appropriate button. ")

	profile_prompt = "Push Green button %s or Yellow button %s." % (green_button_text, yellow_button_text)
	if (green_button_text =="for Accept") and (yellow_button_text=="for more choice"):
		speech_file_name = "push_green_accept_yellow_choice.mp3"
	else:
		fname = profile_prompt.replace(" ", "_")
		fname = fname.replace(".", "")
		speech_file_name = "%s.mp3" % fname

	speech_file_path = generate_audio(speech_text=profile_prompt, filename=speech_file_name)
	button_utils_logger.info("Generated Audio now. Playing audio next: ")
	play_audio(file_path=speech_file_path)
	button_utils_logger.info("Audio played. Done!")

	while (wait_delay and (not button_input_received)):
		button_utils_logger.info("In button thread: waiting for button input")
		sleep(10)
		wait_delay -= 10

	if button_input_received:
		button_utils_logger.info("Button input was received successfully: %d" % button_input_received)
	else:
		button_utils_logger.info("No button press detected!")

		profile_prompt = "No button press was detected. Defaulting to an accept now."
		speech_file_path = generate_audio(speech_text=profile_prompt, filename="no_button_press_was_detected.mp3")
		play_audio(file_path=speech_file_path)

		button_input_received = 1

	if not test_environment:
		if button_input_received == 1:
			if accept_led:
				accept_led.on()
				choice_led.off()
		elif button_input_received == 2:
			if choice_led:
				choice_led.on()
				accept_led.off()

	if not test_environment:
		accept_button.close()
		choice_button.close()

	button_utils_logger.info("Done with button_handler.")

	return button_input_received

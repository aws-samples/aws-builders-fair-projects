import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging
import subprocess
import os
import glob
import json
from mutagen.mp3 import MP3
import math
from time import sleep
import os.path

try:
    #from picamera import PiCamera
    from gpiozero import LED, Button
    #from gpiozero import LED
    test_environment = False
except (ImportError, RuntimeError):
    #import cv2
    test_environment = True

from aws_utils import *
from rpi_utils import *

from selfie_with_filters import *
from apply_image_effects import *
from take_photo import *

from config import Configuration

# --------- Module- Level Globals ---------------
config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

'''
__CEREBRO_TEMP_DIR__ = "/tmp/project_cerebro"
__CEREBRO_LOGS_DIR__ = "/tmp/project_cerebro/logs"
__CEREBRO_MEDIA_DIR__ = "/tmp/project_cerebro/media"
__CEREBRO_SYSTEM_DIR__ = "/tmp/project_cerebro/system"
__CEREBRO_AUDIO_DIR__ = "../assets/audio"
__SQS_QUEUE_NAME__ = 'cerebro_client'
__SQS_BACKEND_QUEUE_NAME__ = 'cerebro_backend'

__GREEN_LED__ = 27
__GREEN_BUTTON__ = 17
__YELLOW_LED__ = 26
__YELLOW_BUTTON__ = 16

__PUSHBUTTON_DELAY__ = 300
'''

def setup_dirs(dir_to_create='/tmp', clean_mode=False):
    setup_dirs_logger = logging.getLogger('cerebro_utils.setup_dirs')

    # cleanup dir, if needed
    does_dir_exist = os.path.exists(dir_to_create)
    if does_dir_exist:
        setup_dirs_logger.info("the dir exists: %s" % dir_to_create)
        # now do cleanup if needed
        if clean_mode:
            delete_local_files(image_dir=dir_to_create)
    else:
        setup_dirs_logger.info("the dir doesn't exist: %s" % dir_to_create)
        # now create the folder
        os.makedirs(dir_to_create, mode=0o777)

    return True

def delete_local_files(image_dir=config.__CEREBRO_MEDIA_DIR__):
    delete_media_logger = logging.getLogger('cerebro_utils.delete_media')

    delete_media_logger.info("Entered the delete local files handler ...")
    delete_media_logger.info(image_dir)
    files = glob.glob('%s/*' % image_dir)
    delete_media_logger.info("Files listing to be deleted ...")
    delete_media_logger.info(files)
    for file in files:
        os.remove(file)
    delete_media_logger.info("all files deleted now")

    return

def get_current_profile(image_dir=config.__CEREBRO_MEDIA_DIR__):
    get_current_profile_logger = logging.getLogger('cerebro_utils.get_current_profile')
    profile_name = ""

    get_current_profile_logger.info("Entered the get_current_profile handler ...")
    get_current_profile_logger.info(image_dir)
    profile_stem = "profile_"
    files = glob.glob('%s/%s*.jpg' % (image_dir, profile_stem))
    get_current_profile_logger.info("Files listing to be analyzed ...")
    get_current_profile_logger.info(files)
    if len(files) > 1:
        get_current_profile_logger.warning("Warning, More than one profile image found!")

    profile_name_file = os.path.basename(files[0]).split('.jpg')[0]
    get_current_profile_logger.info("Profile File: %s" % profile_name_file)
    profile_name = profile_name_file.split(profile_stem)[1]
    get_current_profile_logger.info("Profile Name determined is: %s" % profile_name)

    get_current_profile_logger.info("Profile retrieved now")

    return profile_name

def show_no_images():

    show_no_images_logger = logging.getLogger('cerebro_utils.show_no_images')

    show_no_images_logger.info("Entered the switch_images method ...")
    
    show_no_images_logger.info("And now, starting up the slideshow again ...")
    slideshow_stop_util = "../scripts/stop-picture-frame.sh"
    slideshow_stop_log = "%s/picframe.stop.log" % config.__CEREBRO_LOGS_DIR__
    status = subprocess.call(
        '%s > %s 2>&1 &' % 
        (slideshow_stop_util, slideshow_stop_log), 
        shell=True)

    show_no_images_logger.info("Stopping of images is now complete!")    

    return True

def process_accept_effects(selfie_mode=False, image_path='', device_id=None):

    process_accept_effects_logger = logging.getLogger('cerebro_utils.process_accept_effects')

    if not test_environment:
        led = LED(config.__GREEN_LED__)
        led.on()

    audio_prompt = "Excellent! Seems that you like this effect. Now, lets upload this selfie ..."

    speech_file_path = generate_audio(speech_text=audio_prompt, filename="like_this_text.mp3")
    process_accept_effects_logger.info("Generated Audio now. Playing audio next ...")
    play_audio(file_path=speech_file_path)
    process_accept_effects_logger.info("Audio played. Done!")

    image_path = "%s/%s.jpg" % (config.__CEREBRO_MEDIA_DIR__, "filtered_image_effects")

    process_accept_effects_logger.info("Uploading the selfie now ...")
    upload_image(image_path=image_path)
    process_accept_effects_logger.info("Selfie was uploaded now!")

    profile_prompt = "Selfie was uploaded with image effects!"

    speech_file_path = generate_audio(speech_text=profile_prompt, filename="uploaded_with_effects.mp3")
    process_accept_effects_logger.info("Generated Audio now. Playing audio next ...")
    play_audio(file_path=speech_file_path)
    process_accept_effects_logger.info("Audio played. Done!")

    if not test_environment:
        led.off()

    process_accept_effects_logger.info("Completed the accept of the effects and uploaded. done!")
    
    return True

def process_accept_filters(selfie_mode=False, image_path='', device_id=None):

    process_accept_filters_logger = logging.getLogger('cerebro_utils.process_accept_filters')

    if not test_environment:
        led = LED(config.__GREEN_LED__)
        led.on()

    audio_prompt = "Excellent! Seems that You like this filter. Now, lets apply some effects to this ..."

    speech_file_path = generate_audio(speech_text=audio_prompt, filename="lets_apply_effects.mp3")
    process_accept_filters_logger.info("Generated Audio now. Playing audio next ...")
    play_audio(file_path=speech_file_path)
    process_accept_filters_logger.info("Audio played. Done!")

    image_path = "%s/%s" % (config.__CEREBRO_MEDIA_DIR__, "filtered_image.jpg")
    # now apply an image effect ...
    process_accept_filters_logger.info("Applying the image effect now ...")

    profile_prompt = "Image effects now being applied to the selfie!"

    speech_file_path = generate_audio(speech_text=profile_prompt, filename="effects_now_being_applied")
    process_accept_filters_logger.info("Generated Audio now. Playing audio next ...")
    play_audio(file_path=speech_file_path)
    process_accept_filters_logger.info("Audio played. Done!")

    process_accept_filters_logger.info("Now calling the image effects script inprocess ...")

    filtered_image_effects, chosen_effect_text = apply_image_effect(image_path=image_path)
    process_accept_filters_logger.info("image effects script inprocess completed. image effects file: %s , Chosen Effect: %s" % (filtered_image_effects, chosen_effect_text))

    process_accept_filters_logger.info("Finished with the image effect now ...")
    image_path = "%s/%s.jpg" % (config.__CEREBRO_MEDIA_DIR__, "filtered_image_effects")

    #SHOULD NOT BE NEEDED since the original slideshow with the raw selfie should be running
    process_accept_filters_logger.info("And now, starting up the slideshow again if not in a test env ...")
    if not test_environment:

        profile_prompt = "You should now see the filters with %s effect ...." % chosen_effect_text

        fname = profile_prompt.replace(" ", "_")
        fname = fname.replace(".", "")

        #speech_file_path = generate_audio(speech_text=profile_prompt, filename="you_should_now_see_effects.mp3")
        speech_file_path = generate_audio(speech_text=profile_prompt, filename=fname+".mp3")

        process_accept_filters_logger.info("Generated Audio now. Playing audio next ...")
        play_audio(file_path=speech_file_path)
        process_accept_filters_logger.info("Audio played. Done!")

        control_display(enable_display=False)
        slideshow_util = "../scripts/stop-slideshow-only.sh"
        slideshow_log = "%s/picframe.stop.log" % config.__CEREBRO_LOGS_DIR__
        status = subprocess.call(
            '%s > %s 2>&1 &' % 
            (slideshow_util, slideshow_log), 
            shell=True)

        slideshow_util = "../scripts/start-picture-frame.sh"
        slideshow_log = "%s/picframe.start.log" % config.__CEREBRO_LOGS_DIR__
        status = subprocess.call(
            '%s "%s" > %s 2>&1 &' % 
            (slideshow_util, config.__CEREBRO_MEDIA_DIR__, slideshow_log), 
            shell=True)

        process_accept_filters_logger.info("Switching of images is now complete!")    

    if not test_environment:
        led.off()

    # now send a sqs message to indicate the filter was applied
    sqs_msg = {}
    sqs_msg["action"] = "effects_applied"
    sqs_msg["selfie_mode"] = str(int(selfie_mode))
    sqs_msg["image_path"] = image_path

    send_iot_message(iot_msg=sqs_msg, delay=0, device_id=device_id)

    return True

def process_accept_picture(selfie_mode=False, image_path='', device_id=None):

    process_accept_picture_logger = logging.getLogger('cerebro_utils.process_accept_picture')
    process_accept_picture_logger.info("Entered the process_accept_picture in the cerebroutils script ...")

    if not test_environment:
        led = LED(config.__GREEN_LED__)
        led.on()

    if selfie_mode:
        picture_text = "Selfie"
    else:
        picture_text = "Profile picture"        

    process_accept_picture_logger.info("Launching the announce for the initial accept of picture ...")

    # now process the accept if the image taken was for a selfie or profile picture

    if not selfie_mode:
        audio_prompt = "Excellent! Seems that You like this %s. Uploading now ..." % picture_text
    else:
        audio_prompt = "Excellent! Seems that You like this %s. Now, lets apply some filters to this ..." % picture_text

    speech_file_path = generate_audio(speech_text=audio_prompt, filename="like_this_photo_now_lets.mp3")
    process_accept_picture_logger.info("Generated Audio now. Playing audio next ...")
    play_audio(file_path=speech_file_path)
    process_accept_picture_logger.info("Audio played. Done!")

    process_accept_picture_logger.info("Now, to attempt the filters for a selfie ...")
    process_accept_picture_logger.info(selfie_mode)

    # do the upload for the profile mode, but for selfie call the filter processing
    if not selfie_mode:
        process_accept_picture_logger.info("Uploading the profile now ...")
        upload_image(image_path=image_path)
        process_accept_picture_logger.info("Profile was registered now!")

        profile_prompt = "You are now registered and your profile picture is uploaded. You can now ask alexa to take some pictures"

        speech_file_path = generate_audio(speech_text=profile_prompt, filename="you_are_now_registered_and_uploaded.mp3")
        process_accept_picture_logger.info("Generated Audio now. Playing audio next ...")
        play_audio(file_path=speech_file_path)
        process_accept_picture_logger.info("Audio played. Done!")

        if not test_environment:
            led.off()
    else:
        # calling the filters script
        process_accept_picture_logger.info("Announcing the filters step ...")

        profile_prompt = "Filters now being applied to the selfie taken!"

        speech_file_path = generate_audio(speech_text=profile_prompt, filename="filters_now_being_applied.mp3")
        process_accept_picture_logger.info("Generated Audio now. Playing audio next ...")
        play_audio(file_path=speech_file_path)
        process_accept_picture_logger.info("Audio played. Done!")

        process_accept_picture_logger.info("Now calling the selfie filters script inprocess ...")

        filtered_image = process_image_filter(image_path=image_path)
        process_accept_picture_logger.info("selfie filters script inprocess completed. filteres file: %s " % filtered_image)
 
        profile_prompt = "Filters applied to the selfie taken!"

        speech_file_path = generate_audio(speech_text=profile_prompt, filename="filters_applied_to_selfie_taken.mp3")
        process_accept_picture_logger.info("Generated Audio now. Playing audio next ...")
        play_audio(file_path=speech_file_path)
        process_accept_picture_logger.info("Audio played. Done!")

        process_accept_picture_logger.info("Finished the announce as well!")

        #SHOULD NOT BE NEEDED since the original slideshow with the raw selfie should be running
        process_accept_picture_logger.info("And now, starting up the slideshow again if not in a test env ...")
        if not test_environment:

            profile_prompt = "You should now see the selfie images ...."

            speech_file_path = generate_audio(speech_text=profile_prompt, filename="should_now_see_selfie_images.mp3")
            process_accept_picture_logger.info("Generated Audio now. Playing audio next ...")
            play_audio(file_path=speech_file_path)
            process_accept_picture_logger.info("Audio played. Done!")

            control_display(enable_display=False)
            slideshow_util = "../scripts/stop-slideshow-only.sh"
            slideshow_log = "%s/picframe.stop.log" % config.__CEREBRO_LOGS_DIR__
            status = subprocess.call(
                '%s > %s 2>&1 &' % 
                (slideshow_util, slideshow_log), 
                shell=True)

            slideshow_util = "../scripts/start-picture-frame.sh"
            slideshow_log = "%s/picframe.start.log" % config.__CEREBRO_LOGS_DIR__
            status = subprocess.call(
                '%s "%s" > %s 2>&1 &' % 
                (slideshow_util, config.__CEREBRO_MEDIA_DIR__, slideshow_log), 
                shell=True)

            process_accept_picture_logger.info("Switching of images is now complete!")    

        if not test_environment:
            led.off()

        # now send a sqs message to indicate the filter was applied
        sqs_msg = {}
        sqs_msg["action"] = "filters_applied"
        sqs_msg["selfie_mode"] = str(int(selfie_mode))
        sqs_msg["image_path"] = image_path
        sqs_msg["device_id"] = device_id

        send_iot_message(iot_msg=sqs_msg, delay=0, device_id=device_id)

    return True

# ----
# This is the set of choice functions
# ----

def process_choose_photo(first_attempt=False, selfie_mode=False, image_path='', device_id='default_device', led=None, profile_name=''):

    process_choose_photo_logger = logging.getLogger('cerebro_utils.process_choose_photo')
    process_choose_photo_logger.info("Entered the process_choose_photo in the cerebroutils script ...")

    if not test_environment:
        #led = LED(__YELLOW_LED__)
        led.on()

    if selfie_mode:
        picture_text = "Selfie"
    else:
        picture_text = "Profile picture"        

    process_choose_photo_logger.info("Launching the announce for the initial choice of picture ...")

    # now process the accept if the image taken was for a selfie or profile picture

    if first_attempt:
        audio_prompt = "Absolutely, We can take a %s ... " % picture_text
        speech_filename= "we_can_take_a_%s.mp3" % picture_text.replace(" ", "_")
    else:
        audio_prompt = "Sure, We can take a different %s ... " % picture_text
        speech_filename = "sure_we_can_take_another_%s.mp3" % picture_text.replace(" ", "_")

    speech_file_path = generate_audio(speech_text=audio_prompt, filename=speech_filename)
    process_choose_photo_logger.info("Generated Audio now. Playing audio next ...")
    play_audio(file_path=speech_file_path, delay_to_start=10)
    process_choose_photo_logger.info("Audio played. Done!")

    process_choose_photo_logger.info("Now, to attempt a new picture ...")
    process_choose_photo_logger.info(selfie_mode)

    # now trigger the take_photo script depending on the selfie mode
    #profile_name = ''
    if not selfie_mode:
        process_choose_photo_logger.info("Now normally will trigger the registration process")

        # TBD - figure out the current profile being triggered
        # if profile wasn't passed - usually on subsequent choice runs, calculate
        if not profile_name:
            profile_name = get_current_profile()
            if not profile_name:
                profile_name = "noprofilefound"

        if not test_environment:
            led.off()

        process_choose_photo_logger.info("Now calling the take photo script inprocess ...")

        show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__)
        delete_local_files()
        sleep(1)
        
        # purpose of this method is to 
        #   take the photo , 
        #   show the image captured, and then 
        #   pass a message back saying: ready for button input

        image_path = process_take_photo(profile_name=profile_name, selfie_mode=selfie_mode, iot_mode=False, device_id=device_id)
        process_choose_photo_logger.info("photo script inprocess completed. image file: %s " % image_path)

    else:

        process_choose_photo_logger.info("Now normally will trigger the selfie process")
    
        if not test_environment:
            led.off()

        process_choose_photo_logger.info("Now calling the take photo script inprocess ...")

        show_images(media_dir=config.__CEREBRO_SYSTEM_DIR__)
        delete_local_files()
        sleep(1)
        
        # purpose of this method is to 
        #   take the photo , 
        #   show the image captured, and then 
        #   pass a message back saying: ready for button input

        image_path = process_take_photo(profile_name=profile_name, selfie_mode=selfie_mode, iot_mode=False, device_id=device_id)
        process_choose_photo_logger.info("photo script inprocess completed. image file: %s " % image_path)

    return True

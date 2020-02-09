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

import sys
from time import strftime
from PIL import Image, ImageDraw, ImageFont

from os import listdir
from os.path import isfile, join

try:
    #from picamera import PiCamera
    from gpiozero import LED, Button
    #from gpiozero import LED
    test_environment = False
except (ImportError, RuntimeError):
    #import cv2
    test_environment = True

import cups
import requests

import sqlite3
from datetime import datetime

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
__SQS_BACKEND_QUEUE_NAME__ = 'cerebro_backend's

__GREEN_LED__ = 27
__GREEN_BUTTON__ = 17
__YELLOW_LED__ = 26
__YELLOW_BUTTON__ = 16

__PUSHBUTTON_DELAY__ = 300

__PRINTER_TYPE__ = "selphy"

__APIGW_X_API_KEY__ = "2YSoTXerhD4u3iat9CWUM9kn756MTJIp4c4Tgfqk"
__APIGW_X_API_KEY_QR_CODE__ = "aLCOemQkKa6EzcOQU6xjI8T2hRzD4Cf050EwWdb1"

__APIGW_API__ = "https://lqhvtjhlsc.execute-api.us-east-1.amazonaws.com/production/Cerebro_GetImages_S3List"
__APIGW_API_QR_CODE__ = "https://lqhvtjhlsc.execute-api.us-east-1.amazonaws.com/production/Cerebro_GetQRCode"

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
__IMAGE_MAX_COUNT__ = 100

__GREEN_LED__ = 27
__GREEN_BUTTON__ = 17
__YELLOW_LED__ = 26
__YELLOW_BUTTON__ = 16
'''

def control_display(enable_display=False):
    control_display_logger = logging.getLogger('cerebro_utils.control_display')

    control_display_logger.info("Entered the control_display method ...")
    if enable_display:
        display_cmd = "vcgencmd display_power 1"
    else:
        display_cmd = "vcgencmd display_power 0"

    control_display_logger.info("Calling the display control now ...")
    status = subprocess.call(
        '%s' % (display_cmd), 
        shell=True)

    control_display_logger.info("Display control now complete!")    

    return True

def show_images(media_dir=config.__CEREBRO_MEDIA_DIR__, debug_mode=False):

    show_images_logger = logging.getLogger('cerebro_utils.show_images')

    show_images_logger.info("Entered the switch_images method ...")
    
    if debug_mode:
        show_images_logger.info("In Debug mode, so no showing of images!")
        return True

    show_images_logger.info("And now, starting up the slideshow again ...")
    #slideshow_stop_util = "../scripts/stop-picture-frame.sh"
    slideshow_stop_util = "../scripts/shutoff-display.sh"
    slideshow_util = "../scripts/start-picture-frame.sh"
    slideshow_log = "%s/picframe.start.log" % config.__CEREBRO_LOGS_DIR__
    status = subprocess.call(
        '%s && %s "%s" > %s 2>&1 &' % 
        (slideshow_stop_util, slideshow_util, media_dir, slideshow_log), 
        shell=True)

    show_images_logger.info("Switching of images is now complete!")    

    return True

def generate_audio(voice_id='Joanna', speech_text='sample text', filename='speech.mp3'):

    generate_audio_logger = logging.getLogger('cerebro_utils.generate_audio')
    generate_audio_logger.info("Starting the generate_audio method in cerebro_utils ...")

    polly_client = boto3.Session().client('polly')
    generate_audio_logger.info("Now, going to synthesize_speech with polly")

    speech_tokens = speech_text.split()
    token_cnt = len(speech_tokens)

    if token_cnt > 10:
        mid_token = int(token_cnt/2)
        part_one = " ".join(speech_tokens[:mid_token])
        part_two = " ".join(speech_tokens[mid_token+1:])
        speech_text_with_buffer = '<speak><break time="1s"/>%s<break time="1s"/>%s</speak>' %\
                                    (part_one, part_two)
    else:
        speech_text_with_buffer = '<speak><break time="1s"/>' + speech_text + '</speak>'

    file_path = "%s/%s" % (config.__CEREBRO_AUDIO_DIR__, filename)
    if os.path.isfile(file_path):
        print("\n\nFile already exists locally, not calling Polly..")
    else:
        print("\n\nFile does not exist, making it now. ")
        response = polly_client.synthesize_speech(VoiceId=voice_id,
                    OutputFormat='mp3',
                    TextType='ssml',
                    Text = speech_text_with_buffer)

        generate_audio_logger.info("Next, call to polly completed - now to stream the audio file ...")
        
        file = open(file_path, 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        generate_audio_logger.info("Finally, audio file is written and ready @ %s" % file_path)

    return file_path

def play_audio(file_path='', delay_secs=0, delay_to_start=0):
    play_audio_logger = logging.getLogger('cerebro_utils.play_audio')
    play_audio_logger.info("Starting the play_audio method in cerebro_utils ...")

    play_audio_logger.info("File_path provided : %s" % file_path)   
    if not file_path:
        play_audio_logger.error("No file_path provided!")
        return False

    ''' HACK: RPi is not playing the mp3 reliably so pygame isn't working
    play_audio_logger.info("pygame to be started ...")
    #pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    '''

    # This is a hack to allow alexa to complete its playback
    if delay_to_start:
        sleep(delay_to_start)

    mp3_util = "sudo mpg321"
    status = subprocess.call(
        '%s %s' % 
        (mp3_util, file_path), 
        shell=True)

    if delay_secs:
        play_audio_logger.info("Sleeping for %d secs" % delay_secs)
        sleep(delay_secs)
    '''
    else:
        audio = MP3(file_path)
        audio_ts = math.ceil(audio.info.length)
        play_audio_logger.info("Duration computed as : %d. Sleeping for this duration only ..." % audio_ts)
        sleep(audio_ts)
    '''
    
    filename = os.path.basename(file_path).strip()
    if filename == "speech.mp3":
        # Delete the adhoc file
        os.remove(file_path)

    play_audio_logger.info("done here. audio played ?")
    return True

def get_facial_landmarks(image_path=''):
    get_facial_landmarks_logger = logging.getLogger('selfie_with_filters.get_facial_landmarks')
    get_facial_landmarks_logger.info("In the get_facial_landmarks method ...")

    client=boto3.client('rekognition')

    get_facial_landmarks_logger.info("Running Detect Faces on the image: %s" % image_path)

    with open(image_path, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])

    get_facial_landmarks_logger.info('Completed the detect_faces API call' )
    get_facial_landmarks_logger.info(response)

    if "FaceDetails" not in response:
        get_facial_landmarks_logger.error("No Faces found!")
        return False

    return response["FaceDetails"]

def generate_print_image(image_selected="", \
    bkgrnd_image="../assets/printing/reinvent_bkgrnd.jpg", \
    logo_image="../assets/printing/reinventLogo.png"):

    generate_print_image_logger = logging.getLogger('rpi_utils.generate_print_image')
    generate_print_image_logger.info("In generate_print_image ...")

    if not bkgrnd_image:
        generate_print_image_logger.error("No background image provided")
        return False
    elif not image_selected:
        generate_print_image_logger.error("No image selected")
        return False
    elif not logo_image:
        generate_print_image_logger.error("No logo provided")
        return False

    generate_print_image_logger.info("All images provided correctly!")

    # first load the images
    image1 = Image.open(bkgrnd_image)
    #image2 = Image.open("/Users/sacholla/Downloads/large_user4515692_2951488_757.jpg")
    image2 = Image.open(image_selected)
    imageLogo = Image.open(logo_image)

    generate_print_image_logger.info(image1.size)
    generate_print_image_logger.info(image2.size)
    generate_print_image_logger.info(imageLogo.size)

    # Now, crop the selfie picture
    selfie_size = (image2.size[0]*0.875, image2.size[1]*0.875 )
    image2.thumbnail(selfie_size, Image.ANTIALIAS)

    image2_rotated = image2.rotate(10)

    logo_size = (imageLogo.size[0]*0.25, imageLogo.size[1]*0.25)
    imageLogo.thumbnail(logo_size, Image.ANTIALIAS)

    background_size = (int(1920*0.975), int(1080*0.975))
    generate_print_image_logger.info(background_size)
    background_image = image1.resize(background_size, Image.ANTIALIAS)

    im3_copy = background_image.copy()
    image_box = (int(im3_copy.size[0]*0.035), int(im3_copy.size[1]*0.1))
    generate_print_image_logger.info(image_box)
    im3_copy.paste(image2, image_box)

    fnt = ImageFont.truetype('Arial_Bold', 48)

    d = ImageDraw.Draw(im3_copy)
    title_string = "Cerebro: A Connected Photobooth"
    title_box = (image_box[0]+105, image_box[1]-80)
    d.text(title_box, title_string, font=fnt, fill=(255,255,0))

    logo_box = (image_box[0], image_box[1]-105)
    generate_print_image_logger.info(logo_box)
    im3_copy.paste(imageLogo, logo_box, imageLogo)

    fnt2 = ImageFont.truetype('Verdana', 18)
    d2 = ImageDraw.Draw(im3_copy)
    title_string = "Nov 16 2019 12:30:05 (PST)"
    title_box = (background_size[0]-400, background_size[1]-40)
    d2.text(title_box, title_string, font=fnt2, fill=(255,255,255))

    #im3_copy.show()
    generated_print_image_path = "%s/print_image.jpg" % config.__CEREBRO_MEDIA_DIR__
    im3_copy.save(generated_print_image_path)

    return generated_print_image_path

def print_image(fileName=''):

    print_image_logger = logging.getLogger('rpi_utils.print_image')
    print_image_logger.info("Attempting to run a print job ...")

    # now generate the print image
    generated_image = generate_print_image(image_selected=fileName)
    print_image_logger.info("Generated Print Image: %s" % generated_image)

    # for now just test the underlying function only
    #return

    fileName = generated_image

    conn = cups.Connection()

    printers = conn.getPrinters()

    printer_name = ""
    for printer in printers:
        print_image_logger.info(printer, printers[printer]["device-uri"])
        if config.__PRINTER_TYPE__ in printer.lower():
            printer_name = printer

    #printer_name=list(printers.keys())[1]

    #fileName = "PollyResponse.txt"
    #fileName = "../assets/stock/Simone-Biles.jpg"

    print_image_logger.info("The Printer Chosen: %s , The Image Chosen is in path: %s" % \
        (printer_name, fileName))

    print_image_logger.info("Triggering the print job now for %s ..." % fileName)
    conn.printFile(printer_name, fileName, " ", {})

    print_image_logger.info("Completed the print job!")

    return

def download_media(profile_name="", media_dir='', ignore_stock_profiles=False):
    download_media_logger = logging.getLogger('cerebro_processor.download_media')

    download_media_logger.info("Entered Download_media ...")
    # Create an S3 client
    s3 = boto3.resource('s3')

    download_media_logger.info("Downloading Media now ...")

    payload={}
    payload['profile']=profile_name
    payload['audio']='yes'
    payload['image_max_count'] = str(config.__IMAGE_MAX_COUNT__)
    if ignore_stock_profiles:
        payload['ignore_stock_profiles'] = "1"

    headers = {
        'Content-Type': "application/json",
        'x-api-key': config.__APIGW_X_API_KEY__
        }

    url = config.__APIGW_API__

    download_media_logger.info("URL: %s, payload: %s" % (url, json.dumps(payload)) )
    response = requests.request(
        "POST", 
        url, 
        data=json.dumps(payload), 
        headers=headers)

    s3_bucket = config.__S3_BUCKET__
    s3_key = ""

    download_media_logger.debug("Response: %s" % (json.dumps(response.json())) )

    media_count = len(response.json())
    download_media_logger.info("Total Number of Media files: %d" % media_count )

    for item in response.json():
        download_media_logger.info("Processing Media: %s ..." % item["image_key"])
        # now download the s3 files one by one
        s3_key = item["image_key"]
        media_caption = item["image_caption"]
        if media_dir:
            local_file = "%s/%s" % (media_dir, os.path.basename(s3_key))
        else:
            local_file = "%s/%s" % (config.__CEREBRO_MEDIA_DIR__, os.path.basename(s3_key))

        download_media_logger.info("Try downloading file: %s" % s3_key)
        try:
            s3.Bucket(s3_bucket).download_file(s3_key, local_file)
        except botocore.exceptions.ClientError as e:
            print("Error seen!")
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        download_media_logger.info("Image Downloaded to %s." % local_file)

    download_media_logger.info("Media downloaded.")
    return media_count

# Change - on 11/28/2019 - by Sachin - Start
def persist_setting(setting_name='setting_name', setting_value='setting_value'):

    persist_setting_logger = logging.getLogger('cerebro_utils.persist_setting')
    persist_setting_logger.info("In persist_setting ...")

    if not setting_name:
        persist_setting_logger.error("Invalid parameter provided!")
        return False
        
    db_file = "cerebro.db"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    persist_setting_logger.info("Created the DB connection...")

    # first delete the old entry
    dml_sql = """ DELETE from local_settings where setting_name = '%s' """ % setting_name
    persist_setting_logger.info("Now , executing sql: '%s', with params." % dml_sql)
    c.execute(dml_sql)

    conn.commit()

    # next insert the new entry
    dml_sql = """ INSERT INTO local_settings(setting_name,setting_value,last_updated,last_updated_dt) VALUES(?,?,?,?)"""
    
    epoch_time = datetime(1970,1,1)
    utc_time = datetime.now()
    last_updated = int((utc_time-epoch_time).total_seconds())
    last_updated_dt = utc_time.strftime("%m-%d-%YT%H:%M:%S.%f")
    settings_entry = (setting_name, setting_value, last_updated, last_updated_dt)

    persist_setting_logger.info("Now , executing sql: '%s', with params." % dml_sql)
    c.execute(dml_sql, settings_entry)

    conn.commit()

    persist_setting_logger.info("Setting is persisted into the db!")

    return True

def retrieve_setting(setting_name='setting_name'):

    retrieve_setting_logger = logging.getLogger('cerebro_utils.retrieve_setting')
    retrieve_setting_logger.info("In retrieve_setting ...")

    if not setting_name:
        retrieve_setting_logger.error("Invalid parameter provided!")
        return False
        
    db_file = "cerebro.db"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    retrieve_setting_logger.info("Created the DB connection...")
    dml_sql = """ SELECT setting_value FROM local_settings WHERE setting_name='%s' """ % setting_name
    
    retrieve_setting_logger.info("Now , executing sql: '%s' ." % dml_sql)
    c.execute(dml_sql)

    setting_value = None
    rows = c.fetchall()
    if len(rows) >= 1:
        if len(rows[0]) >= 1:
            setting_value = rows[0][0]

    retrieve_setting_logger.info("Now , retrieved the setting value as: %s ." % setting_value)

    if not setting_value:
        setting_value = ""

    return setting_value

# Change - on 11/29/2019 - by Sachin - End


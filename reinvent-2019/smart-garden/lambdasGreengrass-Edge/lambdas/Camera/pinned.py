import io
import logging
import os
import sys
import time
from datetime import datetime
from subprocess import call
from time import sleep
from fnmatch import fnmatch
import json 

from PIL import Image
import select
import v4l2capture

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './vendored/'))

import boto3

import greengrasssdk
s3client = greengrasssdk.client("iot-data")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Initializing Camera/handler')

OS_PATH_PICS = "/home/ggc_user"
S3_BUCKET_NAME = 'smart-garden-images'
INTERVAL = 300 # seconds -> 5 min

serial = ""
def getserial():
    if serial != "":
        return serial

    logger.info('getserial called')
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except: 
        cpuserial = "ERROR000000000"
    return cpuserial   

def get_bucket_size():
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix="raw-pics/{}/".format(getserial()))      
    if "Contents" in response:      
        return len(response["Contents"])
    else:
        return 0
    
def take_pic():
    video = v4l2capture.Video_device("/dev/video0")
    size_x, size_y = video.set_format(1280, 1024)
    video.create_buffers(1)
    video.queue_all_buffers()
    video.start()
    select.select((video,), (), ())
    image_data = video.read()
    video.close()
    image = Image.fromstring("RGB", (size_x, size_y), image_data)
    in_mem_file = io.BytesIO()
    logger.info("In_men_file pre saved size {}".format(len(in_mem_file.getvalue())))
    image.save(in_mem_file, "JPEG")
    logger.info("In_men_filepost saved size {}".format(len(in_mem_file.getvalue())))
    return in_mem_file    
 
def upload_to_s3(file):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket_size = get_bucket_size()
    logger.info("bucket_size {}".format(bucket_size))
    key = 'raw-pics/{}/IMG{}.jpg'.format(getserial(), str(get_bucket_size() + 1).zfill(3)) 
    bucket.put_object(Key=key, Body=file.getvalue())
    logger.info("image saved to {} with ".format(key))
    s3_client = boto3.client("s3")
    retorno = s3_client.get_object(Key=key, Bucket=S3_BUCKET_NAME)
    logger.info("tamanho do arquivo no bucket s3 {}".format(retorno["ContentLength"]))

def capture_image():
    """
    Captures image from RPi Camera
    """
    logger.info('Invoked function capture_image()')
    file = take_pic()
    upload_to_s3(file)
    logger.info("tirou foto")


def start():
    while True:
        capture_image()
        time.sleep(INTERVAL)

start()

def pinned_handler():
    """
    Mock function to run pinned lambda
    """
    pass

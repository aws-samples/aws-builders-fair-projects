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

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

import requests

from config import Configuration

# --------- Module- Level Globals ---------------

config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------


#python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>
host = 'aiw42dxvn7vdk.iot.us-east-1.amazonaws.com'
rootCAPath = '../iot-certs/root-CA.crt'
certificatePath = '../iot-certs/Cerebro-Ronan.cert.pem'
privateKeyPath = '../iot-certs/Cerebro-Ronan.private.key'
clientId = 'cerebroClientPi-util'
topic = 'cerebro'
#Cerebro-Ronan.public.key

port = 443

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

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

def send_iot_message(iot_msg={}, delay=0, device_id="default_device"):
    send_iot_message_logger = logging.getLogger('take_profile_photo.send_iot_message')
    send_iot_message_logger.info("Entered send_iot_message ...")
    message = {}
    message['message'] = iot_msg
    message['message']['device_id'] = device_id
    messageJson = json.dumps(message)
    print("Trying to publish: " + str(messageJson))
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    return True

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

__APIGW_X_API_KEY__ = "2YSoTXerhD4u3iat9CWUM9kn756MTJIp4c4Tgfqk"
__APIGW_X_API_KEY_QR_CODE__ = "aLCOemQkKa6EzcOQU6xjI8T2hRzD4Cf050EwWdb1"

__APIGW_API__ = "https://lqhvtjhlsc.execute-api.us-east-1.amazonaws.com/production/Cerebro_GetImages_S3List"
__APIGW_API_QR_CODE__ = "https://lqhvtjhlsc.execute-api.us-east-1.amazonaws.com/production/Cerebro_GetQRCode"

__S3_BUCKET__ = "project-cerebro"

'''

def send_sqs_message(sqs_queue=config.__SQS_QUEUE_NAME__, sqs_msg={}, delay=0, device_id="default_device"):
    send_sqs_message_logger = logging.getLogger('take_profile_photo.send_sqs_message')
    send_sqs_message_logger.info("Entered send_sqs_message ...")

    client = boto3.resource('sqs')
    queue = client.get_queue_by_name(QueueName=sqs_queue)

    if sqs_msg:
        if "device_id" not in sqs_msg.keys():
            if device_id:
                sqs_msg["device_id"] = device_id
        send_sqs_message_logger.info(json.dumps(sqs_msg))
        response = queue.send_message(MessageBody=json.dumps(sqs_msg), DelaySeconds=int(delay))
    else:
        response = queue.send_message(MessageBody='Hello World')

    send_sqs_message_logger.info(response)

    return True

def update_button_attributes(ready_for_event="none", image_path="none", selfie_mode=False):

    update_button_attributes_logger = logging.getLogger('cerebro_utils.update_button_attributes')

    client = boto3.client('iot1click-projects', region_name='us-east-1')
    response = client.list_projects()
    update_button_attributes_logger.info(response["projects"][0])
    iot_project_name = response["projects"][0]["projectName"]
    response = client.list_placements(projectName=iot_project_name)
    update_button_attributes_logger.info(response["placements"][0])
    iot_placement_name = response["placements"][0]["placementName"]
    response = client.describe_placement(placementName=iot_placement_name,
                                            projectName=iot_project_name)
    update_button_attributes_logger.info(response["placement"])
    iot_placement_attributes = response["placement"]['attributes']
    # next update the placement attribute with a none - essentially disable for future action
    iot_attributes_to_update = {}
    iot_attributes_to_update['ready_for_event'] = ready_for_event
    iot_attributes_to_update['image_path'] = image_path
    iot_attributes_to_update['selfie_mode'] = str(selfie_mode)

    update_button_attributes_logger.info("The iot attributes to be updated: ")
    update_button_attributes_logger.info(iot_attributes_to_update)
    response = client.update_placement(placementName=iot_placement_name,
                                        projectName=iot_project_name,
                                        attributes=iot_attributes_to_update
                                        )

    return iot_placement_attributes

def delete_object(bucket_name, object_name):
    """Delete an object from an S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: True if the referenced object was deleted, otherwise False
    """

    # Delete the object
    s3 = boto3.client('s3')
    try:
        logging.info("Going to delete: %s from bucket: %s now!" % (object_name, bucket_name))
        s3.delete_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_ddb_data(esk=None, profile_match_only=False, image_id='', hash_keys_only=False):

    get_ddb_data_logger = logging.getLogger('aws_utils.get_ddb_data')
    get_ddb_data_logger.info("In get_ddb_data ...")
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table("cerebro_media")

    if profile_match_only:
        fe = Attr('profile_matched').exists()
    elif image_id:
        fe = Key('external_image_id').eq(str(image_id))
    else:
        fe = None
    #fe = Key('profile').begins_with("serena");

    if hash_keys_only:
        #
        pe = "#external_image_id, #epoch"
        # Expression Attribute Names for Projection Expression only.
        ean = { "#external_image_id": "external_image_id", "#epoch": "epoch" }
    else:
        pe = None
        ean = None

        # defaults if needed
        '''
        pe = "#epoch, #current_time, #external_image_id, #profile"
        # Expression Attribute Names for Projection Expression only.
        ean = { "#epoch": "epoch", "#current_time": "current_time", "#external_image_id": "external_image_id", "#profile": "profile" }
        '''

    if esk:
        if fe and not (pe or ean):
            scanned_data = table.scan(
                FilterExpression=fe,
                ExclusiveStartKey=esk
                )
        elif fe and (pe and ean):
            scanned_data = table.scan(
                FilterExpression=fe,
                ProjectionExpression=pe,
                ExpressionAttributeNames=ean,                
                ExclusiveStartKey=esk
                )            
        else:
            scanned_data = table.scan(
                ExclusiveStartKey=esk
                )            
    else:
        if fe and not (pe or ean):
            scanned_data = table.scan(
                FilterExpression=fe
                )
        elif fe and (pe and ean):
            scanned_data = table.scan(
                FilterExpression=fe,
                ProjectionExpression=pe,
                ExpressionAttributeNames=ean
                )            
        else:
            scanned_data = table.scan(
                )            

    return scanned_data, table

'''
delete all user profile data
1. get all assets where there was a profile matched
2. walk thru' each item retrieved
2a. if not stock profile, then for that pk, get all the ddb entries (filtered)
2b. delete each of those entries
3. done
'''

def is_item_deletable(ddb_item=None, batch_writer=None):

    delete_item_logger = logging.getLogger('aws_utils.delete_item')    
    delete_item_logger.info("In delete_item ...")

    items_marked_for_deletion = None

    profile_whitelist = ('serena', 'biles', 'rock', 'federer', 'unknown', 'bezos', 'jassy')

    delete_item_logger.info("In delete item ...")

    profile_key = "profile"
    profile_list = []
    if profile_key in ddb_item:
        profile_list.append(ddb_item[profile_key])

    profile_key = "profile_matched"
    if profile_key in ddb_item:
        for profile_tagged in ddb_item[profile_key]:
            profile_list.append(profile_tagged)

    delete_item_logger.info(profile_list)
    for profile_tagged in profile_list:
        if profile_tagged.lower() not in profile_whitelist:
            # issue the delete instructions

            return ddb_item['external_image_id']

    delete_item_logger.info("whitelisted profile - no deletes needed")

    return None

def delete_data():

    delete_data_logger = logging.getLogger('aws_utils.delete_data')    
    delete_data_logger.info("In delete_data ...")
    #profile_whitelist = ('serena', 'simone', 'rock', 'jim', 'usain', 'salma', 'federer', 'lebron', 'salman')

    scanned_data, table = get_ddb_data()

    delete_data_logger.info("Retrieved DDB Data ...")

    items_for_deletion = []

    with table.batch_writer() as batch:
        delete_data_logger.info("First pass of DDB Data ...")

        for each in scanned_data['Items']:

            item_to_delete = is_item_deletable(ddb_item=each, batch_writer=batch)
            if item_to_delete:
                items_for_deletion.append(item_to_delete)

        while 'LastEvaluatedKey' in scanned_data:
            logging.info("More to be evaluated")
            scanned_data = get_ddb_data(esk=scanned_data['LastEvaluatedKey'])

            with table.batch_writer() as batch:
                delete_data_logger.info("Additional pass of DDB Data ...")
                for each in scanned_data['Items']:
                    item_to_delete = is_item_deletable(ddb_item=each, batch_writer=batch)
                    if item_to_delete:
                        items_for_deletion.append(item_to_delete)

    # now check if there was anything to be deleted
    delete_data_logger.info("List of items for deleteion ...")
    delete_data_logger.info(items_for_deletion)

    if items_for_deletion:
        for item in items_for_deletion:
            # delete each item - s3 object and DDB item
            delete_data_logger.info("Item: %s" % item)
            # s3 object
            delete_data_logger.info("Deleting s3 object now ...")
            delete_object(bucket_name='project-cerebro', object_name=item)
            # now get the ddb items and delete
            delete_data_logger.info("Getting DDB items ...")
            ddb_items, ddb_table = get_ddb_data(image_id=item, hash_keys_only=True)
            delete_data_logger.info("and now deleting ddb items ...")
            with ddb_table.batch_writer() as batch:
                for each in ddb_items['Items']:
                    batch.delete_item(Key=each)
            delete_data_logger.info("DDB items for this key: %s - deleted!" % item)

    delete_data_logger.info("delete_data completed!")
    return

def upload_image(image_path='', device_id=None):
    upload_image_logger = logging.getLogger('cerebro_utils.upload_image')

    upload_image_logger.info("Entered the upload image with imagepath: %s" % image_path)

    if not image_path:
        upload_image_logger.error("Error! No Image Path found - nothing to upload!")
        return

    # first write into the manifest for a single image
    with open("s3_manifest.txt","w") as fout:
        fout.write("%s" % image_path)

    uploader_util = "python3 media_uploader.py"
    cmd_params = "--imagedir %s --manifest" % os.path.dirname(image_path)

    # next invoke the uploader 
    status = subprocess.call(
                '%s %s 2>&1 &' % 
                (uploader_util, cmd_params), 
                shell=True)                     
    
    # finally send out a message indicating an upload
    profile_name = os.path.basename(image_path).split(".")[0]
    if "profile_" in profile_name:
        profile_name = profile_name.split("profile_")[1]

    sqs_request = {}
    sqs_request["profile_name"] = profile_name
    sqs_request["action"] = "profile_registered"

    send_iot_message(iot_msg=sqs_request, device_id=device_id)

    sqs_request = {}
    sqs_request["profile"] = ""
    sqs_request["audio"] = "yes"
    sqs_request["action"] = "show_profile"


    send_iot_message(iot_msg=sqs_request, device_id=device_id, delay=60)

    # all done so return
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

def download_qrcode(image_id='', image_dir=config.__CEREBRO_MEDIA_DIR__):
    download_qrcode_logger = logging.getLogger('cerebro_processor.download_qrcode')

    download_qrcode_logger.info("Entered download_qrcode ...")
    # Create an S3 client
    s3 = boto3.resource('s3')

    download_qrcode_logger.info("Downloading QRCode now ...")

    payload={}
    if image_id:
        payload['image_id']=image_id
    else:
        payload['image_id']="5e5100ae4880030cfd099a603b3be736.jpg"

    headers = {
        'Content-Type': "application/json",
        'x-api-key': config.__APIGW_X_API_KEY_QR_CODE__
        }

    url = config.__APIGW_API_QR_CODE__

    download_qrcode_logger.info("URL: %s, payload: %s" % (url, json.dumps(payload)) )
    response = requests.request(
        "POST", 
        url, 
        data=json.dumps(payload), 
        headers=headers)

    s3_bucket = config.__S3_BUCKET__
    s3_key = ""

    response_dict = response.json()
    download_qrcode_logger.info("Response: %s" % (json.dumps(response_dict)) )

    download_qrcode_logger.info("Processing QRCode: %s ..." % response_dict["qrcode_key"])
    # now download the s3 files one by one
    s3_key = response_dict["qrcode_key"]
    local_file = "%s/%s" % (image_dir, os.path.basename(s3_key))
    download_qrcode_logger.info(local_file)

    download_qrcode_logger.info("Try downloading file: %s" % s3_key)
    try:
        s3.Bucket(s3_bucket).download_file(s3_key, local_file)
    except botocore.exceptions.ClientError as e:
        download_qrcode_logger.error("Error seen!")
        if e.response['Error']['Code'] == "404":
            download_qrcode_logger.error("The object does not exist.")
        else:
            raise
    download_qrcode_logger.info("Image Downloaded to %s." % local_file)

    download_qrcode_logger.info("QRCode downloaded.")
    return True

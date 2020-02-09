import boto3
import json
import os
import logging

from contextlib import closing

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from random import shuffle

import time

import pyqrcode
import png

__BUCKET_NAME__ = "project-cerebro"

dynamo = boto3.client('dynamodb')
logger = None

print("In initialize fn ...")

logger = logging.getLogger()
if int(os.environ['DEBUG_MODE']):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
        
logger.info("Initialize: Just a test")
logger.debug("Initialize: debug a test")

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        },
    }

# input parameters are:
# 1. image ID
# output parameters are:
# 1. generated QRCode

# workflow:
# 1. first get the image_id
# 2. confirm this exists in s3
# 3. generate a presigned URL with this s3 path
# 4. create a QR Code image with this url embedded
# 5. return the QR code stored in S3 temp.

def main(event, context):
    
    logger.info("In main ...")
    start_time = int(round(time.time() * 1000))

    body_params = json.loads(event["body"])
    logger.debug("Body params:")
    logger.debug(body_params)

    response_data = {}

    # 1. get the image_id
    if "image_id" in body_params:
        image_id = body_params["image_id"]
        # prefix and check for existence
        s3_prefix = "production/%s" % image_id
        # 2. check for the object in s3
        s3 = boto3.resource('s3')
        s3_object = s3.Object(__BUCKET_NAME__, s3_prefix)
        obj_metadata = s3_object.load()  # fetches metadata for the object, but not data.
        logger.info("metadata found:")
        logger.info(obj_metadata)
        if obj_metadata:
            response_data["s3_image"] = s3_prefix

        # 3. generate the presigned url
        presigned_url = create_presigned_url(bucket_name = __BUCKET_NAME__, object_name=s3_prefix, expiration=5*60)
        logger.info("generated the presigned URL:")
        logger.info(presigned_url)
        if presigned_url:
            response_data["presigned_url"] = presigned_url
            logger.info("assigned presigned url")

            # 4. generate the qrcode, convert to png
            url = pyqrcode.create(presigned_url)
            url.png('/tmp/code.png', scale=5)
            logger.info("Created a png file by now!")

            # 5. save to s3
            target_file='/tmp/code.png'
            qrcode_key = "qrcodes/current_qrcode.png"

            logger.info("Now trying to put s3 object ...")
            # Create an S3 client
            s3 = boto3.client('s3')
            response = s3.put_object(
                Body=open(target_file, 'rb'), 
                Bucket=__BUCKET_NAME__, 
                Key=qrcode_key)
            logger.info("Now trying to put s3 object - completed!")

            response_data["qrcode_key"] = qrcode_key

    else:
        response_data["result"] = "Failure"
        return respond(None, response_data)

    end_time = int(round(time.time() * 1000))
    logger.info("Time Taken: %f" % (end_time - start_time))
    logger.info("Done with main!")

    response_data["result"] = "Success"
    response_data["time_taken"] = str(end_time - start_time)

    return respond(None, response_data)

def lambda_handler(event, context):
    return main(event, context)

import json
import boto3
import random
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

pinpoint = boto3.client('pinpoint')

def lambda_handler(event, context):
    message = os.environ['smsText']
    mobile = os.environ['mobileNumber']
    applicationid = os.environ['applicationId']
    
    logging.info('Sending SMS to ' + mobile + ' using applicationid ' + applicationid)
    pinpoint.send_messages(
        ApplicationId=applicationid,
        MessageRequest={
            'Addresses': {
                mobile: {'ChannelType': 'SMS'}
            },
            'MessageConfiguration': {
                'SMSMessage': {
                    'Body': message,
                    'MessageType': 'TRANSACTIONAL'
                }
            }
        }
    )
    logging.info ("Message sent")

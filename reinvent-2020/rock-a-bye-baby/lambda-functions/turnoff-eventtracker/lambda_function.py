import boto3
import time
import logging
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    session = boto3.Session()
    dyn_resource = None

    if dyn_resource is None:
        dyn_resource = boto3.resource('dynamodb')
    table = dyn_resource.Table('RabActivityTracker')

    response = table.query (IndexName='DeviceId-UpdateTime-index',
                KeyConditionExpression=
                Key('DeviceId').eq('RAB') & Key('UpdateTime').gte(int(time.time()-300))
                )
    if (len(response['Items']) > 0):
        if response['Items'][0]['ActivityStatus'] == 'ON':
            logging.info ("Updating item to OFF")
            upd = table.update_item(
                   Key={
                     'DeviceId': 'RAB',
                     'CreationTime': response['Items'][0]['CreationTime']
                   },
                   UpdateExpression="set ActivityStatus=:s",
                   ExpressionAttributeValues={
                    ':s': 'OFF',
                   },
                   ReturnValues="UPDATED_NEW"
                )
            return upd

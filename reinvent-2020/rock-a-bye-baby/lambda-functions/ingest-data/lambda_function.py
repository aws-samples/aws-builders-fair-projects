import boto3
import argparse
from botocore.config import Config
import logging
import time
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
    print ("Query results", response)
    if response['Count']== 0:
        logging.info ("Adding items")
        creationTime = int(time.time())
        upd = table.put_item(
                Item={
                    'DeviceId': 'RAB',
                    'ActivityStatus': 'ON',
                    'CreationTime':creationTime,
                    'UpdateTime': creationTime,
                    'ActivityCounter': 1
                }
             )
        updateEvent('RAB',creationTime,1)
        return 0
    elif response['Items'][0]['ActivityStatus'] == 'OFF':
        logging.info ("Updating items")
        upd = table.update_item(
               Key={
                 'DeviceId': 'RAB',
                 'CreationTime': response['Items'][0]['CreationTime']
               },
               UpdateExpression="set ActivityStatus=:s, UpdateTime=:r, ActivityCounter=:p",
               ExpressionAttributeValues={
                ':s': 'ON',
                ':r': int(time.time()),
                ':p': response['Items'][0]['ActivityCounter'] + 1
               },
               ReturnValues="UPDATED_NEW"
            )
        updateEvent('RAB',response['Items'][0]['CreationTime'],response['Items'][0]['ActivityCounter'] + 1)
        return 2
    else:
        return 1
def updateEvent(deviceid, creationtime, activitycounter):
    DATABASE_NAME = "eventsDB"
    TABLE_NAME = "sleepEvents"
    session = boto3.Session()

    write_client = session.client('timestream-write', config=Config(read_timeout=20, max_pool_connections=5000,
                                                                    retries={'max_attempts': 10}))

    current_time = str(int(round(time.time() * 1000)))

    dimensions = [
        {'Name': 'DeviceId', 'Value': deviceid},
    ]

    activity_counter = {
        'Dimensions': dimensions,
        'MeasureName': 'ActivityCounter',
        'MeasureValue': str(activitycounter),
        'MeasureValueType': 'DOUBLE',
        'Time': current_time
    }

    start_time = {
        'Dimensions': dimensions,
        'MeasureName': 'StartTime',
        'MeasureValue': str(creationtime),
        'MeasureValueType': 'DOUBLE',
        'Time': current_time
    }

    records = [activity_counter,start_time]

    try:
        result = write_client.write_records(DatabaseName=DATABASE_NAME, TableName=TABLE_NAME,
                                               Records=records, CommonAttributes={})
        logging.info("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
    except Exception as err:
        logging.info("Error:", err)

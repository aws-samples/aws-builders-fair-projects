from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib
import os
from datetime import datetime

ddb_table_name = os.environ['CEREBRO_TABLE']

def insert_metadata(exif_data={}):

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.

    table = boto3.resource('dynamodb').Table(ddb_table_name)
    
    metadata_entry = {}
    if "ETag" in exif_data.keys():
        # shortcut for now - assuming we are only doing JPGs
        metadata_entry["ExternalImageId"] = "production/%s.jpg" % (exif_data["ETag"])
    else:
        metadata_entry["ExternalImageId"] = "Unknown!"

    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    current_time = datetime.utcnow()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    current_time_epoch = current_time.strftime("%s")
        
    print(current_time_epoch)
    (dt, micro) = current_time_str.split('.')
    dt = "%s.%s" % (current_time_epoch, micro)
    print(dt,micro)

    current_time_epoch = Decimal(dt)
    print(current_time_epoch) 

    ddb_item = {}
    
    if "ETag" in exif_data.keys():
        # shortcut for now - assuming we are only doing JPGs
        ddb_item['external_image_id'] = "production/%s.jpg" % (exif_data["ETag"])
    else:
        ddb_item['external_image_id'] = "Unknown!"
    
    ddb_item['epoch'] = current_time_epoch
    ddb_item['current_time'] = current_time_str
    ddb_item["rec_type"] = "exif_data"
    
    for key, value in exif_data.items():
        print(key,key.split(":"),value)
        exif_keys = key.split(":")
        if len(exif_keys) < 2:
            continue
        if not value:
            continue
        
        exif_tagname = "%s_%s" % (exif_keys[0], exif_keys[1])
        ddb_item[exif_tagname] = str(value)

    # next, up --- insert exif data for real
    print("ddb item asembled...")
    print(ddb_item)
    
    response = table.put_item(Item=ddb_item)
    print(response)
    
    return response


def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(context)
    
    for record in event["Records"]:
        print(record)
        if "body" in record.keys():
            sqs_msg = json.loads(record["body"])
            print(sqs_msg)
            insert_metadata(exif_data=sqs_msg)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

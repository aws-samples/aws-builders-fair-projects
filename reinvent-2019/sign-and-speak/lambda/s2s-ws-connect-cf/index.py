import boto3
import json
from datetime import datetime, timedelta
import time
import os

def lambda_handler(event, context):
    
    print (event)
    
    msgBody = (event)
    reqContext = event["requestContext"]
    connectionId = reqContext["connectionId"]
    print("connectionId is : " + connectionId)
    
    
    
    #store to dynamo db
    ddbclient = boto3.client('dynamodb')
    nowDTTM = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') # '2019-05-22 06:06:42
    epocSec = int(time.time())

    response = ddbclient.put_item(
    Item={
        'connectionId': {
            'S': str(connectionId),
        },
        'insertdttm' : {
            'S': nowDTTM
        },
        'epocSecond' : {
            'N' : str(epocSec)
        }
    },
    TableName=os.environ['wsclientstable'],
    )

    print(response)
    

    return {
        'statusCode': 200,
        'body': json.dumps('Successful connect')
    }

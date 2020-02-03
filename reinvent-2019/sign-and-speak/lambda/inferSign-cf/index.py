import boto3
import json
import uuid 
from datetime import datetime, timedelta
import time
import os

s2smodelendpoint = os.environ["s2smodelendpoint"]
messagestable = os.environ["messagestable"]

def lambda_handler(event, context):
    
    recordInfo = event["Records"][0]
    
    s3Info = recordInfo["s3"]
    
    bucketInfo = s3Info["bucket"]
    
    bucketName = bucketInfo["name"]
    
    objectInfo = s3Info ["object"]    
    
    key = objectInfo["key"]
    print ("key : " + key)
    
    files3url = "s3://" + bucketName + "/" + key
    print("files3url is " + files3url)
    
    client = boto3.client('sagemaker-runtime')
    
    response = client.invoke_endpoint(
        EndpointName=s2smodelendpoint, #'sagemaker-pytorch-2019-11-22-23-31-53-466',
        Body=json.dumps({'grid': files3url}),
        ContentType='application/json'
    )
    prediction = json.loads(response['Body'].read())
    prediction_label = prediction['output']
    prediction_confidence = prediction['confidence']
    print("prediction_label is "    + prediction_label)
    print("prediction_confidence is "    + str(prediction_confidence))

    #print(prediction)

    #store to dynamo db
    ddbclient = boto3.client('dynamodb')
    nowDTTM = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') # '2019-05-22 06:06:42
    epocSec = int(time.time())

    response = ddbclient.put_item(
    Item={
        'msgid': {
            'S': str(uuid.uuid1()),
        },
        'msg': {
            'S': prediction_label,
        },
        'confidence': {
            'S': str(prediction_confidence),
        },
        'isSign' : {
            'BOOL' : True
        },
        'insertdttm' : {
            'S': nowDTTM
        },
        'epocSecond' : {
            'N' : str(epocSec)
        }
    },
    TableName=messagestable,
    )

    print(response)
    

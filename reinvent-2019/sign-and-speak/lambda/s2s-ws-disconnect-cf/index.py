import json
import boto3
import os
def lambda_handler(event, context):
    
    print (event)
    
    msgBody = (event)
    reqContext = event["requestContext"]
    connectionId = str(reqContext["connectionId"])
    print("connectionId is : " + connectionId)


    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['wsclientstable'])    
    
    response = table.delete_item(
        Key={'connectionId' : connectionId}
    )
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Successful disconnect')
    }

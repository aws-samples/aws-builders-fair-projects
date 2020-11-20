from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import random, time
import boto3
import json
import time

# A random programmatic shadow client ID.
SHADOW_CLIENT = "myShadowClient"

# The unique hostname that &IoT; generated for
# this device.
HOST_NAME = "a3lka4ud7kfmrw-ats.iot.us-east-1.amazonaws.com"

# The relative path to the correct root CA file for &IoT;,
# which you have already saved onto this device.
ROOT_CA = "AmazonRootCA1.pem"

# The relative path to your private key file that
# &IoT; generated for this device, which you
# have already saved onto this device.
PRIVATE_KEY = "c663246bf0-private.pem.key"
# The relative path to your certificate file that
# &IoT; generated for this device, which you
# have already saved onto this device.
CERT_FILE = "c663246bf0-certificate.pem.crt"

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "pi4"

def myShadowUpdateCallback(payload, responseStatus, token):
    print('Loading function')
    print('UPDATE: $aws/things/' + SHADOW_HANDLER +
          '/shadow/update/#')
    print("payload = " + payload)
    print("responseStatus = " + responseStatus)
    print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
                                    CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()
# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
    SHADOW_HANDLER, True)

#dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }


def lambda_handler(event, context):
    #    myDeviceShadow.shadowUpdate(
    #      '{"state":{"reported":{"play":"song.mid"},{"sessionId":"234232323423423234"}}}',

    print("event:",event)
    print("context",context)
    params = event['multiValueQueryStringParameters']
    if ('songId' in params.keys()):
        songId = params['songId'][0]
    else:
        songId = '1'

    if ('duration' in params.keys()):
        duration = params['duration']
    else:
        duration = "30"

    if ('tempo' in params.keys()):
        tempo = params['tempo']
    else:
        tempo = "120"

    if ('stageName' in params.keys()):
        stageName = params['stageName']
    else:
        stageName = "Guest"

    if ('sessionId' in params.keys()):
        sessionId = params['sessionId'][0]
    else:
        sessionId = stageName[0]   # default to stage name as we can control that from the UI

    if ('startRecord' in params.keys()):
        startRecord = params['startRecord'][0]
    else:
        startRecord = "False"

    shadowJson =  '{"state":{"reported": { "play" : "%s", "sessionId": "%s", "duration" : "%s", "tempo" : "%s", "stageName" : "%s", "startRecord" : "%s"} }}' % (songId,sessionId,duration[0],tempo[0],stageName[0],startRecord)
    print(shadowJson)

    myDeviceShadow.shadowUpdate(
        shadowJson,
        myShadowUpdateCallback, 5)
    apiresponse = {
        "statusCode": 200,
        "headers": {
            "content-type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": "sent message to start song",
        "isBase64Encoded": False,
    }
    #return 'sent message to start song'
    return apiresponse


import boto3
import json

client = boto3.client('iot-data', region_name='us-east-1')

def function_handler(event, context):
    topicIOT='SmartGarden/WaterRelease'
    try:
        clickType = event['clickType']
        print("Received event: " + json.dumps(event, indent=2))
        if clickType=="SINGLE":
            topicIOT='SmartGarden/groot'
        elif clickType=="DOUBLE":
            topicIOT='SmartGarden/flowers'
        elif clickType=="LONG":
            topicIOT='SmartGarden/WaterRelease'
    except (ValueError, KeyError, TypeError):
        print("Not a IoT Button")

    # Change topic, qos and payload
    response = client.publish(
        topic=topicIOT, #PlantWatering/WaterRelease #'smartgarden/esp32data', #
        qos=0,
        payload=json.dumps({"water":"plant"})
    )
    return "I'm going to water your Smart Garden!"

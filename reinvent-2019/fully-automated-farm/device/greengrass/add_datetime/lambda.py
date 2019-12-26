#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassHelloWorld.py
# Demonstrates a simple publish to a topic using Greengrass core sdk
# This lambda function will retrieve underlying platform information and send
# a hello world message along with the platform information to the topic 'hello/world'
# The function will sleep for five seconds, then repeat.  Since the function is
# long-lived it will run forever when deployed to a Greengrass core.  The handler
# will NOT be invoked in our example since the we are executing an infinite loop.

import greengrasssdk
import time
import json
import logging

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

def get_input_topic(context):
    try:
        topic = context.client_context.custom['subject']
    except Exception as e:
        logging.error('Topic could not be parsed. ' + repr(e))
    return topic
    
def add_ts(event):
    event['ts'] = int(time.time()*1000)
    

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    
    target_topic = get_input_topic(context)
    add_ts(event)
    
    client.publish(topic=target_topic,payload=json.dumps(event))
    
    return

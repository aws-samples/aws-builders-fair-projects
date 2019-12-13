# HTTPPython.py

import json
import logging
import os
import requests

import greengrasssdk

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

THING_NAME = os.environ['AWS_IOT_THING_NAME']

base_topic = '/http_python' #THING_NAME + '/http_python'
request_topic = base_topic + '/request'
response_topic = base_topic + '/response'

def function_handler(event, context):
    inbound_topic = context.client_context.custom['subject']

    if not inbound_topic.startswith(request_topic):
        logger.info('Inbound topic is not the request topic hierarchy %s %s', inbound_topic, request_topic)
        return

    if not ('id' in event.keys()):
        logger.info('No ID found')
        return

    if not ('action' in event.keys()):
        logger.info('No action found')
        return

    if not ('url' in event.keys()):
        logger.info('No URL found')
        return

    action = event['action']

    if (not action == 'get') and (not action == 'post'):
        logger.info('Only get and post actions are supported %s', action)
        return

    id = event['id']
    url = event['url']

    data = None
    params = None

    if 'data' in event.keys():
        data = event['data']

    if 'params' in event.keys():
        params = event['params']

    response = None

    if action == 'get':
        response = requests.get(url, params=params)
    elif action == 'post':
        response = requests.post(url, params=params, data=data)
    else:
        logger.info('Should never happen 1')
        return

    reply = {}

    if (len(response.text) > (127 * 1024)):
        reply['response'] = ''
        reply['error'] = 'Data was too large to fit in a single MQTT message'
    else:
        reply['response'] = response.text

    json_reply = json.dumps(reply)

    logger.info('Publishing reply %s', json_reply)
    client.publish(topic=response_topic, payload=json_reply)
    return


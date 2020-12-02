import urllib.request
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logging.info('Received event: ' + json.dumps(event))

    ##### Get the TP-Link RESTful API token
    req = { "method": "login", "params": { "appType": "Kasa_Android",  "cloudUserName": " ",  "cloudPassword": " ", "terminalUUID": " " }}
    req['params']['cloudUserName'] = os.environ['kasaLogin']
    req['params']['cloudPassword'] = os.environ['kasaPassword']
    req['params']['terminalUUID'] = os.environ['UUID']

    # Get Kasa API key - send POST to server and get response
    logging.info('Received data: ' + json.dumps(req))
    data = json.dumps(req).encode('utf-8')
    httpReq = urllib.request.Request("https://wap.tplinkcloud.com",
                        data,
                        {'Content-Type': 'application/json'})
    f = urllib.request.urlopen(httpReq)
    response = f.read()
    f.close()
    rsp = json.loads(response)
    apiToken = rsp['result']['token']
    logging.info("Kasa API login response: " + str(response))

    ##### Get List of smart devices registered in Kasa
    req = { "method": "getDeviceList" }
    data = json.dumps(req).encode('utf-8')
    httpReq = urllib.request.Request("https://use1-wap.tplinkcloud.com/?token=" + apiToken,
                        data,
                        {'Content-Type': 'application/json'})
    f = urllib.request.urlopen(httpReq)
    response = f.read()
    f.close()
    logging.info("Kasa API get device list response: " + str(response))

    # Arbitrarily pick first device. This might have to be changed (can be hardcoded one you identify the device you want to control)
    rsp = json.loads(response)
    deviceId = rsp['result']['deviceList'][0]['deviceId']
    logging.info("Device selected: " + deviceId)

    ##### State control
    req = {"method":"passthrough", "params": {"deviceId": " ", "requestData": "{\"system\":{\"set_relay_state\":{\"state\":0}}}" }}
    req['params']['deviceId'] = deviceId

    # Handle different Amazon IoT button press modes
    logging.info('Turning switch OFF')
    # Send HTTP POST indicating to turn the relay on or off
    data = json.dumps(req).encode('utf-8')
    httpReq = urllib.request.Request("https://use1-wap.tplinkcloud.com/?token=" + apiToken,
                        data,
                        {'Content-Type': 'application/json'})
    f = urllib.request.urlopen(httpReq)
    response = f.read()
    f.close()
    logging.info("Kasa API relay state change response: " + str(response))

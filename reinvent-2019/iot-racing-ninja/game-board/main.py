#! /usr/bin/env python3
import asyncio 
from game import Game
from rpi_ws281x import Color
from board import Board
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 
import os, sys, json, logging

## Logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')

ENDPOINT = 'a24t36khlmixhw-ats.iot.us-east-1.amazonaws.com' 
ROOT = '/home/pi/root/AmazonRootCA1.pem' 
CERT_LOCATION = '/home/pi/certs/' 
PRIVATE = '-private.pem.key' 
CERTIFICATE = '-certificate.pem.crt' 
board = Board()
game = Game()
for bot in game.bots:
    board.lightPosition(game.bots[bot].position.x, game.bots[bot].position.y, bot)

""" MQTT Connection """ 
hostname = os.uname()[1]
mqTTClient = AWSIoTMQTTClient(hostname) 
mqTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
mqTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
mqTTClient.configureEndpoint(ENDPOINT, 8883) 
mqTTClient.configureCredentials(ROOT, CERT_LOCATION + hostname + PRIVATE, CERT_LOCATION + hostname + CERTIFICATE) 
mqTTClient.configureOfflinePublishQueueing(-1) 
mqTTClient.configureDrainingFrequency(2) 
mqTTClient.configureConnectDisconnectTimeout(10) 
mqTTClient.configureMQTTOperationTimeout(5)

logging.info('Done configuring MQTT Connection') 

def processMove(client, userdata, message):
    logging.debug(message)
    msg = json.loads(message.payload.decode('utf-8').replace("'",'"'))
    move = msg["move"]
    vehicle = msg["vehicle"]
    bot = game.bots[vehicle]
    board.unlightPosition(bot.position.x, bot.position.y)
    game.move(move, vehicle)
    board.lightPosition(bot.position.x, bot.position.y, bot.color)
    # mqTTClient.publish(f"vehicle/physical/ack/{vehicle}", "\{\}", 0)

if __name__ == '__main__':
    try:
        logging.info("Connecting to MQTT")
        mqTTClient.connect()
        mqTTClient.subscribe("vehicle/physical/move/red", 1, processMove)
        mqTTClient.subscribe("vehicle/physical/move/black", 1, processMove)
        mqTTClient.subscribe("vehicle/physical/move/yellow", 1, processMove)
        mqTTClient.subscribe("vehicle/physical/move/blue", 1, processMove)
        
        loop = asyncio.get_event_loop() 
        loop.run_forever() 
    finally:
        logging.info("Disconnecting from MQTT")
        mqTTClient.disconnect()
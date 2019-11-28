#! /usr/bin/env python3
import asyncio 
from game import Game
from rpi_ws281x import Color
from board import Board
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 
from position import Directions
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
    board.lightPosition(game.bots[bot].position.x, game.bots[bot].position.y, game.bots[bot].color)

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
    try:
        msg = json.loads(message.payload.decode('utf-8').replace("'",'"'))
        move = msg["move"]
        vehicle = msg["vehicle"]
        bot = game.bots[vehicle]
        board.unlightPosition(bot.position.x, bot.position.y)
        game.move(move, vehicle)
        board.lightPosition(bot.position.x, bot.position.y, bot.color)
        status = {"vehicle": vehicle, "status": "completed"}
        mqTTClient.publish(f"vehicle/physical/ack/{vehicle}", json.dumps(status), 0)
    except:
        raise
        logging.info("Exception occured")

def processLocate(client, userdata, message):
    logging.debug(message)
    try:
        msg = json.loads(message.payload.decode('utf-8').replace("'",'"'))
        vehicle = msg["vehicle"]
        bot = game.bots[vehicle]
        board.unlightPosition(bot.position.x, bot.position.y)
        bot.position.y = 6-((msg["y"]+1)-1) 
        bot.position.x = msg["x"]+1
        if msg["facing"] == "N":
            bot.position.direction = Directions.north
        elif msg["facing"] == "S":
            bot.position.direction = Directions.south
        elif msg["facing"] == "E":
            bot.position.direction = Directions.east
        elif msg["facing"] == "W":
            bot.position.direction = Directions.west
        board.lightPosition(bot.position.x, bot.position.y, bot.color)
    except:
        raise
        logging.info("Exception occured")

def processShutoff(client, userdata, message):
    try:
        board.light(list(range(0,1025)), Color(0,0,0))
    except:
        raise
        logging.info("Exception occured")

def processReset(client, userdata, message):
    try:
        game.startGame()
    except:
        raise
        logging.info("Exception occured")

if __name__ == '__main__':
    try:
        logging.info("Connecting to MQTT")
        mqTTClient.connect()

        # For board moves
        mqTTClient.subscribe("vehicle/physical/move/red", 1, processMove)
        mqTTClient.subscribe("vehicle/physical/move/black", 1, processMove)
        mqTTClient.subscribe("vehicle/physical/move/white", 1, processMove)
        mqTTClient.subscribe("vehicle/physical/move/blue", 1, processMove)

        # For explicit position setting
        mqTTClient.subscribe("vehicle/physical/location/red", 1, processLocate)
        mqTTClient.subscribe("vehicle/physical/location/black", 1, processLocate)
        mqTTClient.subscribe("vehicle/physical/location/white", 1, processLocate)
        mqTTClient.subscribe("vehicle/physical/location/blue", 1, processLocate)

        # Shutoff and reset controls 
        mqTTClient.subscribe("vehicle/physical/shutoff", 1, processShutoff)
        mqTTClient.subscribe("vehicle/physical/reset", 1, processReset)

        loop = asyncio.get_event_loop() 
        loop.run_forever() 
    finally:
        logging.info("Disconnecting from MQTT")
        mqTTClient.disconnect()

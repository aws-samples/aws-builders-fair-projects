from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.core.protocol.connection.cores import ProgressiveBackOffCore
from AWSIoTPythonSDK.core.greengrass.discovery.providers import DiscoveryInfoProvider
import sys
import os
import logging
import time
from datetime import datetime
import json
import signal
import serial

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
CONFIG_FILE = APP_ROOT + "/appconfig.json"
if not os.path.exists(CONFIG_FILE):
    print(CONFIG_FILE + " not exists")
    sys.exit("error")

APP_CONFIG = {}
with open(CONFIG_FILE) as f:
    APP_CONFIG = json.load(f)

MAX_RETRIES = 10
DEVICE_INFO_TOPIC = str(APP_CONFIG["DEVICE_INFO_TOPIC"])
MOVE_COMMAND_TOPIC = str(APP_CONFIG["MOVE_COMMAND_TOPIC"])
RAIL_COMMAND_TOPIC = str(APP_CONFIG["RAIL_COMMAND_TOPIC"])
ARDUINO_UNO_PORT = str(APP_CONFIG["ARDUINO_UNO_PORT"])
ROBOT_ACTION_INTERVAL = 5

IOT_ENDPOINT = str(APP_CONFIG["IOT_ENDPOINT"])
CERT_ROOT = APP_ROOT + "certs/"
ROOT_CA_FILE = CERT_ROOT + "rootca.pem"
GROUP_CA_FILE = CERT_ROOT + "groupca.pem"
CERT_FILE = CERT_ROOT + APP_CONFIG["CERT_FILE"]
PRIVATE_KEY_FILE = CERT_ROOT + str(APP_CONFIG["PRIVATE_KEY_FILE"])
PORT = 8883
THING_NAME = str(APP_CONFIG["THING_NAME"])

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Progressive back off core
backOffCore = ProgressiveBackOffCore()
mqttClient = None
robot_last_action_time = 0

# Serial client
serialClient = None

def move_command_callback(client, userdata, message):
    global robot_last_action_time
    logger.info(message.payload)

    now = datetime.now()
    interval = time.mktime(now.timetuple()) - robot_last_action_time
    if interval < ROBOT_ACTION_INTERVAL:
        logger.info("robot action interval is to short.{}".format(interval))
        return

    msg = json.loads(message.payload)
    if not serialClient or not serialClient.isOpen():
        logger.info("serial connection lost. ignore command")
        disconnect_serial()
        return
    cmd = "POS{}\n".format(msg["position"])
    logger.info("send {}".format(cmd))
    serialClient.write(cmd)
    robot_last_action_time = time.mktime(now.timetuple())

def dicovery_greengrass():
    ggHostDict = {}
    discoveryInfoProvider = DiscoveryInfoProvider()
    discoveryInfoProvider.configureEndpoint(IOT_ENDPOINT)
    discoveryInfoProvider.configureCredentials(ROOT_CA_FILE, CERT_FILE, PRIVATE_KEY_FILE)
    discoveryInfoProvider.configureTimeout(10)  # 10 sec
    discoveryInfo = discoveryInfoProvider.discover(THING_NAME)
    caList = discoveryInfo.getAllCas()
    coreList = discoveryInfo.getAllCores()
    groupId, ca = caList[0]
    coreInfo = coreList[0]

    with open(GROUP_CA_FILE, "w") as f:
        f.write(ca)

    return coreInfo

def connect_greengrass():
    global mqttClient, deviceShadowHandler
    retryCount = MAX_RETRIES
    coreInfo = dicovery_greengrass()
    mqttClient = AWSIoTMQTTClient(THING_NAME)

    while retryCount != 0:
        # Connect to Greengrass
        logger.info("MQTT Client setup")
        connected = False
        for connectivityInfo in coreInfo.connectivityInfoList:
            logger.info("connect to IP:{} port:{}".format(connectivityInfo.host, connectivityInfo.port))
            mqttClient.configureEndpoint(connectivityInfo.host, connectivityInfo.port)
            mqttClient.configureCredentials(GROUP_CA_FILE, PRIVATE_KEY_FILE, CERT_FILE)
            try:
                mqttClient.connect()
                logger.info("MQTT Client setup done")
                connected = True
                break
            except BaseException as e:
                print(e)
                pass

        if connected:
            mqttClient.subscribe(MOVE_COMMAND_TOPIC, 0, move_command_callback)
            logger.info("subscribe done")
            return

        # if connection fail
        retryCount -= 1
        backOffCore.backOff()

def disconnect_serial():
    global serialClient
    logger.info("close serial")
    try:
        if serialClient:
            serialClient.close()
    except Exception as e:
        logger.error(e)
        pass
    serialClient = None
    time.sleep(1)

def connect_serial():
    logger.info("connect serial")
    global serialClient
    try:
        serialClient = serial.Serial(ARDUINO_UNO_PORT, 9600)
        time.sleep(1)
        logger.info("serial connection success")
    except serial.serialutil.SerialException as e:
        logger.error(e)
        serialClient = None
        time.sleep(1)
        logger.info("connect fail")

def send_move_status():
    payload = {
        "action": "open"
    }
    mqttClient.publish(RAIL_COMMAND_TOPIC, json.dumps(payload), 0)
    logger.info("status published")

def main():
    global serialClient
    # report robot info
    payload = {
        "ip": os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
    }
    mqttClient.publish(DEVICE_INFO_TOPIC, json.dumps(payload), 0)

    while True:
        if not serialClient or not serialClient.isOpen():
            logger.warn("serial connection lost")
            connect_serial()
            continue

        line = ""
        try:
            line = serialClient.readline()
        except serial.serialutil.SerialException as e:
            logger.error(e)
            disconnect_serial()
            continue

        msg = line.strip()
        if msg == "MF":
            logger.info("robot moved")
            send_move_status()
        elif msg == "NM":
            logger.warn("robot not move")

        time.sleep(1)

    disconnect_serial()

def exit_handler(signal, frame):
    logger.info("abort")
    disconnect_serial()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)

    connect_greengrass()
    connect_serial()
    main()
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
import RPi.GPIO as GPIO
import glob

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
CONFIG_FILE = APP_ROOT + "/appconfig.json"
if not os.path.exists(CONFIG_FILE):
    print(CONFIG_FILE + " not exists")
    sys.exit("error")

APP_CONFIG = {}
with open(CONFIG_FILE) as f:
    APP_CONFIG = json.load(f)

GPIO_PWM_OUT = 4
GPIO_LED_CLOSE = 2
GPIO_LED_OPEN = 3

GPIO_BTN_CLOSE = 17
GPIO_BTN_OPEN = 18
GPIO_BTN_POS1 = 22
GPIO_BTN_POS2 = 23
GPIO_BTN_POS3 = 24

SERVO_OPEN = 4.2
SERVO_CLOSE = 8.6

BOUNCE_TIME=500
MAX_RETRIES = 10
DEVICE_INFO_TOPIC = str(APP_CONFIG["DEVICE_INFO_TOPIC"])
ROBOT_COMMAND_TOPIC = str(APP_CONFIG["ROBOT_COMMAND_TOPIC"])
RAIL_COMMAND_TOPIC = str(APP_CONFIG["RAIL_COMMAND_TOPIC"])
RAIL_STATUS_TOPIC = str(APP_CONFIG["RAIL_STATUS_TOPIC"])
SERVO_ACTION_INTERVAL = 2
ROBOT_ACTION_INTERVAL = 5
RAIL_OPEN = "open"
RAIL_CLOSE = "close"

IOT_ENDPOINT = str(APP_CONFIG["IOT_ENDPOINT"])
CERT_ROOT = APP_ROOT + "certs/"
ROOT_CA_FILE = CERT_ROOT + "rootca.pem"
GROUP_CA_FILE = CERT_ROOT + "groupca.pem"
CERT_FILE = CERT_ROOT + str(APP_CONFIG["CERT_FILE"])
PRIVATE_KEY_FILE = CERT_ROOT + str(APP_CONFIG["PRIVATE_KEY_FILE"])
PORT = 8883
THING_NAME = APP_CONFIG["THING_NAME"]
servo_current_status = None
robot_last_action_time = 0

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# GPIOs
logger.info("GPIO setup")
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_PWM_OUT, GPIO.OUT)
GPIO.setup(GPIO_LED_OPEN, GPIO.OUT)
GPIO.setup(GPIO_LED_CLOSE, GPIO.OUT)
GPIO.setup(GPIO_BTN_OPEN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_BTN_CLOSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_BTN_POS1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_BTN_POS2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_BTN_POS3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
logger.info("GPIO setup done")

# Progressive back off core
backOffCore = ProgressiveBackOffCore()
myAWSIoTMQTTShadowClient = None
myAWSIoTMQTTShadowClientDesire = None
mqttClient = None
deviceShadowHandler = None
deviceShadowHandlerDesire = None

# subscribe callback
def receive_rail_command(client, userdata, message):
    logger.info(message.payload)
    cmd = json.loads(message.payload)
    move_servo(cmd["action"])

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
            mqttClient.subscribe(RAIL_COMMAND_TOPIC, 0, receive_rail_command)
            logger.info("subscribe done")
            return

        # if connection fail
        retryCount -= 1
        backOffCore.backOff()

def move_servo(action):
    logger.info("rail status to: {}".format(action))
    global servo_current_status

    if servo_current_status == action:
        logger.debug("rail status is same")
        return

    GPIO.output(GPIO_LED_OPEN, False)
    GPIO.output(GPIO_LED_CLOSE, False)
    servo = GPIO.PWM(GPIO_PWM_OUT, 50)
    if action == RAIL_OPEN:
        servo.start(SERVO_OPEN)
        GPIO.output(GPIO_LED_OPEN, True)
    else:
        servo.start(SERVO_CLOSE)
        GPIO.output(GPIO_LED_CLOSE, True)
    time.sleep(1.0)
    servo.stop()
    servo_current_status = action

    payload = {
        "status": action
    }
    mqttClient.publish(RAIL_STATUS_TOPIC, json.dumps(payload), 0)

def publish_robot_command(pos):
    logger.info("send command {}".format(pos))
    payload = {
        "position": pos
    }
    mqttClient.publish(ROBOT_COMMAND_TOPIC, json.dumps(payload), 0)

# callback function
def btn_servo_pressed(pin):
    logger.info("btn_servo_pressed:{}".format(pin))

    if pin == GPIO_BTN_OPEN:
        move_servo(RAIL_OPEN)
    elif pin == GPIO_BTN_CLOSE:
        move_servo(RAIL_CLOSE)

def btn_robot_pressed(pin):
    logger.info("btn_robot_pressed:{}".format(pin))
    global robot_last_action_time

    now = datetime.now()
    interval = time.mktime(now.timetuple()) - robot_last_action_time
    if interval < ROBOT_ACTION_INTERVAL:
        logger.info("robot action interval is to short.{}".format(interval))
        return

    if pin == GPIO_BTN_POS1:
        publish_robot_command("1")
    elif pin == GPIO_BTN_POS2:
        publish_robot_command("2")
    elif pin == GPIO_BTN_POS3:
        publish_robot_command("3")

    robot_last_action_time = time.mktime(now.timetuple())

def main():
    # report rail info
    payload = {
        "ip": os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
    }
    mqttClient.publish(DEVICE_INFO_TOPIC, json.dumps(payload), 0)
    # open rail for default
    move_servo(RAIL_OPEN)

    # add event handler for buttons
    GPIO.add_event_detect(GPIO_BTN_OPEN, GPIO.RISING, callback=btn_servo_pressed, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(GPIO_BTN_CLOSE, GPIO.RISING, callback=btn_servo_pressed, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(GPIO_BTN_POS1, GPIO.RISING, callback=btn_robot_pressed, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(GPIO_BTN_POS2, GPIO.RISING, callback=btn_robot_pressed, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(GPIO_BTN_POS3, GPIO.RISING, callback=btn_robot_pressed, bouncetime=BOUNCE_TIME)

    # wait for events
    while True:
        time.sleep(1)

def exit_handler(signal, frame):
    GPIO.cleanup()
    logger.info("abort")
    sys.exit(0)

if __name__== "__main__":
    signal.signal(signal.SIGINT, exit_handler)

    connect_greengrass()
    main()
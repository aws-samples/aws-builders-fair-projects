import sys
import os


from PIL import Image
import numpy as np
import tensorflow as tf
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image as sensor_image
from sensor_msgs.msg import Joy

import logging
import logging.handlers
from time import sleep
from random import uniform
from threading import Thread
import json
from std_msgs.msg import String
import random
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient, AWSIoTMQTTShadowClient

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

logger.addHandler(handler)

# Set your variables here
FROZEN_MODEL_LOCAL_PATH = "model.pb"
FROZEN_MODEL_S3_KEY = "model/model.pb"
AWS_REGION = "us-west-2"


ROOT_CA = '/greengrass/certs/root.ca.pem'
CERT_KEY = '/greengrass/certs/ggc.cert.pem'
PRIVATE_KEY = '/greengrass/certs/ggc.private.key'
THING_NAME = os.environ['AWS_IOT_THING_NAME']
logger.debug('IoT Thing Name: {}'.format(THING_NAME))
IOT_ENDPOINT = os.environ['AWS_IOT_MQTT_ENDPOINT'][:-5]
logger.debug('IoT Endpoint: {}'.format(IOT_ENDPOINT))
logger.debug(os.environ)


TRAINING_IMAGE_SIZE = (160, 120)

class IoT(object):
    # Class to handle AWS IoT SDK connections and commands
    def __init__(self, host, rootCAPath, certificatePath, privateKeyPath,
                 clientId, useWebsocket=False, mode='both'):
        self.AllowedActions = ['both', 'publish', 'subscribe']
        self.host = host
        self.rootCAPath = rootCAPath
        self.certificatePath = certificatePath
        self.privateKeyPath = privateKeyPath
        self.clientId = clientId
        self.useWebsocket = useWebsocket
        self.mode = mode

        # Configure logging
        self.logger = logging.getLogger("AWSIoTPythonSDK.core")
        self.logger.setLevel(logging.ERROR)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)
        self.logger.addHandler(streamHandler)

        self.connect_client()
        self.connect_shadow_client()

    def connect_client(self):
        # Init AWSIoTMQTTClient
        self.myAWSIoTMQTTClient = None
        if self.useWebsocket:
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId, useWebsocket=True)
            self.myAWSIoTMQTTClient.configureEndpoint(self.host, 443)
            self.myAWSIoTMQTTClient.configureCredentials(self.rootCAPath)
        else:
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId)
            self.myAWSIoTMQTTClient.configureEndpoint(self.host, 8883)
            self.myAWSIoTMQTTClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.connect()

    def connect_shadow_client(self, clientId_suffix='_shadow'):
        # Init AWSIoTMQTTShadowClient
        clientId = self.clientId + clientId_suffix
        self.myAWSIoTMQTTShadowClient = None
        if self.useWebsocket:
            self.myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId, useWebsocket=True)
            self.myAWSIoTMQTTShadowClient.configureEndpoint(self.host, 443)
            self.myAWSIoTMQTTShadowClient.configureCredentials(self.rootCAPath)
        else:
            self.myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
            self.myAWSIoTMQTTShadowClient.configureEndpoint(self.host, 8883)
            self.myAWSIoTMQTTShadowClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

        # AWSIoTMQTTShadowClient configuration
        self.myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect to AWS IoT
        self.myAWSIoTMQTTShadowClient.connect()

    def shadow_handler(self, thingName):
        # Create a deviceShadow with persistent subscription
        self.deviceShadowHandler = self.myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

    def shadow_get(self, callback):
        try:
            # Get shadow JSON doc
            return self.deviceShadowHandler.shadowGet(callback, 5)
        except Exception as e:
            logger.exception(e)

    def shadow_update(self, json_payload, callback):
        # Update shadow JSON doc
        self.deviceShadowHandler.shadowUpdate(json_payload, callback, 5)

class InferenceWorker:
    def __init__(self, model_path):
        self.model_path = model_path

    def run(self):
        self.graph = self.load_graph()
        self.session = tf.Session(graph=self.graph, config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True))

        logger.debug('INFO: Creating publisher on /cmd_vel')
        self.ack_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        logger.debug('INFO: Creating subscriber on /camera/bgr/image_raw')
        rospy.Subscriber('/usb_cam/image_raw', sensor_image, self.callback_image)

        logger.debug('INFO: Finished initialization')

    def load_graph(self):
        print('Loading graph...')
        with tf.gfile.GFile(self.model_path, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name="turtlebot")

        print('INFO: Finished loading graph')

        return graph

    def callback_image(self, raw_image):
        try:
            global active_mode
            if active_mode:
                if active_mode == 'tracking':
                    image = Image.frombytes('RGB', (raw_image.width, raw_image.height),
                                            raw_image.data, 'raw', 'BGR', 0, 1)
                    image = image.resize(TRAINING_IMAGE_SIZE)
                    image = np.array(image)

                    # Get the yuma component of the image
                    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
                    image = 0.2989 * r + 0.5870 * g + 0.1140 * b

                    image = np.expand_dims(image, 2)
                    image = np.expand_dims(image, 0)

                    x = self.graph.get_tensor_by_name('turtlebot/main_level/agent/main/online/network_0/observation/observation:0')
                    y = self.graph.get_tensor_by_name('turtlebot/main_level/agent/main/online/network_1/ppo_head_0/policy:0')
                    inferenceOutput = np.argmax(self.session.run(y, feed_dict={
                        x: image
                    }))

                    self.takeAction(inferenceOutput)
        except Exception as e:
            logger.exception(e)

    def takeAction(self, action):
        if action == 0:  # move left
            steering = 0.6
            throttle = x
        elif action == 1:  # move right
            steering = -0.6
            throttle = x
        elif action == 2:  # straight
            steering = 0
            throttle = x
        elif action == 3:  # move left
            steering = 0.3
            throttle = x
        elif action == 4:  # move right
            steering = -0.3
            throttle = x
        else:  # should not be here
            raise ValueError("Invalid action")

        speed = Twist()
        speed.linear.x = throttle
        speed.angular.z = steering
        self.ack_publisher.publish(speed)

class EV3DEV:
    def __init__(self):
        self.shadow_event = None
        self.iot_init()
        self.thing_shadow_init()
        self.joystick_init()

    def iot_init(self):
        try:
            logger.debug('IOT INIT...')
            self.iot = IoT(IOT_ENDPOINT,
                  ROOT_CA,
                  CERT_KEY,
                  PRIVATE_KEY,
                  THING_NAME)
            self.iot.shadow_handler(THING_NAME)
        except Exception as e:
           logger.exception(e)

    def thing_shadow_init(self):
        try:
            logger.debug('ACTIVE MODE INIT...')
            self.mode_publisher = rospy.Publisher('ev3/active_mode', String, queue_size=10, tcp_nodelay=True, latch=False)
            thread = Thread(target=self.thing_shadow_thread)
            thread.daemon = True
            thread.start()
        except Exception as e:
           logger.exception(e)

    def thing_shadow_thread(self):
        logger.debug('Thing Shadow thread started')
        while True:
            try:
                global active_mode
                self.iot.shadow_get(self.shadow_callback_get)

                thing_shadow = self.shadow_event.get('state').get('desired')

                if thing_shadow:
                    logger.debug(thing_shadow)
                    active_mode = thing_shadow.get('active_mode')
                    self.mode_publisher.publish(active_mode)

                    # Update shadow to reflect reported state
                    shadow_payload = json.dumps({"state":{"reported": {'active_mode': active_mode}, 'desired': None}})
                    self.iot.shadow_update(shadow_payload, self.shadow_callback_update)
                    sleep(1)
                    self.iot.shadow_get(self.shadow_callback_get)
                    logger.debug(self.shadow_event.get('state'))

                else:
                    active_mode = self.shadow_event.get('state').get('reported').get('active_mode')
                sleep(1)
            except Exception as e:
                logger.exception('Thing Shadow Thread error: {}'.format(e))
                sleep(5)

    def shadow_callback_get(self, payload, responseStatus, token):
        try:
            self.shadow_event = json.loads(payload)
        except Exception as e:
           logger.exception(e)

    def shadow_callback_update(self, payload, responseStatus, token):
        try:
            if responseStatus == "timeout":
                logger.debug("Update request " + token + " time out!")
            if responseStatus == "accepted":
                payloadDict = json.loads(payload)
                logger.debug("~~~~~~~~~~~~~~~~~~~~~~~")
                logger.debug("Update request with token: " + token + " accepted!")
                logger.debug("active_mode: " + payloadDict["state"]["reported"]["active_mode"])
                logger.debug("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
            if responseStatus == "rejected":
                logger.debug("Update request " + token + " rejected!")
        except Exception as e:
           logger.exception(e)

    def joystick_init(self):
        try:
            logger.debug('JOYSTICK INIT...')
            self.twist = Twist()
            thread = Thread(target=self.joystick_thread)
            thread.daemon = True
            thread.start()
            self.joystick_publisher = rospy.Publisher('ev3/cmd_vel', Twist, queue_size=1)
        except Exception as e:
           logger.exception(e)

    def joystick_thread(self):
        try:
            logger.debug('Joystick thread started')
            rospy.Subscriber('joy', Joy, self.joystick_callback)
        except Exception as e:
           logger.exception(e)

    def joystick_callback(self, data):
        try:
            global active_mode
            if active_mode == 'joystick':
                # button_a = data.buttons[0]
                # button_b = data.buttons[1]
                # button_x = data.buttons[2]
                # button_y = data.buttons[3]
                dpad_x = data.axes[6]
                dpad_y = data.axes[7]
                speed = 0.5
                if abs(dpad_y) == 1:
                    print('DPAD_X: {}, DPAD_Y: {}'.format(dpad_x, dpad_y))
                    if dpad_y == 1:
                        self.move(speed, 0, 0)
                    else:
                        self.move(-speed, 0, 0)
                if abs(dpad_x) == 1:
                    print('DPAD_X: {}, DPAD_Y: {}'.format(dpad_x, dpad_y))
                    if dpad_x == 1:
                        self.move(0, 100, 0)
                        print('left')
                    else:
                        self.move(0, -100, 0)
                        print('right')
                elif abs(dpad_y) == 0 and abs(dpad_x) == 0:
                    print('stop')
                    self.move(0, 0, 0)
        except Exception as e:
           logger.exception(e)

    def move(self, x, z, d):
        try:
            self.twist.linear.x = x
            self.twist.angular.z = z
            self.joystick_publisher.publish(self.twist)
        except Exception as e:
           logger.exception(e)

if __name__ == '__main__':
   try:
        model_path = sys.argv[1]
        logger.debug('Starting Inference Worker, Specified Model Directory: {}'.format(model_path))
        x = 0.2
        ev3dev = EV3DEV()
        rospy.init_node('rl_coach', anonymous=True)
        rate = rospy.Rate(1)
        inference_worker = InferenceWorker(model_path)
        inference_worker.run()
        rospy.spin()
   except Exception as e:
       logger.exception(e)

#!/usr/bin/env python

import argparse
import base64
import csv
import json
import logging
import os
import sys
import tempfile
import time
import uuid

import cv2
import numpy as np
import olympe
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from AWSIoTPythonSDK.core.greengrass.discovery.providers import DiscoveryInfoProvider
from AWSIoTPythonSDK.core.protocol.connection.cores import ProgressiveBackOffCore
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryInvalidRequestException
from olympe.messages import gimbal
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, PCMD
from olympe.messages.ardrone3.PilotingSettings import MaxTilt, MaxAltitude
from olympe.messages.ardrone3.PilotingSettingsState import MaxTiltChanged, MaxAltitudeChanged
from olympe.messages.ardrone3.PilotingState import AltitudeChanged, AttitudeChanged, FlyingStateChanged, \
    AlertStateChanged, MotionState, WindStateChanged, VibrationLevelChanged, SpeedChanged
from olympe.messages.ardrone3.SpeedSettings import MaxVerticalSpeed, MaxRotationSpeed
from olympe.messages.ardrone3.SpeedSettingsState import MaxRotationSpeedChanged, MaxVerticalSpeedChanged

AllowedActions = ['both', 'publish', 'subscribe']

CarModels = {
    'ferrari-red': 0,
    'lamborghini-white': 1,
    'porsche-yellow': 2,
    'lamborghini-orange': 3
}

MAX_DISCOVERY_RETRIES = 10
GROUP_CA_PATH = "./groupCA/"


# General message notification callback
def customOnMessage(message):
    print('Received message on topic %s: %s\n' % (message.topic, message.payload))


# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")


def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")


# Custom Shadow callback
def customShadowCallback_Delta(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    print(responseStatus)
    payloadDict = json.loads(payload)
    print("++++++++DELTA++++++++++")
    print("state: " + str(payloadDict["state"]))
    print("version: " + str(payloadDict["version"]))
    print("+++++++++++++++++++++++\n\n")

    if 'gimbal_pitch' in payloadDict['state'].keys():
        droneThing.drone(gimbal.set_target(
            gimbal_id=0,
            control_mode="position",
            yaw_frame_of_reference="none",  # None instead of absolute
            yaw=0.0,
            pitch_frame_of_reference="absolute",
            pitch=payloadDict['state']['gimbal_pitch'],
            roll_frame_of_reference="none",  # None instead of absolute
            roll=0.0,
        )).wait()

        print('updated gimbal_pitch')

    if 'gimbal_speed' in payloadDict['state'].keys():
        droneThing.drone(gimbal.set_max_speed(
            gimbal_id=0,
            yaw=0.0,
            pitch=payloadDict['state']['gimbal_speed'],
            roll=0.0,
        )).wait()

        print('updated gimbal_speed')

    if 'max_vertical_speed' in payloadDict['state'].keys():
        droneThing.drone(MaxVerticalSpeed(payloadDict['state']['max_vertical_speed'])).wait()

        print('updated max_vertical_speed')

    if 'max_rotation_speed' in payloadDict['state'].keys():
        droneThing.drone(MaxRotationSpeed(payloadDict['state']['max_rotation_speed'])).wait()

        print('updated max_rotation_speed')

    if 'max_tilt' in payloadDict['state'].keys():
        droneThing.drone(MaxTilt(payloadDict['state']['max_tilt'])).wait()

        print('updated max_tilt')

    if 'flight_altitude' in payloadDict['state'].keys():
        droneThing.flight_altitude = payloadDict['state']['flight_altitude']

        print('updated flight_altitude')

    if 'detection_enabled' in payloadDict['state'].keys():
        droneThing.detection_enabled = payloadDict['state']['detection_enabled']

        print('updated detection_enabled')

    if 'detection_mode' in payloadDict['state'].keys():
        droneThing.detection_mode = payloadDict['state']['detection_mode']

        print('updated detection_mode')

    if 'targeted_car' in payloadDict['state'].keys():
        droneThing.targeted_car = payloadDict['state']['targeted_car']

        print('updated targeted_car')


class DroneThing:
    frameCount = 0
    yaw_status = 0

    def __init__(self):
        # Create the olympe.Drone object from its IP address
        self.drone = olympe.Drone(
            "192.168.42.1",
            loglevel=0,
        )
        self.state = {}
        # default settings
        self.gimbal_pitch = -90.0
        self.max_altitude = 3.0
        self.flight_altitude = 2.0
        self.detection_enabled = False
        self.detection_mode = 'cars'
        self.targeted_car = 'porsche-yellow'

        self.tempd = tempfile.mkdtemp(prefix="olympe_streaming_test_")
        print("Olympe streaming example output dir: {}".format(self.tempd))
        self.h264_frame_stats = []
        self.h264_stats_file = open(
            os.path.join(self.tempd, 'h264_stats.csv'), 'w+')
        self.h264_stats_writer = csv.DictWriter(
            self.h264_stats_file, ['fps', 'bitrate'])
        self.h264_stats_writer.writeheader()

    def start(self):
        print('<< start() >>')
        # Connect the the drone
        self.drone.connection()

        # Setup your callback functions to do some live video processing
        self.drone.set_streaming_callbacks(
            raw_cb=self.yuv_frame_cb,
            h264_cb=self.h264_frame_cb
        )

        self.drone(MaxAltitude(self.max_altitude)).wait()

        self.drone(gimbal.set_target(
            gimbal_id=0,
            control_mode="position",
            yaw_frame_of_reference="none",  # None instead of absolute
            yaw=0.0,
            pitch_frame_of_reference="absolute",
            pitch=self.gimbal_pitch,
            roll_frame_of_reference="none",  # None instead of absolute
            roll=0.0
        )).wait()

    def stop(self):
        print('<< stop() >>')
        # Properly stop the video stream and disconnect
        self.drone.stop_video_streaming()
        self.drone.disconnection()
        self.h264_stats_file.close()

    def yuv_frame_cb(self, yuv_frame):
        """
        This function will be called by Olympe for each decoded YUV frame.

            :type yuv_frame: olympe.VideoFrame
        """

        # 30 / LIMIT = FPS that will be processed
        LIMIT = 8

        if self.frameCount < LIMIT:
            self.frameCount = self.frameCount + 1
        elif self.frameCount == LIMIT or self.frameCount > LIMIT:
            self.frameCount = 0

            # the VideoFrame.info() dictionary contains some useful informations
            # such as the video resolution
            info = yuv_frame.info()
            height, width = info["yuv"]["height"], info["yuv"]["width"]
            print(str(width) + " x " + str(height))

            # convert pdraw YUV flag to OpenCV YUV flag
            cv2_cvt_color_flag = {
                olympe.PDRAW_YUV_FORMAT_I420: cv2.COLOR_YUV2BGR_I420,
                olympe.PDRAW_YUV_FORMAT_NV12: cv2.COLOR_YUV2BGR_NV12,
            }[info["yuv"]["format"]]

            # yuv_frame.as_ndarray() is a 2D numpy array with the proper "shape"
            # i.e (3 * height / 2, width) because it's a YUV I420 or NV12 frame

            # Use OpenCV to convert the yuv frame to RGB
            cv2frame = cv2.cvtColor(yuv_frame.as_ndarray(), cv2_cvt_color_flag)

            payload = {
                'b64': self.frameToBase64String(cv2frame, 0.3),
                'timestamp': time.time(),
                'mode': self.detection_mode,
                'target': CarModels[self.targeted_car]
            }

            ui_payload = {
                'b64': self.frameToBase64String(cv2frame, 0.3)
            }

            if self.detection_enabled == True:

                myAWSIoTMQTTShadowClient.getMQTTConnection().publish('detect-cars/{}/infer/input'.format(topic),
                                                                     json.dumps(payload), 0)

            else:

                myAWSIoTMQTTShadowClient.getMQTTConnection().publish('{}/frames'.format(topic), json.dumps(ui_payload),
                                                                     0)

        # # Use OpenCV to show this frame
        # cv2.imshow("Olympe Streaming Example", new_frame)
        # cv2.waitKey(1)  # please OpenCV for 1 ms...

    def frameToBase64String(self, cv2frame, resizeRatio):

        # resize to 50%, and then convert to bytearray
        cv2frame_small = cv2.resize(cv2frame, None, fx=resizeRatio, fy=resizeRatio)
        retval, buffer = cv2.imencode('.jpg', cv2frame_small)
        jpg_bytes = base64.b64encode(buffer).decode()

        return jpg_bytes

    def h264_frame_cb(self, h264_frame):
        """
        This function will be called by Olympe for each new h264 frame.

            :type yuv_frame: olympe.VideoFrame
        """

    def mission(self):
        print('<< mission() >>')
        self.drone(
            TakeOff()
            >> FlyingStateChanged("hovering", _timeout=5)
        ).wait()

        # # up/down
        # self.drone(moveBy(0,0,-1.0,0) >> FlyingStateChanged("hovering", _timeout=5)).wait()
        # self.drone(moveBy(0,0,1.0,0) >> FlyingStateChanged("hovering", _timeout=5)).wait()

        # # forward/backward
        # self.drone(moveBy(-1.0,0,0,0) >> FlyingStateChanged("hovering", _timeout=5)).wait()
        # self.drone(moveBy(1.0,0,0,0) >> FlyingStateChanged("hovering", _timeout=5)).wait()

        # # left/right
        # self.drone(moveBy(0,-1.0,0,0) >> FlyingStateChanged("hovering", _timeout=5)).wait()
        # self.drone(moveBy(0,1.0,0,0) >> FlyingStateChanged("hovering", _timeout=5)).wait()

        self.drone(Landing()).wait()

    def land(self):
        print('<< land() >>')
        self.drone(Landing()).wait()

    def takeOff(self):
        print('<< takeOff() >>')
        self.drone(
            TakeOff()
            >> FlyingStateChanged("hovering", _timeout=5)
        ).wait()

        self.drone(
            moveBy(0, 0, (1.0 - self.flight_altitude), 0)
            >> FlyingStateChanged("hovering", _timeout=5)
        ).wait()

    def startStreaming(self):
        print('<< startStreaming() >>')

        # Start video streaming
        self.drone.start_video_streaming()

    def stopStreaming(self):
        print('<< stopStreaming() >>')

        # Stop video streaming
        self.drone.stop_video_streaming()

    def notSupportedHandler(self):
        print('<< notSupportedHandler() >>')

    def predictionCallback(self, client, userdata, message):
        print('<< predictionCallback() >>')

        # convert from bytearray back to image

        keyName = 'b64'

        data = json.loads(message.payload.decode())
        bytes_jpg = bytes(data[keyName].encode())
        new_buffer = base64.b64decode(bytes_jpg)
        new_frame = cv2.imdecode(np.fromstring(new_buffer, dtype=np.uint8), -1)

        # Use OpenCV to show this frame
        cv2.imshow("Olympe Streaming via callback", new_frame)
        cv2.waitKey(1)  # please OpenCV for 1 ms...

        if self.detection_enabled == True:

            data = json.loads(message.payload.decode())

            yaw = 0
            gaz = 0
            roll = 0
            pitch = 0

            if self.detection_mode == 'cars' and data['dX'] == 'HOLD' and data['dY'] == 'HOLD':
                return

            elif self.detection_mode == 'drones' and data['dX'] == 'HOLD' and data['dY'] == 'HOLD' and data[
                'dZ'] == 'HOLD':
                return

            if data['dX'] == 'FORWARD':
                pitch = int(data['mX'])
            elif data['dX'] == 'BACKWARD':
                pitch = int(-1 * data['mX'])

            if data['dY'] == 'LEFT':
                roll = int(-1 * data['mY'])
            elif data['dY'] == 'RIGHT':
                roll = int(data['mY'])

            if data['dZ'] == 'UP':
                gaz = int(data['mZ'])
            elif data['dZ'] == 'DOWN':
                gaz = int(-1 * data['mZ'])

            for i in range(0, 2):
                print('pcmd - {}({}), {}({}), {}({})'.format(data['dX'], data['mX'], data['dY'], data['mY'], data['dZ'],
                                                             data['mZ']))
                self.drone(PCMD(1, roll, pitch, yaw, gaz, int(time.time())))

    # frame callback
    def frameCallback(self, client, userdata, message):
        print('<< frameCallback() >>')
        # convert from bytearray back to image

        keyName = 'b64'

        data = json.loads(message.payload.decode())
        bytes_jpg = bytes(data[keyName].encode())
        new_buffer = base64.b64decode(bytes_jpg)
        new_frame = cv2.imdecode(np.fromstring(new_buffer, dtype=np.uint8), -1)

        # Use OpenCV to show this frame
        cv2.imshow("Olympe Streaming via callback", new_frame)
        cv2.waitKey(1)  # please OpenCV for 1 ms...

    def commandCallback(self, client, userdata, message):
        print('<< commandCallback() >>')
        data = json.loads(message.payload.decode())

        operations = {
            'take-off': self.takeOff,
            'land': self.land,
            'start-streaming': self.startStreaming,
            'stop-streaming': self.stopStreaming,
            'connect': self.start,
            'disconnect': self.stop,
            'mission': self.mission
        }

        # Get the function from switcher dictionary
        func = operations.get(data['command'])

        if func is None:
            data['success'] = False
            data['exception'] = 'Command is not supported.'

            myAWSIoTMQTTShadowClient.getMQTTConnection().publish('commands/{}/ack'.format(topic), json.dumps(data), 0)

        try:
            # Execute the function
            func()

            data['success'] = True

            myAWSIoTMQTTShadowClient.getMQTTConnection().publish('commands/{}/ack'.format(topic), json.dumps(data), 0)

        except Exception as e:

            data['success'] = False
            data['exception'] = e

            myAWSIoTMQTTShadowClient.getMQTTConnection().publish('commands/{}/ack'.format(topic), json.dumps(data), 0)

    # get telemetry of interest
    def getDroneState(self):

        motionState = None

        try:
            motionState = str(self.drone.get_state(MotionState)['state']).split('.')[1]
        except:
            ''' motionState is not initialized yet '''

        updateShadow = False

        currentState = {
            'max_tilt': self.drone.get_state(MaxTiltChanged)['current'],
            'flying_state': str(self.drone.get_state(FlyingStateChanged)['state']).split('.')[1],
            'alert_state': str(self.drone.get_state(AlertStateChanged)['state']).split('.')[1],
            'motion_state': motionState,
            'wind_state': str(self.drone.get_state(WindStateChanged)['state']).split('.')[1],
            'vibration_level': str(self.drone.get_state(VibrationLevelChanged)['state']).split('.')[1],
            'max_alt': self.drone.get_state(MaxAltitudeChanged)['current'],
            'max_vertical_speed': self.drone.get_state(MaxVerticalSpeedChanged)['current'],
            'max_rotation_speed': self.drone.get_state(MaxRotationSpeedChanged)['current'],
            'gimbal_pitch': self.drone.get_state(gimbal.attitude)['pitch_absolute'],
            'gimbal_speed': self.drone.get_state(gimbal.max_speed)['current_pitch'],
            'flight_altitude': self.flight_altitude,
            'detection_enabled': self.detection_enabled,
            'detection_mode': self.detection_mode,
            'targeted_car': self.targeted_car
        }

        if currentState != self.state:
            updateShadow = True

        self.state = currentState

        return updateShadow, self.state

    # get telemetry of interest
    def getDroneTelemetry(self):

        drone_attitude = self.drone.get_state(AttitudeChanged)
        drone_speed = self.drone.get_state(SpeedChanged)

        telemetry = {
            # 'air_speed': self.drone.get_state(AirSpeedChanged)['airSpeed'],
            'altitude': self.drone.get_state(AltitudeChanged)['altitude'],
            'speedX': drone_speed['speedX'],
            'speedY': drone_speed['speedY'],
            'speedZ': drone_speed['speedZ'],
            'pitch': drone_attitude['pitch'],
            'roll': drone_attitude['roll'],
            'yaw': drone_attitude['yaw']
        }

        return telemetry

    # Read in command-line parameters


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s" % str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
clientId = args.clientId
topic = args.topic
thingName = clientId

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if not args.certificatePath or not args.privateKeyPath:
    parser.error("Missing credentials for authentication, you must specify --cert and --key args.")
    exit(2)

if not os.path.isfile(rootCAPath):
    parser.error("Root CA path does not exist {}".format(rootCAPath))
    exit(3)

if not os.path.isfile(certificatePath):
    parser.error("No certificate found at {}".format(certificatePath))
    exit(3)

if not os.path.isfile(privateKeyPath):
    parser.error("No private key found at {}".format(privateKeyPath))
    exit(3)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.ERROR)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Progressive back off core
backOffCore = ProgressiveBackOffCore()

# Discover GGCs
discoveryInfoProvider = DiscoveryInfoProvider()
discoveryInfoProvider.configureEndpoint(host)
discoveryInfoProvider.configureCredentials(rootCAPath, certificatePath, privateKeyPath)
discoveryInfoProvider.configureTimeout(10)  # 10 sec

retryCount = MAX_DISCOVERY_RETRIES
discovered = False
groupCA = None
coreInfo = None
while retryCount != 0:
    try:
        discoveryInfo = discoveryInfoProvider.discover(thingName)
        caList = discoveryInfo.getAllCas()
        coreList = discoveryInfo.getAllCores()

        # We only pick the first ca and core info
        groupId, ca = caList[0]
        coreInfo = coreList[0]
        print("Discovered GGC: %s from Group: %s" % (coreInfo.coreThingArn, groupId))

        print("Now we persist the connectivity/identity information...")
        groupCA = GROUP_CA_PATH + groupId + "_CA_" + str(uuid.uuid4()) + ".crt"
        if not os.path.exists(GROUP_CA_PATH):
            os.makedirs(GROUP_CA_PATH)
        groupCAFile = open(groupCA, "w")
        groupCAFile.write(ca)
        groupCAFile.close()

        discovered = True
        print("Now proceed to the connecting flow...")
        break
    except DiscoveryInvalidRequestException as e:
        print("Invalid discovery request detected!")
        print("Type: %s" % str(type(e)))
        print("Error message: %s" % e.message)
        print("Stopping...")
        break
    except BaseException as e:
        print("Error in discovery!")
        print("Type: %s" % str(type(e)))
        print("Error message: %s" % e.message)
        retryCount -= 1
        print("\n%d/%d retries left\n" % (retryCount, MAX_DISCOVERY_RETRIES))
        print("Backing off...\n")
        backOffCore.backOff()

if not discovered:
    print("Discovery failed after %d retries. Exiting...\n" % (MAX_DISCOVERY_RETRIES))
    sys.exit(-1)

# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
myAWSIoTMQTTShadowClient.configureCredentials(groupCA, privateKeyPath, certificatePath)
# myAWSIoTMQTTShadowClient.getMQTTConnection().onMessage = customOnMessage

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTShadowClient.getMQTTConnection().configureOfflinePublishQueueing(5)  # Infinite offline Publish queueing
myAWSIoTMQTTShadowClient.getMQTTConnection().configureDrainingFrequency(2)  # Draining: 2 Hz

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(topic, True)

# Delete shadow JSON doc
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)

# Iterate through all connection options for the core and use the first successful one
connected = False
for connectivityInfo in coreInfo.connectivityInfoList:
    currentHost = connectivityInfo.host
    currentPort = connectivityInfo.port
    print("Trying to connect to core at %s:%d" % (currentHost, currentPort))
    myAWSIoTMQTTShadowClient.configureEndpoint(currentHost, currentPort)
    try:
        myAWSIoTMQTTShadowClient.connect()
        connected = True
        break
    except BaseException as e:
        print("Error in connect!")
        print("Type: %s" % str(type(e)))
        print("Error message: %s" % e.message)

if not connected:
    print("Cannot connect to core %s. Exiting..." % coreInfo.coreThingArn)
    sys.exit(-2)

# DroneThing
droneThing = DroneThing()

# Connect and subscribe to AWS IoT
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTShadowClient.getMQTTConnection().subscribe('commands/{}'.format(topic), 1, droneThing.commandCallback)
    myAWSIoTMQTTShadowClient.getMQTTConnection().subscribe('detect-cars/{}/infer/output'.format(topic), 1,
                                                           droneThing.predictionCallback)
    # myAWSIoTMQTTShadowClient.getMQTTConnection().subscribe('detect-cars/{}/infer/output'.format(topic), 1, droneThing.frameCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    if args.mode == 'both' or args.mode == 'publish':
        message = {}
        message['message'] = args.message
        message['sequence'] = loopCount

        try:
            messageJson = json.dumps(droneThing.getDroneTelemetry())
            myAWSIoTMQTTShadowClient.getMQTTConnection().publish("telemetry/{}".format(topic), messageJson, 0)
            if args.mode == 'publish':
                print('Published topic %s: %s\n' % (topic, messageJson))
        except Exception as e:
            print(e)
            print('Drone is not initialized - telemetry is unavailable')

        try:

            updateShadow, currentState = droneThing.getDroneState()

            if updateShadow:
                statePayload = {
                    'state': {
                        'reported': currentState
                    }
                }

                deviceShadowHandler.shadowUpdate(json.dumps(statePayload), customShadowCallback_Update, 5)

        except Exception as e:
            print(e)
            print('Drone is not initialized - state is unavailable')

        loopCount += 1
    time.sleep(1)

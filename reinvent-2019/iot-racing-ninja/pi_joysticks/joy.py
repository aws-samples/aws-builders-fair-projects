import asyncio
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from evdev import InputDevice, list_devices, categorize, ecodes
import json
import logging
import os
import RPi.GPIO as GPIO

ABS_RIGHT = 255
ABS_UP = 0
ABS_DOWN = 0
ABS_LEFT = 0
ABS_X = 0
ABS_Y = 1
KEY_JOYSTICK = 'BTN_JOYSTICK'
KEY_BTNA = 'BTN_A'
KEY_THUMB = 'BTN_THUMB'
KEY_TL2 = 'BTN_TL2'
MOVE_RIGHT = 'right'
MOVE_LEFT = 'left'
MOVE_FORWARD = 'forward'
DOWN = 1
UP = 0
JOYSTICKNAMES = ['Microntek              USB Joystick          ',
    'Sony PLAYSTATION(R)3 Controller']
JOYSTICKSBYINPUT = ['red','blue','white','black']
ENDPOINT = 'a24t36khlmixhw-ats.iot.us-east-1.amazonaws.com'
ROOT = '/home/pi/root/AmazonRootCA1.pem'
CERT_LOCATION = '/home/pi/certs/'
PRIVATE = '-private.pem.key'
CERTIFICATE = '-certificate.pem.crt'
LIGHTS = [{'red':{'pin':9, 'on': False}, 'yellow':{'pin':10, 'on':False},
    'green':{'pin':11, 'on': False}},{'red':{'pin':20, 'on': False},
    'yellow':{'pin':21, 'on':False}, 'green':{'pin':16, 'on': False}}]
PINS = [9, 10, 11, 21, 20 ,16]
RED = 'red'
YELLOW = 'yellow'
GREEN = 'green'
READY_FOR_MOVES = 1
MOVE_LOCKED = 2
MOVE_BAD = 3
MOVE_GOOD = 4
ALL_OFF = 5
LOG_FILENAME = '/home/pi/joystick.log'

joysticks = []

async def handle_event(device, myMQTTClient):
    async for event in device.async_read_loop():
        for num, joystick in enumerate(joysticks):
            if joystick['device']==device:
                jsindex = num
        categorized = categorize(event)
        if event.type == ecodes.EV_KEY:
            logging.debug(f'button push {joysticks[jsindex]["color"]} {joysticks[jsindex]["path"]}: {categorized.keycode}, {categorized.keystate}')
            logging.info(f'move {joysticks[jsindex]["move"]} locked {joysticks[jsindex]["movelocked"]}')
            if (categorized.keycode[0] == KEY_JOYSTICK or categorized.keycode[0]
                == KEY_BTNA) and categorized.keystate == 1 and not (
                joysticks[jsindex]['move'] == '') and not (
                joysticks[jsindex]['movelocked'] == True):
                #submit move if there is one
                logging.debug(f'move submitted for {joysticks[jsindex]["color"]}, {joysticks[jsindex]["device"]}:{joysticks[jsindex]["move"]}')
                joysticks[jsindex]['movelocked']=True
                message = {}
                message['joystick']=joysticks[jsindex]['color']
                message['move']=joysticks[jsindex]['move']
                jsonmsg = json.dumps(message)
                topic = joysticks[jsindex]['movetopic']
                myMQTTClient.publish(topic, jsonmsg, 0)
                logging.info(f'posted move {jsonmsg}')
                await setLightStatus(jsindex, MOVE_LOCKED)
            elif (categorized.keycode==KEY_THUMB or categorized.keycode==KEY_TL2
                ) and categorized.keystate==1:
                #for debugging, clear move
                joysticks[jsindex]['move'] = ''
                joysticks[jsindex]['movelocked']=False
                await setLightStatus(jsindex, READY_FOR_MOVES)
                logging.info(f'{joysticks[jsindex]["color"]} {joysticks[jsindex]["path"]} unlocked')
                logging.info(f'{joysticks}')
        elif event.type == ecodes.EV_ABS and joysticks[jsindex]['movelocked']==False and (
            event.value == ABS_LEFT or event.value==ABS_RIGHT):
            logging.debug(f'joystick move {joysticks[jsindex]["move"]} {joysticks[jsindex]["path"]} value: {event.value} {event}')
            if event.code == ABS_X:
                if event.value == ABS_RIGHT:
                    joysticks[jsindex]['move'] = MOVE_RIGHT
                    logging.info(f'{joysticks[jsindex]["color"]} {joysticks[jsindex]["path"]} right')
                elif event.value == ABS_LEFT:
                    joysticks[jsindex]['move'] = MOVE_LEFT
                    logging.info(f'{joysticks[jsindex]["color"]} {joysticks[jsindex]["path"]} left')
            elif event.code == ABS_Y:
                if event.value == ABS_UP:
                    joysticks[jsindex]['move'] = MOVE_FORWARD
                    logging.info(f'{joysticks[jsindex]["color"]} {joysticks[jsindex]["path"]} forward')

async def setLightStatus(player, state):
    GPIO.output(joysticks[player]['lights'][RED]['pin'], False)
    GPIO.output(joysticks[player]['lights'][YELLOW]['pin'], False)
    GPIO.output(joysticks[player]['lights'][GREEN]['pin'], False)
    if state == READY_FOR_MOVES:
        GPIO.output(joysticks[player]['lights'][GREEN]['pin'], True)
    elif state == MOVE_LOCKED:
        GPIO.output(joysticks[player]['lights'][YELLOW]['pin'], True)
    elif state == MOVE_GOOD:
        GPIO.output(joysticks[player]['lights'][GREEN]['pin'], True)
    elif state == MOVE_BAD:
        GPIO.output(joysticks[player]['lights'][RED]['pin'], True)
        await asyncio.sleep(3)
    return

def statusCallback(client, userdata, message):
    """Callback for game/status"""
    msg = json.loads(message.payload.decode('utf-8').replace("'",'"'))
    logging.info(msg['status'])
    if msg['status']=='running':
        #show the timer
        logging.info('Timer {}'.format(msg['timer']))
    elif msg['status']=='over':
        #lock all possible moves
        for i, joystick in enumerate(joysticks):
            joystick['movelocked'] = True
            asyncio.run(setLightStatus(i, MOVE_LOCKED))
    elif msg['status']=='ready':
        #unlock all controllers
        for i, joystick in enumerate(joysticks):
            joystick['movelocked'] = False
            asyncio.run(setLightStatus(i, READY_FOR_MOVES))

def joystickCallback(client, userdata, message):
    """Callback for joystick/#/#"""
    msg = json.loads(message.payload.decode('utf-8').replace("'",'"'))
    logging.info(msg)
    try:
        for i, joystick in enumerate(joysticks):
            if joystick['color'] == msg['joystick']:
                logging.info(f'{joystick["color"]} unlocked due to {msg["reason"]}')
                joystick['movelocked']=False
                if msg['reason']=='Invalid Move':
                    asyncio.run(setLightStatus(i, MOVE_BAD))
                joystick['move'] = ''
                asyncio.run(setLightStatus(i, READY_FOR_MOVES))
    except ValueError:
        #unknown message, not matching topic
        logging.info(f'cannot figure out why {msg} was sent on {message.topic}')

def commandCallback(client, userdata, message):
    """Callback for commands on commands/"""
    msg = json.loads(message.payload.decode('utf-8').replace("'",'"'))
    if msg['command']=='reset':
        logging.info('reset message received')

def main(myMQTTClient):
    logging.info('Hit Main')
    myMQTTClient.subscribe("game/status", 1, statusCallback)
    myMQTTClient.subscribe("commands", 1, commandCallback)
    #subscribe only to the topics matching joysticks registered
    for joystick in joysticks:
        logging.debug(f'{joystick}')
        myMQTTClient.subscribe(joystick["statustopic"],1, joystickCallback)
        asyncio.ensure_future(handle_event(joystick['device'], myMQTTClient))
    loop = asyncio.get_event_loop()
    loop.run_forever()
    return 'done'

def setupMQTT():
    """setup AWS IoT Connection - this is going to broadcast all joystick devices
    from one.  However, you can use multiple devices to broadcast these topics
    by using a different set of certs and a different USB port on each device"""
    hostname = os.uname()[1]
    myMQTTClient = AWSIoTMQTTClient(hostname)
    myMQTTClient.configureEndpoint(ENDPOINT, 8883)
    myMQTTClient.configureCredentials(ROOT, CERT_LOCATION + hostname + PRIVATE, CERT_LOCATION + hostname + CERTIFICATE)
    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)
    myMQTTClient.configureConnectDisconnectTimeout(10)
    myMQTTClient.configureMQTTOperationTimeout(5)
    logging.info('Done configuring MQTT Connection')
    return myMQTTClient

def setupGPIO():
    """Standard GPIO work"""
    GPIO.setmode(GPIO.BCM)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

def setupJoysticks():
    """Search for joysticks"""
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        try:
            index = JOYSTICKNAMES.index(device.name)
            #this is a known joystick, add it to the array
            #index will throw a ValueError if not found
            logging.debug(f'adding {device}')
            joystick = {}
            joystick['device'] = device
            joystick['path'] = device.path
            #force joystick color by USB port
            if device.phys.find('usb-1.3')>0:
                #top right, red
                index = 0
            elif device.phys.find('usb-1.2')>0:
                #bottom right, blue
                index = 1
            elif device.phys.find('usb-1.1.2')>0:
                #top left, white
                index = 2
            elif device.phys.find('usb-1.1.3')>0:
                #bottom left, black
                index = 3
            joystick['color'] = JOYSTICKSBYINPUT[index]
            joystick['move'] = ''
            joystick['movelocked'] = False
            joystick['movetopic'] = 'joystick/move/' + JOYSTICKSBYINPUT[index]
            joystick['statustopic'] = 'joystick/status/' + JOYSTICKSBYINPUT[index]
            joystick['lights'] = LIGHTS[len(joysticks)]
            joysticks.append(joystick)
            logging.info(f'{joysticks}')
            logging.info(f'{joysticks[len(joysticks)-1]} joystick added')
        except ValueError:
                logging.debug(f'not adding {device.path} : {device.name}')
    logging.info(f'Joysticks found: {joysticks}')

if __name__ == '__main__':
    #logging.basicConfig(filename=LOG_FILENAME, level=logging.NOTSET, format='%(asctime)s - %(levelname)s -%(message)s')
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(levelname)s -%(message)s')
    myMQTTClient = setupMQTT()
    setupGPIO()
    setupJoysticks()
    try:
        logging.info('start of try')
        myMQTTClient.connect()
        logging.info('connected')
        main(myMQTTClient)
    finally:
        myMQTTClient.disconnect()
        GPIO.cleanup()

import json
import datetime
import time
import signal
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from sensors import SoilSensor, UVSensor, DHT22Sensor
from actuators import GrowLight, Pump
import configparser

# read configuration file
config = configparser.ConfigParser()
config.read("config.ini")
endpoint = config["default"]["endpoint"]
port = int(config["default"]["port"])
offlinePublishQueueing = int(config["default"]["offlinePublishQueueing"])
drainingFrequency = int(config["default"]["drainingFrequency"])
connectDisconnectTimeout = int(config["default"]["connectDisconnectTimeout"])
MQTTOperationTimeout = int(config["default"]["MQTTOperationTimeout"])
rootCAPath = config["security"]["rootCA"]
certificatePath = config["security"]["certificate"]
privateKeyPath = config["security"]["privateKey"]
device_id = config["default"]["deviceId"]
topic = config["default"]["topic"]

# initialize sensors and actuators
soil = SoilSensor()
uv = UVSensor()
dht22 = DHT22Sensor()
light = GrowLight()
pump0 = Pump(0)
pump1 = Pump(1)
pump2 = Pump(2)
pump3 = Pump(3)
pump4 = Pump(4)
pump5 = Pump(5)
pump6 = Pump(6)
pump7 = Pump(7)

# initialize AWS IoT MQTT client
client = AWSIoTMQTTClient(device_id)
client.configureEndpoint(endpoint, port)
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
client.configureOfflinePublishQueueing(offlinePublishQueueing)
client.configureDrainingFrequency(drainingFrequency)
client.configureConnectDisconnectTimeout(connectDisconnectTimeout)
client.configureMQTTOperationTimeout(MQTTOperationTimeout)

# initialize AWS IoT MQTT Shadow client
shadow = AWSIoTMQTTShadowClient(device_id + "-shadow")
shadow.configureEndpoint(endpoint, port)
shadow.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
shadow.configureAutoReconnectBackoffTime(1, 32, 20)
shadow.configureConnectDisconnectTimeout(connectDisconnectTimeout)
shadow.configureMQTTOperationTimeout(MQTTOperationTimeout)

def read_sensors(id, raw=False):
    s = []
    for n in range(0, 8):
        if raw:
            s.append(soil.read_raw(n))
        else:
            s.append(soil.read(n))
    u = uv.read_raw()
    d = dht22.read_raw()
    h = 0.0 if d[0] is None else d[0]
    t = 0.0 if d[1] is None else d[1]
    return {
        "id": id,
        "e": datetime.datetime.utcnow().replace(microsecond=0).isoformat(),
        "s0": "{0:.2f}".format(s[0]),
        "s1": "{0:.2f}".format(s[1]),
        "s2": "{0:.2f}".format(s[2]),
        "s3": "{0:.2f}".format(s[3]),
        "s4": "{0:.2f}".format(s[4]),
        "s5": "{0:.2f}".format(s[5]),
        "s6": "{0:.2f}".format(s[6]),
        "s7": "{0:.2f}".format(s[7]),
        "u": "{0:.2f}".format(u),
        "h": "{0:.2f}".format(h),
        "t": "{0:.2f}".format(t)
    }

def combine_readings(old, current):
    new = current
    new['o_s0'] = old["s0"]
    new['o_s1'] = old["s1"]
    new['o_s2'] = old["s2"]
    new['o_s3'] = old["s3"]
    new['o_s4'] = old["s4"]
    new['o_s5'] = old["s5"]
    new['o_s6'] = old["s6"]
    new['o_s7'] = old["s7"]
    new['o_u'] = old["u"]
    new['o_h'] = old["h"]
    new['o_t'] = old["t"]
    return new

# shadow callback
class shadowCallbackContainer:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    # shadow callback
    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # parse shadow state
        print("Received a delta message: " + payload)
        payloadDict = json.loads(payload)

        if payloadDict["state"].get("l", None) is not None:
            if payloadDict["state"]["l"]:
                light.on()
            else:
                light.off()
        if payloadDict["state"].get("p0", None) is not None:
            if payloadDict["state"]["p0"]:
                pump0.on()
            else:
                pump0.off()
        if payloadDict["state"].get("p1", None) is not None:
            if payloadDict["state"]["p1"]:
                pump1.on()
            else:
                pump1.off()
        if payloadDict["state"].get("p2", None) is not None:
            if payloadDict["state"]["p2"]:
                pump2.on()
            else:
                pump2.off()
        if payloadDict["state"].get("p3", None) is not None:
            if payloadDict["state"]["p3"]:
                pump3.on()
            else:
                pump3.off()
        if payloadDict["state"].get("p4", None) is not None:
            if payloadDict["state"]["p4"]:
                pump4.on()
            else:
                pump4.off()
        if payloadDict["state"].get("p5", None) is not None:
            if payloadDict["state"]["p5"]:
                pump5.on()
            else:
                pump5.off()
        if payloadDict["state"].get("p6", None) is not None:
            if payloadDict["state"]["p6"]:
                pump6.on()
            else:
                pump6.off()
        if payloadDict["state"].get("p7", None) is not None:
            if payloadDict["state"]["p7"]:
                pump7.on()
            else:
                pump7.off()

        # report state
        newPayload = {
            "state": {
                "reported": {
                    "l": light.status,
                    "p0": pump0.status,
                    "p1": pump1.status,
                    "p2": pump2.status,
                    "p3": pump3.status,
                    "p4": pump4.status,
                    "p5": pump5.status,
                    "p6": pump6.status,
                    "p7": pump7.status
                }
            }
        }
        self.deviceShadowInstance.shadowUpdate(json.dumps(newPayload), None, 5)

# keyboard interrupt handler
def signal_handler(sig, frame):
    client.disconnect()
    shadow.disconnect()
    sys.exit(0)

# register keyboard interrupt handler
signal.signal(signal.SIGINT, signal_handler)

# connect to AWS IoT
client.connect()
shadow.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = shadow.createShadowHandlerWithName(device_id, True)
shadowCallbackContainerListener = shadowCallbackContainer(deviceShadowHandler)

# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainerListener.customShadowCallback_Delta)

current = read_sensors(device_id)
starttime = time.time()
while True:
    # save previous readings
    old = current

    # read sensor data
    current = read_sensors(device_id)

    # combine readings
    combined = combine_readings(old, current)

    # send sensor data to AWS IoT
    client.publish(topic, json.dumps(combined), 0)

    # print sensor data
    print("Sending telemetry: " + json.dumps(combined))

    # repeat every 5 seconds
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))

client.disconnect()

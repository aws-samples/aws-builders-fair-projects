import boto3
import cv2
import greengrasssdk
import json
import logging
import mxnet as mx
import numpy as np
import requests
import sys
import tarfile
import time
from collections import namedtuple
from datetime import datetime
from picamera import PiCamera
from sense_hat import SenseHat

#########################################################################################
# Default Path to download ML Model that has been created for you to use,
# These can be commented out if you build your own model and paste that information below
ML_BUCKET_NAME = "reinvent2018-recycle-arm-us-east-1"
ML_OBJECT_NAME = "2020/ml-models/model.tar.gz"

# If you have created your own ML model using the Sagemaker notebook provided, 
# the last section will print two lines that can be pasted over the following two lines
#ML_BUCKET_NAME =  "sagemaker-us-east-1-0123456789"
#ML_OBJECT_NAME =  "smart-recycle-kit/output/<model_directory>/output/model.tar.gz"

# S3 Bucket Name to save images taken
# If a S3 Bucket is not specified below, captured images will not be copied to S3
# For example, you can use the Sagemaker Bucket you pasted from the notebook 
BUCKET_NAME = ""
#########################################################################################

# LOCAL_RESOURCE_DIR is where images taken by camera will be saved
LOCAL_RESOURCE_DIR = "/tmp"

# LOCAL_MODEL_DIR is where the ML Model has been saved
LOCAL_MODEL_DIR = "/tmp"
ML_MODEL_FILE = LOCAL_MODEL_DIR + "/" + "model.tar.gz"

# MQTT Topic to send messages to IoT Core
iot_core_topic = 'recycle/info'

#Categories that will be returned by the ML Model
CATEGORIES = ['Compost', 'Landfill', 'Recycling']


# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
gg_client = greengrasssdk.client("iot-data")

# Creating s3 client to download ML Model and to Upload images
s3 = boto3.client('s3')


B = (0, 0, 0)
G = (0, 255, 0)
Bl = (0, 0, 255)
R = (255, 0, 0)
O = (255, 103, 0)

question_mark = [
B, B, B, O, O, B, B, B,
B, B, O, B, B, O, B, B,
B, B, B, B, B, O, B, B,
B, B, B, B, O, B, B, B,
B, B, B, O, B, B, B, B,
B, B, B, O, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, B, O, B, B, B, B
]

Compost = [
B, G, G, G, G, G, G, B,
B, G, G, G, G, G, G, B,
B, G, G, B, B, B, B, B,
B, G, G, B, B, B, B, B,
B, G, G, B, B, B, B, B,
B, G, G, B, B, B, B, B,
B, G, G, G, G, G, G, B,
B, G, G, G, G, G, G, B
]

Landfill = [
B, R, R, B, B, B, B, B,
B, R, R, B, B, B, B, B,
B, R, R, B, B, B, B, B,
B, R, R, B, B, B, B, B,
B, R, R, B, B, B, B, B,
B, R, R, B, B, B, B, B,
B, R, R, R, R, R, R, B,
B, R, R, R, R, R, R, B
]

Recycling = [
B, Bl, Bl, Bl, Bl, Bl, B, B,
B, Bl, Bl, Bl, Bl, Bl, Bl, B,
B, Bl, Bl, B, B, Bl, Bl, B,
B, Bl, Bl, Bl, Bl, Bl, Bl, B,
B, Bl, Bl, Bl, Bl, Bl, B, B,
B, Bl, Bl, B, Bl, Bl, B, B,
B, Bl, Bl, B, B, Bl, Bl, B,
B, Bl, Bl, B, B, Bl, Bl, B
]


# Configure the PiCamera to take square images. Other
# resolutions will be scaled to a square when fed into
# the image-classification model which can result
# in image distortion.
camera = PiCamera(resolution=(400,400))

# Initialize SenseHat
print ("*** Initializing SenseHAT")
sense = SenseHat()



def loadModel(modelname):
        t1 = time.time()
        modelname = LOCAL_MODEL_DIR + "/" + modelname
        sym, arg_params, aux_params = mx.model.load_checkpoint(modelname, 0)
        t2 = time.time()
        t = 1000*(t2-t1)
        print("*** Loaded in {} milliseconds".format(t))
        arg_params['prob_label'] = mx.nd.array([0])
        mod = mx.mod.Module(symbol=sym)
        mod.bind(for_training=False, data_shapes=[('data', (1,3,224,224))])
        mod.set_params(arg_params, aux_params)
        return mod


def prepareNDArray(filename):
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224,))
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 1, 2)
        img = img[np.newaxis, :]
        return mx.nd.array(img)

      
def predict(filename, model, categories, n):
        array = prepareNDArray(filename)
        Batch = namedtuple('Batch', ['data'])
        t1 = time.time()
        model.forward(Batch([array]))
        t2 = time.time()
        t = 1000*(t2-t1)
        print("*** Predicted in {} millsecond".format(t))
        prob = model.get_outputs()[0].asnumpy()
        prob = np.squeeze(prob)
        sortedprobindex = np.argsort(prob)[::-1]
        topn = []
        for i in sortedprobindex[0:n]:
                topn.append([prob[i], categories[i]])
        return topn


def init(modelname):
        s3.download_file(ML_BUCKET_NAME, ML_OBJECT_NAME, ML_MODEL_FILE)
        tar_file = tarfile.open(ML_MODEL_FILE)
        tar_file.extractall(LOCAL_MODEL_DIR)
        
        model = loadModel(modelname)
        cats = ['Compost', 'Landfill', 'Recycling']
        return model, cats


def capture_and_save_image_as(filename):
    camera.capture(filename, format='jpeg')


def create_image_filename():
    current_time_millis = int(time.time() * 1000)
    filename = LOCAL_RESOURCE_DIR + "/" + str(current_time_millis) + ".jpg"
    return filename


def push_to_s3(filename, folder, classify):
    try:
        
        img = open(filename, 'rb')
        now = datetime.now()

        key = str(folder) + "/{}-{}-{}-{}.jpg".format(
                                                now.year, now.month, now.day,
                                                classify)

        response = s3.put_object(ACL='private',
                                 Body=img,
                                 Bucket=BUCKET_NAME,
                                 Key=key,
                                 ContentType= 'image/jpg')

        print ('*** Image copied to S3: {}/{}'.format(BUCKET_NAME, key))

        gg_client.publish(topic=iot_core_topic, payload=json.dumps({'message': 'Image sent to S3: {}/{}'.format(BUCKET_NAME, key)}))
        
        return key
        
    except Exception as e:
        msg = "Pushing to S3 failed: " + str(e)
        print (msg)



# Initialize The Image Classification MXNET model
ic,c = init("image-classification")

while True:
    sense.set_pixels(question_mark)
    print ("*** Waiting for Joystick Event")
    sense.stick.wait_for_event(emptybuffer=True)

    image_filename = create_image_filename()
    capture_and_save_image_as(image_filename)
    print ("*** Picture Taken: {}".format(image_filename))

    print ("*** Image Classification")
    predicted_result = predict(image_filename,ic,c,1)
    print ("*** Classified image as {} with a confidence of {}".format(predicted_result[0][1], predicted_result[0][0]))
    
            
    gg_client.publish(
        topic=iot_core_topic,
        payload=json.dumps({'message':'Classified image as {} with a confidence of {}'.format(predicted_result[0][1], str(predicted_result[0][0]))})
    )

    sense.set_pixels(eval(predicted_result[0][1]))

    if (BUCKET_NAME != ""):
        # Copy image file to s3 with classification and confidence value
        folder = str("smart-recycle-kit/2020/known/") + str(predicted_result[0][1])
        classified = str(predicted_result[0][1]) + "-" + str(predicted_result[0][0])
        push_to_s3(image_filename, folder, classified)

    time.sleep(2)

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop
def function_handler(event, context):
    return
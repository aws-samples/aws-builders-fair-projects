#
# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# Lambda entry point
import greengrasssdk
from cars_model_loader import CarsMLModel
from drones_model_loader import DronesMLModel
import logging
import os
import time
import json

THING_NAME = os.environ['THING_NAME']
ML_MODEL_BASE_PATH = '/ml/od/'
CARS_ML_MODEL_PREFIX = 'deploy_model_algo_4'
DRONES_ML_MODEL_PREFIX = 'model_algo_1'
CARS_ML_MODEL_PATH = os.path.join(ML_MODEL_BASE_PATH, CARS_ML_MODEL_PREFIX)
DRONES_ML_MODEL_PATH = os.path.join(ML_MODEL_BASE_PATH, DRONES_ML_MODEL_PREFIX)
# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')
carsModel = None
dronesModel = None

# Load the model at startup
def initialize(cars_param_path=CARS_ML_MODEL_PATH, drones_param_path=DRONES_ML_MODEL_PATH):
    global carsModel
    carsModel = CarsMLModel(cars_param_path)
    global dronesModel
    dronesModel = DronesMLModel(drones_param_path)


def handler(event, context):
    """
    Gets called each time the function gets invoked.
    """    
    b64 = event['b64']
    mode = event['mode']
    target = event['target']

    start = int(round(time.time() * 1000))

    if mode == 'cars':

        new_b64, prediction, dX, dY, mX, mY = carsModel.predict_from_base64String(b64, mode, target)

        response = {
            'b64': new_b64,
            'prediction': prediction,
            'dX': dX,
            'dY': dY,
            'dZ': 'HOLD',
            'mX': mX,
            'mY': mY,
            'mZ': 1.0
        }

    elif mode == 'drones':

        new_b64, prediction, dX, dY, dZ, mX, mY, mZ = dronesModel.predict_from_base64String(b64)

        response = {
            'b64': new_b64,
            'prediction': prediction,
            'dX': dX,
            'dY': dY,
            'dZ': dZ,
            'mX': mX,
            'mY': mY,
            'mZ': mZ
        }

    else:
        return

    end = int(round(time.time() * 1000))

    logging.info('Prediction: {} for type: {} in: {}'.format(prediction, 'base64 string', end - start))

    OUTPUT_TOPIC = 'detect-cars/{}/infer/output'.format(THING_NAME)

    client.publish(topic=OUTPUT_TOPIC, payload=json.dumps(response))
    return response


# If this path exists then this code is running on the greengrass core and has the ML resources it needs to initialize.
if os.path.exists(ML_MODEL_BASE_PATH):
    initialize()
else:
    logging.info('{} does not exist and we cannot initialize this lambda function.'.format(ML_MODEL_BASE_PATH))

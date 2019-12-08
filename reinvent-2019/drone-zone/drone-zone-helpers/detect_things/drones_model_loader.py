import mxnet as mx
import numpy as np
import base64
import cv2
import logging
import time
from collections import namedtuple
Batch = namedtuple('Batch', ['data'])

DEFAULT_INPUT_SHAPE = 512
CLASSES = [
    "anafi-drone"
]

def get_ctx():
    """
    Automatically choose the device (CPU or GPU) for running inference
    :return: A list of GPUs available. If no GPU is available, return a list with just the CPU device.
    """
    try:
        ctx = [mx.gpu()]
    except:
        ctx = [mx.cpu()]
    return ctx


class DronesMLModel(object):
    """
    Loads the pre-trained model which can be found in /ml/od when running on greengrass core or
    from a different path for testing locally.
    """
    def __init__(self, param_path, label_names=[], input_shapes=[('data', (1, 3, DEFAULT_INPUT_SHAPE, DEFAULT_INPUT_SHAPE))]):

        context = get_ctx()[0]
        # Load the network parameters from default epoch 0
        logging.info('Load network parameters from default epoch 0 with prefix: {}'.format(param_path))
        sym, arg_params, aux_params = mx.model.load_checkpoint(param_path, 0)

        # Load the network into an MXNet module and bind the corresponding parameters
        logging.info('Loading network into mxnet module and binding corresponding parameters: {}'.format(arg_params))
        self.mod = mx.mod.Module(symbol=sym, label_names=label_names, context=context)
        self.mod.bind(for_training=False, data_shapes=input_shapes)
        self.mod.set_params(arg_params, aux_params)
        
    def predict_from_base64String(self, b64, reshape=(DEFAULT_INPUT_SHAPE, DEFAULT_INPUT_SHAPE)):
        
        # convert b64 string to frame
        new_buffer = base64.b64decode(b64)
        _img = cv2.imdecode(np.fromstring(new_buffer, dtype=np.uint8), -1)

        # Switch RGB to BGR format (which ImageNet networks take)
        img = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)

        image_shape = img.shape
        IMAGE_HEIGHT = image_shape[0]
        IMAGE_WIDTH = image_shape[1]

        if img is None:
            return []

        # Resize image to fit network input
        img = cv2.resize(img, reshape)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 1, 2)
        img = img[np.newaxis, :]

        # do inference
        self.mod.forward(Batch([mx.nd.array(img)]))
        prob = self.mod.get_outputs()[0].asnumpy()
        prob = np.squeeze(prob)

        # Grab top result, convert to python list of lists and return
        results = [prob[0].tolist()]
        
        # roll - right axis (left/right)
        dY = 'HOLD' # direction
        mY = 1.0    # magnitude

        # pitch - front axis (forward/backward)
        dX = 'HOLD' # direction
        mX = 1.0    # magnitude

        # gaz - down axis (up/down)
        dZ = 'HOLD' # direction
        mZ = 1.0    # magnitude
        
        if len(results) > 0 and round(results[0][1],2) > 0.15:
        
            x1 = int(results[0][2]*IMAGE_WIDTH)
            y1 = int(results[0][3]*IMAGE_HEIGHT)
            x2 = int(results[0][4]*IMAGE_WIDTH)
            y2 = int(results[0][5]*IMAGE_HEIGHT)
            detectionWidth = x2-x1
            offsetX = IMAGE_WIDTH/2-(x1+x2)/2
            offsetY = IMAGE_HEIGHT/2-(y1+y2)/2

            # proportionately derived from 25/640 and 25/360
            offsetYPercentage = 0.07
            offsetXPercentage = 0.04

            if offsetX < -offsetXPercentage*IMAGE_WIDTH:
                dY = 'RIGHT'
            elif offsetX > offsetXPercentage*IMAGE_WIDTH:
                dY = 'LEFT'

            if offsetY < -offsetYPercentage*IMAGE_HEIGHT:
                dZ = 'DOWN'
            elif offsetY > offsetYPercentage*IMAGE_HEIGHT:
                dZ = 'UP'

            if detectionWidth < IMAGE_HEIGHT*0.10:
                dX = 'FORWARD'
            elif detectionWidth > IMAGE_HEIGHT*0.40:
                dX = 'BACKWARD'
                
            cv2.rectangle(_img,(x1,y1),(x2,y2),(245,185,66),2)
            cv2.putText(_img, str(CLASSES[int(results[0][0])]) + ' - ' + str(round(results[0][1],2)), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), lineType=cv2.LINE_AA)
            cv2.putText(_img, str(IMAGE_WIDTH) + ', ' + str(IMAGE_HEIGHT) + ' | ' + str(offsetX) + ', ' + str(offsetY) + ', ' + str(detectionWidth), (0, IMAGE_HEIGHT-10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), lineType=cv2.LINE_AA)
        
        localtime = time.asctime( time.localtime(time.time()))
        
        cv2.putText(_img, dY + ', ' + dX + ', ' + dZ, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), lineType=cv2.LINE_AA)
        cv2.putText(_img, localtime, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), lineType=cv2.LINE_AA)
        retval, buffer = cv2.imencode('.jpg', _img)
        new_b64 = base64.b64encode(buffer).decode()
        
        return results


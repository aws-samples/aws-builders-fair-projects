import cv2
from dlr import DLRModel
import greengrasssdk
import logging
import numpy as np
import os
from threading import Timer
import time
import railController
import streamServer
import sys
import utils

WIDTH=640
HEIGHT=480
THRESH = 90

MODEL_PATH = os.environ.get("MODEL_PATH", "./model")
dlr_model = DLRModel(MODEL_PATH, "gpu")
current_milli_time = lambda: int(round(time.time() * 1000))
VIDEO_DEVICE = os.environ.get("VIDEO_DEVICE", "/dev/video0")
VIDEO_WIDTH = int(os.environ.get("VIDEO_WIDTH", "640"))
VIDEO_HEIGHT = int(os.environ.get("VIDEO_HEIGHT", "480"))
STREAM_IMAGE_PATH = "/tmp/bfsushi"
STREAM_IMAGE_FILE = STREAM_IMAGE_PATH + "/detected.jpg"
ANORMAL_COUNT = int(os.environ.get("ANORMAL_COUNT", "2"))

# Setup logging to stdout
formatter = "%(asctime)s : [%(levelname)s] %(message)s"
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=formatter)

# create stream temp dir
if not os.path.exists(STREAM_IMAGE_PATH):
    os.mkdir(STREAM_IMAGE_PATH)

# synset.txt is a list of class name
synsets = None
with open("synset.txt", "r") as f:
    synsets = [l.rstrip() for l in f]

client = greengrasssdk.client("iot-data")
railController = railController.RailController(client)

anormal_count = 0

def open_usb_camera():
    gst_str = ("v4l2src device={} ! "
                "video/x-raw, width=(int){}, height=(int){}, framerate=(fraction)30/1 ! "
                "videoconvert !  video/x-raw, , format=(string)BGR ! appsink"
              ).format(
                VIDEO_DEVICE, VIDEO_WIDTH, VIDEO_HEIGHT
              )
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

cap = open_usb_camera()

def predict(image_data):
    global anormal_count
    # use OpenCV to detect sushi saucer
    rect = detect_sushi(image_data)
    if rect is None:
        cv2.imwrite(STREAM_IMAGE_FILE, image_data)
        return

    img = image_data[rect[0]:rect[1], rect[2]:rect[3]]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    img = np.array(img)
    flattened_data = img.astype(np.float32)

    t1 = current_milli_time()
    prediction_scores = dlr_model.run({"data" : flattened_data})#.squeeze()
    t2 = current_milli_time()
    logger.info("finish predicting. duration: {}ms".format(t2 - t1))
    max_score_id = np.argmax(prediction_scores)
    max_score = np.max(prediction_scores)
    predicted_class_name = synsets[max_score_id].split(" ")[1]
    max_score = max_score * 100
    if max_score < THRESH:
        logger.debug("score is too low {:.2f}% {}".format(max_score, predicted_class_name))
        cv2.imwrite(STREAM_IMAGE_FILE, image_data)
        return

    # Prepare result
    color = (240, 168, 34)
    if predicted_class_name.endswith("ship"):
        anormal_count = 0
        logger.debug("Ship detected ignore this.")
        cv2.imwrite(STREAM_IMAGE_FILE, image_data)
        return
    elif predicted_class_name.endswith("anormal"):
        # detect anormal sushi
        anormal_count = anormal_count + 1
    elif predicted_class_name.endswith("empty"):
        # detect empty saucer
        color = (90, 90, 90)
        anormal_count = 0
    else:
        # normal sushi
        anormal_count = 0

    if anormal_count >= ANORMAL_COUNT:
        color = (0, 0, 255)
        anormal_count = 0
        logger.debug("detect anormal. publish close message.")
        # close the rail
        railController.close_rail()
    elif anormal_count > 0:
        logger.debug("detect anormal {} times.".format(anormal_count))

    # write predicted result on image
    cv2.rectangle(image_data, (rect[2], rect[0]),(rect[3], rect[1]), color, thickness=2)
    label = "{}: {:.2f}%".format(predicted_class_name, max_score)
    cv2.putText(image_data, label, (rect[2], rect[0] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.imwrite(STREAM_IMAGE_FILE, image_data)

    # Send result
    logger.info("Prediction Result: score:{:.2f}% {}".format(max_score, predicted_class_name))

# read image from camera and predict
def predict_from_cam():
    ret,image_data  = cap.read()
    if ret:
        predict(image_data)
    else:
        logger.error("image capture faild")

# Use OpenCV HoughCircles to find sushi saucer.
def detect_sushi(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT,
                                    dp=1, minDist=100, param1=50, param2=30,
                                    minRadius=170, maxRadius=400)

    if circles is None:
        return None

    obj_width = 0
    obj_height = 0
    circles = np.uint16(np.around(circles))
    for (x, y, r) in circles[0]:
        x, y, r = int(x), int(y), int(r)
        obj_top = int(y - r - 10)
        if obj_top < 0:
            obj_top = 0

        obj_left = int(x - r - 10)
        if obj_left < 0:
            obj_left = 0

        obj_width = int(r*2+20)
        obj_right = obj_left + obj_width
        if obj_right > WIDTH:
            obj_right = WIDTH
            obj_width = WIDTH - obj_left

        obj_height = int(r*2+20)
        obj_bottom =  obj_top + obj_height
        if obj_bottom > HEIGHT:
            obj_bottom = HEIGHT
            obj_height = HEIGHT - obj_top
        break

    if obj_width < 380 or obj_height < 380 or obj_width > 420 or obj_height > 420:
        # skip if circle is small or too large
        return None

    # return the detected rectangle
    return (obj_top, obj_bottom, obj_left, obj_right)

# infinite loop to detect sushi
def detection_run():
    if dlr_model is not None:
        predict_from_cam()

    # Asynchronously schedule this function to be run again
    Timer(0, detection_run).start()

detection_run()

# Distribute image stream
streamServer.main()

# Lambda Function is not use for event
def function_handler(event, context):
    return
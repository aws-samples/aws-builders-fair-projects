import datetime
import json
import glob
import cv2
import numpy as np
import os
import sys
import shutil


OUTPUT_DIR = '/tmp/sushi_training'
OUTPUT_IMG_FILE_NAME = "output"
JPG_PREFIX = ".jpg"

WIDTH=640
HEIGHT=480

def open_cam_usb():
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ("v4l2src device=/dev/video0 ! "
                "video/x-raw, width=(int){}, height=(int){}, framerate=(fraction)30/1 ! "
                "videoconvert !  video/x-raw, , format=(string)BGR ! appsink"
              ).format(WIDTH, HEIGHT)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


def check_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)

# When use usb camera, uncomment this code
cap = open_cam_usb()

# remove old files
check_dir(OUTPUT_DIR)
check_dir(OUTPUT_DIR + "/image")
cnt_img = 0

while True:
    try:
        ret, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT,
                                    dp=1, minDist=100, param1=50, param2=30,
                                    minRadius=170, maxRadius=400)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            dt_now = datetime.datetime.now()
            fname=dt_now.strftime('%Y%m%d%H%M%S%f')

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
                #print("width:{} height:{}".format(obj_width, obj_height))
                break

            if obj_width < 380 or obj_height < 380:
                # skip if circle is small
                continue
            cnt_img = cnt_img + 1
            print("save file {}".format(cnt_img))
            # write image classification image
            out_name = "{}/image/{}.jpg".format(OUTPUT_DIR, fname)
            #print(out_name)
            cv2.imwrite(out_name, img[obj_top:obj_bottom, obj_left:obj_right])

    except Exception as e:
        print("Failed to grab")
        print(e)
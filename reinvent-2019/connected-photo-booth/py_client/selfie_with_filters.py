import cv2
import numpy as np
#import dlib
from math import hypot

import argparse
from time import gmtime, strftime, sleep
import logging

import boto3
import json

from random import randrange

from cerebro_utils import *

from time import gmtime, strftime

from config import Configuration

# --------- Module- Level Globals ---------------
filter_list = ('pig','crown', 'dog')

config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

'''
# global vars, consts
__CEREBRO_TEMP_DIR__ = "/tmp/project_cerebro"
__CEREBRO_LOGS_DIR__ = "/tmp/project_cerebro/logs"
__CEREBRO_MEDIA_DIR__ = "/tmp/project_cerebro/media"
__FILTERED_IMAGE_NAME__ = "filtered_image.jpg"

__PIG_NOSE_FILTER__ = "../assets/filters/pig_nose.png"

__FLOWER_CROWN_FILTER__ = "../assets/filters/flower_crown.png"
#__FLOWER_CROWN_FILTER__ = "../overlays/mop.png"

__EYE_MASK_FILTER__ = "../assets/filters/mustache.png"
#__EYE_MASK_FILTER__ = "../overlays/cowboy.png"

__DOG_NOSE_FILTER__ = "../assets/filters/dog_nose.png"
__DOG_LEFT_EAR_FILTER__ = "../assets/filters/dog_left_ear.png"
__DOG_RIGHT_EAR_FILTER__ = "../assets/filters/dog_right_ear.png"
__DOG_TONGUE_FILTER__ = "../assets/filters/dog_tongue.png"
'''


# purpose - to read images taken by the camera, apply snapchat filter (pig nose), display/save image 
# enhancements.1 - use opencv to only read the image in as a frame, use reko to do all face attributes detection (not opencv/dlib)
# enhancements.2 - try and apply other images from pixlab , for eg.

def print_value(value=None):
	if not value:
		print("No value provided")
		return

	if type(value) == type(dict()):
		for k,v in value.items():
			print("%s: %s" % (k,str(v)))
	elif type(value) == type(list()):
		for idx, val in enumerate(value):
			print_value(val)
	else:
		print(value)

	return

def get_facial_landmarks(image_path=''):
	get_facial_landmarks_logger = logging.getLogger('selfie_with_filters.get_facial_landmarks')
	get_facial_landmarks_logger.info("In the get_facial_landmarks method ...")

	client=boto3.client('rekognition')

	get_facial_landmarks_logger.info("Running Detect Faces on the image: %s" % image_path)

	with open(image_path, 'rb') as image:
		response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])

	get_facial_landmarks_logger.info('Completed the detect_faces API call' )

	if "FaceDetails" not in response:
		get_facial_landmarks_logger.error("No Faces found!")
		return False

	return response["FaceDetails"]

def get_landmark_value(landmarks=None, parameter_name='', image_width=0, image_height=0):
	get_landmark_value_logger = logging.getLogger('selfie_with_filters.get_landmark_value')
	get_landmark_value_logger.info("In the get_landmark_value method ...")

	if not landmarks:
		get_landmark_value_logger.error("No Landmarks provided!")
		return None

	if not parameter_name:
		get_landmark_value_logger.error("No Parameter provide! Nothing to return!!")
		return None

	# now walk thru' the landmarks looking for the parameter name
	for landmark in landmarks:
		if "Type" not in landmark:
			continue
		if landmark["Type"] == parameter_name:
			get_landmark_value_logger.info(landmark)
			x_coord = landmark["X"]
			y_coord = landmark["Y"]
			get_landmark_value_logger.info("Raw Coords: (%f, %f)" % (x_coord, y_coord))
			x_coord_px = int(x_coord*image_width)
			y_coord_px = int(y_coord*image_height)
			get_landmark_value_logger.info("Coords in px: (%d, %d)" % (x_coord_px, y_coord_px))

			return (x_coord_px, y_coord_px)
			break

	return True


def create_pig_nose_filter(image_path='', nose_image_type=config.__PIG_NOSE_FILTER__):
	create_pig_nose_filter_logger = logging.getLogger('selfie_with_filters.create_pig_nose_filter')

	create_pig_nose_filter_logger.info("In the create_pig_nose_filter method ...")

	# 0. check if there is a valid file
	if not image_path:
		create_pig_nose_filter_logger.error("Error! No Image provided! Can't create filter if there is no image!!")
		return ""

	# 1. read image (selfie) 

	frame = cv2.imread(image_path)

	create_pig_nose_filter_logger.info("The image is at: %s" % image_path)
	image_height, image_width = frame.shape[:2]
	create_pig_nose_filter_logger.info("Image Height: %d, Image Width: %d" % (image_height, image_width))

	# 2. now run a detect faces on this image

	faces = get_facial_landmarks(image_path=image_path)

	for face_idx, face in enumerate(faces):

		# Now get the nose positions for each face
		if "Landmarks" in face:
			center_nose = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="nose", image_width=image_width, image_height=image_height)
			left_nose = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="noseLeft", image_width=image_width, image_height=image_height)
			right_nose = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="noseRight", image_width=image_width, image_height=image_height)
		else:
			create_pig_nose_filter_logger.warning("No Landmarks found in face!")
			continue

		create_pig_nose_filter_logger.info("Retrieved Nose positions for face: %d" % (face_idx+1))

		nose_width = int(hypot(left_nose[0] - right_nose[0],
		                   left_nose[1] - right_nose[1]) * 1.7)
		nose_height = int(nose_width * 0.77)

		# New nose position
		top_left = (int(center_nose[0] - nose_width / 2),
		                      int(center_nose[1] - nose_height / 2))
		bottom_right = (int(center_nose[0] + nose_width / 2),
		               int(center_nose[1] + nose_height / 2))

		# 3. apply effects of pig nose

		nose_image = cv2.imread(nose_image_type)
		rows, cols, _ = frame.shape
		nose_mask = np.zeros((rows, cols), np.uint8)

		nose_mask.fill(0)
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Adding the new nose
		nose_pig = cv2.resize(nose_image, (nose_width, nose_height))
		nose_pig_gray = cv2.cvtColor(nose_pig, cv2.COLOR_BGR2GRAY)
		_, nose_mask = cv2.threshold(nose_pig_gray, 25, 255, cv2.THRESH_BINARY_INV)

		nose_area = frame[top_left[1]: top_left[1] + nose_height,
		            top_left[0]: top_left[0] + nose_width]
		nose_area_no_nose = cv2.bitwise_and(nose_area, nose_area, mask=nose_mask)
		final_nose = cv2.add(nose_area_no_nose, nose_pig)

		frame[top_left[1]: top_left[1] + nose_height,
		            top_left[0]: top_left[0] + nose_width] = final_nose

		create_pig_nose_filter_logger.info("Added the pig nose for face: %d" % (face_idx+1))

	# 4. display the frame thus computed
	# 5. save the image
	filtered_image = "%s/%s" % (config.__CEREBRO_MEDIA_DIR__, config.__FILTERED_IMAGE_NAME__)
	cv2.imwrite(filtered_image, frame)

	return filtered_image

def create_flower_crown_filter(image_path=''):
	create_flower_crown_filter_logger = logging.getLogger('selfie_with_filters.create_flower_crown_filter')

	create_flower_crown_filter_logger.info("In the create_flower_crown_filter method ...")

	# 0. check if there is a valid file
	if not image_path:
		create_flower_crown_filter_logger.error("Error! No Image provided! Can't create filter if there is no image!!")
		return ""

	# 1. read image (selfie) 

	frame = cv2.imread(image_path)

	create_flower_crown_filter_logger.info("The image is at: %s" % image_path)
	image_height, image_width = frame.shape[:2]
	create_flower_crown_filter_logger.info("Image Height: %d, Image Width: %d" % (image_height, image_width))

	# 2. now run a detect faces on this image

	faces = get_facial_landmarks(image_path=image_path)

	for face_idx, face in enumerate(faces):

		create_flower_crown_filter_logger.info(face["BoundingBox"])
		bb_left = face["BoundingBox"]["Left"]
		bb_left_px = int(bb_left*image_width)

		bb_top = face["BoundingBox"]["Top"]
		bb_top_px = int(bb_top*image_height)

		bb_height = face["BoundingBox"]["Height"]
		bb_height_px = int(bb_height*image_height)

		bb_width = face["BoundingBox"]["Width"]
		bb_width_px = int(bb_width*image_width)

		create_flower_crown_filter_logger.info("BB - Left: %f, BB - Left (in px): %d" % (bb_left, bb_left_px))
		create_flower_crown_filter_logger.info("BB - Top: %f, BB - Top (in px): %d" % (bb_top, bb_top_px))
		create_flower_crown_filter_logger.info("BB - Height: %f, BB - Height (in px): %d" % (bb_height, bb_height_px))
		create_flower_crown_filter_logger.info("BB - Width: %f, BB - Width (in px): %d" % (bb_width, bb_width_px))

		bb_left_top = (bb_left_px, bb_top_px)
		bb_bottom_right = (bb_left_px+bb_width_px, bb_top_px+bb_height_px)
		#cv2.rectangle(frame,bb_left_top, bb_bottom_right, (0,255,0), 2)


		# Now get the nose positions for each face
		if "Landmarks" in face:
			upper_jawline_left = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="upperJawlineLeft", image_width=image_width, image_height=image_height)
			upper_jawline_right = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="upperJawlineRight", image_width=image_width, image_height=image_height)
		else:
			create_flower_crown_filter_logger.warning("No Landmarks found in face!")
			continue

		create_flower_crown_filter_logger.info("Retrieved Jaw positions for face: %d" % (face_idx+1))

		#cv2.circle(frame, upper_jawline_left, 3, (255,0,0), -1)
		#cv2.circle(frame, upper_jawline_right, 3, (255,0,0), -1)

		head_crown_width = int(bb_width_px*1.25)
		head_crown_height = int(bb_height_px/2.5)
		create_flower_crown_filter_logger.info(head_crown_width)
		create_flower_crown_filter_logger.info(head_crown_height)

		hc_left_top = (int(bb_left_px-head_crown_width/7), int(bb_top_px-head_crown_height))
		hc_bottom_right = (int(bb_left_px+(head_crown_width*3)), int(bb_top_px-head_crown_height/2))
		create_flower_crown_filter_logger.info(hc_left_top)
		create_flower_crown_filter_logger.info(hc_bottom_right)

		#cv2.rectangle(frame, hc_left_top, hc_bottom_right, (0,0,255), 2)

		# 3. apply effects of flower crown

		crown_image = cv2.imread(config.__FLOWER_CROWN_FILTER__)
		rows, cols, _ = frame.shape
		crown_mask = np.zeros((rows, cols), np.uint8)

		crown_mask.fill(0)
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Adding the new crown
		flower_crown = cv2.resize(crown_image, (head_crown_width, head_crown_height))
		flower_crown_gray = cv2.cvtColor(flower_crown, cv2.COLOR_BGR2GRAY)
		_, crown_mask = cv2.threshold(flower_crown_gray, 25, 255, cv2.THRESH_BINARY_INV)

		crown_area = frame[hc_left_top[1]: hc_left_top[1] + head_crown_height,
			hc_left_top[0]: hc_left_top[0] + head_crown_width]
		crown_area_no_crown = cv2.bitwise_and(crown_area, crown_area, mask=crown_mask)
		final_crown = cv2.add(crown_area_no_crown, flower_crown)

		frame[hc_left_top[1]: hc_left_top[1] + head_crown_height,
			hc_left_top[0]: hc_left_top[0] + head_crown_width] = final_crown

		create_flower_crown_filter_logger.info("Added the crown for face: %d" % (face_idx+1))

	# 4. display the frame thus computed
	'''
	cv2.imshow("ImageFrame", frame)
	while True:
		key = cv2.waitKey(0)

		print(key)
		print(int(key))
		test = int(key) == 27 
		print(test)

		if int(key) == 27:
			cv2.destroyAllWindows()
			print("Destroyed the Window")
			break

	return "TESTONLY"
	'''

	# 5. save the image
	filtered_image = "%s/%s" % (config.__CEREBRO_MEDIA_DIR__, config.__FILTERED_IMAGE_NAME__)
	cv2.imwrite(filtered_image, frame)

	return filtered_image

def create_eye_mask_filter(image_path=''):
	create_eye_mask_filter_logger = logging.getLogger('selfie_with_filters.create_eye_mask_filter')

	create_eye_mask_filter_logger.info("In the create_eye_mask_filter method ...")

	filtered_image = ''

	# 0. check if there is a valid file
	if not image_path:
		create_eye_mask_filter_logger.error("Error! No Image provided! Can't create filter if there is no image!!")
		return ""

	# 1. read image (selfie) 

	frame = cv2.imread(image_path)

	create_eye_mask_filter_logger.info("The image is at: %s" % image_path)
	image_height, image_width = frame.shape[:2]
	create_eye_mask_filter_logger.info("Image Height: %d, Image Width: %d" % (image_height, image_width))

	# 2. now run a detect faces on this image

	faces = get_facial_landmarks(image_path=image_path)

	for face_idx, face in enumerate(faces):

		create_eye_mask_filter_logger.info(face["BoundingBox"])
		bb_left = face["BoundingBox"]["Left"]
		bb_left_px = int(bb_left*image_width)

		bb_top = face["BoundingBox"]["Top"]
		bb_top_px = int(bb_top*image_height)

		bb_height = face["BoundingBox"]["Height"]
		bb_height_px = int(bb_height*image_height)

		bb_width = face["BoundingBox"]["Width"]
		bb_width_px = int(bb_width*image_width)

		create_eye_mask_filter_logger.info("%f, %f" % (bb_left, bb_left_px))
		create_eye_mask_filter_logger.info("%f, %f" % (bb_top, bb_top_px))
		create_eye_mask_filter_logger.info("%f, %f" % (bb_height, bb_height_px))
		create_eye_mask_filter_logger.info("%f, %f" % (bb_width, bb_width_px))

		bb_left_top = (bb_left_px, bb_top_px)
		bb_bottom_right = (bb_left_px+bb_width_px, bb_top_px+bb_height_px)
		cv2.rectangle(frame,bb_left_top, bb_bottom_right, (0,255,0), 2)

		# Now get the nose positions for each face
		if "Landmarks" in face:
			upper_jawline_left = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="upperJawlineLeft", image_width=image_width, image_height=image_height)
			upper_jawline_right = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="upperJawlineRight", image_width=image_width, image_height=image_height)

			leftEyeBrowLeft = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="leftEyeBrowLeft", image_width=image_width, image_height=image_height)
			leftEyeBrowUp = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="leftEyeBrowUp", image_width=image_width, image_height=image_height)
			leftEyeBrowRight = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="leftEyeBrowRight", image_width=image_width, image_height=image_height)

			rightEyeBrowLeft = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="rightEyeBrowLeft", image_width=image_width, image_height=image_height)
			rightEyeBrowUp = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="rightEyeBrowUp", image_width=image_width, image_height=image_height)
			rightEyeBrowRight = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="rightEyeBrowRight", image_width=image_width, image_height=image_height)

		else:
			create_eye_mask_filter_logger.warning("No Landmarks found in face!")
			continue

		create_eye_mask_filter_logger.info("Retrieved Jaw positions for face: %d" % (face_idx+1))

		create_eye_mask_filter_logger.info(upper_jawline_left)
		cv2.circle(frame, upper_jawline_left, 3, (255,0,0), -1)
		cv2.circle(frame, upper_jawline_right, 3, (255,0,0), -1)

		cv2.circle(frame, leftEyeBrowLeft, 3, (0,255,0), -1)
		cv2.circle(frame, leftEyeBrowUp, 3, (0,255,0), -1)
		cv2.circle(frame, leftEyeBrowRight, 3, (0,255,0), -1)

		cv2.circle(frame, rightEyeBrowLeft, 3, (0,0,255), -1)
		cv2.circle(frame, rightEyeBrowUp, 3, (0,0,255), -1)
		cv2.circle(frame, rightEyeBrowRight, 3, (0,0,255), -1)

		eye_mask_width = int(bb_width_px*1.25)
		eye_mask_height = int(bb_height_px/2.5)
		create_eye_mask_filter_logger.info(eye_mask_width)
		create_eye_mask_filter_logger.info(eye_mask_height)

		#em_left_top = (int(bb_left_px-eye_mask_width/7), int(bb_top_px-eye_mask_height))
		em_left_top = (upper_jawline_left[0],int(upper_jawline_left[1]-eye_mask_height/2))
		#em_bottom_right = (int(bb_left_px+(eye_mask_width*1)), int(bb_top_px-eye_mask_height/2))
		em_bottom_right = (upper_jawline_right[0],int(upper_jawline_left[1]+eye_mask_height/10))

		create_eye_mask_filter_logger.info(em_left_top)
		create_eye_mask_filter_logger.info(em_bottom_right)

		cv2.rectangle(frame, em_left_top, em_bottom_right, (0,0,255), 2)

		# 3. apply effects of flower crown

		eyemask_image = cv2.imread(config.__EYE_MASK_FILTER__)
		rows, cols, _ = frame.shape
		eyemask_mask = np.zeros((rows, cols), np.uint8)

		eyemask_mask.fill(0)
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Adding the new crown
		eyemask = cv2.resize(eyemask_image, (eye_mask_width, eye_mask_height))
		eyemask_gray = cv2.cvtColor(eyemask, cv2.COLOR_BGR2GRAY)
		_, eyemask_mask = cv2.threshold(eyemask_gray, 25, 255, cv2.THRESH_BINARY_INV)

		eyemask_area = frame[em_left_top[1]: em_left_top[1] + eye_mask_height,
			em_left_top[0]: em_left_top[0] + eye_mask_width]
		eyemask_area_no_eyemask = cv2.bitwise_and(eyemask_area, eyemask_area, mask=eyemask_mask)
		final_eyemask = cv2.add(eyemask_area_no_eyemask, eyemask)

		#cv2.imshow("eyemask", final_eyemask)

		frame[em_left_top[1]: em_left_top[1] + eye_mask_height,
			em_left_top[0]: em_left_top[0] + eye_mask_width] = final_eyemask

		create_eye_mask_filter_logger.info("Added the eyemask for face: %d" % (face_idx+1))

		'''
		eye_mask_image = cv2.imread(__EYE_MASK_FILTER__)
		rows, cols, _ = frame.shape
		eyemask_mask = np.zeros((rows, cols), np.uint8)

		eyemask_mask.fill(0)
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Adding the new crown
		eye_mask = cv2.resize(eye_mask_image, (eye_mask_width, eye_mask_height))
		eye_mask_gray = cv2.cvtColor(eye_mask, cv2.COLOR_BGR2GRAY)
		_, eyemask_mask = cv2.threshold(eye_mask_gray, 25, 255, cv2.THRESH_BINARY_INV)

		eyemask_area = frame[em_left_top[1]: em_left_top[1] + eye_mask_height,
			em_left_top[0]: em_left_top[0] + eye_mask_width]
		eyemask_area_no_eyemask = cv2.bitwise_and(eyemask_area, eyemask_area, mask=eyemask_mask)
		final_eyemask = cv2.add(eyemask_area_no_eyemask, eye_mask)

		frame[em_left_top[1]: em_left_top[1] + eye_mask_height,
			em_left_top[0]: em_left_top[0] + eye_mask_width] = final_eyemask

		create_eye_mask_filter_logger.info("Added the eyemask for face: %d" % (face_idx+1))
		'''

	# 4. display the frame thus computed
	cv2.imshow("ImageFrame", frame)
	while True:
		key = cv2.waitKey(0)

		print(key)
		print(int(key))
		test = int(key) == 27 
		print(test)

		if int(key) == 27:
			cv2.destroyAllWindows()
			print("Destroyed the Window")
			break

	return "TESTONLY"

	'''
	# 5. save the image
	filtered_image = "%s/%s" % (__CEREBRO_MEDIA_DIR__, __FILTERED_IMAGE_NAME__)
	cv2.imwrite(filtered_image, frame)
	'''

	return filtered_image

def apply_nose(frame=None,face=None, image_width=0, image_height=0, nose_filter_image=''):
	apply_nose_logger = logging.getLogger('selfie_with_filters.apply_nose')
	apply_nose_logger.info("In the apply_nose method ...")

	# Now get the nose positions for each face
	if "Landmarks" in face:
		center_nose = get_landmark_value(landmarks=face["Landmarks"], 
			parameter_name="nose", image_width=image_width, image_height=image_height)
		left_nose = get_landmark_value(landmarks=face["Landmarks"], 
			parameter_name="noseLeft", image_width=image_width, image_height=image_height)
		right_nose = get_landmark_value(landmarks=face["Landmarks"], 
			parameter_name="noseRight", image_width=image_width, image_height=image_height)
	else:
		apply_nose_logger.warning("No Landmarks found in face!")
		return None

	apply_nose_logger.info("Retrieved Nose positions for face ...")

	nose_width = int(hypot(left_nose[0] - right_nose[0],
	                   left_nose[1] - right_nose[1]) * 1.9)
	nose_height = int(nose_width * 0.77)

	# New nose position
	top_left = (int(center_nose[0] - nose_width / 2),
	                      int(center_nose[1] - nose_height / 2))
	bottom_right = (int(center_nose[0] + nose_width / 2),
	               int(center_nose[1] + nose_height / 2))

	# 3. apply effects of pig nose

	nose_image = cv2.imread(nose_filter_image)
	rows, cols, _ = frame.shape
	nose_mask = np.zeros((rows, cols), np.uint8)

	nose_mask.fill(0)
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Adding the new nose
	nose_dog = cv2.resize(nose_image, (nose_width, nose_height))
	nose_dog_gray = cv2.cvtColor(nose_dog, cv2.COLOR_BGR2GRAY)
	_, nose_mask = cv2.threshold(nose_dog_gray, 25, 255, cv2.THRESH_BINARY_INV)

	nose_area = frame[top_left[1]: top_left[1] + nose_height,
	            top_left[0]: top_left[0] + nose_width]
	nose_area_no_nose = cv2.bitwise_and(nose_area, nose_area, mask=nose_mask)
	final_nose = cv2.add(nose_area_no_nose, nose_dog)

	frame[top_left[1]: top_left[1] + nose_height,
	            top_left[0]: top_left[0] + nose_width] = final_nose

	return frame

def apply_tongue(frame=None,face=None, image_width=0, image_height=0, tongue_filter_image=''):
	apply_tongue_logger = logging.getLogger('selfie_with_filters.apply_nose')
	apply_tongue_logger.info("In the apply_nose method ...")

	# Now get the nose positions for each face
	if "Landmarks" in face:
		center_tongue = get_landmark_value(landmarks=face["Landmarks"], 
			parameter_name="mouthDown", image_width=image_width, image_height=image_height)
		left_tongue = get_landmark_value(landmarks=face["Landmarks"], 
			parameter_name="mouthLeft", image_width=image_width, image_height=image_height)
		right_tongue = get_landmark_value(landmarks=face["Landmarks"], 
			parameter_name="mouthRight", image_width=image_width, image_height=image_height)
	else:
		apply_nose_logger.warning("No Landmarks found in face!")
		return None

	apply_tongue_logger.info("Retrieved Nose positions for face ...")

	tongue_width = int(hypot(left_tongue[0] - right_tongue[0],
	                   left_tongue[1] - right_tongue[1]) * 1.25)
	tongue_height = int(tongue_width * 0.75)

	# New nose position
	#top_left = (int(center_nose[0] - nose_width / 2),
	#                      int(center_nose[1] - nose_height / 2))
	top_left = (int(center_tongue[0] - tongue_width / 2),
	                      int(center_tongue[1] - tongue_height / 3))
	bottom_right = (int(center_tongue[0] + tongue_width / 2),
	               int(center_tongue[1] + tongue_height / 2))

	# 3. apply effects of pig nose

	tongue_image = cv2.imread(tongue_filter_image)
	rows, cols, _ = frame.shape
	tongue_mask = np.zeros((rows, cols), np.uint8)

	tongue_mask.fill(0)
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Adding the new nose
	tongue_animal = cv2.resize(tongue_image, (tongue_width, tongue_height))
	tongue_animal_gray = cv2.cvtColor(tongue_animal, cv2.COLOR_BGR2GRAY)
	_, tongue_mask = cv2.threshold(tongue_animal_gray, 25, 255, cv2.THRESH_BINARY_INV)

	tongue_area = frame[top_left[1]: top_left[1] + tongue_height,
	            top_left[0]: top_left[0] + tongue_width]
	tongue_area_no_tongue = cv2.bitwise_and(tongue_area, tongue_area, mask=tongue_mask)
	final_tongue = cv2.add(tongue_area_no_tongue, tongue_animal)

	frame[top_left[1]: top_left[1] + tongue_height,
	            top_left[0]: top_left[0] + tongue_width] = final_tongue

	return frame

def apply_ear(frame=None,face=None, image_width=0, image_height=0, ear_direction="", ear_filter_image=''):
	apply_ear_logger = logging.getLogger('selfie_with_filters.apply_ear')
	apply_ear_logger.info("In the apply_ear method ...")

	# Now get the nose positions for each face
	if "Landmarks" in face:
		#center_tongue = get_landmark_value(landmarks=face["Landmarks"], 
		#	parameter_name="mouthDown", image_width=image_width, image_height=image_height)
		#left_tongue = get_landmark_value(landmarks=face["Landmarks"], 
		#	parameter_name="upperJawlineLeft", image_width=image_width, image_height=image_height)
		if ear_direction == "left":
			center_ear = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="upperJawlineLeft", image_width=image_width, image_height=image_height)
			# get the left eye dimensions
			left_eye_left = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="leftEyeLeft", image_width=image_width, image_height=image_height)
			left_eye_right = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="leftEyeRight", image_width=image_width, image_height=image_height)

		elif ear_direction == "right":
			center_ear = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="upperJawlineRight", image_width=image_width, image_height=image_height)
			# get the right eye dimensions
			right_eye_left = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="rightEyeLeft", image_width=image_width, image_height=image_height)
			right_eye_right = get_landmark_value(landmarks=face["Landmarks"], 
				parameter_name="rightEyeRight", image_width=image_width, image_height=image_height)

		#right_tongue = get_landmark_value(landmarks=face["Landmarks"], 
		#	parameter_name="mouthRight", image_width=image_width, image_height=image_height)
	else:
		apply_ear_logger.warning("No Landmarks found in face!")
		return None

	apply_ear_logger.info("Retrieved Ear positions for face ...")

	#tongue_width = int(hypot(left_tongue[0] - right_tongue[0],
	#                   left_tongue[1] - right_tongue[1]) * 1.25)
	# reko doesn't give any info. on ear dimensions, so 
	# lets use the width of the eyes as a proxy for face scale
	if ear_direction == "left":
		ear_width = int(hypot(left_eye_left[0] - left_eye_right[0],
							left_eye_left[1] - left_eye_right[1]) * 2.0)
	elif ear_direction == "right":
		ear_width = int(hypot(right_eye_left[0] - right_eye_right[0],
							right_eye_left[1] - right_eye_right[1]) * 2.0)

	ear_height = int(ear_width * 1.25)

	# New nose position
	#top_left = (int(center_nose[0] - nose_width / 2),
	#                      int(center_nose[1] - nose_height / 2))
	if ear_direction == "left":
		top_left = (int(center_ear[0] - ear_width / 1.25),
		                      int(center_ear[1] - ear_height / 0.75))
		bottom_right = (int(center_ear[0] + ear_width / 2),
		               int(center_ear[1] + ear_height / 2))
	elif ear_direction == "right":
		top_left = (int(center_ear[0]),
		                      int(center_ear[1] - ear_height / 0.75))
		bottom_right = (int(center_ear[0] + ear_width / 1),
		               int(center_ear[1] + ear_height / 1))

	# 3. apply effects of pig nose

	ear_image = cv2.imread(ear_filter_image)
	rows, cols, _ = frame.shape
	ear_mask = np.zeros((rows, cols), np.uint8)

	ear_mask.fill(0)
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Adding the new nose
	ear_animal = cv2.resize(ear_image, (ear_width, ear_height))
	ear_animal_gray = cv2.cvtColor(ear_animal, cv2.COLOR_BGR2GRAY)
	_, ear_mask = cv2.threshold(ear_animal_gray, 25, 255, cv2.THRESH_BINARY_INV)

	ear_area = frame[top_left[1]: top_left[1] + ear_height,
	            top_left[0]: top_left[0] + ear_width]
	ear_area_no_ear = cv2.bitwise_and(ear_area, ear_area, mask=ear_mask)
	final_ear = cv2.add(ear_area_no_ear, ear_animal)

	frame[top_left[1]: top_left[1] + ear_height,
	            top_left[0]: top_left[0] + ear_width] = final_ear

	return frame

def create_dog_face_filter(image_path=''):
	create_dog_face_filter_logger = logging.getLogger('selfie_with_filters.create_dog_face_filter')

	create_dog_face_filter_logger.info("In the create_dog_face_filter_logger method ...")

	# 0. check if there is a valid file
	if not image_path:
		create_dog_face_filter_logger.error("Error! No Image provided! Can't create filter if there is no image!!")
		return ""

	# 1. read image (selfie) 

	frame = cv2.imread(image_path)

	create_dog_face_filter_logger.info("The image is at: %s" % image_path)
	image_height, image_width = frame.shape[:2]
	create_dog_face_filter_logger.info("Image Height: %d, Image Width: %d" % (image_height, image_width))

	# 2. now run a detect faces on this image

	faces = get_facial_landmarks(image_path=image_path)

	for face_idx, face in enumerate(faces):

		frame = apply_nose(frame=frame,face=face, image_width=image_width, image_height=image_height, nose_filter_image=config.__DOG_NOSE_FILTER__)
		frame = apply_ear(frame=frame,face=face, image_width=image_width, image_height=image_height, ear_direction="left" , ear_filter_image=config.__DOG_LEFT_EAR_FILTER__)
		frame = apply_ear(frame=frame,face=face, image_width=image_width, image_height=image_height, ear_direction="right" , ear_filter_image=config.__DOG_RIGHT_EAR_FILTER__)
		frame = apply_tongue(frame=frame,face=face, image_width=image_width, image_height=image_height, tongue_filter_image=config.__DOG_TONGUE_FILTER__)

		create_dog_face_filter_logger.info("Added the dog nose for face: %d" % (face_idx+1))

	# 4. display the frame thus computed
	'''
	cv2.imshow("ImageFrame", frame)
	while True:
		key = cv2.waitKey(0)

		print(key)
		print(int(key))
		test = int(key) == 27 
		print(test)

		if int(key) == 27:
			cv2.destroyAllWindows()
			print("Destroyed the Window")
			break

	return "TESTONLY"
	'''

	# 5. save the image
	filtered_image = "%s/%s" % (config.__CEREBRO_MEDIA_DIR__, config.__FILTERED_IMAGE_NAME__)
	cv2.imwrite(filtered_image, frame)

	return filtered_image

def initialize():

    parser = argparse.ArgumentParser()
    parser.add_argument("--logfile", help="Logfile for all INFO/DEBUG level logs")
    parser.add_argument("--debug", help="debug mode to not run scripts", action='store_true')
    parser.add_argument("--image", help="Image (jpg) to be processed - filter to be added")
    parser.add_argument("--filter", help="Different filter choices ('pig','crown', 'dog') . ")

    args = parser.parse_args()

    # and now setup the logging profile
    # set up logging to file - see previous section for more details
    if args.logfile:
        logFile = args.logfile
    else:
        current_time = strftime("%Y_%m_%dT%H_%M_%S", gmtime())
        logFile = '%s/selfie_with_filters_%s.log' % (config.__CEREBRO_LOGS_DIR__, current_time)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=logFile,
                        filemode='w')
    
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    #logging.getLogger('').addHandler(console)

    # Now, define a couple of other loggers which might represent areas in your application:
    initialize_logger = logging.getLogger('selfie_with_overlay.initialize')
    initialize_logger.info(args)

    if args.image:
    	image_path = args.image
    else:
    	# Just a default setting for now
    	image_path = "/Users/sacholla/Downloads/PhotoBooth_ProfilePicture.jpg"

    chosen_filter = ""
    if args.filter:
    	chosen_filter = args.filter
    else:
        # Change - on 11/29/2019 - by Sachin - Start
        chosen_filter = ""
        # Change - on 11/29/2019 - by Sachin - End

    # setup the local dirs, only in debug mode
    if args.debug:
    	setup_dirs(dir_to_create=config.__CEREBRO_MEDIA_DIR__, clean_mode=True)
    	setup_dirs(dir_to_create=config.__CEREBRO_LOGS_DIR__, clean_mode=True)

    return image_path, chosen_filter

# Change - on 11/30/2019 - by Sachin - Start
def choose_filter(chosen_filter=''):

  choose_filter_logger = logging.getLogger('selfie_with_filters.choose_filter')
  choose_filter_logger.info("In choose_filter ...")

  # 1. get the setting from the DB (eventually replace with the aws-param store)
  db_setting_name = "image_filter_applied"
  filters_applied = retrieve_setting(setting_name=db_setting_name)

  # 2. if the chosen effect was passed, confirm that this is not in the list retrieved from the database
  choose_filter_logger.info("Checking if a valid filter was provided...: %s" % chosen_filter)
  if chosen_filter:
    if not filters_applied:
      return chosen_filter
    if chosen_filter not in filters_applied:
      # chosen filter wasmn't found in list of previously applied filter
      return chosen_filter

  choose_filter_logger.info("No valid filter was provided so cycling thru' a randomized one ...")
  # 3. if the chosen filter was not passed, randomize the list and get the next filter
  acceptable_filter = False
  while not acceptable_filter:
    choose_filter_logger.error("Warning! No Filter provided - one will be chosen for you.")
    filter_index = randrange(len(filter_list))
    chosen_filter = filter_list[filter_index]
    # 3a. ensure that the chosen filter is not in the list from the database, if not, keep trying
    choose_filter_logger.info("Chosen Filter: %s, List of filters previously applied: %s" % (chosen_filter, filters_applied))
    if chosen_filter not in filters_applied:
      choose_filter_logger.info("A valid filter determined: %s" % chosen_filter)
      acceptable_filter = True
      break

  # chosen filter wasmn't found in list of previously applied effects

  # now optimistically add to the list of database manitained filters
  if filters_applied:
    filters_applied += ",%s" % chosen_filter
  else:
    filters_applied = chosen_filter

  # now do a simplistic error checking for size of filter_list and confirm its not the same as the src list
  filters_applied_list = filters_applied.split(",")
  if len(filters_applied_list) >= len(filter_list):
    filters_applied = ""

  persist_setting(setting_name=db_setting_name, setting_value=filters_applied)

  choose_filter_logger.info("chosen_filter persisted and being returned: %s" % chosen_filter)
  return chosen_filter

# Change - on 11/30/2019 - by Sachin - End

def process_image_filter(image_path='', filter_type=''):

    process_image_filter_logger = logging.getLogger('selfie_with_filters.process_image_filter')
    process_image_filter_logger.info("Entered process_image_filter method ...")

    filtered_image = ''

    # first assign the filter_type if not provided
    # Change - on 11/30/2019 - by Sachin - Start
    filter_type = choose_filter(chosen_filter=filter_type)

    '''
    if not filter_type:
        # randomize the filter choice
        filter_index = randrange(len(filter_list))
        filter_type = filter_list[filter_index]
	'''
    # Change - on 11/30/2019 - by Sachin - End

    # now generate the filtered image
    process_image_filter_logger.info("Image Path: %s" % image_path)

    if filter_type == "pig":
        filtered_image = create_pig_nose_filter(image_path=image_path)
    elif filter_type == "crown":
        filtered_image = create_flower_crown_filter(image_path=image_path)
    #elif chosen_filter == "eyemask":
    #    #filtered_image = create_pig_nose_filter(image_path=image_path, nose_image_type=__DOG_NOSE_FILTER__)
    #    filtered_image = create_eye_mask_filter(image_path=image_path)
    elif filter_type == "dog":
        filtered_image = create_dog_face_filter(image_path=image_path)
    else:
        process_image_filter_logger.error("Error! No filter specified!!")
        return filtered_image

    process_image_filter_logger.info("Converted image at: %s" % filtered_image)    

    return filtered_image

if __name__ == "__main__":

	image_path, chosen_filter = initialize()

	main_logger = logging.getLogger('selfie_with_overlay.main')

	main_logger.info("In main thread ...")

	process_image_filter(image_path=image_path, filter_type=chosen_filter)
#!/usr/bin/python3

from PIL import Image, ImageFilter
import cv2
import numpy as np

import argparse
import subprocess
import logging
from random import randrange
import os

import skimage
from skimage import io, filters
# from skimage.viewer import ImageViewer
import numpy as np

from rpi_utils import persist_setting, retrieve_setting

from config import Configuration

'''
__PROFILE_PATH__ = "/tmp/project_cerebro/profiles"
__CEREBRO_LOGS_DIR__ = "/tmp/project_cerebro/logs"
__CEREBRO_TEMP_DIR__ = "/tmp/project_cerebro"
__CEREBRO_MEDIA_DIR__ = "/tmp/project_cerebro/media"
__CEREBRO_SYSTEM_DIR__ = "/tmp/project_cerebro/system"
'''

# --------- Module- Level Globals ---------------

imaging_effects_list = (\
  'grayscale', \
  'sepia', \
  'gotham', \
  #'blur', 'primary', 'contour', 'emboss', \
  'edge', \
  'sharpen', \
  'smooth', \
  'contrast', \
  #'gaussianblur', \
  #'medianblur',\
  'cannyedge',\
  'denoise'\
  )

config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

# Open an Image
def open_image(path):
  newImage = Image.open(path)
  return newImage

# Save Image
def save_image(image, path):
  image.save(path, 'png')


# Create a new image with the given size
def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image


# Get the pixel from the given image
def get_pixel(image, i, j):
  # Inside image bounds?
  invalid_pixel = (0,0,0)
  width, height = image.size
  if i >= width or j >= height:
    return invalid_pixel

  # Get Pixel
  try:
    pixel = image.getpixel((i, j))
  except IndexError as e:
    print(e)
    print(i,j)
    print(width, height)
    return invalid_pixel

  return pixel

# Create a Grayscale version of the image
def convert_grayscale(image):
  convert_grayscale_logger = logging.getLogger('apply_image_effects.convert_grayscale')
  convert_grayscale_logger.info("In convert_grayscale ...")

  # Get size
  width, height = image.size

  # Create new Image and a Pixel Map
  new = create_image(width, height)
  pixels = new.load()

  # Transform to grayscale
  for i in range(width):
    for j in range(height):
      # Get Pixel
      pixel = get_pixel(image, i, j)

      # Get R, G, B values (This are int from 0 to 255)
      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      # Transform to grayscale
      gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

      # Set Pixel in new image
      pixels[i, j] = (int(gray), int(gray), int(gray))

  convert_grayscale_logger.info("Completed convert_grayscale .")
  # Return new image
  return new

# Create a Half-tone version of the image
def convert_halftoning(image):
  # Get size
  width, height = image.size

  # Create new Image and a Pixel Map
  new = create_image(width, height)
  pixels = new.load()

  # Transform to half tones
  for i in range(0, width, 2):
    for j in range(0, height, 2):
      # Get Pixels
      p1 = get_pixel(image, i, j)
      p2 = get_pixel(image, i, j + 1)
      p3 = get_pixel(image, i + 1, j)
      p4 = get_pixel(image, i + 1, j + 1)

      # Transform to grayscale
      gray1 = (p1[0] * 0.299) + (p1[1] * 0.587) + (p1[2] * 0.114)
      gray2 = (p2[0] * 0.299) + (p2[1] * 0.587) + (p2[2] * 0.114)
      gray3 = (p3[0] * 0.299) + (p3[1] * 0.587) + (p3[2] * 0.114)
      gray4 = (p4[0] * 0.299) + (p4[1] * 0.587) + (p4[2] * 0.114)

      # Saturation Percentage
      sat = (gray1 + gray2 + gray3 + gray4) / 4

      # Draw white/black depending on saturation
      if sat > 223:
       pixels[i, j]         = (255, 255, 255) # White
       pixels[i, j + 1]     = (255, 255, 255) # White
       pixels[i + 1, j]     = (255, 255, 255) # White
       pixels[i + 1, j + 1] = (255, 255, 255) # White
      elif sat > 159:
       pixels[i, j]         = (255, 255, 255) # White
       pixels[i, j + 1]     = (0, 0, 0)       # Black
       pixels[i + 1, j]     = (255, 255, 255) # White
       pixels[i + 1, j + 1] = (255, 255, 255) # White
      elif sat > 95:
       pixels[i, j]         = (255, 255, 255) # White
       pixels[i, j + 1]     = (0, 0, 0)       # Black
       pixels[i + 1, j]     = (0, 0, 0)       # Black
       pixels[i + 1, j + 1] = (255, 255, 255) # White
      elif sat > 32:
       pixels[i, j]         = (0, 0, 0)       # Black
       pixels[i, j + 1]     = (255, 255, 255) # White
       pixels[i + 1, j]     = (0, 0, 0)       # Black
       pixels[i + 1, j + 1] = (0, 0, 0)       # Black
      else:
       pixels[i, j]         = (0, 0, 0)       # Black
       pixels[i, j + 1]     = (0, 0, 0)       # Black
       pixels[i + 1, j]     = (0, 0, 0)       # Black
       pixels[i + 1, j + 1] = (0, 0, 0)       # Black

  # Return new image
  return new

# Return color value depending on quadrant and saturation
def get_saturation(value, quadrant):
  if value > 223:
    return 255
  elif value > 159:
    if quadrant != 1:
      return 255

    return 0
  elif value > 95:
    if quadrant == 0 or quadrant == 3:
      return 255

    return 0
  elif value > 32:
    if quadrant == 1:
      return 255

    return 0
  else:
    return 0


# Create a dithered version of the image
def convert_dithering(image):
  # Get size
  width, height = image.size

  # Create new Image and a Pixel Map
  new = create_image(width, height)
  pixels = new.load()

  # Transform to half tones
  for i in range(0, width, 2):
    for j in range(0, height, 2):
      # Get Pixels
      p1 = get_pixel(image, i, j)
      p2 = get_pixel(image, i, j + 1)
      p3 = get_pixel(image, i + 1, j)
      p4 = get_pixel(image, i + 1, j + 1)

      # Color Saturation by RGB channel
      red   = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
      green = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
      blue  = (p1[2] + p2[2] + p3[2] + p4[2]) / 4

      # Results by channel
      r = [0, 0, 0, 0]
      g = [0, 0, 0, 0]
      b = [0, 0, 0, 0]

      # Get Quadrant Color
      for x in range(0, 4):
        r[x] = get_saturation(red, x)
        g[x] = get_saturation(green, x)
        b[x] = get_saturation(blue, x)

      # Set Dithered Colors
      pixels[i, j]         = (r[0], g[0], b[0])
      pixels[i, j + 1]     = (r[1], g[1], b[1])
      pixels[i + 1, j]     = (r[2], g[2], b[2])
      pixels[i + 1, j + 1] = (r[3], g[3], b[3])

  # Return new image
  return new


# Create a Primary Colors version of the image
def convert_primary(image):
  # Get size
  width, height = image.size

  # Create new Image and a Pixel Map
  new = create_image(width, height)
  pixels = new.load()

  # Transform to primary
  for i in range(width):
    for j in range(height):
      # Get Pixel
      pixel = get_pixel(image, i, j)

      # Get R, G, B values (This are int from 0 to 255)
      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      # Transform to primary
      if red > 127:
        red = 255
      else:
        red = 0
      if green > 127:
        green = 255
      else:
        green = 0
      if blue > 127:
        blue = 255
      else:
        blue = 0

      # Set Pixel in new image
      pixels[i, j] = (int(red), int(green), int(blue))

  # Return new image
  return new

def sepia(image_path:str)->Image:
    sepia_logger = logging.getLogger('apply_image_effects.sepia')
    sepia_logger.info("In sepia ...")

    img = Image.open(image_path)
    width, height = img.size

    pixels = img.load() # create the pixel map

    for py in range(height):
     for px in range(width):
         r, g, b = img.getpixel((px, py))

         tr = int(0.393 * r + 0.769 * g + 0.189 * b)
         tg = int(0.349 * r + 0.686 * g + 0.168 * b)
         tb = int(0.272 * r + 0.534 * g + 0.131 * b)

         if tr > 255:
             tr = 255

         if tg > 255:
             tg = 255

         if tb > 255:
             tb = 255

         pixels[px, py] = (tr,tg,tb)

    sepia_logger.info("Completed sepia .")
    return img

def sepia_cv(image_path:str)->Image:
    """
    Optimization on the sepia filter using cv2 
    """

    image = Image.open(image_path)

    # Load the image as an array so cv knows how to work with it
    img = np.array(image)

    # Apply a transformation where we multiply each pixel rgb 
    # with the matrix for the sepia

    filt = cv2.transform( img, np.matrix([[ 0.393, 0.769, 0.189],
                                          [ 0.349, 0.686, 0.168],
                                          [ 0.272, 0.534, 0.131]                                  
    ]) )

    # Check wich entries have a value greather than 255 and set it to 255
    filt[np.where(filt>255)] = 255

    # Create an image from the array 
    img_sepia = Image.fromarray(filt)
    print(type(img_sepia))
    cv2.imshow("image", img_sepia)

    return

#---
def split_image_into_channels(image):
    """Look at each image separately"""
    red_channel = image[:, :, 0]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 2]
    return red_channel, green_channel, blue_channel


def merge_channels(red, green, blue):
    """Merge channels back into an image"""
    return np.stack([red, green, blue], axis=2)

def sharpen(image, a, b):
    """Sharpening an image: Blur and then subtract from original"""
    blurred = skimage.filters.gaussian(image, sigma=10, multichannel=True)
    sharper = np.clip(image * a - blurred * b, 0, 1.0)
    return sharper


def channel_adjust(channel, values):
    # preserve the original size, so we can reconstruct at the end
    orig_size = channel.shape
    # flatten the image into a single array
    flat_channel = channel.flatten()

    # this magical numpy function takes the values in flat_channel
    # and maps it from its range in [0, 1] to its new squeezed and
    # stretched range
    adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)

    # put back into the original image shape
    return adjusted.reshape(orig_size)

def apply_gotham_filter(source_image=None, target_file=None):

    apply_gotham_filter_logger = logging.getLogger('apply_image_effects.apply_gotham_filter')
    apply_gotham_filter_logger.info("In apply_gotham_filter ...")

    apply_gotham_filter_logger.info('Instagram Filter Remake: Gotham')
    original_image = skimage.io.imread(source_image)
    original_image = skimage.util.img_as_float(original_image)

    r, g, b = split_image_into_channels(original_image)
    im = merge_channels(r, g, b)

    # 1. Colour channel adjustment example
    r, g, b = split_image_into_channels(original_image)
    r_interp = channel_adjust(r, [0, 0.8, 1.0])
    red_channel_adj = merge_channels(r_interp, g, b)
    #skimage.io.imsave('images/1_red_channel_adj.jpg', red_channel_adj)

    # 2. Mid tone colour boost
    r, g, b = split_image_into_channels(original_image)
    r_boost_lower = channel_adjust(r, [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0])
    r_boost_img = merge_channels(r_boost_lower, g, b)
    #skimage.io.imsave('images/2_mid_tone_colour_boost.jpg', r_boost_img)

    # 3. Making the blacks bluer
    bluer_blacks = merge_channels(r_boost_lower, g, np.clip(b + 0.03, 0, 1.0))
    #skimage.io.imsave('images/3_bluer_blacks.jpg', bluer_blacks)

    # 4. Sharpening the image
    sharper = sharpen(bluer_blacks, 1.3, 0.3)
    #skimage.io.imsave('images/4_sharpened.jpg', sharper)

    # 5. Blue channel boost in lower-mids, decrease in upper-mids
    r, g, b = split_image_into_channels(sharper)
    b_adjusted = channel_adjust(b, [0, 0.047, 0.118, 0.251, 0.318, 0.392, 0.42, 0.439, 0.475, 0.561, 0.58, 0.627, 0.671, 0.733, 0.847, 0.925, 1])
    gotham = merge_channels(r, g, b_adjusted)
    skimage.io.imsave(target_file, gotham)

    apply_gotham_filter_logger.info("Completed apply_gotham_filter .")
    return target_file

#---

def initialize():

  parser = argparse.ArgumentParser()
  #parser.add_argument("echo", help="echo the string you use here")
  parser.add_argument("--logfile", help="Logfile for all INFO/DEBUG level logs")
  parser.add_argument("--debug", help="debug mode to not run scripts", action='store_true')
  parser.add_argument("--effect", help="effect to implement on image (imagepath). \
    Options are: 'grayscale', 'sepia', 'gotham', 'blur', 'primary',\
    'contour', 'emboss', 'edge', 'sharpen', 'smooth',\
    'contrast', 'gaussianblur', 'medianblur','cannyedge',\
    'denoise' ")
  parser.add_argument("--imagepath", help="Location/path of image file")

  args = parser.parse_args()
  #print(args)

  # and now setup the logging profile
  # set up logging to file - see previous section for more details
  if args.logfile:
    logFile = args.logfile
  else:
    logFile = '%s/apply_image_effects.log' % config.__CEREBRO_LOGS_DIR__

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
  logging.getLogger('').addHandler(console)

  # Now, we can log to the root logger, or any other logger. First the root...
  #logging.info('Jackdaws love my big sphinx of quartz.')

  # Now, define a couple of other loggers which might represent areas in your
  # application:
  initialize_logger = logging.getLogger('apply_image_effects.initialize')
  initialize_logger.info(args)

  if args.imagepath:
    image_path = args.imagepath
  else:
    image_path = "/Users/sacholla/Downloads/PhotoBooth_ProfilePicture.jpg"

  if args.effect and args.effect in imaging_effects_list:
    # tbd
    chosen_effect = args.effect
  else:
    # Change - on 11/29/2019 - by Sachin - Start
    effect_index = randrange(len(imaging_effects_list))
    chosen_effect = imaging_effects_list[effect_index]
    # Change - on 11/29/2019 - by Sachin - End
    chosen_effect = ""

  return image_path, chosen_effect

# Change - on 11/28/2019 - by Sachin - Start
def choose_effect(chosen_effect=''):

  choose_effect_logger = logging.getLogger('apply_image_effects.choose_effect')
  choose_effect_logger.info("In choose_effect ...")

  # 1. get the setting from the DB (eventually replace with the aws-param store)
  db_setting_name = "image_effect_applied"
  effects_applied = retrieve_setting(setting_name=db_setting_name)

  # 2. if the chosen effect was passed, confirm that this is not in the list retrieved from the database
  choose_effect_logger.info("Checking if a valid effect was provided...: %s" % chosen_effect)
  if chosen_effect:
    if not effects_applied:
      return chosen_effect
    if chosen_effect not in effects_applied:
      # chosen effect wasmn't found in list of previously applied effects
      return chosen_effect

  choose_effect_logger.info("No valid effect was provided so cycling thru' a randomized one ...")
  # 3. if the chosen effect was not passed, randomize the list and get the next effect
  acceptable_effect = False
  while not acceptable_effect:
    choose_effect_logger.error("Warning! No Effect provided - one will be chosen for you.")
    effect_index = randrange(len(imaging_effects_list))
    chosen_effect = imaging_effects_list[effect_index]
    # 3a. ensure that the chosen effect is not in the list from the database, if not, keep trying
    choose_effect_logger.info("Chosen Effect: %s, List of effects previously applied: %s" % (chosen_effect, effects_applied))
    if chosen_effect not in effects_applied:
      choose_effect_logger.info("A valid effect determined: %s" % chosen_effect)
      acceptable_effect = True
      break

  # chosen effect wasmn't found in list of previously applied effects

  # now optimistically add to the list of database manitained effects
  if effects_applied:
    effects_applied += ",%s" % chosen_effect
  else:
    effects_applied = chosen_effect

  # now do a simplistic error checking for size of effects_applied and confirm its not the same as the src list
  effects_applied_list = effects_applied.split(",")
  if len(effects_applied_list) >= len(imaging_effects_list):
    effects_applied = ""

  persist_setting(setting_name='image_effect_applied', setting_value=effects_applied)

  choose_effect_logger.info("chosen_effect persisted and being returned: %s" % chosen_effect)
  return chosen_effect



# Change - on 11/28/2019 - by Sachin - End

def apply_image_effect(image_path='', chosen_effect=''):
  apply_image_effect_logger = logging.getLogger('apply_image_effects.apply_image_effect')

  if not image_path:
    apply_image_effect_logger.error("ERROR! No Image Path provided!")
    return

  # Change - on 11/29/2019 - by Sachin - Start
  chosen_effect = choose_effect(chosen_effect=chosen_effect)

  '''
  if not chosen_effect:
    apply_image_effect_logger.error("Warning! No Effect provided - one will be chosen for you.")
    effect_index = randrange(len(imaging_effects_list))
    chosen_effect = imaging_effects_list[effect_index]
  '''
  # Change - on 11/29/2019 - by Sachin - End

  apply_image_effect_logger.info("Image: %s, Effect Requested: %s" % (image_path, chosen_effect))

  # Load Image (JPEG/JPG needs libjpeg to load)
  original = open_image(image_path)

  file_stem = os.path.basename(image_path).split(".")[0]
  target_file = "%s/%s_effects.jpg" % (config.__CEREBRO_MEDIA_DIR__, file_stem)
  apply_image_effect_logger.info("Target File: %s" % target_file)

  # Example Pixel Color
  #apply_image_effect_logger.info('Color: %s ' % (str(get_pixel(original, 0, 0))))

  #imaging_effects_list = ('grayscale', 'sepia', 'gotham', 'blur', 'primary', 
  #'contour', 'emboss', 'edge', 'sharpen', 'smooth', 'contrast')

  chosen_effect_text = ""

  if chosen_effect == "blur":
    apply_image_effect_logger.info("Converting to blur ... ")    
    img = cv2.imread(image_path)
    blur = cv2.blur(img,(5,5))
    cv2.imwrite(target_file, blur)
    chosen_effect_text = "Blur"
  elif chosen_effect == "gaussianblur":
    apply_image_effect_logger.info("Converting to gaussianblur ... ")    
    img = cv2.imread(image_path)
    #blur = cv2.blur(img,(5,5))
    blur_image = cv2.GaussianBlur(img, (7,7), 0)
    #cv2.imshow('Gaussian Blur Image', blur_image)
    #cv2.waitKey(0)
    cv2.imwrite(target_file, blur_image)
    chosen_effect_text = "Gaussian Blur"
  elif chosen_effect == "medianblur":
    apply_image_effect_logger.info("Converting to medianblur ... ")
    img = cv2.imread(image_path)
    #blur = cv2.blur(img,(5,5))
    blur_image = cv2.medianBlur(img, 5)
    #cv2.imshow('Median Blur Image', blur_image)
    #cv2.waitKey(0)
    cv2.imwrite(target_file, blur_image)
    #cv2.imwrite(target_file, blur)
    chosen_effect_text = "Median Blur"
  elif chosen_effect == "grayscale":
    apply_image_effect_logger.info("Converting to grayscale ... ")
    # Convert to Grayscale and save
    new = convert_grayscale(original)
    save_image(new, target_file)
    apply_image_effect_logger.info("Grayscale effect applied!")
    chosen_effect_text = "Gray Scale"
  elif chosen_effect == "sepia":
    apply_image_effect_logger.info("Converting to sepia ... ")
    sepia_img = sepia(image_path)
    save_image(sepia_img, target_file)
    chosen_effect_text = "Sepia"
  elif chosen_effect == "primary":
    apply_image_effect_logger.info("Converting to primary ... ")
    # Convert to Primary and save
    new = convert_primary(original)
    save_image(new, target_file)
    chosen_effect_text = "Primary"
  elif chosen_effect == "gotham":
    apply_image_effect_logger.info("Running Gotham filter ... ")
    target_file = apply_gotham_filter(source_image=image_path, target_file=target_file)
    chosen_effect_text = "Gotham"
  elif chosen_effect == "contour":
    apply_image_effect_logger.info("Converting to contour ... ")
    #original = Image.open(image_path)
    # Convert to Contour and save
    new = original.filter(filter=ImageFilter.CONTOUR)
    save_image(new, target_file)
    chosen_effect_text = "Contour"
  elif chosen_effect == "emboss":
    apply_image_effect_logger.info("Converting to emboss ... ")
    #original = Image.open(image_path)
    # Convert to Contour and save
    new = original.filter(filter=ImageFilter.EMBOSS)
    save_image(new, target_file)
    chosen_effect_text = "Emboss"
  elif chosen_effect == "edge":
    apply_image_effect_logger.info("Converting to edge ... ")
    #original = Image.open(image_path)
    # Convert to Contour and save
    new = original.filter(filter=ImageFilter.EDGE_ENHANCE_MORE)
    save_image(new, target_file)
    chosen_effect_text = "Edge"
  elif chosen_effect == "sharpen":
    apply_image_effect_logger.info("Converting to sharpen ... ")
    #original = Image.open(image_path)
    # Convert to Contour and save
    new = original.filter(filter=ImageFilter.SHARPEN)
    save_image(new, target_file)
    chosen_effect_text = "Sharpen"
  elif chosen_effect == "smooth":
    apply_image_effect_logger.info("Converting to sharpen ... ")
    #original = Image.open(image_path)
    # Convert to Contour and save
    new = original.filter(filter=ImageFilter.SMOOTH_MORE)
    save_image(new, target_file)
    chosen_effect_text = "Smooth"
  elif chosen_effect == "contrast":
    apply_image_effect_logger.info("Converting to contrast ... ")
    original = cv2.imread(image_path)
    contrast_img = cv2.addWeighted(original, 2.5, np.zeros(original.shape, original.dtype), 0, 0)
    cv2.imwrite(target_file, contrast_img)
    #cv2.imshow('Contrast Image', contrast_img)
    #cv2.waitKey(0)
    #original = Image.open(image_path)
    # Convert to Contour and save
    #original.filter(filter=ImageFilter.SMOOTH_MORE).show()
    #save_image(new, target_file)
    chosen_effect_text = "Contrast"
  elif chosen_effect == "cannyedge":
    apply_image_effect_logger.info("Converting to cannyedge ... ")
    original = cv2.imread(image_path)
    edge_img = cv2.Canny(original,100,200)
    #contrast_img = cv2.addWeighted(original, 2.5, np.zeros(original.shape, original.dtype), 0, 0)
    #cv2.imshow('Canny Edge Image', edge_img)
    #cv2.waitKey(0)
    cv2.imwrite(target_file, edge_img)
    #original = Image.open(image_path)
    # Convert to Contour and save
    #original.filter(filter=ImageFilter.SMOOTH_MORE).show()
    #save_image(new, target_file)
    chosen_effect_text = "Canny Edge"
  elif chosen_effect == "denoise":
    apply_image_effect_logger.info("Converting to denoise ... ")
    original = cv2.imread(image_path)
    result = cv2.fastNlMeansDenoisingColored(original,None,20,10,7,21)
    #edge_img = cv2.Canny(original,100,200)
    #contrast_img = cv2.addWeighted(original, 2.5, np.zeros(original.shape, original.dtype), 0, 0)
    #cv2.imshow('Denoised Image', result)
    #cv2.waitKey(0)
    cv2.imwrite(target_file, result)
    chosen_effect_text = "De Noise"
  else:
    apply_image_effect_logger.warning("Unknown Effect requested!")
    return

  apply_image_effect_logger.info("All done applying the effects!")
  apply_image_effect_logger.info("Effect applied to file: %s " % target_file)

  return target_file, chosen_effect_text

# Main
if __name__ == "__main__":

  image_path, chosen_effect = initialize()

  main_logger = logging.getLogger('apply_image_effects.main')
  main_logger.info("In main thread ...")

  main_logger.info("Image: %s, Effect Requested: %s" % (image_path, chosen_effect))

  image_effects_file, chosen_effect_text = apply_image_effect(image_path=image_path, chosen_effect=chosen_effect)

  main_logger.info("Image Effects in file: %s" % image_effects_file)


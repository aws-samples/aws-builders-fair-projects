#
# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Image Utilities.
#
import numpy as np

def transform_image(image):
    r"""
    Transform image for dlr model example.
    """
    image = np.array(image) - np.array([123., 117., 104.])
    image /= np.array([58.395, 57.12, 57.375])
    image = image.transpose((2, 0, 1))
    image = image[np.newaxis, :]
    image = image.astype(np.float32)
    return image

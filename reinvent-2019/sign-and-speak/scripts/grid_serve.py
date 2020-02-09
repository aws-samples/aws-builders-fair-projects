"""Sign & Speak Inference Script

This script defines the methods required by Amazon SageMaker to create an
inference endpoint for the Sign & Speak project. It expects image input,
where each image is a 3x3 grid of video frames, and is stored in an Amazon S3
bucket. The output is the text version of the label and a confidence score.

Input sent to the endpoint should be JSON with the following format:
{'grid': <S3_URI_OF_GRID_IMAGE>}

Output returned will be JSON with the following format:
{'output': <TEXT_LABEL>,
'confidence': <FLOAT_VALUE>}
"""

import json
import logging
import os
import tempfile
import re

import boto3
import torch
from torchvision import transforms
from PIL import Image


logger = logging.getLogger(__name__)
JSON_CONTENT_TYPE = 'application/json'
# Define a data transformation similar to the one used to train the original ResNet model
transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
classes = {}


def model_fn(model_dir):
    """
    Loads the trained model from the model directory.
    """
    logger.info('Loading the model.')
    logger.info(model_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info('Current device: {}'.format(device))
    if device == "cuda":
        model = torch.load(os.path.join(model_dir, 'model.pth')) #GPU
    else:
        model = torch.load(os.path.join(model_dir, 'model.pth'), map_location="cpu") #CPU
    model.to(device).eval()

    logger.info('Loading the classes.')
    global classes
    with open(os.path.join(model_dir, 'class_indices.json'), 'r') as file_handler:
        classes = json.load(file_handler)

    return model


def input_fn(serialized_input_data, content_type=JSON_CONTENT_TYPE):
    """
    Loads the JSON input, fetches the image from S3, and transforms the image.
    """
    logger.info('Deserializing the input data.')
    if content_type == JSON_CONTENT_TYPE:
        # Load JSON input
        input_data = json.loads(serialized_input_data)
        image_loc_s3 = input_data['grid']

        # Fetch bucket and object details
        url_components = re.search("s3://(.+?)/(.*)", image_loc_s3)
        bucket_name = url_components.group(1)
        object_name = url_components.group(2)

        # Load image file from S3 bucket
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'wb') as file_handle:
            s3_client = boto3.client('s3')
            s3_client.download_fileobj(bucket_name, object_name, file_handle)
            image = Image.open(tmp.name)

        # Transform image same as during training
        transformed_image = transform(image)
        model_input = transformed_image.unsqueeze(0)
        return model_input
    raise Exception("Requested unsupported ContentType in content_type: {}".format(content_type))


def output_fn(prediction_output, accept=JSON_CONTENT_TYPE):
    """
    Transforms the model output to return the text label instead of its index. Returns
    the result as JSON.
    """
    logger.info('Serializing the generated output.')
    logger.info("Original output is {}".format(prediction_output))

    # Normalize the confidence value to be a float value between 0 and 1
    normalized_output = torch.nn.functional.softmax(prediction_output[0], dim=0)
    batched_norm = normalized_output.unsqueeze(0)
    values, indices = torch.max(batched_norm.data, 1)

    # Fetch the text label based on the label index
    #classes = {"cat": 0, "eight o clock": 1, "friend": 2, "good how are you": 3, "goodbye": 4, "grandfather": 5, "grandmother": 6, "hello": 7, "pleased to meet you": 8, "pub": 9, "restaurant": 10, "thank you": 11}
    for label, index in classes.items():
        if index == indices.item():
            class_from_idx = label
    
    # Format and return the final result
    if accept == JSON_CONTENT_TYPE:
        return json.dumps({'output': class_from_idx, 'confidence': values.item()}), accept
    raise Exception('Requested unsupported ContentType in Accept: ' + accept)

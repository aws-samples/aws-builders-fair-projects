#!/usr/bin/env python

# This is a build-time script used to download a file
# from S3 and place it in a desired location. It is invoked
# by CMake during build time.

import boto3
import sys
import yaml

def load_config(config_path):
    stream = file(config_path, 'r')
    context = yaml.safe_load(stream)

    required_items = (
        'bucket_name',
        'model_key',
        'region_name'
    )

    if not all(item in context for item in required_items):
        raise ValueError('Config file is missing required items')

    return context

def download_model_from_s3(context, dest_path):
    s3 = boto3.resource('s3',
        region_name=context['region_name'])
    s3.meta.client.download_file(
        Bucket=context['bucket_name'],
        Key=context['model_key'],
        Filename=dest_path)

def main(argv):
    if len(argv) != 3:
        raise ValueError('Model downloader usage: python model_downloader.py config_file_path dest_path')

    source_config = argv[1]
    dest_path = argv[2]

    context = load_config(source_config)

    download_model_from_s3(context, dest_path)

    print 'Successfully downloaded model to ', dest_path

if __name__ == '__main__':
    main(sys.argv)

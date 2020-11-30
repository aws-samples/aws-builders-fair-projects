#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

from botocore.session import Session
import greengrasssdk

import sys
import logging

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client('iot-data')

logger.info('Hello from pinned lambda. Outside of handler.')

# Get creds from TES
# Note: must make sure that creds are not available within local folder
# Can get cred info from /greengrass/var/log/system/tes.log
session = Session()
creds = session.get_credentials()
formatted_creds = """
Access Key: {}\n
Secret Key: {}\n
Session Key: {}\n""".format(creds.access_key, creds.secret_key, creds.token)

# Logging credential information is not recommended. This is for demonstration purposes only.
# logger.info(formatted_creds)


def lambda_handler(event, context):
    logger.debug("Hello from pinned lambda. Inside handler.")
    return

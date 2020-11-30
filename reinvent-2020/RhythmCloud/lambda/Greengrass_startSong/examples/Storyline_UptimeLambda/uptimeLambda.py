#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

import sys
import logging
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client('iot-data')


def uptime_handler(event, context):
    logger.info("Received message!")
    if 'state' in event:
        if event['state'] == "on":
            client.publish(
                topic='/topic/metering',
                payload="Robot arm turned ON")
            logger.info("Triggering publish to topic "
                        "/topic/metering with ON state")
        elif event['state'] == "off":
            client.publish(
                topic='/topic/metering',
                payload="Robot arm turned OFF")
            logger.info("Triggering publish to topic "
                        "/topic/metering with OFF state")

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


def message_handler(event, context):
    logger.info("Received message!")
    if 'state' in event:
        if event['state'] == "on":
            client.update_thing_shadow(
                thingName="RobotArm_Thing",
                payload='{"state":{"desired":{"myState":"on"}}}')
            logger.info("Triggering publish to shadow "
                        "topic to set state to ON")
        elif event['state'] == "off":
            client.update_thing_shadow(
                thingName="RobotArm_Thing",
                payload='{"state":{"desired":{"myState":"off"}}}')
            logger.info("Triggering publish to shadow "
                        "topic to set state to OFF")

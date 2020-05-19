import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './vendored/'))

import greengrasssdk
from water_pump import WaterPumpControl


logger = logging.getLogger()
logger.setLevel(logging.INFO)


logger.info('Initializing WaterPumpControl/handler')


def release_water(event, context):
    """
    Turn on pump releasing water for `WaterPumpControl.RELEASE_DURATION` seconds
    """
    logger.info('Invoked function release_water()')

    pump = WaterPumpControl()
    pump.release()
    return
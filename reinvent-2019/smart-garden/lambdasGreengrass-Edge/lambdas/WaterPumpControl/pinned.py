import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vendored/'))

import json
import logging
import time
from datetime import datetime

from dateutil.parser import parse as parse_date
import greengrasssdk
from water_pump import WaterPumpControl


logger = logging.getLogger()
logger.setLevel(logging.INFO)


PUMP_ACTIVATION_DELTA = 12 * 3600 # in seconds
DATA_FILE = '/home/ggc_user/data.json'


def _write_data(content):
    f = open(DATA_FILE, 'w')
    f.write(json.dumps(content))
    f.close()

def _read_data():
    try:
        f = open(DATA_FILE, 'r')
    except IOError:
        return {}

    try:
        content = json.loads(f.read())
    except ValueError:
        content = {}

    f.close()
    
    return content

def device_boot():
    """
    Starts timer to activate pump every PUMP_ACTIVATION_DELTA hours.

    If for some reason the device gets rebooted during a water release
    it should turn off the pump after being restarted.
    """
    logger.info('Turning pump off after device start')
    
    pump = WaterPumpControl()
    pump.off()

    while True:
        data = _read_data()

        now = datetime.now()
        last_watering = data.get('last_watering')

        if last_watering:
            last_watering = parse_date(last_watering)
        
        if not last_watering or \
            (now - last_watering).seconds > PUMP_ACTIVATION_DELTA:
            # if it was never watered or if last watering is > then max delta,
            # activate pump
            pump.release()

            # updates local data file
            _write_data({
                'last_watering': now.isoformat(),
            })

        logger.info('Sleeping for 30s')
        time.sleep(30)


device_boot()

def pinned_handler(event, context):
    """
    Mock function for pinned/long-lived Lambda
    """
    pass
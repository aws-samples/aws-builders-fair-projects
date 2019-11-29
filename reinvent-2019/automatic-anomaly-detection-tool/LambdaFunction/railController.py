import json
import logging
import os
import time
import sys


RAIL_COMMAND_TOPIC = os.getenv("RAIL_COMMAND_TOPIC", "cmd/rail")
RAIL_THING_NAME = os.getenv("RAIL_THING_NAME", "rail_controller")
RAIL_STATUS_OPEN = "open"
RAIL_STATUS_CLOSE = "close"
RAIL_STATUS_PAYLOAD = {"action":""}

class RailController(object):

    def __init__(self, ggClient):
        self.ggClient = ggClient

    def open_rail(self):
        payload = RAIL_STATUS_PAYLOAD.copy()
        payload["action"] = RAIL_STATUS_OPEN
        self.ggClient.publish(
            topic=RAIL_COMMAND_TOPIC,
            payload=json.dumps(payload)
        )

    def close_rail(self):
        payload = RAIL_STATUS_PAYLOAD.copy()
        payload["action"] = RAIL_STATUS_CLOSE
        self.ggClient.publish(
            topic=RAIL_COMMAND_TOPIC,
            payload=json.dumps(payload)
        )

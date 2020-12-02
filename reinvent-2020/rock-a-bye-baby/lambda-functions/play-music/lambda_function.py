import json
import urllib.request
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)

musicurl = os.environ['musicUrl']

def lambda_handler(event, context):
    logging.info('Received event: ' + json.dumps(event))
    req = urllib.request.Request (musicurl)
    f = urllib.request.urlopen(req)
    response = f.read()
    f.close()
    logging.info("Play music response: " + str(response))

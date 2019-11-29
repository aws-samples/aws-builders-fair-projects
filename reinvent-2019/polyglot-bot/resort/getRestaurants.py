import requests
import re
import json
import boto3
import urllib.request
import time
import logging
from common.iotpublish import *
from common.aurora_dal import *

"""
This function is to call open weather api to get weather detaisl for city passed in
city - city
"""
def getRestaurantsForResort(resortName):
    authToken = os.getEnv('YELP_AUTH_KEY')
    searchResort = resortName+",LasVegas"
    response = requests.get(
          "https://api.yelp.com/v3/businesses/search?location="+searchResort+"&categories=restaurants&sort_by=distance",
          headers={
          "Authorization": authToken
        },
    )
    restResponse = response.json()
    restaurants = list()
    for restaurant in restResponse['businesses']:
        restaurants.append(restaurant["name"])
    #return top 5 only
    return restaurants[:5]

"""
This function is to generate polly message based on weather data
weatherDict - Dictionary containing weather data for city
"""
def generateOutputMessage(resortName,restaurants):    
    text = "{} is a fun place to stay. Here are few restaurant options for your dinner tonight at {}.   ".format(resortName, resortName)
    for restaurant in restaurants:
        text = text + restaurant + ","
    text = text + '. Have a great time in re:Invent!'
    print(text)
    return text


"""
This function is to be invoked when lambda is called
"""
def lambda_handler(event, context):
    print(event)
    txId = begin_transaction()
    transcript_text=event['transcribed_text']
    s3key = event['s3key']
    result = re.search('/(.*)_(.*).wav', s3key)
    languageCode=result.group(1)
    try:
        bot_request_id=int(result.group(2))
        insert_bot_request_steps(bot_request_id, 'resort', s3key, txId)
        print(languageCode)   
        resortName = transcript_text
        print(resortName)
        if resortName in (None, '') or not resortName.strip():
            raise 'Resort not found'
        restaurants = getRestaurantsForResort(resortName)
        print(restaurants)
        outputText = generateOutputMessage(resortName,restaurants)
        generatePollyMessageAndPublish(outputText, languageCode,'goodbye')
        update_bot_request_steps(bot_request_id, resortName, 'resort', txId)
        update_bot_request_resort(bot_request_id, resortName, txId)
        commit_transaction(txId)
    except Exception as e:
        logging.exception(e)
        generatePollyErrorMessageAndPublish(languageCode,'resort')
        rollback_transaction(txId)

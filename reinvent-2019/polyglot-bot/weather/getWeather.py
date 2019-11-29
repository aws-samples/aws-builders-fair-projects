import requests
import re
import json
import pytemperature
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
def city_forecast(city):
    print(city)
    weatherApiKey = os.getenv('WEATHER_API_KEY')
    response = requests.get(
          "https://community-open-weather-map.p.rapidapi.com/weather?q="+city,
          headers={
          "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
          "X-RapidAPI-Key": weatherApiKey
        },
    )  
    weatherDict = response.json()
    print(weatherDict)
    weatherData = {}
    weatherData['desc'] = weatherDict['weather'][0]['description']
    weatherData['currentTemp'] = pytemperature.k2f(weatherDict['main']['temp'])
    weatherData['MinTemp']= pytemperature.k2f(weatherDict['main']['temp_min'])
    weatherData['MaxTemp']=pytemperature.k2f(weatherDict['main']['temp_max'])
    print(weatherData)
    return weatherData


"""
This function is to generate polly message based on weather data
weatherDict - Dictionary containing weather data for city
"""
def generateOutputMessage(weatherDict):
    vegasWeather = city_forecast('LasVegas')
    tempAssesment = 'Colder'
    city = weatherDict['city']
    lang = weatherDict['languageCode']
    current = weatherDict['currentTemp']
    minTemp = weatherDict['MinTemp']
    maxTemp = weatherDict['MaxTemp']
    weatherDesc = weatherDict['desc']
    (translateLang, voice) = getTranslateLangAndPollyVoice(lang)
    if vegasWeather['currentTemp'] > current:
        tempAssesment = 'Hotter'
    text = "{} is a great city. Today's weather at {} is {}. Current temperature at {} is {}.Maximum temperature is {}. Minimum temperature today is {}.Right now, it is {} in Vegas than it is in {}. Which hotel or resort are you staying in?".format(city, city, weatherDesc, city, current,maxTemp, minTemp,tempAssesment,city )
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
        insert_bot_request_steps(bot_request_id, 'weather', s3key, txId)
        print(languageCode)   
        print('transcribe text', transcript_text)
        city = transcript_text
        city = city[:-1] if city.endswith('.') else city
        if city in (None, '') or not city.strip():
            raise 'city not found'
        weatherDict = city_forecast(city)
        weatherDict['city'] = city 
        weatherDict['languageCode'] = languageCode
        outputText = generateOutputMessage(weatherDict)
        generatePollyMessageAndPublish(outputText, languageCode,'resort')
        update_bot_request_steps(bot_request_id, city, 'weather', txId)
        update_bot_request_city(bot_request_id, city, txId)
        commit_transaction(txId)
    except Exception as e:
        logging.exception(e)
        generatePollyErrorMessageAndPublish(languageCode,'weather')
        rollback_transaction(txId)




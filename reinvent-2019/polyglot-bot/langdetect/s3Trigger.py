from __future__ import print_function
import os
import json
import boto3
import time
import urllib
import re
import logging
from datetime import datetime
import random
import string
from boto3.session import Session
from common.iotpublish import *
from common.aurora_dal import *

# Load the libraries
boto3.setup_default_session(region_name='us-west-2')
s3client = boto3.client('s3')
transcribe = boto3.client('transcribe')
lambda_client = boto3.client('lambda')
translate = boto3.client(service_name='translate')
wishList = ['Good Day','Morning','Good Morning','Good Evening','Good Night','Good Afternoon','Nice Day','Hello','Hi ','Hi.','Hey ','Hey.']


queue='queue'
jobdef1='transcribejob:1'

def random_four():
    """Returns a random 4 charactors"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))




def lambda_handler(event, context):
    # TODO implement
    print(event)
    s3bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    s3path = 's3://'+s3bucket+'/'+key
    result = re.search('/(.*).wav', key)
    bot_request_id=int(result.group(1))
    print(bot_request_id)
    realTimeLanguages = ['en-US','es-US',]
    languages = ['de-DE','it-IT','fr-FR','hi-IN','ar-SA','ko-KR','pt-BR','ru-RU']
    txId = begin_transaction()
    try:
        insert_bot_request(bot_request_id,txId)
        insert_bot_request_steps(bot_request_id, 'greetings', s3path, txId)
        for language in languages: 
            job_name = "langdet-transcribe-resort-"+language +"-"+random_four()
            job_uri = s3path
            transcribe.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                MediaFormat='wav',
                LanguageCode=language
            )
            insert_bot_request_lang_detection(bot_request_id, language, txId)
            lambda_payload={}
            lambda_payload['transcription_job_name']=job_name
            lambda_payload['language_code']=language
            lambda_payload['s3_url']=job_uri
            lambda_payload['bot_request_id']=bot_request_id
            invoke_response = lambda_client.invoke(FunctionName="bdfairLangDetection", InvocationType= "Event",Payload= json.dumps(lambda_payload))
        for realTimeLanguage in realTimeLanguages:
            (translateLang, voice) = getTranslateLangAndPollyVoice(realTimeLanguage)
            realtimePayload={}
            realtimePayload['s3Path']= s3path
            realtimePayload['languageCode']=realTimeLanguage
            print('processing realtime for languagecode'+ realTimeLanguage)
            startTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            response = lambda_client.invoke(FunctionName="bdfairRTTranscribe", InvocationType= "RequestResponse",Payload= json.dumps(realtimePayload))
            print(response)
            streamingbody = response['Payload'].read().decode("utf-8")
            streamingbody = streamingbody[:-1] if streamingbody.endswith('.') else streamingbody
            print(streamingbody)
            sql= 'insert into bot_request_lang_detection (bot_request_id,language,transcript_text,start_time,end_time) values (:bot_request_id,:language,:transcript_text,:start_time, now())'
            entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}},
            {'name':'language','value':{'stringValue':f'{realTimeLanguage}'}},
            {'name':'transcript_text','value':{'stringValue':f'{streamingbody}'}},
            {'name':'start_time','value':{'stringValue':f'{startTime}'}}]
            execute_statement(sql, entry, txId)
            if streamingbody:
                if(realTimeLanguage != 'en-US'):
                    translate_dict=translate.translate_text(Text=streamingbody,SourceLanguageCode=translateLang, TargetLanguageCode='en')
                    translate_text = translate_dict['TranslatedText']
                else:
                    translate_text = streamingbody
                print('translated text'+translate_text )
                greeting = False
                update_bot_request_steps(bot_request_id, translate_text, 'greetings', txId)
                if any(x.lower() in translate_text.lower() for x in wishList):
                    greeting = True
                    outputText = "Hello! Welcome to Vegas and welcome to Re Invent. Hope you are having some fun here. Which city are you from?"
                    generatePollyMessageAndPublish(outputText, realTimeLanguage,'weather')
                    update_bot_request_language(bot_request_id,realTimeLanguage,txId)
                    break 
        commit_transaction(txId)
    except Exception as e:
        logging.exception(e)
        generatePollyErrorMessageAndPublish('en-US','greetings')
        rollback_transaction(txId)

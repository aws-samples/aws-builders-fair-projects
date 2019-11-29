from __future__ import print_function
import time
import boto3
import urllib.request
import random
import os
import json
import logging
from common.iotpublish import *
from common.aurora_dal import *


boto3.setup_default_session(region_name='us-west-2')
transcribe = boto3.client('transcribe')
translate = boto3.client(service_name='translate')
wishList = ['Good Day','Morning','Good Morning','Good Evening','Good Night','Good Afternoon','Nice Day','Hello','Hi ','Hi.','Hey ','Hey.']


def checkForLanguageAndRaiseException(bot_request_id):
    bot_language = getBotLanguage(bot_request_id)
    if bot_language in (None, '') or not bot_language.strip():
        jobcount = getPendingLanguageDetectionJobs(bot_request_id)
        if jobcount == 0:
            raise 'No language detected exception'

    

"""
This function is to be invoked when lambda is called
"""
def lambda_handler(event, context):
    job_name=event['transcription_job_name']
    languageCode = event['language_code']
    txId = begin_transaction()
    try:
        s3_url= event['s3_url']
        bot_request_id= event['bot_request_id']
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            data = {}
            bot_language = getBotLanguage(bot_request_id)
            if bot_language:
                break
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED']:
                print('Transcription job succeeded')
                transcriptionUri=status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                print(transcriptionUri)
                webURL = urllib.request.urlopen(transcriptionUri)
                data = webURL.read()
                encoding = webURL.info().get_content_charset('utf-8')
                data = json.loads(data.decode(encoding))
                transcript_text = data['results']['transcripts'][0]['transcript']
                update_text = transcript_text
                if transcript_text:
                    (translateLang, voice) = getTranslateLangAndPollyVoice(languageCode)
                    translate_dict=translate.translate_text(Text=transcript_text,SourceLanguageCode=translateLang, TargetLanguageCode='en')
                    translate_text = translate_dict['TranslatedText']
                    update_text = translate_text
                    greeting = False
                    update_bot_request_steps(bot_request_id, translate_text, 'greetings', txId)
                    if any(x.lower() in translate_text.lower() for x in wishList):
                        greeting = True
                        outputText = "Hello! Welcome to Las Vegas and welcome to ReInvent. Hope you are having a good time here. Which city are you from?"
                        generatePollyMessageAndPublish(outputText, languageCode,'weather')  
                        update_bot_request_language(bot_request_id,languageCode,txId)
                sql= 'update bot_request_lang_detection set end_time=now(), transcript_text=:transcript_text where language=:language and bot_request_id=:bot_request_id'
                entry = [{'name':'bot_request_id','value':{'longValue':bot_request_id}},
                {'name':'transcript_text','value':{'stringValue':f'{update_text}'}},
                {'name':'language','value':{'stringValue':f'{languageCode}'}}]
                execute_statement(sql, entry, txId)
                checkForLanguageAndRaiseException(bot_request_id)    
                break              
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['FAILED']:
                print('Transcription job failed')
                checkForLanguageAndRaiseException(bot_request_id)
                break
            print("Not ready yet...")
            time.sleep(5)
        commit_transaction(txId)
        print(status)
    except Exception as e:
        logging.exception(e)
        generatePollyErrorMessageAndPublish('en-US','greetings')
        rollback_transaction(txId)
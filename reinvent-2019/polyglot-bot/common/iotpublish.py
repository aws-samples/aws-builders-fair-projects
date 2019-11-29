
import json
import boto3
import time

boto3.setup_default_session(region_name='us-west-2')
translate = boto3.client(service_name='translate')
iot = boto3.client('iot-data')
polly = boto3.client('polly')
codes=list()
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='en-US'
translatePollyLanguageCode['translateLang']='en'
translatePollyLanguageCode['pollyVoice']='Joanna'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='hi-IN'
translatePollyLanguageCode['translateLang']='hi'
translatePollyLanguageCode['pollyVoice']='Aditi'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='ko-KR'
translatePollyLanguageCode['translateLang']='ko'
translatePollyLanguageCode['pollyVoice']='Seoyeon'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='ar-SA'
translatePollyLanguageCode['translateLang']='ar'
translatePollyLanguageCode['pollyVoice']='Zeina'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='es-US'
translatePollyLanguageCode['translateLang']='es'
translatePollyLanguageCode['pollyVoice']='Penelope'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='de-DE'
translatePollyLanguageCode['translateLang']='de'
translatePollyLanguageCode['pollyVoice']='Marlene'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='it-IT'
translatePollyLanguageCode['translateLang']='it'
translatePollyLanguageCode['pollyVoice']='Bianca'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='fr-FR'
translatePollyLanguageCode['translateLang']='fr'
translatePollyLanguageCode['pollyVoice']='Celine'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='pt-BR'
translatePollyLanguageCode['translateLang']='pt'
translatePollyLanguageCode['pollyVoice']='Vitoria'
codes.append(translatePollyLanguageCode)
translatePollyLanguageCode = {}
translatePollyLanguageCode['pollyLang']='ru-RU'
translatePollyLanguageCode['translateLang']='ru'
translatePollyLanguageCode['pollyVoice']='Tatyana'
codes.append(translatePollyLanguageCode)

defaultFailureUrl='s3://failure/failure_english.mp3'


def getTranslateLangAndPollyVoice(languageCode):
    for code in codes:
        if code['pollyLang'] == languageCode:
            return (code['translateLang'],code['pollyVoice'])

def publishIoTMessage(s3outputuri, lang, outtype):
    response = iot.publish(
        topic='sdk/test/Python',
        qos=1,
        payload=json.dumps({"s3output":s3outputuri, "language":lang, "type":outtype})
    )
    print('Published topic ')

def generatePollyMessage(text, languageCode,outputType):
    pollyText = text
    (translateLang, voice) = getTranslateLangAndPollyVoice(languageCode)
    if(languageCode != 'en-US'):
        translate_dict=translate.translate_text(Text=text,SourceLanguageCode='auto',TerminologyNames=["ReInvent"], TargetLanguageCode=translateLang)
        translate_text = translate_dict['TranslatedText']
        print('translated text', translate_text)
        pollyText = translate_text 
    response = polly.start_speech_synthesis_task(VoiceId=voice,
                OutputS3BucketName='bdfairdev',
                LanguageCode=languageCode,
                OutputS3KeyPrefix='output/'+outputType,
                OutputFormat='mp3', 
                Text = pollyText)
    taskId = response['SynthesisTask']['TaskId']
    return taskId

def generatePollyMessageAndPublish(text,language, outputType):
     pollyTaskId = generatePollyMessage(text,language,outputType)
     while True:
        task_status = polly.get_speech_synthesis_task(TaskId = pollyTaskId)
        if(task_status['SynthesisTask']['TaskStatus'] == 'completed'):
            s3outputuri = task_status['SynthesisTask']['OutputUri']
            s3url = s3outputuri.replace('https://s3.us-west-2.amazonaws.com/','s3://')
            publishIoTMessage(s3url, language, outputType)
            break
        elif(task_status['SynthesisTask']['TaskStatus'] == 'failed'):
            publishIoTMessage(failureurls[language], language, 'error')
            break

def generatePollyErrorMessageAndPublish(language, outputType):
    text = "Sorry! I did not hear what you said. Can you please repeat?"
    pollyTaskId = generatePollyMessage(text,language)
    while True:
        task_status = polly.get_speech_synthesis_task(TaskId = pollyTaskId)
        if(task_status['SynthesisTask']['TaskStatus'] == 'completed'):
            s3outputuri = task_status['SynthesisTask']['OutputUri']
            s3url = s3outputuri.replace('https://s3.us-west-2.amazonaws.com/','s3://')
            publishIoTMessage(s3url, language, outputType)
            break
        elif(task_status['SynthesisTask']['TaskStatus'] == 'failed'):
            publishIoTMessage(defaultFailureUrl, language, outputType)
            break
from __future__ import print_function
import boto3
import json
import datetime
from pprint import pprint

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "Smart Garden - " + title,
            'content': "Smart Garden - " + output,
            'text': "Smart Garden - " + output,
            'image': {
                'smallImageUrl': 'https://s3.amazonaws.com/bfgg-smartgarden-website/SmartGarden.jpg',
                'largeImageUrl': 'https://s3.amazonaws.com/bfgg-smartgarden-website/SmartGarden.jpg'
            }
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hi! Welcome to the Alexa Smart Garden. " \
                    "Please tell one of these options: water garden, temperature, soil moisture or timelapse. You can also try water flowers and water Groot or I am Groot."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell one of these options: water garden, temperature, soil moisture or timelapse."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Smart Garden!" \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print(intent_name)

    if intent_name == 'PlantWatering':
        return water_garden(intent, session, 'SmartGarden/WaterRelease')
    elif intent_name == 'Temperature':
        return get_temperature(intent, session)
    elif intent_name == 'Timelapse':
        return get_timelapse(intent, session)
    elif intent_name == 'SoilMoisture':
        return get_soil_moisture(intent, session)
    elif intent_name == 'SayHi':
        return say_hi(intent, session)
    elif intent_name == 'groot':
        return water_garden(intent, session,'SmartGarden/groot')
    elif intent_name == 'flowers':
        return water_garden(intent, session, 'SmartGarden/flowers')
    elif intent_name == 'Goodbye':
        return goodbye(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise Exception('Intent with name ' + intent_name + ' not supported')

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def say_hi(intent, session):
    card_title = "Welcome"
    session_attributes = {}
    should_end_session = False

    speech_output = "Ola bom te ver por aqui"
    reprompt_text = "Hi, how are you?"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_temperature(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    temperature = read_s3_data('temperature')

    if temperature=="error":
        speech_output = "Could you try again, please?"
    else:
        speech_output = temperature
    reprompt_text = "Could you repeat, please?"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_soil_moisture(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    #moisture = read_s3_data("moisture")
    #if moisture=='0':
        #speech_output='You need to water your Smart Garden because the humidity is low'
    #elif moisture=='1':
        #speech_output='You do not need to water your smart garden, the humidity is ok'
    #else:
        #speech_output= 'Could you retry, please'

    moisture = read_s3_data("moisture")
    print("Moisture")
    print(moisture)
    moistureNum=int(moisture)
    print(moistureNum)
    if moistureNum>=2747:
        speech_output='You need to water your Smart Garden because the soil is very dry.'
    elif moistureNum>=2501 and moistureNum<2747:
        speech_output='You can water your Smart Garden because the soil is just slight moisture.'
    elif moistureNum>=2108 and moistureNum<2501:
        speech_output='You do not need to water your smart garden, the humidity is ok.'
    elif moistureNum>=1636 and moistureNum<2108:
        speech_output='Better do not water your smart garden, the soil is very moist.'
    elif moistureNum<=1636:
        speech_output='Stop to water your garden right now, the soil is soaking!'
    else:
        speech_output='Could you retry please?'

    reprompt_text = "Could you repeat, please"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_timelapse(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    send_timelapse_email()
    speech_output = "I\'ll generate your Smart Garden Timelapse and send to your e-mail: mariaane16@gmail.com"
    reprompt_text = "Could you repeat, please?"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def goodbye(intent, session):
    card_title = "Session Ended"
    session_attributes = {}
    should_end_session = True

    speech_output = "I'll miss you, see ya..."
    reprompt_text = "Could you repeat, please?"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def water_garden(intent, session, mytopic):
    client = boto3.client('iot-data', region_name='us-east-1')
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "I'm going to water your Smart Garden!"
    reprompt_text = "You can ask me to water your garden to ask me Water Garden."

    client.publish(topic=mytopic, qos=0, payload=json.dumps({"water":"plant"}))

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def read_s3_data(data_type):
    try:
        my_date = datetime.datetime.utcnow()
        my_time = my_date.time()
        my_hour = "{0:0>2}".format(my_time.hour)
        my_minute = "{0:0>2}".format((my_time.minute-2))
        my_minute1 = "{0:0>2}".format((my_time.minute-3))
        my_minute2 = "{0:0>2}".format((my_time.minute-4))
        my_minute3 = "{0:0>2}".format((my_time.minute-5))
        my_second= "{0:0>2}".format(my_time.second)

        my_day = my_date.date()
        my_day_2 = "{0:0>2}".format(my_day.day)
        my_month_2 = "{0:0>2}".format(my_day.month)

        startAfter = str(my_day.year)+"/"+str(my_month_2)+"/"+str(my_day_2)+"/"+str(my_hour)
        contains = str(my_day.year)+"-"+str(my_month_2)+"-"+str(my_day_2)+"-"+str(my_hour)+"-"+str(my_minute)
        contains1 = str(my_day.year)+"-"+str(my_month_2)+"-"+str(my_day_2)+"-"+str(my_hour)+"-"+str(my_minute1)
        contains2 = str(my_day.year)+"-"+str(my_month_2)+"-"+str(my_day_2)+"-"+str(my_hour)+"-"+str(my_minute2)
        contains3 = str(my_day.year)+"-"+str(my_month_2)+"-"+str(my_day_2)+"-"+str(my_hour)+"-"+str(my_minute3)

        s3client = boto3.client('s3', region_name='us-east-1')
        bucket = 'origin of data sensor bucket'

        theobjects = s3client.list_objects_v2(Bucket=bucket, StartAfter=startAfter)

        contains = "no"
        for object in theobjects['Contents']:
            key = object['Key']
            if (contains in key) or (contains1 in key) or (contains2 in key)  or (contains3 in key) :
                contains ="yes"
                data = s3client.get_object(Bucket=bucket, Key=key)
                contents = data['Body'].read()
                longi = len(contents)
                position = contents.find("}",0,longi)+1
                contents1= str(contents[:position])
                try:
                    decoded = json.loads(contents1)
                    if data_type=='temperature':
                        temperature_num = int(decoded['temperature'])+32
                        return "The air temperature is "+ str(temperature_num) + " Fahrenheit degrees and the air humidity is "+ str(decoded['humidity'])+ " percent"
                    elif data_type=='deviceId':
                        return str(decoded['deviceId'])
                    elif data_type=='timestp':
                        return str(decoded['timestp'])
                    elif data_type=='humidity':
                        return str(decoded['humidity'])
                    elif data_type=='moisture':
                        return str(decoded['water_level'])
                except (ValueError, KeyError, TypeError):
                    return "error"
        if contains=="no":
            return "error"
    except (ValueError, KeyError, TypeError):
        return "error"

def send_timelapse_email():
    s3_link = "https://s3.amazonaws.com"
    s3client = boto3.client('s3', region_name='your region eg us-east-1')
    bucket = 'name of the timelapse bucket'

    my_date = datetime.datetime.utcnow()
    my_day = my_date.date()
    my_month_2 = "{0:0>2}".format(my_day.month)

    startAfter = str(my_day.year)+"/"+str(my_month_2)

    theobjects = s3client.list_objects_v2(Bucket=bucket, StartAfter=startAfter)
    key_prefix = s3_link+"/"+bucket
    key=""
    for object in theobjects['Contents']:
        key = object['Key']

    final_key=key_prefix+"/"+key

    SENDER = "Sender Name <sender email here>"
    RECIPIENT = "recipient email here"

    AWS_REGION = "us-east-1"
    SUBJECT = "See your Smart Garden Timelapse!"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("See your Smart Garden Timelapse: " + final_key + " \r\n"
        "This email was sent with Amazon SES using the "
        "AWS SDK for Python (Boto)."
        )

    # The HTML body of the email.
    BODY_HTML = """<html>
        <head></head>
        <body>
        <h1>See your Smart Garden Timelapse: <a href='"""+ final_key +"""'>Smart Garden Video</a></h1>

        <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
            """
    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
           )
    # Display an error if something goes wrong.
    except ClientError as e:
        return "error"
    else:
        return "error"

import math
import dateutil.parser
import datetime
import time
import os
import logging
import json
import boto3
import time
import datetime
from pprint import pprint
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {
                'contentType': 'PlainText',
                'content': message
                }
        }
    }
    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """
def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def validate_order_flowers(flower_type, date, pickup_time):
    flower_types = ['lilies', 'roses', 'tulips']
    if flower_type is not None and flower_type.lower() not in flower_types:
        return build_validation_result(False,
                                       'FlowerType',
                                       'We do not have {}, would you like a different type of flower?  '
                                       'Our most popular flowers are roses'.format(flower_type))

    if date is not None:
        if not isvalid_date(date):
            return build_validation_result(False, 'PickupDate', 'I did not understand that, what date would you like to pick the flowers up?')
        elif datetime.datetime.strptime(date, '%Y-%m-%d').date() <= datetime.date.today():
            return build_validation_result(False, 'PickupDate', 'You can pick up the flowers from tomorrow onwards.  What day would you like to pick them up?')

    if pickup_time is not None:
        if len(pickup_time) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'PickupTime', None)

        hour, minute = pickup_time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'PickupTime', None)

        if hour < 10 or hour > 16:
            # Outside of business hours
            return build_validation_result(False, 'PickupTime', 'Our business hours are from ten a m. to five p m. Can you specify a time during this range?')

    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """
def order_flowers(intent_request):
    """
    Performs dialog management and fulfillment for ordering flowers.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    flower_type = get_slots(intent_request)["FlowerType"]
    date = get_slots(intent_request)["PickupDate"]
    pickup_time = get_slots(intent_request)["PickupTime"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        validation_result = validate_order_flowers(flower_type, date, pickup_time)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        if flower_type is not None:
            output_session_attributes['Price'] = len(flower_type) * 5  # Elegant pricing model

        return delegate(output_session_attributes, get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Thanks, your order for {} has been placed and will be ready for pickup by {} on {}'.format(flower_type, pickup_time, date)})


def water_plant(intent_request, mytopic):
    client = boto3.client('iot-data', region_name='us-east-1')
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    client.publish(topic=mytopic, qos=0, payload=json.dumps({"water":"plant"}))

    #response = {
     #   'sessionAttributes':
     #       { 'key1': 'value1' },
     #   'dialogAction': {
     #       'type': 'Close',
     #       'fulfillmentState': 'Fulfilled',
     #       'message': {
     #           'contentType': 'PlainText',
     #           'content': 'I am going to water your plant!'
     #           }
     #       }
     #   }

    message= 'I am going to water your plant!'
    return close({ 'key1': 'value1' }, 'Fulfilled', message)

def say_hi(intent_request):
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    message = 'Hi! How are you? I\'m the Smart Garden Bot, say me what do you want? Water garden, Timelapse, Temperature or Soil Moisture?'
    return close({ 'key1': 'value1' }, 'Fulfilled', message)

def get_temperature(intent_request):
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    #Call local GG Lambda that reads the temperature
    temperature = read_s3_data('temperature')
    if temperature == "error":
        message = "Could you retry please?"
    else:
        message= temperature
    return close({ 'key1': 'value1' }, 'Fulfilled', message)

def get_soil_moisture(intent_request):
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    #response1 = client.get_thing_shadow(thingName='#')
    #streamingBody = response1["payload"]
    #jsonState = json.loads(streamingBody.read())
    #print jsonState

    #Call local GG Lambda that reads the Soil Moisture
    moisture = read_s3_data("moisture")
    moistureNum=int(moisture)
    print(moistureNum)
    if moistureNum>=2747:
        message='You need to water your Smart Garden because the soil is very dry.'
    elif moistureNum>=2501 and moistureNum<2747:
        message='You can water your Smart Garden because the soil is just slight moisture.'
    elif moistureNum>=2108 and moistureNum<2501:
        message='You do not need to water your smart garden, the humidity is ok.'
    elif moistureNum>=1636 and moistureNum<2108:
        message='Better do not water your smart garden, the soil is very moist.'
    elif moistureNum<=1636:
        message='Stop to water your garden right now, the soil is soaking!'
    else:
        message='Could you retry please?'

    return close({ 'key1': 'value1' }, 'Fulfilled', message)

def get_timelapse(intent_request):
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    #Get Timelapse
    send_timelapse_email()
    message='I\'ll generate your Smart Garden Timelapse and send to your e-mail: mariaane16@gmail.com'
    return close({ 'key1': 'value1' }, 'Fulfilled', message)

def goodbye(intent_request):
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    message='I\'ll miss you. Bye... see ya!'
    return close({ 'key1': 'value1' }, 'Fulfilled', message)


""" --- Intents --- """
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'PlantWatering':
        return water_plant(intent_request, 'SmartGarden/WaterRelease')
    elif intent_name == 'Temperature':
        return get_temperature(intent_request)
    elif intent_name == 'Timelapse':
        return get_timelapse(intent_request)
    elif intent_name == 'SoilMoisture':
        return get_soil_moisture(intent_request)
    elif intent_name == 'SayHi':
        return say_hi(intent_request)
    elif intent_name == 'groot':
        return water_plant(intent_request, 'SmartGarden/groot')
    elif intent_name == 'flowers':
        return water_plant(intent_request, 'SmartGarden/flowers')
    elif intent_name == 'Goodbye':
        return goodbye(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)

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
        bucket = 'bucket name here'

        print "startAfter "+ str(startAfter)

        theobjects = s3client.list_objects_v2(Bucket=bucket, StartAfter=startAfter)

        print "theobjects "+ str(theobjects)
        #for o in theobjects.get('CommonPrefixes'):
           #print 'sub folder : ', o.get('Prefix')

        print "contains "+ str(contains)
        print "contains1 "+ str(contains1)
        print "contains2 "+ str(contains2)
        print "contains3 "+ str(contains3)

        contains = "no"
        for object in theobjects['Contents']:
            key = object['Key']
            print "key " + str(key)
            if (contains in key) or (contains1 in key) or (contains2 in key)  or (contains3 in key) :
                contains ="yes"
                print "Contains"
                data = s3client.get_object(Bucket=bucket, Key=key)

                contents = data['Body'].read()
                longi = len(contents)
                position = contents.find("}",0,longi)+1
                contents1= str(contents[:position])
                print "contents "+ str(contents1)
                try:
                    decoded = json.loads(contents1)
                    print decoded #json.dumps(decoded, sort_keys=True, indent=4)
                    #print "Device ID: ", decoded['deviceId']
                    #print "Humidity: ", decoded['humidity']
                    #print "Moisture: ", decoded['moisture']
                    #print "Temperature: ", decoded['temperature']
                    #print "Timestamp: ", decoded['timestp']
                    #print "Water level: ", decoded['water_level']
                    #print "Complex JSON parsing example: ", decoded['two']['list'][1]['item']

                    if data_type=='temperature':
                        temperature_num = (int(decoded['temperature'])*1.8) +32
                        return "The air temperature is "+ str(temperature_num) + " Fahrenheit degrees and the air humidity is "+ str(decoded['humidity'])+"%"
                    elif data_type=='deviceId':
                        return str(decoded['deviceId'])
                    elif data_type=='timestp':
                        return str(decoded['timestp'])
                    elif data_type=='humidity':
                        return str(decoded['humidity'])
                    elif data_type=='moisture':
                        return str(decoded['water_level'])
                except (ValueError, KeyError, TypeError):
                    print "error "
                    return "error"
        if contains=="no":
            print "Not contains"
            return "error"
    except Exception as e:
        print "error 1 "+str(e)
        return "error"

def send_timelapse_email():
    s3_link = "https://s3.amazonaws.com"
    s3client = boto3.client('s3', region_name='us-east-1')
    bucket = 'generated timelapse S3 bucket name'

    my_date = datetime.datetime.utcnow()
    my_day = my_date.date()
    my_month_2 = "{0:0>2}".format(my_day.month)

    startAfter = str(my_day.year)+"/"+str(my_month_2)

    theobjects = s3client.list_objects_v2(Bucket=bucket, StartAfter=startAfter)
    key_prefix = s3_link+"/"+bucket
    key=""
    print theobjects['Contents']
    for object in theobjects['Contents']:
        key = object['Key']

    print "Prefix "+ str(key_prefix)
    print " Key "+ str(key)

    final_key=key_prefix+"/"+key
    print "final_key " + str(final_key)

    SENDER = "Sender Name <sender email>"
    RECIPIENT = "recipient email"

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
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

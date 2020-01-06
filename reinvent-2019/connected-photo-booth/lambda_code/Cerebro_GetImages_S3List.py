import boto3
import json
import os
import logging

from contextlib import closing

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from random import shuffle

import time

__CLOUDFRONT_URL__ = "https://d1urhfgpizyj5c.cloudfront.net/"

dynamo = boto3.client('dynamodb')
tagged_faces = []
logger = None

print("In initialize fn ...")

logger = logging.getLogger()
if int(os.environ['DEBUG_MODE']):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
        
logger.info("Initialize: Just a test")
logger.debug("Initialize: debug a test")

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        },
    }

def get_images_list(profile_name='', ignore_stock_profiles=False):

    logger.debug("In get_images_list ...")

    # strategy is to do a search in stored media and find all profiles tagged
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cerebro_media')
    if profile_name:
        fe = Key('external_image_id').begins_with('production') & Attr('rec_type').begins_with('file_metadata') & Attr('profile_matched_string').contains(profile_name)
    else:
        fe = Key('external_image_id').begins_with('production') & Attr('rec_type').begins_with('file_metadata')

    pe = "#extid, #profmatchstr,#rectype,#captext,#capaudio,#profmatch"
    # Expression Attribute Names for Projection Expression only.
    ean = { 
        "#extid": "external_image_id", 
        "#profmatchstr": "profile_matched_string",
        "#rectype": "rec_type",
        "#captext": "caption_text",
        "#capaudio": "caption_audio",
        "#profmatch": "profile_matched"
    }
    esk = None

    exclusive_start_key = None
    
    result_set = []
    
    while True:
        logger.debug("Start Key: %s" % exclusive_start_key)
        
        if exclusive_start_key:
            #
            response = table.scan(
            FilterExpression=fe,
            #KeyConditionExpression=Key('external_image_id').begins_with('profile')
            ProjectionExpression=pe,
            ExpressionAttributeNames=ean,
            ExclusiveStartKey=exclusive_start_key
            )

        else:
            response = table.scan(
            FilterExpression=fe,
            #KeyConditionExpression=Key('external_image_id').begins_with('profile')
            ProjectionExpression=pe,
            ExpressionAttributeNames=ean
            )

        logger.debug("Response, itemcount")
        logger.debug(response)
        logger.debug(len(response['Items']))
        
        result_set += response['Items']
            
        #ExclusiveStartKey
        if "LastEvaluatedKey" in response:
            exclusive_start_key = response["LastEvaluatedKey"]
            logger.debug("New Start Key: %s" % exclusive_start_key)
        else:
            logger.debug("No more items to read")
            break
        
    logger.debug("Out of get_images_list loop now ...")
    logger.debug(result_set)
    logger.debug(len(result_set))

    if len(result_set) < 1:
        logger.debug("ERROR: No user content located. Exiting !")
        return ''
        
    if ignore_stock_profiles:
        print("working on the ignore stock profiles: ")
        stock_profiles_list = os.environ["STOCK_PROFILES"].split("&")
        print(stock_profiles_list)
        filtered_result_set = []
        for item in result_set:
            print(item)
            uses_stock_profile = None
            for profile in item["profile_matched"]:
                if profile in stock_profiles_list:
                    print("this belongs to a stock profile")
                    uses_stock_profile = True
                    break
                else:
                    print("this doesn't belong to a stock profile")
                    uses_stock_profile = False
                    
            if uses_stock_profile == False:
                filtered_result_set.append(item)
                
        print("The filtered list :")
        print(filtered_result_set)
        
        return filtered_result_set

    return result_set
    
def generate_caption(tagged_face_list, album="Unknown"):
    logger.debug(tagged_face_list)
    
    # confirm if the tagged faces was sent properly
    if not tagged_face_list:
        logger.debug("No Faces Provided")
        return "No Faces provided"
    
    faces = ""
    # now walk thru' the list of tagged faces
    for face in tagged_face_list:
        if face.lower().startswith("unknown"):
            continue
        
        if faces:
            faces += ", "
        faces += "%s" % face
    
    caption_text = "Found %s ." % (faces)

    return caption_text
            
def generate_audio(audioKey, textMessage, pollyVoice=os.environ["POLLY_VOICE"]):

    logger.debug("In generate_welcome_audio ...")
    logger.debug(textMessage)
    logger.debug(pollyVoice)
    
    rest = textMessage
    
    #Because single invocation of the polly synthesize_speech api can 
    # transform text with about 1,500 characters, we are dividing the 
    # post into blocks of approximately 1,000 characters.
    textBlocks = []
    while (len(rest) > 1100):
        begin = 0
        end = rest.find(".", 1000)

        if (end == -1):
            end = rest.find(" ", 1000)
            
        textBlock = rest[begin:end]
        rest = rest[end:]
        textBlocks.append(textBlock)
    textBlocks.append(rest)            

    logger.debug(textBlocks)

    #For each block, invoke Polly API, which will transform text into audio
    polly = boto3.client('polly')
    isNewFile = True
    for textBlock in textBlocks: 
        logger.debug("Polly is processing:  %s" % textBlock)
        response = polly.synthesize_speech(
            OutputFormat='mp3',
            Text = textBlock,
            VoiceId = pollyVoice
        )
        
        logger.debug(response)
        
        # set the write mode if it is a new file or not
        if isNewFile:
            write_mode = "wb"
            isNewFile = False
        else:
            write_mode = "ab"
        
        #Save the audio stream returned by Amazon Polly on Lambda's temp 
        # directory. If there are multiple text blocks, the audio stream
        # will be combined into a single file.
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join("/tmp/", audioKey)
                with open(output, write_mode) as file:
                    file.write(stream.read())

    logger.debug("Finished the audio generating now ...")
    audio_s3key = os.environ['AUDIO_CONTENT_DIR'] + "/" + audioKey + ".mp3"
    
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/' + audioKey, 
      os.environ['BUCKET_NAME'], 
      audio_s3key)
    '''
    s3.put_object_acl(ACL='public-read', 
      Bucket=os.environ['BUCKET_NAME'], 
      Key=welcome_audio_s3key)
    '''
    
    logger.debug("The s3 file should be ready now !")
    return audio_s3key

def is_randomize_requested(body_params):
    logger.debug("In is_randomize_requested ...")

    randomize_requested = False
    if "image_randomize" in body_params and body_params['image_randomize']:
        if int(body_params['image_randomize']):
            logger.debug("request from body params")
            randomize_requested = True
        else:
            logger.debug("detected in body param but false")
    elif (int(os.environ["IMAGE_RANDOMIZE"])):
        logger.debug("Sys param evaluated to true")
        randomize_requested = True

    return randomize_requested

def get_max_items(body_params):
    logger.debug("In get_max_items ...")

    get_max_items = 0
    if "image_max_count" in body_params and body_params['image_max_count']:
        get_max_items = int(body_params['image_max_count'])

        if get_max_items:
            logger.debug("image_max_count from body params: %d" % get_max_items)
        else:
            logger.debug("detected in body param but false")
    elif (int(os.environ["IMAGE_MAX_COUNT"])):
        get_max_items = int(os.environ["IMAGE_MAX_COUNT"])
        logger.debug("Sys param evaluated to true: %s" % get_max_items)

    return get_max_items

def main_optimized(event, context):
    
    logger.info("In main_optimized ...")
    start_time = int(round(time.time() * 1000))

    body_params = json.loads(event["body"])
    logger.debug("Body params:")
    logger.debug(body_params)

    checkpoint_time = int(round(time.time() * 1000))
    logger.debug("Checkpoint1: %d" % (checkpoint_time - start_time))
    start_time = checkpoint_time
    faces_matched_list = []

    if "ignore_stock_profiles" in body_params and body_params['ignore_stock_profiles']:
        ignore_stock_profiles = True
    else:
        ignore_stock_profiles = False


    if "profile" in body_params and body_params['profile']:
        logger.info("Profile requested: %s" % body_params['profile'])
        # now to get the media content matching this profile (face)
        profile_name = body_params['profile'].lower()
        logger.debug("Profile mapped to: %s" % profile_name)

        faces_matched_list = get_images_list(profile_name=profile_name)
        logger.info("The full s3 listing to be returned ...")
        logger.debug(faces_matched_list)
            
    else:
        # this means the full list must be returned
        faces_matched_list = get_images_list(profile_name='', ignore_stock_profiles=ignore_stock_profiles)
        logger.info("The full s3 listing to be returned ...")
        logger.debug(faces_matched_list)

    checkpoint_time = int(round(time.time() * 1000))
    logger.debug("Checkpoint2: %d" % (checkpoint_time - start_time))
    start_time = checkpoint_time

    # check if randomize is needed
    randomize_requested = is_randomize_requested(body_params)

    logger.info("now doing the actual randomize as requested ...")
    if randomize_requested:
        # now randomize list 
        shuffle( faces_matched_list )
        logger.info("Randomized List : ")
        logger.debug(faces_matched_list)
        logger.debug(type(faces_matched_list))
    else:
        logger.info("no randomize requested!")

    checkpoint_time = int(round(time.time() * 1000))
    logger.debug("Checkpoint3: %d" % (checkpoint_time - start_time))
    start_time = checkpoint_time

    # now limit the array
    logger.debug("Total Count of Items detected: %d" % len(faces_matched_list))
    faces_matched_list = faces_matched_list[:get_max_items(body_params)]
    logger.debug("Total Count of Items detected: %d" % len(faces_matched_list))

    checkpoint_time = int(round(time.time() * 1000))
    logger.debug("Checkpoint4: %d" % (checkpoint_time - start_time))
    start_time = checkpoint_time

    # now do the face matching logic
    face_list_returned = []

    if "ignore_stock_profiles" in body_params and body_params['ignore_stock_profiles']:
        ignore_stock_profiles = True
    else:
        ignore_stock_profiles = False

    logger.info("Now finalizing audio and captions ...")
    for matched_image in faces_matched_list:
        logger.info("Matched Image is: %s" % matched_image)
        # now get the matched face images now

        if 'profile_matched_string' in matched_image:
            contained_faces = matched_image['profile_matched_string'].split('&')
        else:
            contained_faces = ''

        logger.debug("The list exists too: ")
        if 'profile_matched' in matched_image:
            logger.debug(matched_image['profile_matched'])
            logger.debug(type(matched_image['profile_matched']))

        logger.debug("Retrieved the contained Faces as : ")
        logger.debug(contained_faces)
        unique_faces = list(set(contained_faces))
        logger.debug("Unique Faces: ")
        logger.debug(unique_faces)
        
        if 'external_image_id' in matched_image:
            image_id = matched_image['external_image_id'].split('/')[1]
        else:
            image_id = ''

        logger.debug("IMAGE ID: %s" % image_id)

        # generate the caption based on the tagged faces and album
        album_name = "Not Implemented Yet"
        #caption_text = generate_caption(contained_faces, album_name)
        #caption_text = generate_caption(unique_faces, album_name)
        if 'caption_text' in matched_image:
            caption_text = matched_image['caption_text']
        else:
            caption_text = ''
        logger.debug("Caption Text: %s" % caption_text)

        #caption_audio = generate_audio(audioKey=image_id, textMessage=caption_text)
        if 'caption_audio' in matched_image:
            caption_audio = matched_image['caption_audio']
        else:
            caption_audio = ''

        logger.debug("The key for caption audio is: %s" % caption_audio)

        face_item = {
            "image_id": image_id,
            "image_key": matched_image['external_image_id'],
            #"image_face_tags": contained_faces,
            "image_face_tags": unique_faces,
            #"image_in_album": album_name,
            "image_caption": caption_text,
            "image_caption_audio": caption_audio
        }

        logger.info("Constructed item: ")
        logger.info(face_item)

        face_list_returned.append(face_item)
        #return

        logger.debug("next image ...")

    checkpoint_time = int(round(time.time() * 1000))
    logger.debug("Checkpoint5: %d" % (checkpoint_time - start_time))
    start_time = checkpoint_time

    logger.info("Done with main_optimized version!")

    # 3. return this set of photos
    return respond(None, face_list_returned)

def lambda_handler(event, context):
    #return main(event, context)
    #initialize()
    return main_optimized(event, context)

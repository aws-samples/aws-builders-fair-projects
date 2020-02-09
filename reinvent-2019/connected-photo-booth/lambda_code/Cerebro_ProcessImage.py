from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib
import os
from datetime import datetime
from contextlib import closing


from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

print('Loading function')

rekognition = boto3.client('rekognition')
ddb_table_name = os.environ['CEREBRO_TABLE']

# --- utils ----
def get_list_of_tagged_faces():

    print("In get_list_of_tagged_faces ...")
    # strategy is to do a search in stored media and find all profiles tagged
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cerebro_media')
    #fe = Key('external_image_id').begins_with('profile');
    fe = Attr('external_image_id').begins_with('profile') & Attr('rec_type').begins_with('file_metadata')
    pe = "#extid, #profile, #faceid, #imageid"
    # Expression Attribute Names for Projection Expression only.
    ean = { 
        "#extid": "external_image_id", 
        "#profile": "profile",
        "#faceid": "FaceId",
        "#imageid": "ImageId"
    }
    esk = None

    exclusive_start_key = None
    
    result_set = []
    
    while True:
        print("Start Key : %s" % exclusive_start_key)
        
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
    
        print("Response, Itemcount")
        print(response,len(response['Items']))
        
        result_set += response['Items']
            
        #ExclusiveStartKey
        if "LastEvaluatedKey" in response:
            exclusive_start_key = response["LastEvaluatedKey"]
            print("New Start Key : %s" % exclusive_start_key)
            #print(exclusive_start_key)
        else:
            print("No more items to iterate over ...")
            break
        
    print("Out of loop of getting the list of profiled faces now ...")
    print(result_set)
    print(len(result_set))

    if len(result_set) < 1:
        print("ERROR: No user content located. Exiting !")
        return ''
        
    return result_set


# --------------- Helper Functions to call Rekognition APIs ------------------


def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def detect_labels(bucket, key, profile_name=""):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    label_entry = {}
    label_entry["Labels"] = getFaceAttribute(response,attribute="Labels",is_array_type=True,value_key="Name", confidence_level=50)
    label_entry["ExternalImageId"] = os.path.basename(key)
    
    print(label_entry)
    
    table = boto3.resource('dynamodb').Table(ddb_table_name)
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    current_time = datetime.utcnow()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    current_time_epoch = current_time.strftime("%s")
        
    print(current_time_epoch)
    (dt, micro) = current_time_str.split('.')
    dt = "%s.%s" % (current_time_epoch, micro)
    print(dt,micro)

    current_time_epoch = Decimal(dt)
    print(current_time_epoch) 

    ddb_item = {}
    ddb_item['external_image_id'] = key
    ddb_item['epoch'] = current_time_epoch
    ddb_item['current_time'] = current_time_str
    ddb_item['Labels'] = label_entry["Labels"]
    ddb_item["rec_type"] = "image_labels"
    
    if profile_name:
        ddb_item['profile'] = profile_name
        
    print(ddb_item)
    
    table.put_item(Item=ddb_item)

    return label_entry

def generate_caption(tagged_face_list, album="Unknown"):
    print(tagged_face_list)
    
    # confirm if the tagged faces was sent properly
    if not tagged_face_list:
        print("No Faces Provided")
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

    print("In generate_welcome_audio ...")
    print(textMessage, pollyVoice, audioKey)
    imageid = audioKey.split('/')[1]
    print("Imageid: %s" % imageid)
    
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

    print(textBlocks)

    #For each block, invoke Polly API, which will transform text into audio
    polly = boto3.client('polly')
    isNewFile = True
    for textBlock in textBlocks: 
        print("Polly is processing:  %s" % textBlock)
        response = polly.synthesize_speech(
            OutputFormat='mp3',
            Text = textBlock,
            VoiceId = pollyVoice
        )
        
        print(response)
        
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
                output = os.path.join("/tmp/", imageid)
                with open(output, write_mode) as file:
                    file.write(stream.read())

    print("Finished the audio generating now ...")
    audio_s3key = os.environ['AUDIO_CONTENT_DIR'] + "/" + imageid + ".mp3"
    
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/' + imageid, 
      os.environ['BUCKET_NAME'], 
      audio_s3key)
    
    print("The s3 audio file should be ready now !")
    return audio_s3key

def insert_file_metadata(key, s3_metadata):

    table = boto3.resource('dynamodb').Table(ddb_table_name)

    current_time = datetime.utcnow()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    current_time_epoch = current_time.strftime("%s")
        
    print(current_time_epoch)
    (dt, micro) = current_time_str.split('.')
    dt = "%s.%s" % (current_time_epoch, micro)
    print(dt,micro)

    current_time_epoch = Decimal(dt)
    print(current_time_epoch) 

    ddb_item = {}
    ddb_item['external_image_id'] = key
    ddb_item['epoch'] = current_time_epoch
    ddb_item['current_time'] = current_time_str
    ddb_item["rec_type"] = "file_metadata"
    
    if "exif_data" in s3_metadata:
        ddb_item["exif_data"] = s3_metadata["exif_data"]
    if "file_datetime" in s3_metadata:
        ddb_item["original_datetime"] = s3_metadata["file_datetime"]
    if "file_datetime_epoch" in s3_metadata:
        ddb_item["original_datetime_epoch"] = s3_metadata["file_datetime_epoch"]
    if "profile" in s3_metadata:
        ddb_item["profile"] = s3_metadata["profile"]
        #
        ddb_item["profile_owner"] = s3_metadata["profile"]
    else:
        # now construct the profile list
        profile_list = matchImageToProfile(key)
        print("Retrieved list of profiles as: ")
        print(profile_list)
        profile_list_str = '&'.join(profile for profile in profile_list)
        print("Profiles merged is: %s" % profile_list_str)

        ddb_item["profile_matched"] = profile_list
        ddb_item["profile_matched_string"] = profile_list_str

        # also generate the caption text
        ddb_item["caption_text"] = generate_caption(tagged_face_list=profile_list)
        
        # next up - caption audio file
        ddb_item["caption_audio"] = generate_audio(audioKey=key, textMessage=ddb_item["caption_text"])

    print(ddb_item)
    
    response = table.put_item(Item=ddb_item)

    return response

def index_faces(bucket, key, profile_name=""):

    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    collectionId = os.environ["REKO_COLLECTION"]
    response = rekognition.index_faces(
                Image={"S3Object": {"Bucket": bucket, "Name": key}}, 
                CollectionId=collectionId, 
                ExternalImageId=os.path.basename(key), 
                DetectionAttributes=['ALL','DEFAULT']
                )
    
    print("Response from indexingfaces ...")
    print(response)
    
    sortkey = 2

    for face in response["FaceRecords"]:
        face_entry = {}
        print('--------------------------')
        
        del face["FaceDetail"]["Landmarks"]
        del face["FaceDetail"]["BoundingBox"]
        del face["FaceDetail"]["Pose"]
        del face["Face"]["BoundingBox"]
                
        face_entry["Eyeglasses"] = getFaceAttribute(face["FaceDetail"], "Eyeglasses")
        face_entry["Sunglasses"] = getFaceAttribute(face["FaceDetail"], "Sunglasses")
        face_entry["Gender"] = getFaceAttribute(face["FaceDetail"], "Gender")
        
        eyesOpen = getFaceAttribute(face["FaceDetail"], "EyesOpen")
        #face_entry["EyesOpen"] = getFaceAttribute(face["FaceDetail"], "EyesOpen")
        print(eyesOpen)
        if isinstance(eyesOpen,(bool)):
            face_entry["EyesOpen"] = eyesOpen
        
        smileValue = getFaceAttribute(face["FaceDetail"], "Smile")
        #face_entry["Smile"] = getFaceAttribute(face["FaceDetail"], "Smile")
        print(smileValue)
        if isinstance(smileValue,(bool)):
            face_entry["Smile"] = smileValue
        
        face_entry["MouthOpen"] = getFaceAttribute(face["FaceDetail"], "MouthOpen")
        face_entry["Mustache"] = getFaceAttribute(face["FaceDetail"], "Mustache")
        face_entry["Beard"] = getFaceAttribute(face["FaceDetail"], "Beard")

        face_entry["Emotions"] = getFaceAttribute(face["FaceDetail"], "Emotions", value_key="Type", is_array_type=True)

        face_entry["AgeRange_High"] = face["FaceDetail"]["AgeRange"]["High"]
        face_entry["AgeRange_Low"] = face["FaceDetail"]["AgeRange"]["Low"]
        face_entry["Sharpness"] = face["FaceDetail"]["Quality"]["Sharpness"]
        face_entry["Brightness"] = face["FaceDetail"]["Quality"]["Brightness"]
        
        face_entry["FaceId"] = face["Face"]["FaceId"]
        face_entry["ExternalImageId"] = face["Face"]["ExternalImageId"]
        face_entry["Confidence"] = face["Face"]["Confidence"]
        face_entry["ImageId"] = face["Face"]["ImageId"]

        table = boto3.resource('dynamodb').Table(ddb_table_name)
        #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
        current_time = datetime.utcnow()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        current_time_epoch = current_time.strftime("%s")
        
        print(current_time_epoch)
        (dt, micro) = current_time_str.split('.')
        dt = "%s.%s" % (current_time_epoch, micro)
        print(dt,micro)

        current_time_epoch = Decimal(dt)
        print(current_time_epoch) 
        
        face_entry['epoch'] = current_time_epoch
        face_entry['current_time'] = current_time_str
        face_entry['external_image_id'] = key
        del face_entry['ExternalImageId']
        
        face_entry['Confidence'] = Decimal(face_entry['Confidence'])
        face_entry['Brightness'] = Decimal(face_entry['Brightness'])
        face_entry['Sharpness'] = Decimal(face_entry['Sharpness'])        
        
        if profile_name:
            face_entry['profile'] = profile_name
            # the above is for backward compat. . 
            # really maps to the profile name for the picture submmitted as the profile
            face_entry['profile_owner'] = profile_name
            
        face_entry["rec_type"] = "face_attributes"
        
        print(face_entry)
        
        table.put_item(Item=face_entry)
        
        sortkey += 1
        
    return response

def matchImageToProfile(imageKey=None):
    
    print("In matchImageToProfile ...")

    if not imageKey:
        return ["Invalid Image ID"]

    # first get a list of all available profile images
    print("Getting the profile images now ...")
    profile_images = get_list_of_tagged_faces()
    print("The list of profile images are ...")
    print(profile_images)

    print("imageKey: %s" % imageKey)
    profile_list = []
    # next for each profile image
    ## run a compare with the latter as the source and the imageKey as the target
    for image in profile_images:
        print("Profile Image to be compared against: ")
        print(image)

        response = rekognition.compare_faces(
            SourceImage={
                'S3Object': {
                    'Bucket': 'project-cerebro',
                    'Name': image['external_image_id']
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': 'project-cerebro',
                    'Name': imageKey
                }
            },
            SimilarityThreshold=75.0
        )        

        matched_faces = response['FaceMatches']
        print("The Compare Faces Response matches ...")
        print(matched_faces)
        if matched_faces:
            print("Located a match. Match: %s" % image['profile'])
            profile_list.append(image['profile'])

    print("List of Profiles: ", profile_list)

    if profile_list:
        return profile_list

    return ["Unknown"]

def getFaceAttribute(face_detail,attribute,value_key="Value",confidence_key="Confidence",is_array_type=False,confidence_level=80):
    if attribute:
        if attribute in face_detail:
            if is_array_type:
                print(face_detail[attribute])
                item_list = []
                for entry in face_detail[attribute]:
                    print(entry)
                    if entry[confidence_key] > confidence_level:
                        item_list.append(entry[value_key])
                print(item_list)
                return item_list
                
            else:
                if face_detail[attribute][confidence_key] > confidence_level:
                    return face_detail[attribute][value_key]
                
# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''

    print("Received event: " + json.dumps(event, indent=2))
    key  = event['Records'][0]['s3']['object']['key']
    filenames = os.path.splitext(key)

    file_extension = filenames[1][1:]
    print (file_extension)
    valid_extensions = ['JPG','JPEG','PNG']
    
    if file_extension.upper() in valid_extensions:
        print("This is a valid Image file!")
        # now check for the 
        if (key.startswith('production') or key.startswith('staging') or key.startswith('profiles') or key.startswith('dev')):
            print('Triggered by a staging file upload. Good to go!')
        else:
            print('Triggered by a non-staging file upload. Exiting!')
            return
    else:
        print("This is a invalid Image file!")
        return

    print("All Checks passed - onwards ...")

    # extract the metadata
    s3 = boto3.resource('s3')
    print("Getting the metadata ... ")
    #  get the metadata from the s3 object as well
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    response = s3.Object(bucket_name, key)
    print(response)
    print(response.metadata)
    s3_metadata = response.metadata
    
    # now copy to production if staging object
    if key.startswith('dev'):

        # extract eTag id , bucket name, first
        eTagID = event['Records'][0]['s3']['object']['eTag']
        
        new_key = "%s/%s.%s" % ("staging",eTagID,file_extension)
        
        s3_metadata["original_filename"] = key
        
        copy_source_data = {'Bucket': '%s' % (bucket_name), 'Key': "%s" % key}
        print(eTagID, bucket_name, key, file_extension, new_key, copy_source_data)
        
        print("Copying object to production now ...")
        # copy to production bucket
        
        print("Copy/delete completed!")
        return 

    # now copy to production if staging object
    if key.startswith('staging'):

        # extract eTag id , bucket name, first
        eTagID = event['Records'][0]['s3']['object']['eTag']
        
        new_key = "%s/%s.%s" % ("production",eTagID,file_extension)
        
        s3_metadata["original_filename"] = key
        
        copy_source_data = {'Bucket': '%s' % (bucket_name), 'Key': "%s" % key}
        print(eTagID, bucket_name, key, file_extension, new_key, copy_source_data)
        
        print("Copying object to production now ...")
        # copy to production bucket
        
        response = s3.Object(bucket_name, new_key).copy_from(CopySource=copy_source_data, Metadata=s3_metadata, MetadataDirective='REPLACE')
        print(response)
        
        # delete staging object
        response = s3.Object(bucket_name, key).delete()
        print(response)
        print("Copy/delete completed!")
        return 
    
    # Get the object from the event
        
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))

    # setup for profile photo if sent over
    profile_name=""
    if key.startswith('profiles'):
        if "profile" in s3_metadata:
            profile_name = s3_metadata["profile"]
        else:
            profile_name = os.path.splitext(os.path.basename(key))[0]
        print(profile_name)

    try:

        # insert metadata and original file details
        response = insert_file_metadata(key, s3_metadata)
        print(response)
        
        # Calls rekognition DetectLabels API to detect labels in S3 object
        response = detect_labels(bucket, key, profile_name=profile_name)
                
        # Calls rekognition IndexFaces API to detect faces in S3 object and index faces into specified collection
        response = index_faces(bucket, key, profile_name=profile_name)
        
        print("Completely processed image and persisted metadata into DDB")

        return response

    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

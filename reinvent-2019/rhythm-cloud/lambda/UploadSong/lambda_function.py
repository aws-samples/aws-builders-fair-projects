import boto3
import uuid
import base64
import email.parser

BUCKET_NAME = 'rhythmcloud-songs'
def lambda_handler(event, context):
    rawBody = event['body-json']
    content_type = event['params']['header']['content-type']
    body_content = base64.b64decode(rawBody)
#    body_content = event['body-json']
    body_content_plus_headers = bytes('content-type: '+content_type+'\n'+'\n', 'utf-8') + body_content
#    print("bodycontentwithcontentype:",body_content_plus_headers)
    msg = email.parser.BytesParser().parsebytes(body_content_plus_headers)
#    msg2 = email.message_from_string(msg.get_payload())
    headers = event['headers']
    
#    print("headers",event['headers'])
    print("content-type:",content_type)
#    print("event", event)
#    print("raw msg:",msg)
    print("msg ismultipart:",msg.is_multipart())
#    print("msg2 ismultipart:",msg2.is_multipart())
#    print("msg:", str(msg))
    file_content = msg.get_param('content')
    print("file_content=",file_content)
    print("file name0", msg.get_payload(0).get_filename())
    print("file name1", msg.get_payload(1).get_filename())
    
    print("song name0", msg.get_payload(0).get_all('Content-Disposition'))
    print("song name1", msg.get_payload(1).get('Content-Disposition'))
    
    if (not msg.get_payload(1).get_filename()):
       fileName = msg.get_payload(0).get_filename()
       file_content = msg.get_payload(0).get_payload()

    if (not msg.get_payload(0).get_filename()):
       fileName = msg.get_payload(1).get_filename()
       file_content = msg.get_payload(1).get_payload()
       
    if ('name="songName"' in msg.get_payload(0).get('Content-Disposition')):
        dispositions = msg.get_payload(0).get('Content-Disposition').strip().split(";")
        songName = msg.get_payload(0).get_payload()
       
    if ('name="songName"' in msg.get_payload(1).get('Content-Disposition')):
       dispositions = msg.get_payload(1).get('Content-Disposition').strip().split(";")    
       songName = msg.get_payload(1).get_payload()     
       
       
       
#    songName = msg.get_param('songName')
    print("song name:",songName)
#    fileName = msg.get_filename()
    print("file name:", fileName)
    
#    print("payload[0]:",msg.get_payload(0))
#    print("payload[1]:",msg.get_payload(1))
#    print("payload[2]:",msg.get_payload(2))
#    print("payload[1]:",msg.get_payload(1))
       
#    for part in msg.get_payload():
#        partPayload = part.get_payload(decode=True)
#        print("part:",part)
        
#    print({
#        part.get_param('name', header='content-disposition'): part.get_payload(decode=True)
#            for part in msg.get_payload()
#    })
#    songName = 'takeonmid.mid' #event['songName']
    file_path = str(fileName)
    s3 = boto3.client('s3')
#    try:
    s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=file_content)
    print("s3response:",s3_response)
#        print("file_content=",file_content)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('RhythmCloudSongs')
    response = table.put_item(
        Item={
            's3url': str(fileName), 
            'Title': str(songName),
            'id': str(uuid.uuid1())
        }
    )
    print("response=",response)

#    except Exception as e:
#        raise IOError(e)
    return {
        'statusCode': 200,
        'body': {
            'file_path': file_path
        }
    }
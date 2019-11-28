import boto3
import json

print('Loading function')
dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    print('Getting songs')
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('RhythmCloudSongs')
    
    print("RhythmCloud Songs")
    
    response = table.scan()
    
    beatList = []
    data = []
    
    for i in response['Items']:
         row = [i['Title'], str(i['id']),i['s3url'],i['fileType']]
        
    
#        data.append([{
#                "beatName": i['Title'],
#                "id": str(i['id']),
#                "s3url: i['s3url'],
#            }])
         data.append(row)
#    print (json.dumps(data))
    beatList = {'aaData' : data }
#    return json.dumps(beatList, sort_keys=False, indent=4, separators=(',', ': '))
    return beatList
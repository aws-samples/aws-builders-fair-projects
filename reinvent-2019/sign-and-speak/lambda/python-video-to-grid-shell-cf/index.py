import json
import os
import boto3


def lambda_handler(event, context):
    # TODO implement

    recordInfo = event["Records"][0]
    #print ('records info : ')
    #print (recordInfo)
    
    s3Info = recordInfo["s3"]
    #print ('s3event info : ')
    #print(s3Info)
    
    bucketInfo = s3Info["bucket"]
    #print ('bucket info : ')
    #print (bucketInfo)
    
    bucketName = bucketInfo["name"]
    print ('bucket Name : ' + bucketName)
    #print (bucketName)
    
    objectInfo = s3Info ["object"]
    #print ('objectInfo : ')
    #print (objectInfo)
    
    
    
    key = objectInfo["key"]
    print ("key : " + key)
    #print (key )  02_app/upload/hello.mp4

    split = key.split('/')
    filename =  split[2]
    print (filename)


    
    s3 = boto3.client('s3')
    ##reinvent-signs-data/02_app/upload/hello.mp4    


    #Download the video to /tmp folder
    s3.download_file(bucketName, key, '/tmp/' + filename)
    
    # Copy all the scripts over to /tmp
    os.system('cp testscript.sh /tmp/testscript.sh')
    os.system('cp video_to_grid.sh /tmp/video_to_grid.sh')
    os.system('cp frame_picker.py /tmp/frame_picker.py')
    os.system('cp /opt/ffmpeg-git-20190826-amd64-static2/ffmpeg /tmp/ffmpeg')    
    os.system('echo copy done')


    cmd = '/usr/bin/bash /tmp/testscript.sh '+ filename
    os.system(cmd)
    
    stream = os.popen('echo Returned output')
    output = stream.read()
    print(output)
    
    
    
    #hello_grid.png
    #/02_app/grid-image/lambda_grid.png

    split = filename.split('.')
    filenameonlywithoutextension = split[0]
    print('ready to upload grid file : ' + filenameonlywithoutextension)

    response = s3.upload_file('/tmp/' + filenameonlywithoutextension + '_grid.png', bucketName, '02_app/grid-image/' + filenameonlywithoutextension + '_grid.png')
    
    print('Uploaded grid image success')
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

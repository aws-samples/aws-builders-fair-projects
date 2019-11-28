#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassHelloWorld.py
# Demonstrates a simple publish to a topic using Greengrass core sdk
# This lambda function will retrieve underlying platform information and send
# a hello world message along with the platform information to the topic
# 'hello/world'. The function will sleep for five seconds, then repeat.
# Since the function is long-lived it will run forever when deployed to a
# Greengrass core.  The handler will NOT be invoked in our example since
# the we are executing an infinite loop.

import greengrasssdk
import platform
from threading import Timer
from subprocess import check_output
from multiprocessing import Process
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from pid import PidFile

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('RhythmCloudSongs')
s3 = boto3.resource('s3')

def start_record_drums(sessionId, song = "/home/pi/song.mid", duration="30"):
    print('function start_record_drum')
    print('start_record_drum for sessionId:', sessionId)
    print("start_record_drums for song:", song)
    print("start_record_drums for duration:", duration)
    try:
       out = check_output(['/usr/bin/python','/home/pi/respondToHitCloud.py',str(duration),song,sessionId])
       print("recording complete out:",out)
    except:
        print("Error running respondToHitCloud!")




# When deployed to a Greengrass core, this code will be executed immediately
# as a long-lived lambda function.  The code will enter the infinite while
# loop below.
# If you execute a 'test' on the Lambda Console, this test will fail by
# hitting the execution timeout of three seconds.  This is expected as
# this function never returns a result.

def greengrass_hello_world_run(event,context):
    if not my_platform:
        client.publish(
            topic='hello/world',
            payload='Hello world! Sent from Greengrass Core - not really running on the pi. Something is amiss.')
    else:
# start playing the song
#       subprocess.call(['python','/home/pi/metronome.py', '120'])
# fire up all of the listeners for the song on each drum
        print(str(event))
        songId = event['state']['reported']['play']
        print("songId:",songId)
        duration = event['state']['reported']['duration']
        print("duration:",duration)
        tempo = event['state']['reported']['tempo']
        print("tempo=",tempo)
        sessionId = event['state']['reported']['sessionId']
        print("sessionId:",sessionId)
        print("Getting sondId from dynamo",songId)
        response = table.query(
           KeyConditionExpression=Key('id').eq(songId)
        )
        if (len(response['Items']) == 0):
           print("Error song not found!")
           return {
               'error':'songId not found please check it exists'
           }

        print("found song in db:",response['Items'])
        filename = response['Items'][0]['s3url']
#        filename = "song.mid"
        print("Getting filename:",filename)

#        filename = "/home/pi/"+
        s3.Bucket("rhythmcloud-songs").download_file(filename,"/home/pi/"+filename)
        print("downloaded file:",filename)

        try:
            drum1 = Process(target=start_record_drums, args=(sessionId,filename,duration))
            drum1.start()
        except:
            print("Error running record drums!")

        try:
            out = check_output(['/usr/bin/python','/home/pi/midiplay.py',str(duration),"/home/pi/"+filename,sessionId,str(tempo)])
            print(out)
        except:
            print('Error running midiplay!')
# start lambda for each instrument to start to listen and transmit to queue
        client.publish(
            topic='hello/world',
            payload='Music Trainer started ')


    # Asynchronously schedule this function to be run again in 5 seconds
#    Timer(5, greengrass_hello_world_run).start()


# Start executing the function above
#greengrass_hello_world_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    with PidFile():
       greengrass_hello_world_run(event, context)
    return

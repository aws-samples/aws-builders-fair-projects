#!/usr/bin/python3

import boto3
import argparse
import logging
#import pygame
from time import sleep
from mutagen.mp3 import MP3
import math
import subprocess
import os.path

from time import gmtime, strftime

from cerebro_utils import *

from config import Configuration

# --------- Module- Level Globals ---------------
config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

'''
__TMP_DIR__ = "../assets/audio"
__CEREBRO_LOGS_DIR__ = "/tmp/project_cerebro/logs"
'''

'''
def generate_audio(voice_id='Joanna', speech_text='sample text', filename='speech.mp3'):

    generate_audio_logger = logging.getLogger('generate_audio.generate_audio')
    generate_audio_logger.info("Starting the generate_audio method ...")

    polly_client = boto3.Session().client('polly')
    generate_audio_logger.info("Now, going to synthesize_speech with polly")
    file_path = "%s/%s" % (__TMP_DIR__, filename)
    generate_audio_logger.info("\n\nFile path: " + str(file_path) + "\n\n")
    
    
    if os.path.isfile(file_path):
        print("\n\ngenerate_audio.py -- File already exists locally, not calling Polly..")
    else:
        print("\n\nFile does not exist..")

        response = polly_client.synthesize_speech(VoiceId=voice_id,
            OutputFormat='mp3',
            TextType='ssml',
            Text = '<speak><break time="1s"/>' + speech_text + '</speak>')

        generate_audio_logger.info("Next, call to polly completed - now to stream the audio file ...")
        file = open(file_path, 'wb')
        file.write(response['AudioStream'].read())
        file.close()
        generate_audio_logger.info("Finally, audio file is written and ready @ %s" % file_path)

    return file_path


def play_audio(file_path='', delay_secs=0):
    play_audio_logger = logging.getLogger('generate_audio.play_audio')
    play_audio_logger.info("Starting the play_audio method ...")

    play_audio_logger.info("File_path provided : %s" % file_path)   
    if not file_path:
        play_audio_logger.error("No file_path provided!")
        return False

    mp3_util = "sudo mpg321"
    status = subprocess.call(
        '%s %s' %
        (mp3_util, file_path),
        shell=True)

    if delay_secs:
        play_audio_logger.info("Sleeping for %d secs" % delay_secs)
        sleep(delay_secs)
    else:
        audio = MP3(file_path)
        audio_ts = math.ceil(audio.info.length)
        play_audio_logger.info("Duration computed as : %d. Sleeping for this duration only ..." % audio_ts)
        sleep(audio_ts)

    play_audio_logger.info("done here. audio played ?")
    return True
'''

def initialize():

    parser = argparse.ArgumentParser()
    parser.add_argument("--logfile", help="Logfile for all INFO/DEBUG level logs")
    parser.add_argument("--voiceid", help="Provide an AWS Polly VoiceId" )
    parser.add_argument("--text", help="Provide the text to be converted" )
    parser.add_argument("--filename", help="Provide the filename to be used" )
    parser.add_argument("--delay", help="Provide a delay to wait till the audio is completed" )
    parser.add_argument("--debug", help="debug mode to not run scripts", action='store_true')
    args = parser.parse_args()

    # and now setup the logging profile
    # set up logging to file - see previous section for more details
    if args.logfile:
        logFile = args.logfile
    else:
        current_time = strftime("%Y_%m_%dT%H_%M_%S", gmtime())
        logFile = '%s/generate_audio_%s.log' % (config.__CEREBRO_LOGS_DIR__, current_time)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=logFile,
                        filemode='w')
    
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    #logging.getLogger('').addHandler(console)

    # Now, define a couple of other loggers which might represent areas in your
    # application:
    initialize_logger = logging.getLogger('generate_audio.initialize')

    initialize_logger.info(args)

    if not args.text:
        initialize_logger.error("No Text for audio to be generated!")
        exit(1)

    if args.voiceid:
        voice_id = args.voiceid
    else:
        voice_id = 'Joanna'

    if args.filename:
        speech_file = args.filename
    else:
        speech_file = "speech.mp3"
    
    if args.delay:
        delay_secs = int(args.delay)
    else:
        delay_secs = 0

    if args.debug:
        debug_mode = True
    else:
        debug_mode = False

    return voice_id, args.text, speech_file, delay_secs, debug_mode

if __name__ == "__main__":

    voice_id, speech_text, speech_file, delay_secs, debug_mode = initialize()

    main_logger = logging.getLogger('generate_audio.main')
    main_logger.info("In main thread ...")
    main_logger.info("%s, %s, %s" % (voice_id, speech_text, speech_file))

    speech_file_path = generate_audio(voice_id=voice_id,speech_text=speech_text, filename=speech_file)
    main_logger.info("Generated Audio now. Playing audio next ...")

    if not debug_mode:
        play_audio(file_path=speech_file_path, delay_secs=delay_secs)
        main_logger.info("Audio played. Done!")
    else:
        main_logger.info("In Debug mode, so not playing back audio")

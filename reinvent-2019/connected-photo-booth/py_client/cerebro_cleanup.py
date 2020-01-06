#!../venv/bin/python3

from __future__ import print_function # Python 2/3 compatibility

import boto3
import os
import json
import time

from PIL import Image
import piexif

from datetime import datetime
from time import sleep

import pyexifinfo as p
import argparse

import logging

import glob

import hashlib

import sqlite3

import subprocess

from subprocess import Popen, PIPE, STDOUT

import boto3
import json
import sys
import decimal
from boto3.dynamodb.conditions import Key, Attr

import shutil

from config import Configuration

# --------- Module- Level Globals ---------------

# Create an S3 client
s3 = boto3.client('s3')

cleanup_logger = None

config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

'''
# AWS RESOURCE: Switch
__QUEUE_CLIENT_URL__ = "https://queue.amazonaws.com/456038447595/cerebro_client"
__QUEUE_REQUESTS_URL__ = "https://queue.amazonaws.com/456038447595/cerebro_requests"
__SQS_QUEUE_NAME__ = 'cerebro_client'
__APIGW_X_API_KEY__ = "2YSoTXerhD4u3iat9CWUM9kn756MTJIp4c4Tgfqk"
__APIGW_API__ = "https://lqhvtjhlsc.execute-api.us-east-1.amazonaws.com/production/Cerebro_GetImages_S3List"
__S3_BUCKET__ = "project-cerebro"
__DDB_TABLE__ = "cerebro_media"

__TMP_DIR__ = "/tmp/project_cerebro"
__LOGS_DIR__ = "logs"
__PROFILES_DIR__ = "profiles"
__MEDIA_DIR__ = "media"
__SYSTEM_DIR__ = "system"
'''

def delete_local_store():

	cleanup_logger = logging.getLogger('cerebro_cleanup.delete_local_store')

	# now setup the connection/cursor
	db_file = "cerebro.db"
	conn = sqlite3.connect(db_file)

	c = conn.cursor()

	cleanup_logger.info("DB cursor created")

	dml_sql = ' DELETE FROM media_files '

	c.execute(dml_sql)
	conn.commit()
	
	cleanup_logger.info("Deleted local store items")

	return True

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def process_ddb_items(response, table):

	cleanup_logger = logging.getLogger('cerebro_cleanup.process_ddb_items')

	cleanup_logger.info("In process_ddb_items")

	for count, i in enumerate(response['Items']):

		response = table.delete_item(Key={
			'external_image_id': i["external_image_id"],
			'epoch': i["epoch"]
		})

		if ((count+1) % config.__CADENCE__) == 0:
			cleanup_logger.info("\nDeleted Item: %d" % (count+1))
		else:
			print('. ', end="")
			sys.stdout.flush()

	cleanup_logger.info("Processed Items")


def get_ddb_items(prefix='production'):

	cleanup_logger = logging.getLogger('cerebro_cleanup.get_ddb_items')

	cleanup_logger.info("In get_ddb_items")

	cleanup_logger.info("Retrieving DDB Items for prefix: %s" % prefix)

	dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

	table = dynamodb.Table(config.__DDB_TABLE__)

	fe = Key('external_image_id').begins_with(prefix);
	pe = "#epoch, #current_time, #external_image_id"
	# Expression Attribute Names for Projection Expression only.
	ean = { "#epoch": "epoch", "#current_time": "current_time", "#external_image_id": "external_image_id" }
	esk = None

	response = table.scan(
		FilterExpression=fe,
		ProjectionExpression=pe,
		ExpressionAttributeNames=ean,
		)

	process_ddb_items(response, table)

	while 'LastEvaluatedKey' in response:
		cleanup_logger.info("\n---------- NEXT SET -----------")
		response = table.scan(
			ProjectionExpression=pe,
			FilterExpression=fe,
			ExpressionAttributeNames= ean,
			ExclusiveStartKey=response['LastEvaluatedKey']
			)

		process_ddb_items(response, table)

	cleanup_logger.info("\nAll items were retrieved now!")

def setup_db():

	cleanup_logger = logging.getLogger('cerebro_cleanup.setup_db')

	db_file = "cerebro.db"

	conn = sqlite3.connect(db_file)

	create_table_sql = """ CREATE TABLE IF NOT EXISTS media_files (
								id integer PRIMARY KEY,
								file_name text NOT NULL,
								md5_hash text,
								file_type text,
								current_state text,
								last_updated integer,
								last_updated_dt text
							);
						"""
	cleanup_logger.debug("SQL to be used for creating table is: \n%s" % create_table_sql)

	c = conn.cursor()
	c.execute(create_table_sql)

	cleanup_logger.info("DB and table created now!")

	return

def log_subprocess_output(pipe):
	cleanup_logger = logging.getLogger('cerebro_cleanup.log_subprocess_output')

	# b'\n'-separated lines
	for line in iter(pipe.readline, b''):
		cleanup_logger.info('%r', str(line.strip()))

def process_command(cmd_line):

	cleanup_logger = logging.getLogger('cerebro_cleanup.process_command')

	cleanup_logger.info("In process_command")

	if not cmd_line:
		print("Error! No command provided")
		return

	cmd_array = cmd_line.split(" ")

	cleanup_logger.info("Before Popen")
	#process = Popen(aws_cmd, stdout=PIPE, stderr=STDOUT)
	process = subprocess.Popen(cmd_array, stdout=PIPE, stderr=PIPE)

	with process.stdout:
		log_subprocess_output(process.stdout)
	exitcode = process.wait() # 0 means success
	cleanup_logger.info("Exitcode: %d" % int(exitcode))

	return True

def delete_local_files(image_dir=''):
	delete_media_logger = logging.getLogger('cerebro_cleanup.delete_local_files')

	delete_media_logger.info("Entered the delete local files handler ...")
	delete_media_logger.info(image_dir)
	files = glob.glob('%s/*' % image_dir)
	delete_media_logger.info("Files listing to be deleted ...")
	delete_media_logger.info(files)
	for file in files:
		os.remove(file)
	delete_media_logger.info("all files deleted now")

def reset_local_dirs():

	reset_local_dirs_logger = logging.getLogger('cerebro_cleanup.reset_local_dirs')
	reset_local_dirs_logger.info("Entered the reset_local_dirs function ...")

	# cleanup dir, if needed
	image_dir = config.__CEREBRO_TEMP_DIR__

	reset_local_dirs_logger.info("Checking for the dir now ...")
	does_dir_exist = os.path.exists(image_dir)

	if does_dir_exist:
		reset_local_dirs_logger.info("the dir exists: %s" % image_dir)
		# now delete dir
		shutil.rmtree(image_dir)
		reset_local_dirs_logger.info("dir tree now deleted.")
	else:
		reset_local_dirs_logger.info("the dir doesn't exist: %s" % image_dir)

	reset_local_dirs_logger.info("Creating the dir tree now ...")
	# now create dir tree
	os.makedirs(image_dir, mode=0o777)
	os.makedirs("%s" % (config.__CEREBRO_LOGS_DIR__), mode=0o777)
	os.makedirs("%s" % (config.__CEREBRO_MEDIA_DIR__), mode=0o777)
	os.makedirs("%s" % (config.__CEREBRO_PROFILES_DIR__), mode=0o777)
	os.makedirs("%s" % (config.__CEREBRO_SYSTEM_DIR__), mode=0o777)

	reset_local_dirs_logger.info("Dir tree all created now. Done with the reset_dirs")
	return True

def cleanup_data():
	cleanup_logger = logging.getLogger('cerebro_cleanup.cleanup_data')

	cleanup_logger.info("In Cleanup_data")

	#aws_cmd_line = "aws s3 ls"
	#process_command(aws_cmd_line)

	# Delete s3 files from profiles
	aws_cmd_line = "aws s3 rm s3://project-cerebro/profiles/ --recursive"
	process_command(aws_cmd_line)
	# Delete s3 files from production
	aws_cmd_line = "aws s3 rm s3://project-cerebro/production/ --recursive"
	process_command(aws_cmd_line)
	# Delete s3 files from staging
	aws_cmd_line = "aws s3 rm s3://project-cerebro/staging/ --recursive"
	process_command(aws_cmd_line)

	# Delete reko collection & create a new collection
	aws_cmd_line = "aws rekognition delete-collection --collection-id Cerebro"
	process_command(aws_cmd_line)
	aws_cmd_line = "aws rekognition create-collection --collection-id Cerebro"
	process_command(aws_cmd_line)
	aws_cmd_line = "aws rekognition list-faces --collection-id Cerebro"
	process_command(aws_cmd_line)

	# Delete all DDB entries
	cleanup_logger.info("Starting the DDB Deletion Script ...")
	get_ddb_items(prefix='production')
	get_ddb_items(prefix='profile')
	cleanup_logger.info("Complete the DDB Deletion!")

	# Delete all local sqlite DB entries
	delete_local_store()
	cleanup_logger.info("Complete the local sqlite3 DB deletion!")

	# now delete the local files in the tmp dir and create if none exists
	reset_local_dirs()
	cleanup_logger.info("Reset the local dirs!")

	##
	cleanup_logger.info("Cleanup completed!")

	return True

def initialize():

	init_status = False
	parser = argparse.ArgumentParser()
	parser.add_argument("--logfile", help="Logfile for all INFO/DEBUG level logs")
	args = parser.parse_args()

	# and now setup the logging profile
	# set up logging to file - see previous section for more details
	if args.logfile:
		logFile = args.logfile
	else:
		logFile = '/tmp/cerebro_cleanup.log'

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
	logging.getLogger('').addHandler(console)

	# Now, define a couple of other loggers which might represent areas in your
	# application:

	cleanup_logger = logging.getLogger('cerebro_cleanup.initialize')

	cleanup_logger.info("In initiailize fn")

	# now setup the database as well
	setup_db()

	init_status = True
	return init_status

if __name__ == "__main__":

	init_status = initialize()
	cleanup_logger = logging.getLogger('cerebro_cleanup.main')
	cleanup_logger.info("Completed the initialize ...")
	cleanup_logger.info("Init: %d" % (init_status))

	if init_status:
		cleanup_logger.info("Successful Init.")
		cleanup_data()
		#processFiles(scan_only=scan_mode, retry_mode=retry_mode)
		cleanup_logger.info("Completely uploaded files")

	cleanup_logger.info("=============================")
	cleanup_logger.info("Media Uploading Finished!")




#!../venv/bin/python3

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

from pathlib import Path

from config import Configuration

# --------- Module- Level Globals ---------------
# Create an S3 client
s3 = boto3.client('s3')

image_dir = ""

sqs_logger = None
uploads_logger = None

config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

'''
# AWS RESOURCE: Switch
__QUEUE_URL__ = "https://sqs.us-east-1.amazonaws.com/456038447595/cerebro_requests"
__S3_BUCKET_NAME__ = "project-cerebro"
'''

def rotate_jpeg(filename, manifest_mode=False):
	global image_dir

	uploads_logger = logging.getLogger('media_downloader.rotate_jpeg')

	#print(filename)
	#print(image_dir)

	exif_dict = {}
	dt_str = ""
	dt_epoch = None

	target_file = filename

	uploads_logger.info("Opening image: %s" % filename)
	img = Image.open(filename)
	if "exif" in img.info:
		uploads_logger.debug("exif exists")
		exif_dict = piexif.load(img.info["exif"])
		#print(exif_dict)

		# extract the datetime from the tags, if available
		if 36867 in exif_dict['Exif'].keys():
			uploads_logger.debug(exif_dict['Exif'][36867])
			exif_dt_str = exif_dict['Exif'][36867].decode("utf-8")
			uploads_logger.debug(exif_dt_str)
			date_str = exif_dt_str.split()[0].replace(":","-")
			uploads_logger.debug(date_str)
			dt_str = "%sT%s" % (date_str,exif_dt_str.split()[1])
			uploads_logger.debug(dt_str)

			#check for valid format
			dt_str_tokens = dt_str.split("-")
			if len(dt_str_tokens) == 3:
				if (int(dt_str_tokens[0]) > 0) and (int(dt_str_tokens[1]) > 0):

					uploads_logger.info("Validated Timestamp ...")
					utc_time = datetime.strptime(
						dt_str,
						"%Y-%m-%dT%H:%M:%S")
					uploads_logger.info(utc_time)

					epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
					dt_epoch = epoch_time

		else:
			file_stats = os.stat(filename)
			uploads_logger.debug(file_stats)
			file_mod_epoch = "%d" % file_stats.st_mtime
			dt_str = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(file_stats.st_mtime))
			dt_epoch = file_stats.st_mtime

		uploads_logger.debug(dt_str)

		exif_dict.pop("thumbnail")

		uploads_logger.info("Now checking if the orientation exists ...")
		if piexif.ImageIFD.Orientation in exif_dict["0th"]:
			uploads_logger.debug("orientation attributes exists")
			orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)

			# HACK to avoid the error due to a misformatted exif tag
			if 41729 in exif_dict['Exif'].keys():
				exif_dict['Exif'].pop(41729)
			
			exif_bytes = piexif.dump(exif_dict)

			uploads_logger.debug(orientation)
			# HACK on 07/19/2019 to avoid the rotate since its messing things up!!
			'''
			if orientation == 1:
				uploads_logger.debug("detected orientation 1 ... rotating now!")
				img = img.rotate(-90, expand=True)
			elif orientation == 2:
				img = img.transpose(Image.FLIP_LEFT_RIGHT)
			elif orientation == 3:
				img = img.rotate(180)
			elif orientation == 4:
				img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
			elif orientation == 5:
				img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
			elif orientation == 6:
				img = img.rotate(-90, expand=True)
			elif orientation == 7:
				img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
			elif orientation == 8:
				img = img.rotate(90, expand=True)
			'''

			uploads_logger.debug("just before saving ... ")
			target_file = "/tmp/%s" % os.path.basename(filename)

			#img.save(target_file)
			img.save(target_file, exif=exif_bytes)
			uploads_logger.info("Saved new file ...")

		else:
			uploads_logger.debug("no orientation attributes")
		
	else:
		uploads_logger.info("... fallback calc of file datetime")
		file_stats = os.stat(filename)
		uploads_logger.debug(file_stats)
		file_mod_epoch = "%d" % file_stats.st_mtime
		dt_str = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(file_stats.st_mtime))
		dt_epoch = file_stats.st_mtime

	uploads_logger.debug(dt_str)
	uploads_logger.debug(dt_epoch)

	# now extract the exif_dict using the alt method
	exif_dict = p.get_json(filename)[0]
	#print(exif_dict)

	file_info = {}
	file_info["target_file"] = target_file
	file_info["exif_dict"] = exif_dict
	# create an epoch date
	epoch_dt_str = datetime.utcfromtimestamp(0).strftime("%m-%d-%YT%H:%M:%S")
	epoch_val = 0

	if not dt_str:
		dt_str = epoch_dt_str
		uploads_logger.debug(dt_str)
	file_info["datetime_str"] = dt_str

	if not dt_epoch:
		dt_epoch = epoch_val
		uploads_logger.debug(dt_epoch)
	file_info["datetime_epoch"] = dt_epoch

	# now setup the album tags
	uploads_logger.info("Now figuring out album tags ...")
	album_tags = {}
	#print(filename)

	uploads_logger.debug(manifest_mode)
	uploads_logger.debug(image_dir)

	if manifest_mode:
		# generate a fake imagedir for the file
		image_dir = os.path.dirname(filename)

	path_tokens = filename.split("%s/" % image_dir)[1]
	#print(path_tokens.split("/"))
	for index, token in enumerate(path_tokens.split("/")):
		if not Path(token).suffix:
			#print("this is an album tag: %s" % token)
			album_tag = "album_tag_%02d" % (index+1)
			album_tags[album_tag] = token
	
	#print(album_tags)
	file_info["album_tags"] = album_tags
	#print(file_info.keys())

	return file_info

def getFilesListing(
	manifest_file="", 
	images_source_dir="", 
	read_from_manifest_file=True):

	uploads_logger = logging.getLogger('media_downloader.getFilesListing')

	if read_from_manifest_file:
		if not manifest_file:
			manifest_file = "s3_manifest.txt"
	else:
		if not images_source_dir:
			uploads_logger.error("invalid inputs")
			return

	if read_from_manifest_file:
		# lets read the manifest file now
		upload_list = []
		with open(manifest_file,"r") as fin:
			for line in fin:
				upload_list.append(line.strip())

		uploads_logger.debug(upload_list)
	else:
		# now read from imagedir
		upload_list = []

		allowed_extensions = ["jpg","JPG","jpeg","JPEG","png","PNG"]
		uploads_logger.debug(images_source_dir)
		for index, filename in enumerate(Path(images_source_dir).glob('**/*')):
			#print(type(filename))
			filename_str = str(filename)
			uploads_logger.debug(filename_str)

			if "venv" not in filename_str:
				uploads_logger.debug(filename_str)
				path_tokens = filename_str.split("%s/" % images_source_dir)[1].split("/")
				uploads_logger.debug(path_tokens)
				uploads_logger.debug("~".join(path_tokens))
				if filename.suffix:
					uploads_logger.debug(filename.suffix[1:])
					if filename.suffix[1:] not in allowed_extensions:
						continue
					else:
						# now update the database
						upload_list.append(filename_str)
						uploads_logger.debug("valid image")
						#if index > 25:
						#	break
				else:
					continue
		uploads_logger.info("Scanned for all media types")
		uploads_logger.debug(upload_list)

	return upload_list

def uploadFile(target_file="", dt_str="", dt_epoch=None, exif_dict=None, album_tags=None):

	uploads_logger = logging.getLogger('media_downloader.uploadFile')

	filename = os.path.basename(target_file)
	uploads_logger.info(" Processing %s ... " % filename)

	bucket_name = config.__S3_BUCKET__

	if "profile" in target_file:
		temp_profile = os.path.basename(target_file).split("profile_")[1]
		profile_name = temp_profile.replace("_", " ").replace(".jpg","")
		filename = temp_profile
		uploads_logger.debug("%s, %s, %s" % (temp_profile, profile_name, filename))
	else:
		filename = filename.replace(" ","_").replace("(","_").replace(")","_")
		profile_name = ""

	if profile_name:
		s3_key = "profiles/%s" % (filename)
	else:
		s3_key = "staging/%s" % (filename)

	metadata = {
		"file_datetime": dt_str,
		"file_datetime_epoch": "%d" % dt_epoch
	}

	if profile_name:
		metadata["profile"] = profile_name

	# now insert the albumtags
	if album_tags:
		for album_key, album_value in album_tags.items():
			metadata[album_key] = album_value

	uploads_logger.debug("%s, %s, %s, %s" % (target_file, bucket_name, s3_key, metadata))

	response = s3.put_object(
		Body=open(target_file, 'rb'), 
		Bucket=bucket_name, 
		Key=s3_key,
		Metadata=metadata)

	uploads_logger.info("Successfully uploaded !")
	#uploads_logger.info(response)

	return response

def sendMetadata(response=None, exif_dict=None):

	uploads_logger = logging.getLogger('media_downloader.sendMetadata')

	if "ETag" in response.keys():
		uploads_logger.debug(response["ETag"].strip('\"'))
		uploads_logger.debug(type(response["ETag"]))
		# now send a sqs message with exifdata
		exif_dict["ETag"] = response["ETag"].strip('\"')
		str_msg = json.dumps(exif_dict)

		uploads_logger.info("Trying to send message with EXIF data ...")
		uploads_logger.debug(str_msg)
		sqs = boto3.resource('sqs')
		queue = sqs.get_queue_by_name(QueueName='cerebro_requests')
		#uploads_logger.info(sqs)
		#uploads_logger.info(queue)
		response = queue.send_message(MessageBody=str_msg)

		#uploads_logger.info(response)
		uploads_logger.info("SQS message should have been sent now with EXIF data")

	return response

def md5(fname):
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)

	return hash_md5.hexdigest()

def getFilesListingFromDB():

	uploads_logger = logging.getLogger('media_downloader.getFilesListingFromDB')

	file_list = []
	# now setup the connection/cursor
	db_file = "cerebro.db"
	conn = sqlite3.connect(db_file)

	c = conn.cursor()

	uploads_logger.debug("DB cursor created in getFilesListingFromDB")

	dml_sql = """ SELECT file_name FROM media_files WHERE current_state='Detected File' """

	c.execute(dml_sql)
	rows = c.fetchall()
	for row in rows:
		uploads_logger.debug(row)
		if len(row) >= 1:
			if str(row[0]):
				if str(row[0]) not in file_list:
					file_list.append(str(row[0]))

	uploads_logger.debug(file_list)

	return file_list

def retrieve_processed_hashes():

	uploads_logger = logging.getLogger('media_downloader.retrieve_processed_hashes')
	hash_list = []
	# now setup the connection/cursor
	db_file = "cerebro.db"
	conn = sqlite3.connect(db_file)

	c = conn.cursor()

	uploads_logger.debug("DB cursor created")

	dml_sql = """ SELECT md5_hash FROM media_files WHERE current_state != 'Detected File' """

	c.execute(dml_sql)
	rows = c.fetchall()
	for row in rows:
		uploads_logger.debug(row)
		if len(row) >= 1:
			if str(row[0]):
				if str(row[0]) not in hash_list:
					hash_list.append(str(row[0]))

	uploads_logger.debug(hash_list)

	return hash_list

def update_db(file_name, md5_hash="", file_type="",
				current_state="Not Started", update_mode=True):

	uploads_logger = logging.getLogger('media_downloader.update_db')

	if not file_name:
		uploads_logger.error("Error! Not a valid file entry!!")
		return

	# now setup the connection/cursor
	db_file = "cerebro.db"
	conn = sqlite3.connect(db_file)

	c = conn.cursor()

	uploads_logger.debug("DB cursor created")
	
	if update_mode:
		if not md5_hash:
			uploads_logger.error("Error! No valid file hash sent!!")
			return

		dml_sql = """ UPDATE media_files 
						SET file_name=?,
							file_type=?,
							current_state=?,
							last_updated=?,
							last_updated_dt=?
					WHERE md5_hash=? """
	else:
		dml_sql = """ INSERT INTO media_files(file_name,md5_hash,file_type,current_state,last_updated,last_updated_dt)
					VALUES(?,?,?,?,?,?)"""

	# setup the date time
	epoch_time = datetime(1970,1,1)
	utc_time = datetime.now()
	last_updated = int((utc_time-epoch_time).total_seconds())
	last_updated_dt = utc_time.strftime("%m-%d-%YT%H:%M:%S.%f")

	if update_mode:
		# setup the media file tuple for update mode
		media_file_entry = (file_name, file_type, current_state, 
						last_updated, last_updated_dt, md5_hash)
	else:
		# setup the media_file tuple
		media_file_entry = (file_name, md5_hash, file_type,
							current_state, last_updated, last_updated_dt)
	uploads_logger.debug(media_file_entry)

	c.execute(dml_sql, media_file_entry)
	conn.commit()

	uploads_logger.info("Database updated now ...")
	uploads_logger.debug(c.lastrowid)

	return

def processFiles(scan_only=False, retry_mode=False, manifest_mode=False):

	uploads_logger = logging.getLogger('media_downloader.processFiles')
	global image_dir
	#print(image_dir)

	# also get the list of file hashes
	file_hash = retrieve_processed_hashes()
	uploads_logger.info("Retrieved File Hashes that were processed ...")
	uploads_logger.debug(file_hash)
	#return

	if retry_mode:
		# get the files listing from the DB
		upload_list = getFilesListingFromDB()
	else:
		if "tmp" not in image_dir:
			upload_list = getFilesListing(images_source_dir=image_dir, read_from_manifest_file=False)

		if manifest_mode:
			upload_list = getFilesListing(read_from_manifest_file=True)

	#print(upload_list)
	#return False
	upload_file_count = len(upload_list)
	if upload_file_count > 6:
		uploads_logger.debug(upload_list[:5])

	for index, file in enumerate(upload_list):
		uploads_logger.info("----------------")
		uploads_logger.info("\tProcessing %d of %d ..." % (index+1, upload_file_count))

		uploads_logger.debug("%s , %s" % (index, file))

		# first determine the file hash
		uploads_logger.debug(file)
		file_md5 = md5(file)
		uploads_logger.debug(file_md5)
		if file_md5 in file_hash:
			# this means a dupe was found
			uploads_logger.info("\tDupe was found. Skipping ...")
			continue
		else:
			# this means this was a new pass
			uploads_logger.info("\tNo Dupe was found. Continuing ...")
			file_hash.append(file_md5)

		# Insert entry with the file and hash to setup for processing
		update_db(file_name=file, md5_hash=file_md5, 
			current_state="Detected File", update_mode=False)
		# now update the entry with the hash
		#update_db(file_name=file, md5_hash=file_md5,
		#	current_state="Processing Hash", update_mode=True)
		#continue

		if scan_only:
			continue

		file_info = rotate_jpeg(file, manifest_mode)
		target_file = file_info["target_file"]
		exif_dict = file_info["exif_dict"]
		dt_str = file_info["datetime_str"]
		dt_epoch = int(file_info["datetime_epoch"])
		uploads_logger.debug("%s, %s, %s" % (target_file, dt_str, dt_epoch))

		album_tags = file_info["album_tags"]

		update_db(file_name=file, md5_hash=file_md5, 
			current_state="Before Uploading", update_mode=True)
		#continue

		response = uploadFile(target_file, dt_str, dt_epoch, exif_dict, album_tags)
		uploads_logger.info("\tUploaded file: %s" % target_file)
		update_db(file_name=file, md5_hash=file_md5, 
			current_state="Uploaded File", update_mode=True)

		sleep(2)
		sendMetadata(response, exif_dict)
		update_db(file_name=file, md5_hash=file_md5, 
			current_state="Metadata and File Uploaded", update_mode=True)

		uploads_logger.info("\tFile Processed: %s" % target_file)

	uploads_logger.info("All Files processed now!")
	return True

# create the SQLITE3 DB and 
# create tables if they don't exist already

def setup_db():

	uploads_logger = logging.getLogger('media_downloader.setup_db')

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
	uploads_logger.debug("SQL to be used for creating table is: \n%s" % create_table_sql)

	c = conn.cursor()
	c.execute(create_table_sql)

	uploads_logger.info("DB and table created now!")

	return

def initialize():

	global image_dir
	global sqs_logger
	#global uploads_logger

	init_status = False
	parser = argparse.ArgumentParser()
	#parser.add_argument("echo", help="echo the string you use here")
	parser.add_argument("--logfile", help="Logfile for all INFO/DEBUG level logs")
	parser.add_argument("--imagedir", help="directory to source all images from")
	parser.add_argument("--scan", help="scan all images only", action='store_true')
	parser.add_argument("--retry", help="retry scanned images only", action='store_true')
	parser.add_argument("--debug", help="debug mode to not run scripts", action='store_true')
	parser.add_argument("--manifest", help="manifest mode", action='store_true')
	args = parser.parse_args()
	#print args

	# 1. setup env. vars
	if args.imagedir:
		#print("Image dir is available: %s" % args.imagedir)
		image_dir = args.imagedir
		# now call the media downloader
		# download_media(image_dir=args.imagedir)
		#print("Images are all downloaded now !!")
	else:
		#print("Dumping to tmp dir")
		image_dir = "/tmp"
		#download_media()

	if args.debug:
		debug_mode = True
	else:
		debug_mode = False

	if args.scan:
		scan_mode = True
	else:
		scan_mode = False

	if args.retry:
		retry_mode = True
	else:
		retry_mode = False

	if args.manifest:
		manifest_mode = True
	else:
		manifest_mode = False

	# and now setup the logging profile
	# set up logging to file - see previous section for more details
	if args.logfile:
		logFile = args.logfile
	else:
		logFile = '/tmp/media_downloader.log'

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

	# Now, we can log to the root logger, or any other logger. First the root...
	#logging.info('Jackdaws love my big sphinx of quartz.')

	# Now, define a couple of other loggers which might represent areas in your
	# application:

	sqs_logger = logging.getLogger('media_downloader.sqs_agent')
	uploads_logger = logging.getLogger('media_downloader.initialize')

	#sqs_logger.debug('Quick zephyrs blow, vexing daft Jim.')
	#sqs_logger.info('How quickly daft jumping zebras vex.')
	#uploads_logger.warning('Jail zesty vixen who grabbed pay from quack.')
	#uploads_logger.error('The five boxing wizards jump quickly.')

	uploads_logger.info("In initiailize fn")
	uploads_logger.debug("Image Dir: %s, Debug Mode: %d" % (image_dir, debug_mode))

	#print(sqs_logger, uploads_logger)

	# now setup the database as well
	setup_db()

	init_status = True
	return init_status, debug_mode, scan_mode, retry_mode, manifest_mode

if __name__ == "__main__":
	#print("starting ...")
	init_status, debug_mode, scan_mode, retry_mode, manifest_mode = initialize()
	uploads_logger = logging.getLogger('media_downloader.main')
	#print(uploads_logger)
	uploads_logger.info("Completed the initialize ...")
	uploads_logger.info("Init: %d, Debug: %d, Scan: %d, Retry: %d" % (init_status, debug_mode, scan_mode, retry_mode))
	#init_status = False
	if init_status:
		uploads_logger.info("Successful Init.")
		#getFilesListingRecursive(image_dir)

		processFiles(scan_only=scan_mode, retry_mode=retry_mode, manifest_mode=manifest_mode)
		if scan_mode:
			uploads_logger.info("Completely scanned files")
		else:
			uploads_logger.info("Completely uploaded files")

	uploads_logger.info("=============================")
	uploads_logger.info("Media Uploading Finished!")




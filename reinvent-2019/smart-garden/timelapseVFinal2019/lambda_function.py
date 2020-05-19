import os
import stat
import shutil
import boto3
import datetime
import logging
import subprocess

print('Loading function')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

image_path = "/tmp/images"
video_path = "/tmp/video"
video_name = "timelapse.mov"

# ffmpeg is stored with this script.
# When executing ffmpeg, execute permission is requierd.
# But Lambda source directory do not have permission to change it.
# So move ffmpeg binary to `/tmp` and add permission.
ffmpeg_bin = "/tmp/ffmpeg"
shutil.copyfile('/opt/bin/ffmpeg', ffmpeg_bin)
os.environ['IMAGEIO_FFMPEG_EXE'] = ffmpeg_bin
os.chmod(ffmpeg_bin, os.stat(ffmpeg_bin).st_mode | stat.S_IEXEC)

s3 = boto3.client('s3')
image_bucket = "S3 image bucket name"
video_bucket = "S3 bucket to generated timelapse"

def prepare_path(target):
  print("prepare path "+target)
  if os.path.exists(target):
    logger.info("{0} exists".format(target))
    shutil.rmtree(target)
  print("mkdir")
  os.mkdir(target)

def copy_object(bucket, source, dest):
  name = source.split('/')[-1]
  local_file = "{0}/{1}".format(dest, name)
  logger.debug("{0} to {1}".format(source, local_file))
  s3.download_file(bucket, source, local_file)
  if os.path.exists(local_file):
      b = open(local_file,"r")
  return local_file

def create_video(images, video_file):
  print("create video")
  images.sort()
  logger.info("create video from {0} images.".format(len(images)))
  ffmpega="/opt/bin/ffmpeg"
  command = ffmpega+' -r 1 -y -i /tmp/images/IMG%03d.jpg  -codec:v prores -profile:v 2 '+'/tmp/video/timelapse.mov'
  try:
    output = subprocess.check_output(command, shell=True)
    print("SUCESS OUTPUT")
    print(output)
  except subprocess.CalledProcessError as e:
    print("ERROR")
    print(e.output)
    print("end error")
  logger.info("video: {0}".format(video_file))

def move_video(video_file, bucket, dest_key):
  print("video_file "+video_file)
  print(bucket)
  print(dest_key)

  video = open(video_file,"rb")

  s3.put_object(
    Bucket=bucket,
    ACL='public-read',
    Body=video,
    Key=dest_key,
    ContentType="video/mov"
  )

  logger.info("video moved to {0}/{1}".format(bucket, dest_key))

def lambda_handler(event, context):
  tdatetime = datetime.datetime.now()
  prefix = "raw-pics/00000000be9a0795"
  result = s3.list_objects_v2(
        Bucket=image_bucket,
        Prefix=prefix
    )

  images = []
  if 'Contents' in result:
    prepare_path(image_path)
    for item in result['Contents']:
      if "jpg" in item['Key']:
        #print("item "+item['Key'])
        images.append(copy_object(image_bucket, item['Key'], image_path))
  else:
    return

  if len(images) > 0:
    prepare_path(video_path)
    video_file = "{0}/{1}".format(video_path, video_name)
    create_video(images, video_file)
    prefix1=tdatetime.strftime('%Y/%m/%d/')
    ymd = prefix1.split('/')
    video_key = "{0}/{1}/{2}.mp4".format(ymd[0], ymd[1],"".join(ymd))
    move_video(video_file, video_bucket, video_key)
  else:
    return

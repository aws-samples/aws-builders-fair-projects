echo "hello from script"

echo "param"
echo $1

echo "-----------------------"
chmod 755 /tmp/ffmpeg
echo "cd /tmp"
cd /tmp
pwd
ls -lrt
echo "-----------------------"
echo "conversion started"
/usr/bin/bash /tmp/video_to_grid.sh $1 /tmp/
echo "conversion done"
echo "-----------------------"
cd /tmp
ls -lrt
echo "script done"
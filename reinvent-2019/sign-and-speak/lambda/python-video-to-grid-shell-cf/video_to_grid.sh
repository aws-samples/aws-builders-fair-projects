#!/bin/bash

######################
# This script turns a video file into a grid image file.
# Example:
#   ./video_to_grid.sh -i input-video.mp4 ./out-dir
######################

pwd

# Retrieve command line input
input_video=$1
output_dir=$2
#mkdir $output_dir

# Use a temporary directory to save files between steps
temp_dir="/tmp/wip"
mkdir $temp_dir

# Separate the video file path into its parts
file_name=$(basename -- "$input_video")
extension=${file_name##*.}
video_name=${file_name%.*}

echo ${input_video}

# Center crop
if [ $extension == "mp4" ]
then
    # The mp4 videos tend to be larger, which center crop needs to take into account
    cropped_video="${temp_dir}/cropped.${extension}"
    /tmp/ffmpeg -i $input_video -vf crop=700:700 $cropped_video
else
    cropped_video="${temp_dir}/cropped.${extension}"
    /tmp/ffmpeg -i $input_video -vf crop=480:480 $cropped_video
fi
# Resize
resized_video="${temp_dir}/resized.${extension}"
/tmp/ffmpeg -i $cropped_video -vf scale=76:76 $resized_video
# Split into frames
frame_file="${temp_dir}/frame_%01d.png"
/tmp/ffmpeg -i $resized_video -vf "select=not(mod(n\,6))" -vsync vfr -q:v 2 $frame_file
# Choose 9 evenly spread frames
frame_set=$(python frame_picker.py ${temp_dir} 2>&1 >/dev/null)
frames=(${frame_set//|/ })
# Combine frames into grid image
grid_file="${output_dir}/${video_name}_grid.png"

rm $grid_file

/tmp/ffmpeg -i "${temp_dir}/frame_${frames[0]}.png" -i "${temp_dir}/frame_${frames[1]}.png" -i "${temp_dir}/frame_${frames[2]}.png" -i "${temp_dir}/frame_${frames[3]}.png" -i "${temp_dir}/frame_${frames[4]}.png" -i "${temp_dir}/frame_${frames[5]}.png" -i "${temp_dir}/frame_${frames[6]}.png" -i "${temp_dir}/frame_${frames[7]}.png" -i "${temp_dir}/frame_${frames[8]}.png" -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v][6:v][7:v][8:v]xstack=inputs=9:layout=w3_0|w3_h0+h2|w3_h0|0_h4|0_0|w3+w1_0|0_h1+h2|w3+w1_h0|w3+w1_h1+h2[v]" -map "[v]" $grid_file

# Clean up
rm -r $temp_dir
#!/bin/bash
xscreensaver-command -deactivate
vcgencmd display_power 1
sudo pkill feh
photo_path=$1
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority /usr/bin/feh \
	--quiet --preload --auto-zoom --fullscreen --recursive --reload 10 --hide-pointer \
	--slideshow-delay 3 --font FreeMono/96 --fontpath /usr/share/fonts/truetype/freefont \
	--draw-tinted --draw-action --randomize --borderless --image-bg black \
	--caption-path captions $photo_path


#!/bin/sh
###Drone-Zone Jetson Nano System Configuration Set-up###

echo "Starting Jetson configuration"
sudo apt -y update
sudo apt -y install repo

###GitHub Configuration###
read -p 'GitHub Email: ' email
read -p 'GitHub Name: ' name
git config --global user.email "$email"
git config --global user.name "$name"

###Early SwapFile Installation###
git clone https://github.com/JetsonHacksNano/installSwapfile.git
read -p 'Swap Partition Size (Number in GB): ' swapSize
./installSwapFile/installSwapFile.sh -s $swapSize
Echo "Rebooting Jetson..."
sudo reboot

###First Reboot###

###Setting up Olympe Environment
Echo "Installing required dependencies..."
sudo apt -y install build-essential git graphviz libatlas-base-dev libopencv-dev python-pip unzip nano python3-opencv libjpeg-dev
Echo "Setting up Olympe environment..."
mkdir -p code/parrot-groundsdk
cd code/parrot-groundsdk
repo init -u https://github.com/Parrot-Developers/groundsdk-manifest.git
repo sync
sed -i "/\b\(opencv-python\)\b/d" ./packages/olympe/requirements.txt
./products/olympe/linux/env/postinst
./build.sh -p olympe-linux -A all final -j
cd
cp /usr/lib/python3/dist-packages/cv2.cpython-36m-aarch64-linux-gnu.so ~/code/parrot-groundsdk/.python/py3/lib/python3.6/site-packages/cv2.cpython-36m-aarch64-linux-gnu.so
cp -r /usr/lib/python3/dist-packages/numpy ~/code/parrot-groundsdk/.python/py3/lib/python3.6/site-packages/

###Setting up VSCode###
git clone https://github.com/JetsonHacksNano/installVSCode.git
./installVSCode/installVSCode.sh

###mmxnet dependencies###
sudo apt update
sudo pip install --upgrade pip setuptools
sudo pip install graphviz==0.8.4 jupyter numpy==1.15.2

###AWS CLI, pre-built configurations and mxnet setup###
curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" 
unzip awscliv2.zip 
sudo ./aws/install
Echo "Set AWS Credentials..."
read -p 'AWS Access Key ID [None]: ' awsAKID
read -p 'AWS Secret Access Key [None]: ' awsSAK
read -p 'Default region name [None]: ' defReg
aws configure set aws_access_key_id $awsAKID
aws configure set aws_secret_access_key $awsSAK
aws configure set default.region $defReg
aws s3 cp s3://drone-zone-resources/mxnet.zip mxnet.zip
unzip mxnet.zip
cd ~/mxnet/python
sudo pip install -e .
cd

###Begin GreenGrass Set-up###
#####THIS PART NEEDS TO BE DONE AND WRITTEN OUT YET####
aws s3 cp s3://drone-zone-resources/gg-bootstrap.tar.gz gg-bootstrap.tar.gz
tar xvzf gg-bootstrap.tar.gz
sudo adduser --system ggc_user
sudo addgroup --system ggc_group
sudo sed -i '/s/#fs.protected_hardlinks=0/fs.protected_hardlinks=1/g' ~/etc/sysctl.d/99-sysctl.conf
sudo sed -i '/s/#fs.protected_symlinks=0/fs.protected_symlinks=1/g' ~/etc/sysctl.d/99-sysctl.conf
Echo "Rebooting Jetson..."
sudo reboot

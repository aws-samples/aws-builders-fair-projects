# aws drone zone 
![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiUmYrQzlvK2JVYWloK3N5NFh5WUZNS1duYUtVeFN2eWJLNk9VdU9NdzdDdGtobldPcHBKYjdVQ0YxV0NQLzRZeXhWbkJVTkc2Ymd2TEpJblNYb1BraXFNPSIsIml2UGFyYW1ldGVyU3BlYyI6IjRObVVDcVUyb3JJUEFYQTciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

## Setup

<details>
<summary>Manual</summary>

### Compatible regions ###
See the [AWS Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) for the current list of regions for AWS IoT Core.

### Required tools ###
* Ubuntu/Raspian
* Python 3
* [awscli](https://aws.amazon.com/cli/)
* [jq](https://stedolan.github.io/jq/)
* Parrot olympe

### Setup Jetson Nano ###

Update system and install repo
```
sudo apt -y update
sudo apt -y install repo
```
Configure GitHub credentials for downloading repos later in setup
```
git config --global user.email "$email"
git config --global user.name "$name"
```
Swapfile configuration for image processing 
```
git clone https://github.com/JetsonHacksNano/installSwapfile.git
./installSwapFile/installSwapFile.sh -s 16
sudo reboot
```

### Setup Olympe Environment ###

Install dependencies
```
sudo apt -y install build-essential git graphviz libatlas-base-dev libopencv-dev python-pip unzip nano python3-opencv libjpeg-dev
```
Set up directories and download repo
```
mkdir -p code/parrot-groundsdk
cd code/parrot-groundsdk
repo init -u https://github.com/Parrot-Developers/groundsdk-manifest.git
repo sync
```
Configure opencv for use with Olympe on a Jetson Nano
```
sed -i "/\b\(opencv-python\)\b/d" ./packages/olympe/requirements.txt
./products/olympe/linux/env/postinst
./build.sh -p olympe-linux -A all final -j
cd
cp /usr/lib/python3/dist-packages/cv2.cpython-36m-aarch64-linux-gnu.so ~/code/parrot-groundsdk/.python/py3/lib/python3.6/site-packages/cv2.cpython-36m-aarch64-linux-gnu.so
cp -r /usr/lib/python3/dist-packages/numpy ~/code/parrot-groundsdk/.python/py3/lib/python3.6/site-packages/
```

### Text Editor Install ###

Installing VSCode
```
git clone https://github.com/JetsonHacksNano/installVSCode.git
./installVSCode/installVSCode.sh
```

### Configure MXNET ###
Installing mxnet dependencies
```
sudo apt update
sudo pip install --upgrade pip setuptools
sudo pip install graphviz==0.8.4 jupyter numpy==1.15.2
```
Install AWS CLI and configure credentials
```
curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" 
unzip awscliv2.zip 
sudo ./aws/install
aws configure set aws_access_key_id $awsAKID
aws configure set aws_secret_access_key $awsSAK
aws configure set default.region $defReg
```
Download MXNET from S3 and install
```
aws s3 cp s3://drone-zone-resources/mxnet.zip mxnet.zip
unzip mxnet.zip
cd ~/mxnet/python
sudo pip install -e .
cd
```

### Prepare Jetson Nano for Greengrass ###
Add ggc_user and ggc_group to system:
```
sudo adduser --system ggc_user
sudo addgroup --system ggc_group
```
Edit 99-sysctl.conf file:
```
sudo nano /etc/sysctl.d/99-sysctl.conf
```
Make sure the following variables are un-commented and enabled (at the bottom of 99-sysctl.conf):
```
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
```
Add a symbolic link for Python 3.7:
```
sudo ln -s /usr/bin/python3 /usr/bin/python3.7
```
Reboot after configuration changes:
```
sudo reboot
```

### Install Greengrass on Jetson Nano ###
* Download [gg-bootstrap.zip](drone-zone-helpers/gg-bootstrap.zip) (right click, save link as) and extract to ~/gg-bootstrap
* Install Greengrass:
```
sudo ./installGreengrass.sh
```

### Deploy CloudFormation stack for Drone Zone ###
> NOTE: You can complete this section on the Jetson Nano, or another environment if you don't want to install the AWS SAM CLI on your Jetson Nano.
* Install AWS SAM CLI. See [installing the AWS SAM CLI on Linux](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html)
* Clone the aws-drone-zone repository to your workspace
* Open terminal in aws-drone-zone repository, and navigate to drone-zone-helpers directory
* Edit the variables in the bin/deploy.sh script:
```
# declare variables
BUCKET_NAME_PREFIX=<YOUR-BUCKET-NAME-PREFIX>
DRONE_NAME=<DRONE-NAME>
REGION=us-west-2
DRONE_DETECTION_MODEL_PATH=s3://drone-zone-resources-us-west-2/deploy_model_v2.zip
CAR_DETECTION_MODEL_PATH=s3://drone-zone-resources-us-west-2/porsche_model_v1.zip
```
* Deploy the stack by running the script from the drone-zone-helpers directory:
```
./bin/deploy.sh
```

### Configure and start Greengrass on Jetson Nano ###
* In the Resources section of your CloudFormation stack, find the Logical ID *GreengrassConfigsBucket* and navigate to the associated S3 Bucket
* Download the bootstrap.json file located in this bucket to the directory ~/gg-bootstrap on the Jetson Nano 
* Run the following to configure Greengrass with the proper certificates, key, and configuration file:
```
sudo ./setupConfig.sh
```
* Attempt to start Greengrass:
```
sudo /greengrass/ggc/core/greengrassd start
```

</details>

## Clean up

<details>
<summary>Manual</summary>

### Delete the CloudFormation Stack ###

Just delete the CloudFormation stack you deployed with the deploy.sh script.

### Remove Greengrass, certs, and key ###

On your Jetson Nano, run the following command in your ~/gg-bootstrap directory:
```
sudo ./cleanUp.sh
```

</details>

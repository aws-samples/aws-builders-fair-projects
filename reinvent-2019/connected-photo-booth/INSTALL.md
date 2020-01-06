# INSTALL

Project Cerebro is a simple MVP for doing face recognition of images and be used as a Photo Media Panel and eventually as a Digital Photo Booth as well.
Most of the resources are currently fixed to the original creators' (Sachin) resources. Will be noted as much as possible.

## Env Setup

### Hardware Setup

#### Hardware Parts Needed

1. Raspberry Pi 4
2. [Raspberry Pi Camera v2](https://www.amazon.com/Raspberry-Pi-Camera-Module-Megapixel/dp/B01ER2SKFS/ref=sr_1_3?crid=2M7X5FMA4RXN6&keywords=raspberry+pi+camera+v2&qid=1571640335&sprefix=raspberry+pi+cam%2Caps%2C214&sr=8-3)
3. [Interconnects](https://www.amazon.com/gp/product/B07GD2BWPY)
4. [PushButtons](https://www.amazon.com/ELEGOO-Electronics-Component-resistors-Potentiometer/dp/B01ERPXFZK), [Resistors, LEDs](https://www.amazon.com/ELEGOO-Electronics-Component-resistors-Potentiometer/dp/B01ERPXFZK/ref=sr_1_16?keywords=raspberry+pi+button&qid=1571640479&sr=8-16)
5. Alexa Echo Dot/Show
6. [Breadboard](https://www.amazon.com/DEYUE-breadboard-Set-Prototype-Board/dp/B07NVWR495/ref=sr_1_22_sspa?crid=26KOU5A5QAC9U&keywords=raspberry%2Bpi%2Bbreadboard&qid=1571640587&sprefix=raspberry%2Bpi%2Bbread%2Caps%2C195&sr=8-22-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzTFdHRk1JV0hSTFRaJmVuY3J5cHRlZElkPUEwODY4MDA1MTc3MFFTMlFBR1BIQSZlbmNyeXB0ZWRBZElkPUEwNTczNzg0MVpBUEk4S0s3ME9GNSZ3aWRnZXROYW1lPXNwX2J0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1)
7. Audio Output
8. USB Mouse, Keyboard 
9. Monitor/Display

#### Raspberry Pi Setup

##### Prepare Rasbian OS
We used and tested against Raspbian Buster. Follow [the instruction guide here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) to get the microSDHC card installed with the Raspbian OS.

##### Powerup Raspberry Pi

* Install the microSD card (containing the Raspbian OS).
* Connect the Raspberry PI to a HDMI-capable Display using a micro-HDMI cable - use the primary display slot.
* Connect a USB Keyboard, Mouse to get the initial setup working.
* Finally connect the Power Cable to into the USB-C slot

#### Validate and Configure Raspberry Pi

* Use the Mouse and Launch app to confirm mouse and keyboard connectivity
* Connect to the Wifi network (preferably a 5G network)
* Launch Browser and connect to the internet and establish connectivity
* If there's no audio via HDMI, use external speakers or headphones. 
* Turn off the WiFi Power management

```
echo "Current Wifi Settings: " && sudo iwconfig wlan0
echo "Changing WiFi Power Mgmt: " && sudo iwconfig wlan0 power off
echo "New Wifi Settings: " && sudo iwconfig wlan0
```

* And fix the change in the cron too so the wifi is never lost

```
crontab -e
... at the bottom of the file ...
*/5 * * * * sudo iwconfig wlan0 power off
... save file ...
```

* Enable the SSH service by launching Raspberry Pi Configuration and go to Interfaces. More details here [TBD]
* Validate by connecting in headless mode now

```
ifconfig
<use the ip address>
<from remote host> 
ssh pi@<ipaddress>
```

#### Hardware setup & cable mapping

* Connect the wires as per the following photo [TBD]
* Cable Mapping

| Breadboard Port | Component         | Cable Color | Pi Port          |
|-----------------|-------------------|-------------|------------------|
| D6              | Green Pushbutton  | BLK         | pin 9 / GND      |
| D8              | Green Pushbutton  | BLUE        | pin 11 / GPIO 17 |
| F19             | Yellow Pushbutton | BLK         | pin 34 / GND     |
| F21             | Yellow Pushbutton | BLUE        | pin 36 / GPIO 16 |
| A3              | Green LED         | GREEN       | pin13 - GPIO27   |
| J5              | Green LED         | BLK         | pin14 - GND      |
| I29             | Yellow LED        | GREEN       | pin37 - GPIO26   |
| J26             | Yellow LED        | BLK         | pin39 - GND      |

* Component Mapping

| Component              | Slots on Bread Board                    | Notes                                                          |
|------------------------|-----------------------------------------|----------------------------------------------------------------|
| Push Button            | E6, E8, F6, F8                          | No Polarity so direction doesn't matter                        |
| Push Button            | H19, H21, J19, J21                      | No Polarity so direction doesn't matter                        |
| Green LED              | shorter end \- I5 \- longer end \- I3   | Polarity matters\. Reversing will result in LED not lighting\. |
| Yellow LED             | shorter end \- I26 \- longer end \- I24 | Polarity matters\. Reversing will result in LED not lighting\. |
| Green LED \- Resistor  | near LED \- H3 \- near cable \- E3      | No Polarity so direction doesn't matter                        |
| Yellow LED \- Resistor | near LED \- H24 \- near cable \- H29    | No Polarity so direction doesn't matter                        |

### Software

#### Pre-Requisites needed

This assumes the following dev sandbox

* direct access to AWS account
* python3 installed
* virtualenv for sandboxing python environments
* Exiftool - [Install exiftool](https://sno.phy.queensu.ca/~phil/exiftool/install.html#Unix) which is needed as the py wrapper expects this
	* The exiftool website has Win/MacOS distributions but is cross-platform as well via the perl binaries

#### Install Pre-Requisites

* Setup AWS credentials

You can choose whatever mechanism that you prefer. For me, have dumped my aws creds as my default aws profile so its easy to access directly.

```
aws configure
... provide credentials as needed ...
aws s3 ls
```

* Check/Install python3

```
pi@rpi4:~ $ python --version
Python 2.7.16
pi@rpi4:~ $ python3 --version
Python 3.7.3
```

* Install Virtual Env as described [here](http://raspberrypi-aa.github.io/session4/venv.html)

```
sudo pip install virtualenv
```

* Check/Install git

```
pi@rpi4:~ $ git --version
git version 2.20.1
```

* Use CodeCommit helpers: 

```
git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true
```

* Download git repo

```
mkdir code_repos & cd code_repos
git clone https://github.com/aws-samples/aws-builders-fair-projects/tree/master/reinvent-2019/connected-photo-booth
...

cd project-cerebro/

git status
On branch master
Your branch is up to date with 'origin/master'.
...

```

* Create and setup virtual environment to be used

```
virtualenv venv
source venv/bin/activate

(venv) pi@rpi4:~/Projects/git_repos/project-cerebro $
```

* Install/Check pip3 

```
(venv) pi@rpi4:~/Projects/git_repos/project-cerebro $ pip3 --version
pip 18.1 from /usr/lib/python3/dist-packages/pip (python 3.7)
```

* Open CV 
OpenCV needs to be installed in the following manner:

```
pip3 install opencv-python 
sudo apt-get install libatlas-base-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test
```

* Install exiftool

https://sno.phy.queensu.ca/%7Ephil/exiftool/install.html#Unix

```
cd /tmp/ && wget https://sno.phy.queensu.ca/%7Ephil/exiftool/Image-ExifTool-11.70.tar.gz

(venv) pi@rpi4:/tmp $ gzip -dc Image-ExifTool-11.70.tar.gz | tar -xf -

(venv) pi@rpi4:/tmp $ cd Image-ExifTool-11.70
(venv) pi@rpi4:/tmp/Image-ExifTool-11.70 $

(venv) pi@rpi4:/tmp/Image-ExifTool-11.70 $ which perl
/usr/bin/perl
(venv) pi@rpi4:/tmp/Image-ExifTool-11.70 $ perl Makefile.PL
Checking if your kit is complete...
Looks good
Generating a Unix-style Makefile
Writing Makefile for Image::ExifTool
Writing MYMETA.yml and MYMETA.json
(venv) pi@rpi4:/tmp/Image-ExifTool-11.70 $

(venv) pi@rpi4:/tmp/Image-ExifTool-11.70 $ make test
cp lib/Image/ExifTool/Charset/DOSLatinUS.pm blib/lib/Image/ExifTool/Charset/DOSLatinUS.pm
cp lib/Image/ExifTool/AES.pm blib/lib/Image/ExifTool/AES.pm
...


(venv) pi@rpi4:/tmp/Image-ExifTool-11.70 $ sudo make install
Manifying 1 pod document
Manifying 34 pod documents
Manifying 33 pod documents
Manifying 33 pod documents
Manifying 32 pod documents
Manifying 32 pod documents
Manifying 15 pod documents
Installing /usr/local/share/perl/5.28.1/Image/ExifTool.pod
...
Installing /usr/local/bin/exiftool
Appending installation info to /usr/local/lib/arm-linux-gnueabihf/perl/5.28.1/perllocal.pod

(venv) pi@rpi4:/tmp/Image-ExifTool-11.70 $ which exiftool
/usr/local/bin/exiftool
```

* Install py requirements

```
pip3 install -r requirements.txt
```

* Install scikit-image correctly

```
sudo apt-get install python3-matplotlib python3-numpy python3-pil python3-scipy python3-tk
sudo apt-get install build-essential cython3
```

* Install mpg321, feh

```
sudo apt-get -y install mpg321
sudo apt-get -y install feh
```

* Fonts on Pi

```
sudo apt-get install ttf-mscorefonts-installer
```

* and for easy font mgmt

```
sudo apt install font-manager
```

### Hardware Validation
* Run Hardware test script which will test for packages installed, Camera available, Audio connectivity, LED/Button functioning

```
cd ~/Projects/git_repos/project-cerebro
source venv/bin/activate
cd scripts
./cerebro_test_hardware.sh
```

### Download / Locate media

This can be some sample photos that you have lying around. There are going to be stock assets to get started with in the assets/ folder

### Create AWS Resources
There are a few AWS resources that need to be created manually (CDK tooling coming soon). Please create the following:

* S3 Bucket: `project-cerebro`
* Dynamo DB Table: `cerebro-media`
* Rekognition Collection: `Cerebro`
	* Will be created by the cerebro_start script anyway
* SQS Queues
	* `cerebro_backend`, `cerebro_requests`, `cerebro_client`
 
* API Gateway (with lambda proxies)
	* GetImages_S3List - this is to get the images from S3/DDB
	* GetQRCode - this is to retrieve a QR code for a given image
	* Generate API Keys for the APIs to be used later
	* Add a Production stage as well to deploy the APIs. Note the URL generated

* Lambda's
	* Cerebro_ProcessImage - this is triggered on the S3 bucket created above. S3 Trigger:
		* Bucket name ^^^
		* Event Type - Object_created
	* Cerebro_ProcessFileMetadata - this is triggered by the EXIF data dumped on the SQS queue. SQS Trigger:
		* queue name: cerebro_requests
		* batch size: 10
	* Lambda code is available in lambda_code folder
	* Will need Execution Role with needed permissions, in addition to the basic execution policies (cloudwatch).
	* And environment vars as needed

| Function Name   | Env. Var Name     | Value. |
|-----------------|-------------------|--------|
| GetImages_S3List | AUDIO\_CONTENT\_DIR | caption-audio |
| GetImages_S3List | BUCKET_NAME | project-cerebro |
| GetImages_S3List | DEBUG_MODE | 0 |
| GetImages_S3List | IMAGE_MAX_COUNT | 5 |
| GetImages_S3List | IMAGE_RANDOMIZE | 0 |
| GetImages_S3List | POLLY_VOICE | Salli |
| GetImages_S3List | STOCK_PROFILES | rock&jassy&bezos&serena&biles&federer |
| Cerebro_GetQRCode | DEBUG_MODE | 0 |
| Cerebro_ProcessImage | AUDIO\_CONTENT\_DIR | caption-audio |
| Cerebro_ProcessImage | BUCKET_NAME | project-cerebro |
| Cerebro_ProcessImage | POLLY_VOICE | Salli |
| Cerebro_ProcessImage | CEREBRO_TABLE | cerebro_media |
| Cerebro_ProcessImage | REKO_COLLECTION | Cerebro |
| Cerebro_ProcessFileMetadata | CEREBRO_TABLE | cerebro_media |
| GetImages_S3List |  |  |
|  |  |  |

| Function Name   | Service     | Permissions |
|-----------------|-------------------|--------|
| GetImages_S3List | S3 | Full Access (or s3:Get\*, s3:List\*) |
| GetImages_S3List | Polly | Full Access |
| GetImages_S3List | Dynamo DB | All table acces to delete/get/put/update items, scan, query |
| GetImages_S3List | Rekognition | Cerebro collection - SearchFaces, SearchFacesByImage |
| Cerebro_GetQRCode | S3 | Full Access |
| Cerebro_GetQRCode | Dynamo DB | All table acces to delete/get/put/update items, scan, query |
| Cerebro_ProcessImage | S3 | Bucket-based --- DeleteObjectTagging, PutObject, GetObject, DeleteObjectVersion, DeleteObjectVersionTagging, DeleteObject |
| Cerebro_ProcessImage | Polly | Read Only Access |
| Cerebro_ProcessImage | Dynamo DB | All table acces to delete/get/put/update items, scan, query |
| Cerebro_ProcessImage | Rekognition | Cerebro collection - CreateCollection, IndexFaces, CompareFaces, DetectFaces, DetectLabels |
| GetImages_S3List | SQS | DeleteMessage, GetQueueAttributes, ReceiveMessage |
| Cerebro_ProcessFileMetadata | SQS | DeleteMessage, GetQueueAttributes, ReceiveMessage |
| Cerebro_ProcessFileMetadata | Dynamo DB | cerebro_table specific access to put/update items |
|  |  |  |

| Function Name   | Memory (in MB)     | Timeout |
|-----------------|-------------------|--------|
| GetImages_S3List | 512 | 3 mins |
| Cerebro_GetQRCode | 512 | 10 secs |
| Cerebro_ProcessImage | 128 | 5 mins |
| Cerebro_ProcessFileMetadata | 128 | 3 secs |

* Generate IOT Certs
	* Create a Thing in IOT Core service
	* Generate certs by going to the Security tab
	* Download the certs into the iot-certs/ folder

### Update Configuration
The local client configuration is maintained using the cerebro.ssm_config file. This is then used to create parameters in Systems Manager in the Parameter Store.

* Update local config file - in `py_client/ssm_config`
* Push SSM parameters using the script `ssm_helper.py`
* Validate parameters - use the console to confirm parameters are written
* Don't modify the cerebro.config unless you have changed the parameter name in SSM 

### System Validation

* Run Cerebro\_clean script to cleanup old content, reset dirs and setup for new run (will also be used at the end)
Run cerebro\_processor to listen for cerebro commands (from alexa, etc.)

```
pwd
cd scripts
./cerebro_clean_start.sh
```
	
## Usage
For now, use the web client or python CLI to access the capability of the photo booth. An Alexa skill is coming shortly for you to use on your account.

### Python CLI
The CLI is contained in the cerebro\_requester.py script. This can be used for development and testing environments.

* To display all selfies taken:

```
python3 cerebro_requester.py 'sachin-pi' --profile all
```

* To display selfies for a specific profile (say 'Thor'):

```
python3 cerebro_requester.py 'sachin-pi' --profile 'thor'
```

* To create or register a profile (person) with Cerebro:

```
python3 cerebro_requester.py 'sachin-pi' --register 'thor'
```

* To take a selfie of registered profiles:

```
python3 cerebro_requester.py 'sachin-pi' --selfie
```

* To show the picture for downloads (onto phone):

```
python3 cerebro_requester.py 'sachin-pi' --download_image
```
 
### Web Portal

* Upload the web client to a Cloudfront distribution 
	* Create an S3 folder and upload web portal from ./web-client
	* Create a CF distribution with this as the origin folder
	* After the distribution is available, confirm bty going to the website

### Use Cerebro with Web Portal

* Start Using the portal by asking for different profiles - empty profile entry shows all selfies available
* Trigger the create profile first
* Then ask to take a selfie
* Ending the session will delete all images from the system

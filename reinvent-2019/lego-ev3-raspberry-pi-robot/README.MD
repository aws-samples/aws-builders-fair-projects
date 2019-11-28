# LEGO® Mindstorms® EV3 and AWS

## Description

This repository contains all of the required content to build a LEGO® Mindstorms® EV3 Robot, which has been integrated with the Robot Operating System, AWS RoboMaker, AWS IoT Greengrass, Raspberry Pi, Raspberry Pi Camera and a console gaming controller.

## Overview

With the LEGO® Mindstorms® EV3 we have near infinite combinations of use cases that can be built. The flexibility of the LEGO® System coupled with the functionality of the EV3 kit and it's ability to run Open Source Operating Systems makes for an awesome robotics development platform for all ages.

With AWS RoboMaker we are able to build, train and evaluate AI/ML enabled robotic applications in the cloud and use AWS IoT Greengrass, installed on edge devices like Raspberry Pi, to deploy and run these robotic apps on the device. Greengrass launches your ROS app which will interact with the hardware using standard ROS communications and perform functions based on the AI/ML model bundled with the app package.

In order to bridge the gap between the cloud and the limited power of the EV3 Computer, we make use of the classic Raspberry Pi computer. With it's ability to run AWS Greengrass and perform simple AI/ML inferencing using video streams from the Raspberry Pi Camera, it's the perfect companion to the LEGO® System and crucial to achieve the goal of this project.


- [Architecture](#architecture)
  - [High level Architecture](#high-level-architecture)
  - [AWS RoboMaker Development Process](#aws-robomaker-development-process)
  - [AWS IoT Alexa Architecture](#aws-iot-alexa-architecture)
  - [ROS and AWS IoT Architecture](#ros-and-aws-iot-architecture)
- [Components](#components)
- [FAQ](#faq)
- [Deployment Instructions](#deployment-instructions)
  - [Create AWS Resources (**[PLACEHOLDER]** mins)](#create-aws-resources-placeholder-mins)
    - [Deploy CloudFormation Template](#deploy-cloudformation-template)
    - [Create RoboMaker Development Environment](#create-robomaker-development-environment)
  - [EV3DEV Setup (120 mins)](#ev3dev-setup-120-mins)
    - [Build EV3DEV Container](#build-ev3dev-container)
    - [Build EV3DEV Image](#build-ev3dev-image)
    - [Run and Setup EV3DEV Image](#run-and-setup-ev3dev-image)
  - [Raspberry Pi Setup (**[PLACEHOLDER]** mins)](#raspberry-pi-setup-placeholder-mins)
    - [Install Raspbian](#install-raspbian)
    - [Setup Raspbian (**[PLACEHOLDER]** mins)](#setup-raspbian-placeholder-mins)
  - [Checkpoint](#checkpoint)
- [Usage Instructions](#usage-instructions)
  - [RoboMaker](#robomaker)
    - [Train the model and simulate](#train-the-model-and-simulate)
    - [Using Gazebo](#using-gazebo)
    - [Using rqt](#using-rqt)
    - [Using rviz](#using-rviz)
    - [Using the terminal](#using-the-terminal)
    - [Using CloudWatch](#using-cloudwatch)
    - [Evaluate the trained model](#evaluate-the-trained-model)
    - [Visualize the RL model working](#visualize-the-rl-model-working)
    - [Build and bundle the robot application (60 mins)](#build-and-bundle-the-robot-application-60-mins)
    - [Download and use a pre-trained model and ROS app](#download-and-use-a-pre-trained-model-and-ros-app)
    - [Deploy your model and ROS app](#deploy-your-model-and-ros-app)
    - [AWS IoT Console](#aws-iot-console)
    - [Alexa Developer Portal](#alexa-developer-portal)
    - [EV3DEV](#ev3dev)
    - [Raspberry Pi](#raspberry-pi)
- [References](#references)
  - [AWS IoT & RoboMaker](#aws-iot--robomaker)
- [Issues](#issues)

## Architecture

### High level Architecture
![High level Architecture](images/Slide2.png "High level Architecture")
### AWS RoboMaker Development Process
![AWS RoboMaker Development Process](images/Slide3.png "AWS RoboMaker Development Process")
### AWS IoT Alexa Architecture
![AWS IoT Alexa Architecture](images/Slide4.png "AWS IoT Alexa Architecture")
### ROS and AWS IoT Architecture
![ROS and AWS IoT Architecture](images/Slide5.png "ROS and AWS IoT Architecture")

## Components
 - **LEGO® Mindstorms® EV3 Kit**
   - EV3 Computer
   - 2 x Large motors
   - Touch sensor
   - IR sensor
   - Various LEGO® EV3 Technique parts
   - 6 x AA Batteries or EV3 Li battery pack
   - Compatible Wifi USB Adapter
   - USB to Mini-USB cable
   - 8GB or more Micro SD-CARD
 - **Raspberry Pi 3B+ or above**
   - 2A Battery bank
   - Micro USB charging cable
   - Raspberry Pi Camera (USB cam should also work)
   - 16GB or more Micro SD-CARD
   - Raspberry Pi Lego Case
 - **XBOX360 Controller and USB Wifi receiver**
 - **Your computer, Linux, Windows or OSX, as long as it can run the latest Docker**

## FAQ
**Q: What is goals of this project?**
The primary goal of this project is to provide an introduction to robotics and how to use it in conjunction with the cloud, while having fun playing with the LEGO® Mindstorms® EV3 system.

**What will I learn from this project?**
In this project you will learn to:
- Setup EV3DEV with ROS on the EV3
- Setup Greengrass Core on the Raspberry Pi
- Train and evaluate the Reinforcement Learning Model in AWS RoboMaker
- Deploy the robot application to your Greengrass Core Device
- Use Alexa to interact with the Greengrass Core IoT shadow and control your robot
- Build this awesome little LEGO® Mindstorms® EV3 robot we designed for this purpose

**Q: For who is this project intended?**
This project is geared towards those who already own this Mindstorms® kit or those who are planning on purchasing the kit. Perhaps this project will convince you to take that step. Besides the Mindstorms® kit, we have aimed to make use of components that are simple to come buy and which you may already have. All of the LEGO® required, for the robot, is part of the [LEGO® Mindstorms® EV3 kit][067e401b], however the LEGO® case for the Raspberry Pi, are the only parts which are not part of the EV3 kit.

**Q: What is running on the LEGO® Mindstorms® EV3 system?**
A Debian based operating called **EV3DEV** is deployed to the EV3 Computer by inserting a flashed SD-Card. This OS contains all of the required EV3 hardware libraries as well as ROS Python libraries.

**Q: What is the function of the Raspberry Pi in this project?**
Inside the EV3 Computer there is an older generation of ARM processor and has limited processing power, so due to this **AWS Greengrass** is unable to be installed directly to the EV3. This limited power also hinders the ability for a full **ROS Core** to run on the EV3 and in this use case we will only be running ROS as a pub/sub node, which is connected to the Raspberry Pi running as ROS Master.

The Raspberry Pi does most of the complex work of running AWS Greengrass and the ROS app.

**Q: How does the object tracking feature work?**
The ROS app receives the video stream from the attached Raspberry Pi Camera and applies the ML model on it through inferencing each frame and making a decision as to turn left or right and direct the robot towards the object it's tracking. The ROS app then sends navigational ROS Twist messages to a topic, which the ROS app on the EV3 subscribes to. When the EV3 receives the message it interprets it and uses the ev3dev Python library to move the motors according to the message it received.

**Q: What kind of machine learning model does this project use?**
This project uses a reinforcement learning model.For this robot's machine learning model we took the **Object Tracking** sample app from RoboMaker Console then trained and evaluated the model without changes. We then adjusted the Turtlebot based code to our needs for a native Raspberry Pi and added some additional code to interact with AWS IoT. This is then all bundled in a package in the RoboMaker Cloud 9 Development Environment and deployed to the Raspberry Pi via Greengrass.

**Q: What other features does this robot have?**
The ROS app on the Raspberry Pi also has the ability to switch mode from tracking an object to using input from an attached USB game controller and in the same way send navigational commands to the EV3 dev, which then drives in the direction that you press on the D-Pad.

**Q: What other features does this robot have?**
In order to command the robot and set an active mode, this project uses the AWS Greengrass Core IoT Thing Shadow to set a parameter, which is retrieved by the ROS app and then relayed on to the EV3 via another ROS topic. The EV3 receives the message and then changes mode. The EV3 has a few modes built in which can be triggered by updating the Thing Shadow which can be found in the document.

**Q: How to I change modes?**
You can change modes by either updating the Greengrass Core IoT Thing Shadow via the Greengrass Console or you can use the provided Alexa Skill which allows you to use voice commands to change the Thing Shodow and in turn activat the mode the robot should be in.

**Q: What are the other modes that you can change to?**
- Joystick: Control via game controller
- Halt: Stop moving
- Snake: Move forward in a serpentine manoeuvre
- Square: Move in a square shape back to where it started
- Charge: Run at full speed in a straight line until the infra-red sensor detects an object approaching and stop right before crashing into it
- Return: Reverse in a straight line about 80cm

**Q: How long will it take to build this project?**
This project will take about **[PLACEHOLDER]** hours to complete depending on whether you use a pre-trained model or plan on training your own. Training your own will take an additional 8 hours minimum.

Each section below will state next to it how long it takes to complete the section.

**Q: What are the costs of this project?**
Running this project will incur costs on your AWS Account, the amount of which again will depend on using a pre-trained model. When using a pre-trained model the costs will be approximately $**[PLACEHOLDER]** and $**[PLACEHOLDER]** when training your own.

**Q: What regions does this project support?**
- This project must be run in the us-east-1 North Virginia region. However can be adjusted to run in pother regions that have AWS Greengrass, RoboMaker and Cloud 9

## Deployment Instructions

### Create AWS Resources (**[PLACEHOLDER]** mins)
In order to deploy the required resources in AWS, you will deploy an AWS CloudFormation template in your account. This template will deploy a majority of the resources for you, which will save you considerable time from setting them up by hand. There are still some final resources that you must launch and configure by hand.

#### Deploy CloudFormation Template

1. From this repository, download the [lego_robot_demo.yaml][1705700a] template.

2. Open the AWS CloudFormation console **in the us-east-1 region.**

3. Create a new stack and under **Specify template** select **￼
Upload a template file** then choose the file you just downloaded and click **Next**.

4. Enter a name for this stack like `lego-robot`.

5. For **Parameters** you can either go with the default options or fill in your own **CoreName** and pick the **InstanceType** you want, then click **Next**.

6. At the next screen you may go with the default settings and click **Next**.

7. At the final screen, review your entries, scroll to the bottom, check the box for **I acknowledge that AWS CloudFormation might create IAM resources.** and click **Create Stack**

8. Monitor the deployment of your stack, once it has completed (this will take approx. **[PLACEHOLDER]** mins) you may continue.

9. When the stack has completed creating, go to the **Outputs** section and note down all of the outputs, you will use them later.

#### Create RoboMaker Development Environment
1. Sign in to the AWS RoboMaker console at https://console.aws.amazon.com/robomaker/.

2. In the left navigation pane, choose Development, and then choose IDEs.

3. In the Create AWS RoboMaker development environment page, type a name for the environment, like `lego-robot`.

4. Select the **ROS Kinetic Distribution** ([See issue 4](#Issues)). For more information about the Robot Operating System (ROS), see www.ros.org.

5. For Instance type, you may choose an m4.large for this project. If you want your builds to run a bit faster you can choose a larger instance type.
_Note:
Choosing instance types with more RAM and vCPUs might result in additional charges to your AWS account for Amazon EC2._

6. In Networking, select the VPC that was just deployed by the CloudFormation template, it should be named after the **CoreName** you entered as a stack parameter and then select the subnet listed.

7. Choose Create to create the development environment.

8. The environment should start to launch immediately. If not, on the Environment details page, choose Open environment. It might take a few moments to prepare the environment.
_You can list available development environments by choosing Development in the left navigation pane, then choosing Development environments._

9. When the Cloud9 RoboMaker Console has finished launching, go to the terminal at the bottom and clone this repository with:
```
git clone [PLACEHOLDER]
```

10. When the process has finished, you will see a new folder in the left pane called **lego-robot**.

11. Next we are going to setup the `roboMakerSettings.json` file. In the left pane, browse to the **lego-robot/robomaker** directory and double-click on the **roboMakerSettings.json** file.

12. In this file, replace the following placeholders using with your environment details, which you will find in the Outputs of your CloudFormation stack:
  - `<bucket name>`
  - `<IAM Role ARN for RoboMaker>`
  - `<security group id>`
  - `<subnet id 1>`

13. Now you need to import this file into RoboMaker as new settings. Click on the **Run** menu item and select **Add or Edit Configurations**.

14. At the bottom click the **Switch config** button then navigate and select `lego-robot/robomaker/roboMakerSettings.json` file and click **Ok** and then click **Save**

**Congrats, your development environment is now ready!**

### EV3DEV Setup (120 mins)
One of the great features of the EV3 computer is that it will run a Linux OS that has been burned on an SD-Card and inserted into the EV3 Computer. There are no firmware or hardware hacks needed, the device will natively boot up whatever supported Linux OS has been plugged in. If you want to go back to the on-board EV3 OS, you simply shutdown and remove the SD-Card.

This project makes use of the most popular EV3 Linux based OS named EV3DEV, there are others out there but this one is well supported by the community and is very mature.

In our use case we need to build our own version of the EV3DEV Debian Stretch image as we need to include ROS, so that our Raspberry Pi running as the ROS Master can communicate with the EV3DEV using ROS topics. Unfortunately due to some limitations on ROS the packages available for ARM based processors, we have to compile our own ROS installation.[See issue 1 below for more background on this](#Issues). We also build the ROS App into the image that will be run on the EV3 and this has been setup to run as a service on start-up.

You can either build this image using your Cloud9 environment, or if you want to be frugal you can also build it on your own machine. The instructions and scripts provided are designed to work for Cloud9 but should work with minor adjustments on your own machine.

#### Build EV3DEV Container
1. From the Cloud9 RoboMaker environment, you are now going to build the EV3DEV ARM Image using Docker. Go to the terminal and run the following commands:
```
cd lego-robot/docker
sudo ./build_ev3dev_image.sh
```

2. Wait for the build process to complete. This will take about 1h10m, depending on your instance type. You may safely ignore any errors you see, as long as it completes the build everything should be ok.

#### Build EV3DEV Image
1. Next we need to use the [EV3DEV brickstrap tool][9b3ae94d] to build the image for the SD-Card. This was installed with the `build_ev3dev_image.sh` script. Again from the Cloud9 terminal run these commands:
```
brickstrap create-tar ev3-ros-melodic ev3-ros-melodic.tar
brickstrap create-image ev3-ros-melodic.tar ev3-ros-melodic.img
```

2. Now get the bucket name from the CloudFormation outputs, upload the image to S3 and create a pre-signed URL so that we can download the image to your machine:
  _Note the file should be about 3.5GB. To save time, space and your bandwidth we are compressing the img file (to ~650MB) before uploading it to S3. We also use ZIP since the image burning tool we use supports it in this format without the need to decompress. This is optional, adjust according to your preference._
```
zip ev3-ros-melodic.zip ev3-ros-melodic.img
aws s3 cp ev3-ros-melodic.zip s3://<your_bundles_bucket_name>
aws s3 presign s3://<your_bundles_bucket_name>/ev3-ros-melodic.zip
```

3. The **presign** command will output a URL like the one below, which will be valid for an hour by default. Then use your browser or wget to download this file to your local machine:
```
https://<your_bundles_bucket_name>.s3.amazonaws.com/ev3-ros-melodic.zip?AWSAccessKeyId=...
```

4. Burn the image to your 8GB or larger Micro SD-Card using a tool like [Balena Etcher][53179d5c].

5. Once the process has completed, before you eject the drive we need to make one small change to the image. Docker does not allow us to modify the **/etc/hosts** file during build and so we need to update this file now for EV3DEV and ROS to communicate. **Open as root** and edit the file `rootfs/etc/hosts` and add the following host entries to the bottom:
```
  127.0.1.1 ev3dev
  10.42.0.1 raspberrypi
```
Save and close the file
5. Now un-mount any of the SD-Cards partitions which auto-mounted after being burned.

6. Eject/remove the SD-Card.

#### Run and Setup EV3DEV Image
1. Ensure that your EV3 is turned off and insert the SD-Card into the slot on it's side, then power it up.

2. EV3DEV should now boot up. This might take a few minutes. Once complete you will be presented with the EV3DEV Brickman menu. [If not, see issue 2 below.](#Issues)

3. From the Brickman menu we need to setup the wifi and ethernet.
  _Note that setting up the wifi is not a hard requirement. This project can function without the wifi as the communications between EV3 and Raspberry Pi all happen over the low latency ethernet. And you can ssh from the Raspberry Pi to the EV3 if need be. It is just much easier to troubleshoot the EV3 if you have direct dedicated connection to it._

4. Using the up and down buttons on the EV3, scroll down to **Wireless and Networks** and press the middle button.

5. Ensure that the USB Wi-Fi Dongle is connected to the EV3. There are  a few supported Wi-Fi dongles [listed on the EV3 site][d7c3aaef]. We tested the Ralink Technology, Corp. RT5370 Wireless Adapter and since we also needed 5GHz wifi, we used the Edimax AC600 Dual-Band adapter. Both worked great and had out of the box support with EV3DEV Stretch.

6. Select **Wi-Fi** and check that the square next to **Powered** is filled in, if not, select it.

7. Now select **Start Scan** and wait for your nearby wifi networks to appear below.

8. Select your wifi SSID, then select **Connect** and use the navigation buttons to enter your password.
   _**Pro tip:** this step can be tedious depending on your password length. If you have a **powered** USB hub and keyboard, you can plug both the wifi dongle and the keyboard in the hub and connect that to the Ev3, enter the password, complete the wifi setup then remove the hub and re-insert the wifi dongle._

9. Once your wifi is connected go back pressing the top left button on the EV3 and select **All Network Connections**.

10. Ensure that your **USB to Mini-USB cable** is connected to the EV3 and the Raspberry Pi. The Mini-USB end goes in the EV3 and the normal male USB end plugs into the Raspberry Pi.

11. Select **Wired**, select **Connect**, then **Connect automatically**.

12. Select **IPV4** then **Change** and now select **Load Linux defaults**.

13. This should now set your ethernet to:
```
IP address: 10.42.0.3
Mask: 255.255.255.0
Gateway: 10.42.0.1
```

14. You may now go back to the main menu by pressing the back button.

**Congrats, your EV3 is now ready!**

### Raspberry Pi Setup (**[PLACEHOLDER]** mins)

#### Install Raspbian
1. Download Raspbian Buster Lite from [raspberrypi.org][b154578b].

2. Burn the image to your 16GB or larger Micro SD-Card using a tool like [Balena Etcher][53179d5c].

3. After the image is burned, mount the SD-Card **rootfs** partition.

4. In order to connect the Raspberry Pi to the EV3 Robot via the Ethernet over USB cable, we need to setup the interface. **Open as root** and edit the file `rootfs/etc/dhcpcd.conf` and add the following to the end of the file:
```
interface usb0
static ip_address=10.42.0.1/24
```

5. We can also setup our wifi at this point and avoid the need to connect a screen and keyboard to the Raspberry Pi to complete the setup. **Open as root** and edit `rootfs/etc/wpa_supplicant/wpa_supplicant.conf` and add the following at the end of the file:
```
  country=YOURCOUNTRYCODE

  network={
  	ssid="SSIDNAME"
  	psk="PASSWORD"
  }
```

6. To activate SSH you need to create a file on the **boot** partition of the SD-Card. Mount the volume and create an empty file called `ssh`.

7. To activate the Raspberry Pi Camera, open the `config.txt` in the **boot** partition and add the following to the end of the file:
```
start_x=1
```

8. Since Docker does not allow us to modify the **/etc/hosts** file during build and so we need to update this now for EV3DEV and ROS to communicate. **Open as root** and edit the file `rootfs/etc/hosts` and add the following host entries to the bottom:
```
  10.42.0.3 ev3dev
```
Save and close the file

9. Unmount your SD-Card and insert it into the Raspberry Pi

#### Setup Raspbian (**[PLACEHOLDER]** mins)
_These instructions are summarized from the [Greengrass documentation](https://docs.aws.amazon.com/greengrass/latest/developerguide/setup-filter.rpi.html) and [more here][74504248]_
1. Power on your Raspberry Pi and a wait a few moments for the OS to boot.

2. If you don't have a keyboard and mouse connected to the device then through some networking investigations you should be able to track down the current IP address of your device. You could look at your DHCP Server's list of IP leases and find the IP or use a ping scanner to discover any new devices on your network.

3. SSH to the device using it's IP and username `pi`. The default password is `raspberry`.

4. To setup and install dependencies, Greengrass Core and other required system settings, download and run the following script:
```
wget ##GITHUBURL/raspberrypi_setup.sh
chmod +x raspberrypi_setup.sh
./raspberrypi_setup.sh
```

5. Once that has completed you need to place the IoT Thing certificates onto the device. To do this you will need to retrieve the key contents from the AWS Secrets Manager, where the certificates, that were created by the CFN template you deployed earlier, has been stored. Navigate to the Secrets Manager console and look for the following stored secrets: `ThingCertificatePEM`, `ThingPrivateKey`.

6. Open the `ThingCertificatePEM` Secret and click **Retrieve secret value**. Copy the plaintext value outputted.

7. Write the value to the `certs` folder on the Greengrass Core Raspberry Pi with:
```
  sudo tee /greengrass/certs/ggc.cert.pem > /dev/null <<'TXT'
  #### PASTE YOUR CERT DATA HERE ####
  -----BEGIN CERTIFICATE-----
  ABCD
  .....
  ==WXYZ
  -----END CERTIFICATE-----
  TXT
```
_Ensure to end the command with the TXT delimiter._

8. Open the **ThingPrivateKey** Secret and click **"Retrieve secret value"**. Copy the plaintext value outputted.

9. Write the value to the `certs` folder on the Greengrass Core Raspberry Pi with:
```
  sudo tee /greengrass/certs/ggc.private.key > /dev/null <<'TXT'
  #### PASTE YOUR KEY DATA HERE ####
  -----BEGIN RSA PRIVATE KEY-----
  ABCD
  .....
  ==WXYZ
  -----END RSA PRIVATE KEY-----
  TXT
```
_Ensure to end the command with the TXT delimiter._

10. Next you need to update the `/greengrass/config/config.json` file by replacing references to your certificates. Fill in the variables below and run the commands to replace the placeholders in the file.
_Note that these values can be retrieved from your CloudFormation's Stack Outputs._
```
THINGARN='<yourthingarn>'
IOTHOST='<youriotendpointhostname>'
sudo sed -i "s#%THINGARN%#$THINGARN#g" "/greengrass/config/config.json"
sudo sed -i "s#%IOTHOST%#$IOTHOST#g" "/greengrass/config/config.json"
```

11. Check that all the files has been correctly written to their respective locations:
```
sudo cat /greengrass/certs/ggc.cert.pem
sudo cat /greengrass/certs/ggc.private.key
sudo cat /greengrass/config/config.json
```

12. Now reboot the device with:
```
sudo reboot
```

13. Once the device has been rebooted, navigate over to the Greengrass Console and under **Greengrass/Groups** look for the group with the name you entered in the ClouFormation stack for the **Greengrass Core name**.

14. Open the Greengrass group and in the Deployments section, click **Actions** then **Deploy**. At the next screen you are being asked to **Configure how Devices discover your Core**. Select **Automatic detection**.

15. If all goes well your Greengrass deployment should complete deploying to the Greengrass Core Device. Navigate to **Cores**, in the left menu, and click on the core listed. Now click **Connectivity** in the menu. Under **Core Endpoints** you should now see your device's IP address listed with Port **8883**.

16. Now click on **Shadow** in the menu and click **Create shadow document**.

**Congrats, Greengrass core is now fully deployed to the Raspberry Pi!**

### Checkpoint
At this point we need to set a checkpoint and ensure we have everything ready to continue.

1. You should have created your AWS Resources and your RoboMaker Development environment.

2. Your EV3 should be running EV3DEV and is connected to wifi and via ethernet-over-usb to the Raspberry Pi. If either of these are not running after you happen to restart the EV3, [see issue 3 below.](#Issues)

3. Your Raspberry Pi should be up an running with Greengrass Core deployed.

4. You should be able to **ping** the EV3 from the Raspberry Pi using it's hostname **ev3dev** and from the EV3DEV to the Raspberry Pi using **raspberrypi**. This will go over the USB connection and should have a low stable latency.

5. You should build the LEGO® robot using the instructions found in this repository under ```lego-designs```. Both a PDF and the source files are there. To design these files we used the [LDraw Library][293682da] of parts imported into [LEOCad][0719d3f1] and published to the manual file using [WebLic][9c985bf5].

6. You should connect your XBOX wifi adapter to the Raspberry Pi via USB.

7. Both your EV3 and Raspberry Pi should be booted up and ready.

## Usage Instructions
Now with your hardware ready we may run through the rest of the procedures to complete the setup.

### RoboMaker

#### Train the model and simulate
With your RoboMaker Development Environment setup you can now prepare your reinforcement learning model and ROS application. This part of the project is optional, but recommended in order to understand how everything works and learn how to train and evaluate your own model. Training takes up to 8 hours to get a good model and an additional [PLACEHOLDER] hours to build and bundle the app. So if you want to just get the robot working and use our pre-trained model and app instead,then you are welcome to skip this part and move on to step: [Download and use a pre-trained model and ROS app](#Download and use a pre-trained model and ROS app).

1. On the AWS Cloud9 menu bar, select **RoboMaker Run**, **Launch simulation**, then **1. ObjectTracker Train Model**. This process uploads the **output.tar** bundle file to the S3 bundles bucket created by CloudFormation, then it creates a simulation application and a simulation job in AWS RoboMaker.

2. On the AWS Cloud9 menu bar, select **RoboMaker Simulation (Pending)**, then **View Simulation Job Details**. This takes you to the AWS RoboMaker Simulation Job console.

3. In the AWS RoboMaker Simulation Job details page, make sure the job status is **Running** before continuing to the next step.

4. Scroll down to the bottom of the page and choose the **Simulation application** tab, you see the environment variables and the **MODEL_S3_BUCKET** variable is where the trained model is uploaded once training is completed.

#### Using Gazebo
AWS RoboMaker provides tools to visualize, test and troubleshoot robots in the simulation. For example, Gazebo lets you build 3D worlds with robots, terrain, and other objects. It also has a physic engine for modeling illumination, gravity, and other forces. Robotics developers use Gazebo to evaluate and test robots in different scenarios, often times more quickly than using physical robots and scenarios.

On the job detail page, choose the Gazebo icon to visualize the simulation world. You can zoom in and out in the world to explore. The robot works in two phases. In the first phase, the robot performs actions based on the model, and is given a reward based on how well it performs. In the second phase, the robot is training the model using the rewards from the first phase. To learn more about the Reinforcement Learning library used in the tutorial, review the [Reinforcement Learning Coach by Intel AI Lab][f029998a] on GitHub. There could be times where the robot might move in circles or may look stuck while training the reinforcement learning model, this is perfectly normal.

#### Using rqt
The rqt tool is a Qt-based framework and plugins for ROS GUI development. The tool hosts a number of different plugins for visualizing ROS information. Multiple plugins can be displayed on a custom dashboard, providing a unique view of your robot.

1. On the job detail page, choose **rqt** to look at node graph and look at how messages flow through the system. On the **rqt** menu bar, select **Plugins**, **Introspection**, and **Node Graph**.

2. Another useful way to use **rqt** is to look at all topics and messages in the system. On the **rqt** menu bar, select **Plugins**, **Topics**, and **Topic Monitor** to view all running topics.

#### Using rviz
ROS Visualizer (rviz) is a tool for visualizing sensor data and state information from ROS. The tool is a 3D visualization tool for ROS applications. It provides a view of your robot model, capture sensor information from robot sensors, and replay captured data. It can display data from camera, lasers, from 3D and 2D devices including pictures and point clouds.

1. On the job detail page, choose **rviz**. You can use this tool to visualize what the robot sees through its camera. On the **rviz** menu bar, choose **Add**, select **By topic** tab, **/rgb/image_raw/Image** topic, and choose **OK**.

2. You now see the images captured by the Robot’s camera as it moves.

#### Using the terminal
The **terminal** provides access to a command line on the simulation job host. You can use ROS commands such as rostopic list, rostopic info to test, debug and troubleshoot in the simulation environment.

**You can also access the Gazebo, rqt, rviz, and Terminal tools from the AWS Cloud9 IDE menu bar.**

#### Using CloudWatch
If something goes wrong in one of your own simulations, the ROS logs are a good place to start debugging. You can find ROS stdout and stderr outputs for the simulation job in CloudWatch Logs. To access full ROS logs, it is in the output folder located in the S3 bucket that you created in module 1.

1. In the AWS RoboMaker Simulation Job details page, scroll down to the bottom of the page and choose **Configuration** tab then **Logs** to access CloudWatch Logs.

2. You can also see CloudWatch metric published by AWS RoboMaker in the Cloudwatch Metric and Custom Namespace section.

3. The metric published by Object Tracker is the reward that the robot earned every episode. You can think of this metric as an indicator into how well your model has been trained. If the graph shows a plateau, then your robot has finished learning. By default, a training job is complete in 8 hours. You can extend the training job longer. Longer training typically would mean a more accurate model. With Amazon SageMaker GPU instance, the training can be much faster.

4. The trained models are stored in your S3 bucket at **model-store/model/**. In the next module you use an AWS RoboMaker simulation to evaluate this model.

5. Wait 8 hours for the training to complete and then continue below.   

#### Evaluate the trained model
Now that the model has been trained, you need to evaluate the model by placing the TurtleBot 3 Burger in different locations, and checking whether the trained model can successfully navigate the TurtleBot 3 Waffle Pi to the Burger.

1. To start the evaluation simulation job go to the AWS Cloud9 menu bar, select **RoboMaker Run**, **Launch simulation**, then **2. ObjectTracker Evaluate Model**.

2. If the following dialog pops up, **You already have a job running..."** choose **OK** to continue.

#### Visualize the RL model working
1. In the AWS RoboMaker console, go to Simulation jobs section and select the new simulation job created by choosing the link. Make sure the job has the status of **Running**.

2. In the evaluation job detail page, open Gazebo again. This time, try to move the TurtleBot 3 Burger around and see if the TurtleBot 3 Waffle Pi follows it. To move the TurtleBot 3 Burger around, choose the arrow button in action bar.

#### Build and bundle the robot application (60 mins)
In this step, you’ll build and bundle the robot application with the trained RL model for the Raspberry Pi ARM architecture.

1. In AWS Cloud9 IDE, go to `lego_robot/robomaker/robot_ws/src/object_tracker_robot/config` folder, open `model_config.yaml` file and fill in the bundles bucket name. This file instructs build process to download the trained reinforcement model from your Amazon S3 bucket and put it in the bundle that you deploy to the robot.

2. In AWS Cloud9 IDE terminal window, execute the following command to download and build a cross-platform container image. This image is used for compiling and bundling a robot application for the TurtleBot ARM architecture. This process takes about 10 minutes to complete.
```
cd ~/environment/lego-robot/docker
sudo ./build_raspberry_image.sh
```

3. When that process has completed, execute the following commands to create a running container with image built in earlier step.
```
cd ~/environment/lego-robot/robomaker/robot_ws
docker run -v $(pwd):/robot_ws -v ~/.aws:/root/.aws ros-cross-compile:armhf robot_ws/src/build_arm_pkg.sh
```
**Note, there is a known issue here where the first time the build & bundle process above is run, the output.tar file is not complete. The above docker step must be run again to ensure the file is complete.**

4. When the process has completed, the robot application is now built and bundled for ARMHF, the same architecture that is used by the Raspberry Pi. The **output.tar** bundle file is created in the **lego-robot/robomaker/robot_ws/bundle/** folder. The bundle contains the trained reinforcement learning model and the logic that helps the robot use the model in real world.

5. Upload the bundle file to your S3 bucket with this command:
```
aws s3 cp bundle/output.tar s3://<your_bundles_bucket_name>
```

#### Download and use a pre-trained model and ROS app
_If you trained your own model and bundled your own ROS app, you must skip this step and go on to: **Deploy your model**._
1. From your Cloud9 terminal run the following commands:
```
cd ~/lego-robot/robomaker/
wget [PLACEHOLDER]/output.tar
aws s3 cp output.tar s3://<your_bundles_bucket_name>
```

#### Deploy your model and ROS app
1. From the RoboMaker console select **Deployments** from the menu.

2. Click **Create deployment**.

3. From **Fleet** select the **RobotFleet** deployed by the CloudFormation template.

4. From **Robot application** select the **RobotApp** deployed by your CloudFormation template.

5. Under **Robot application version** select **Create new** and click **Create**. If all is well a green bar should appear with a message **Version successfully created**.

6. Enter `object_tracker_robot` in the **Package Name** field and `main.launch` in **Launch file** field.

7. Leave the rest as is, scroll down and click **Create**.

8. At the deployment details page you will now be able to monitor the deployment of your app to the Raspberry Pi using Greengrass. The first time this will take about [PLACEHOLDER] mins to complete.
_Note that subsequent deployments of your robot app will be much quicker as Greengrass will work out what's changed and only upload that to the device. Additionally, creating a new deployment is much easier the next time you need to deploy an updated output.tar in S3. All you do is open a previous deployment and click **Clone**, create a new version from the new file in S3 and click deploy, the rest of the fields will already be filled in._

#### AWS IoT Console
While this robot is designed to be controlled via Alexa, you can also interact with it via the AWS IoT Greengrass Thing Shadow, as this is the way that Alexa sends updates to the device.

1. Go to IoT Greengrass console, click on **Cores** in the left menu.

2. Select your Core device, it will have the name you gave it during CloudFormation Stack creation.

3. Select **Shadow** from the menu on the left.

4. Under **Shadow Document** click **Edit** and enter the following for the shadow state:
```
{
  "desired": {
    "active_mode": "tracking"
      }
}
```
Substitute **tracking** with and other supported modes, found in the [FAQ](#FAQ).

5. Click **Save**. If everything has been setup correctly, your robot should start to move according to the mode you chose. If you chose tracking, move the robot to a clear area where there is a uniform, light coloured background and place a dark object in front of it, in theory it should track towards it.  

#### Alexa Developer Portal
1. From the same account linked to your Amazon Echo, log in to the [Alexa Developer Portal][e3980573] and click **Create skill**

2. Enter a name for the skill like `Lego Robot`.

3. Choose the **Custom** model and **Provision your own** endpoint.

4. Click **Create skill**.

5. Choose **Start from scratch**.

6. Now that the skill console is open, go to **Endpoint** in the menu.

7. Select **AWS Lambda ARN**.

8. Click **Copy to Clipboard** to store the **Skill ID**.

9. From the CloudFormation stack ouputs, enter the **Alexa Lambda Arn** into the **Default Region** field.

10. Now go to the AWS Lambda Console and open the same Lambda function. In the **Designed** pane, click **Add trigger**.

11. From the drop down list, select **Alexa Skills Kit** and paste your skills id in the box and click **Add**. Your skill id should now be linked to the function.

12. Go back to the Alexa Developer Portal and click **Save Endpoints**.

13. Now go to **JSON Editor** in the left menu.

14. Drag and drop the `alexa/skill.json` file in this repo to the **JSON Editor**.

15. Click **Save Model**.

16. Click **Build Model** and wait for the build job to complete and say **Full Build Successful**

17. Go to the **Test** menu at the top and enable this skill for **Development**

18. You should no be able to invoke the skill with "Alexa, open my robot project". She will reply: "Welcome, choose a mode", now you can say a supported mode: "Tracking, joystick, halt, snake, square, charge"

#### EV3DEV
Needing to work on the EV3DEV OS can be useful for troubleshooting and development. Full instructions on using the EV3DEV OS is out of scope for this document but there is lots of help that can be found in the references below.

For our use case we would just need to SSH to the device and perhaps restart the ROS service.

SSH to the device with:
```
ssh robot@IPADDRESS
```
Password is: `maker`

Restart the ROS service with:
```
sudo systemctl restart roscontroller
```
_Note at this point there are no logs being written to a file as this was not working as expected. Stop the roscontroller service and run the bash script controller.sh manually as and monitor for print statements._

#### Raspberry Pi
To troubleshoot ROS on the raspberry pi doa a `sudo -i` to switch to root. This will run a script to set your ROS environment variables and allow you to run things like `rostopic echo cmd_vel` or `rostopic echo ev3/active_mode` etc.

Monitoring logs on the Raspberry Pi can be crucial when troubleshooting Greengrass and your ROS app.

Still as root, have a look through:
```
/home/ggc_user/ros/home/deployment-<DEPLOYMENTID>/log/latest/
/greengrass/ggc/var/log/user/us-east-1/<ACCOUNTID>/aws-robomaker-deployment-function-armhf_DO_NOT_DELETE.log
/var/log/syslog
```

## References
This project made use of the following references:

## ROS and EV3
https://www.ev3dev.org/
https://github.com/ev3dev/brickstrap/blob/master/docs/brickstrap.md
https://github.com/osmado/ev3dev_ros_distribution
https://github.com/moriarty/ros-ev3
http://wiki.ros.org/

### AWS IoT & RoboMaker
https://aws.amazon.com/robomaker/resources/train-a-robot-using-reinforcement-learning-project/
https://aws.amazon.com/blogs/iot/automating-aws-iot-greengrass-setup-with-aws-cloudformation/
https://docs.aws.amazon.com/robomaker/latest/dg/what-is-robomaker.html
https://docs.aws.amazon.com/robomaker/latest/dg/gs-following.html
https://github.com/aws-robotics/aws-robomaker-sample-application-objecttracker


## Issues
1. Some might note that there are some older ROS packages available in the EV3DEV repositories, however during the build of this project, we were unable to get the EV3DEV ROS packages to work with Python 3, and since it is strongly recommended to use the Python 3 EV3DEV libraries, we went with an alternative working solution and provided us the ability to run the latest ROS Melodic. If the EV3DEV repositories are to be updated to ROS Melodic with Python 3 support or ROS 2 Dashing, then this would simplify the install and negate the need to compile ROS on EV3DEV.

There were a variety of ways found to run ROS on EV3DEV, this process was the only one we could get to work and a lot of thanks goes to [Alex Moriarty](https://github.com/moriarty) and [osmado](https://github.com/osmado) for their work on a ROS EV3 build.

2. If your EV3DEV has not completed booting up after 5 minutes and there is some text on the screen, it's gotten stuck on some timeout (It might say: "Timed out waiting...."). This is OK, it happens intermittently and if you hold both the middle button and the top left down for 2-3 seconds, it will reboot and start up again, chances are it will boot up ok. If it gets stuck again, repeat until it boots up. We have not been able to ascertain what is the cause of this issue, but it always seems to come right after 2 or 3 boots. If anyone figures out why, please let us know by reporting an issue.

3. When booting up the EV3, on one device it would start up the wifi automatically but not the ethernet, on another device, it would start up the ethernet automatically and not the wifi. So you may have to turn on the wifi/ethernet and connect manually on boot.

4. Currently the Object Tracking ROS App does not support ROS Melodic so for now we have stuck with Kinetic until an updated build process can be developed.


  [067e401b]: https://www.lego.com/en-us/product/lego-mindstorms-ev3-31313 "LEGO® Mindstorms® EV3 kit"
  [1705700a]: github.com "Lego Robot Demo CloudFormation Template"
  [9b3ae94d]: https://github.com/ev3dev/brickstrap "EV3DEV brickstrap tool"
  [d7c3aaef]: https://github.com/ev3dev/ev3dev/wiki/USB-Wi-Fi-Dongles "EV3DEV Supported wifi adapters"
  [b154578b]: https://www.raspberrypi.org/downloads/raspbian/ "Raspberry Pi images"
  [53179d5c]: https://www.balena.io/etcher/ "Balena Etcher - Image burning tool"
  [293682da]: https://www.ldraw.org/downloads-2/third-party-software.html "LDraw Library"
  [0719d3f1]: http://www.leocad.org/ "LEOCad"
  [9c985bf5]: http://bugeyedmonkeys.com/lic/ "WebLic"
  [e3980573]: https://developer.amazon.com/alexa/console/ask "Alexa Developer Portal"
  [f029998a]: https://github.com/NervanaSystems/coach "Reinforcement Learning Coach by Intel AI Lab"


## Authors
- Ruald Andreae rualda@amazon.com
- Kyle Huang kylehh@amazon.com

## License Summary
This sample code in this repo is made available under the Apache 2.0 license. See the LICENSE file.

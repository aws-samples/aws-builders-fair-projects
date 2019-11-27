# PI Joysticks for IOTRacer.Ninja #
This readme will walk through all the steps that you need to follow to create the physical joysticks for IoTRacer.Ninja.  For re:Invent 2019, we are creating 2 joystick housings, each holding 2 joysticks.  This 

## Bill of Materials ##
1. 2 [Raspberry Pi 3 Model B+](https://www.amazon.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/dp/B07P4LSDYV/ref=sr_1_1_sspa?keywords=raspberry+pi+3+b%2B+motherboard&qid=1573661642&s=electronics&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzMFJVSDdKM0ZEWjhDJmVuY3J5cHRlZElkPUEwNjg1MDUyMVlJTVdHSERGOFdHNCZlbmNyeXB0ZWRBZElkPUEwNzYyOTk2M09aSE0yNFA4QTBXWiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=)
2. 2 [32 GB microSDHC card](https://www.amazon.com/Samsung-MicroSDHC-Adapter-MB-ME32GA-AM/dp/B06XWN9Q99/ref=pd_bxgy_147_img_3/131-3201718-1263266?_encoding=UTF8&pd_rd_i=B06XWN9Q99&pd_rd_r=c67892c4-cd79-4100-98da-13f5648d4b26&pd_rd_w=Qx0wU&pd_rd_wg=SVVrn&pf_rd_p=09627863-9889-4290-b90a-5e9f86682449&pf_rd_r=S0PWX7A0KRBZTPC1PFXJ&psc=1&refRID=S0PWX7A0KRBZTPC1PFXJ)
3. 2 [Raspberry Pi 3 Model B+ case](https://www.amazon.com/gp/product/B079M96KWZ/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
4. 2 [Raspberry Pi 3 Model B+ power supply](https://www.amazon.com/CanaKit-Raspberry-Supply-Adapter-Listed/dp/B00MARDJZ4/ref=sr_1_5?crid=2BSCPTVZN7184&keywords=raspberry+pi+3+b%2B+power+supply&qid=1573661825&s=electronics&sprefix=raspberry+pi+3+b%2B+power%2Celectronics%2C186&sr=1-5)
5. 1 [Hikig 4 Player Joystick Kit](https://www.amazon.com/gp/product/B07KFWRPF7/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
6. 4 [Traffic Lights]()
7. 2 [Breadboards]()
8. 2 2' x 1' x .5" MDF Boards (~1 foot per joystick)
9. 8' 1" x 2" board for base
10. 16 bolts and nuts

## Raspberry Pi Setup ##
1. Install Noobs onto the memory card following directions on the [Raspberrypi.org site](https://www.raspberrypi.org/documentation/installation/noobs.md).  We used Noobs v 3.0.1 for this project.
2. Install the memory card into the Raspberry Pi 3B+ motherboard, connect a mouse, keyboard, and monitor, and connect a power supply to it to boot it up.
3. Follow the on-screen prompts for a full Raspian installation to continue the installation and reboot the device.  Once reboot is complete, follow the prompts to:
* Set the country inputs and timezone appropriate to your location
* Set the password to something you will remember.
* Connect the Pi to a Network.  Note the IP address of the Pi so that you can ssh to it later.
* Update the system software
4. [Enable SSH to the Raspberry Pi](https://www.raspberrypi.org/documentation/remote-access/ssh/)
5. [Enable Boot Option for Wait on Network](https://raspberrypi.stackexchange.com/questions/45769/how-to-wait-for-networking-on-login-after-reboot)
6. On the Raspberry Pi, open a Terminal session and type 
```
sudo apt-get update -y
```

## Update Python to version 3.7.4 ##
The joystick code relies on Python 3.7.4 to be installed on the Raspberry Pi.  There is not a distribution of this currently.  Follow the steps below to complete this update.

1. Install the Build Tools
```
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
```

2. Download and Install Python 3.7.4
```
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz
tar xf Python-3.7.4.tar.xz
cd Python-3.7.4
./configure
make -j 4
sudo make altinstall
```

3. Validate the installation
```python3.7 --version```

This command should report Python 3.7.4

4. Clean up from Installation

```
cd ~
sudo rm -r Python-3.7.4
rm Python-3.7.4.tar.xz
sudo apt-get --purge remove build-essential tk-dev -y
sudo apt-get --purge remove libncurses5-dev libncursesw5-dev libreadline6-dev -y
sudo apt-get --purge remove libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev -y
sudo apt-get --purge remove libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
sudo apt-get autoremove -y
sudo apt-get clean
```

## Update Hostname ##
Give your Pi a unique hostname.  This value will be used to register it with AWS IoT and will use this name to read the appropriate certificates for AWS IoT.

1. Use the command below to edit the /etc/hostname file to update your hostname value
```
sudo nano /etc/hostname
```

Replace 'raspberrypi" with your host name, press Control-X and save the file

2. Use the command below to update your /etc/hosts file to update your host
```
sudo nano /etc/hosts
```

Replace "raspberrypi" with your host name, press Control-X and save the file

3. Reboot the Pi
```
sudo nano reboot
```

## Install Python Libraries for Joystick ##
The Joystick requires Asyncio, AWSIoTPythonSDK.MQTTLib, evdev, json, logging, os, and RPi.GPIO libraries to be installed with Python3.7.  Use the following line to perform these installations.
```
sudo python3.7 -m pip install asyncio AWSIoTPythonSDK evdev RPi.GPIO
```

## Raspberry Pi Wiring ##
The Traffic Lights are used to communicate the state of the device to the user.
* Green = Ready for Input
* Yellow = Input Locked
* Red = Bad Input (will change to Green after flashing red)

For this project, we are connecting 2 Traffic Lights to 1 Pi, one for each player.  

The Traffic Light has 4 connectors, from left to right, GND, I011 (GREEN), I09 (RED), and I010 (YELLOW).  Connect the lights as follows:

| Light 1 | PIN | GPIO |
|---------|-----|------|
| GND     | 25  | NA   |
| I09     | 23  | 11   |
| I010    | 21  | 9    |
| I011    | 19  | 10   |

| Light 2 | PIN | GPIO |
|---------|-----|------|
| GND     | 34  | NA   |
| I09     | 33  | 13   |
| I010    | 38  | 20   |
| I011    | 40  | 21   |

These connections in the example are done via a breadboard.

## USB Connections for Joysticks ##
The USB slot each joystick is connected to identifies the color of the car that joystick will control.  With the Pi's ports facing you, the settings are:

| Network Port | USB Port: BLACK   | USB Port: RED |
| Network Port | USB Port: WHITE   | USB Port: BLUE |

## Installation of IoTRacer.Ninja ##
1. Download the joy.py file from this repository and place it in the home/pi directory.
2. Download the Amazon Root CA certificate from [AWS](https://docs.aws.amazon.com/iot/latest/developerguide/server-authentication.html#server-authentication-certs) and place it in the home/pi/root directory
3. Download your device certificate from AWS IoT and place it in the home/pi/certs directory
4. Update the joy.py file to identify your IOT Endpoint on line 27 by modifying the value stored in ENDPOINT

## Configuration to Run Joy.py from startup ##
In progress

## Physical Build ##
1. Measure where you will be drilling on the MDF for the Joystick and Button
* Measure out where you would like to place the joystick.
* Measure a spot for the button at this time.  The button in our example is placed to the outside of the joystick.
* Measure a spot where you will run wiring from the bottom

2. Drill the holes for the joystick and the button
* Holes for the joysticks should be approximately 1" circle, to allow for movement
* Holes for the buttons should be 1 1/8" circles
* Holes for wiring should be 1/2" circles
* 
3. Place the joystick in the area where you will be mounting it and mark the areas for mounting it using the base

4. Remove the joystick and drill your mounting holes
* Holes for the joystick mounts should be ??" and you will need 4 of them

5. Replace the joystick in the hole and connect it to the board using bolts and nuts through the 4 mounting holes you just drilled

6. Place the button in the hole you drilled for it and connect it with a nut from the joystick kit

7. Add the footings to the bottom of the board.  In our case, we used a 2' 2"x1" board for the foot and an 11" 2"x1" board for the sides, leaving the back open

8. Mount the Raspberry Pi and the Breadboard to the bottom of the MDF, using Velcro

9. Feed the wires for the traffic lights through the holes that were drilled for lighting 

10. Connect the traffic lights to the wires and mount them to the board or other mounting
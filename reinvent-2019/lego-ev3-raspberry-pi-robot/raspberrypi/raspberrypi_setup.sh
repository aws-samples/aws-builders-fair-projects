# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash

# Update the OS
sudo apt-get update
sudo apt-get upgrade -y

# Install some dependencies
sudo apt-get install xboxdrv liblapack-dev libblas3 -y

# Setup Greengrass user and other required system settings
sudo adduser --system ggc_user
sudo addgroup --system ggc_group
echo -e "fs.protected_hardlinks = 1\nfs.protected_symlinks = 1" | sudo tee -a /etc/sysctl.d/98-rpi.conf
sudo sysctl -a 2> /dev/null | grep fs.protected
sudo sed -i '$ s/$/ cgroup_enable=memory cgroup_memory=1/' /boot/cmdline.txt

# Install Greengrass
wget https://d1onfpft10uf5o.cloudfront.net/greengrass-core/downloads/1.9.4/greengrass-linux-armv7l-1.9.4.tar.gz
sudo tar -xzvf greengrass-linux-armv7l-1.9.4.tar.gz -C /

sudo wget -O /greengrass/certs/root.ca.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem

sudo tee /etc/systemd/system/greengrass.service > /dev/null <<'TXT'
[Unit]
Description=Greengrass Daemon

[Service]
Type=forking
PIDFile=/var/run/greengrassd.pid
Restart=on-failure
ExecStart=/greengrass/ggc/core/greengrassd start
ExecReload=/greengrass/ggc/core/greengrassd restart
ExecStop=/greengrass/ggc/core/greengrassd stop

[Install]
WantedBy=multi-user.target
TXT
sudo systemctl enable greengrass.service

sudo tee /greengrass/config/config.json > /dev/null <<TXT
{
  "coreThing" : {
    "caPath" : "root.ca.pem",
    "certPath" : "ggc.cert.pem",
    "keyPath" : "ggc.private.key",
    "thingArn" : "%THINGARN%",
    "iotHost" : "%IOTHOST%",
    "ggHost" : "greengrass-ats.iot.us-east-1.amazonaws.com",
    "keepAlive" : 600
  },
  "runtime" : {
    "cgroup" : {
      "useSystemd" : "yes"
    }
  },
  "managedRespawn" : false,
  "crypto" : {
    "principals" : {
      "SecretsManager" : {
        "privateKeyPath" : "file:///greengrass/certs/ggc.private.key"
      },
      "IoTCertificate" : {
        "privateKeyPath" : "file:///greengrass/certs/ggc.private.key",
        "certificatePath" : "file:///greengrass/certs/ggc.cert.pem"
      }
    },
    "caPath" : "file:///greengrass/certs/root.ca.pem"
  }
}
TXT

# Setup permissions to access the video and input devices
sudo usermod -a -G video ggc_user
sudo tee /etc/udev/rules.d/99-custom.rules > /dev/null <<'TXT'
SUBSYSTEM=="video4linux", ATTR{index}=="0", ATTR{name}=="camera0", MODE="0777"

SUBSYSTEM=="input", KERNEL=="js0", MODE="0777"
TXT

# Setup ROS env variable script
sudo tee /root/set_ros_env.sh > /dev/null <<'TXT'
#!/bin/bash

files=$(ls /home/ggc_user/roboMakerDeploymentPackage/ | grep -vwE '\w{1,30}')
array=($files)
exec 3>&2
exec 2>/dev/null
BUNDLE_CURRENT_PREFIX=/home/ggc_user/roboMakerDeploymentPackage/${array[0]} . /home/ggc_user/roboMakerDeploymentPackage/${array[0]}/setup.sh;
BUNDLE_CURRENT_PREFIX=/home/ggc_user/roboMakerDeploymentPackage/${array[1]} . /home/ggc_user/roboMakerDeploymentPackage/${array[1]}/setup.sh;
exec 2>&3
TXT

echo "source set_ros_env.sh" | sudo tee -a /root/.bashrc

# Give access to the Pi user to view ggc_user files
sudo usermod -a -G ggc_group pi

# Set EV3DEV Hostname and IP
echo -e "10.42.0.3\tev3dev" | sudo tee -a /etc/hosts

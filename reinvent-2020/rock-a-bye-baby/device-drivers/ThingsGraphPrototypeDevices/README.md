# AWS IoT Things Graph Prototype Devices

This download contains drivers for the devices used in the AWS IoT Things Graph [Creating a Flow with Devices](https://docs.aws.amazon.com/thingsgraph/latest/ug/iot-tg-gs-thing-sample.html) (motion sensor, camera, and screen).

## Prerequisites

To install the devices on your Raspberry Pi, follow the instructions in [Set Up Your Raspberry Pi](https://docs.aws.amazon.com/thingsgraph/latest/ug/iot-tg-gs-thing-sample.html#iot-tg-gs-thing-sample-rpi).

After you install the devices, make sure that you have the following installed on your Raspberry Pi:

- [``raspistill``](https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md): A command line tool that the camera driver uses to capture photographs.
- [``feh``](https://www.oreilly.com/library/view/raspberry-pi-3/9781786462121/fb685f1f-b543-457a-84fa-d395ed874e68.xhtml): An image viewer that the screen driver uses.
- [``xdotool``](https://www.semicomplete.com/projects/xdotool): A utility that the screen driver uses for window management.

## Setup

[Create Things](https://docs.aws.amazon.com/thingsgraph/latest/ug/iot-tg-gs-thing-sample.html#iot-tg-gs-thing-sample-thingssetup) contains instructions for creating things and certificates for your devices.

Enter values for the certificate paths and thing names in the following files in the configuration directory: 

- `aws-iot-ms.properties`
- `aws-iot-camera.properties`
- `aws-iot-screen.properties`

The credentials that you enter in the `aws-iot-camera.properties` file must have write access to the Amazon S3 bucket that you created for this example.

The configuration files also require your account ID, AWS Region, and client endpoint. If you're using an ATS-signed data endpoint, use the following command to get your client endpoint.

``aws iot describe-endpoint --endpoint-type iot:Data-ATS``

If you're using a VeriSign-signed data endpoint, use ``iot:Data`` as the value of the ``endpoint-type`` parameter.

### Verify

Run all of the drivers from the same directory that contains this README file.

**Screen**

Run the following command for help.

`java -cp "lib/*" com.amazon.iot.thingsgraph.devices.screen.DisplayDevice -h`

**Camera**

Run the following command for help.

`java -cp "lib/*" com.amazon.iot.thingsgraph.devices.camera.Camera -h`

**Motion Sensor**

Run the following command for help.

`java -cp "lib/*" com.amazon.iot.thingsgraph.devices.motionsensor.RaspiMotionSensor -h`

## Run the Drivers on the Raspberry Pi

Enter the following command to start the motion sensor driver. The required `-g` parameter specifies the GPIO pin to which you've attached the motion sensor.

`sudo java -cp "lib/*" com.amazon.iot.thingsgraph.devices.motionsensor.RaspiMotionSensor -f aws-iot-ms.properties -g **GPIO pin to which the motion sensor is connected**`

Enter the following command to start the camera driver. Make sure ``raspistill`` is installed on the Raspberry Pi.

`sudo java -cp "lib/*" com.amazon.iot.thingsgraph.devices.camera.Camera -f aws-iot-camera.properties -b **Your Amazon S3 Bucket**`

Enter the following command to start the screen driver. Make sure ``feh`` and ``xdotool`` are installed on the Raspberry Pi.

`java -cp "lib/*" com.amazon.iot.thingsgraph.devices.screen.DisplayDevice -f aws-iot-screen.properties`

## What the Drivers Do

The drivers perform the following tasks and send the following MQTT messages.

* The motion sensor driver waits for motion events on the GPIO pin to which it's attached. When motion is detected, it sends the following JSON to **Motion Sensor Thing Name**/motion.

`{"isMotionDetected": true}`

* The camera driver listens to capture commands sent to **Camera Thing Name**/capture and saves captured images to your Amazon S3 bucket. When each upload is
complete, it then sends the following JSON to **Camera Thing Name**/capture/finished.

`{"imageUri":"**Amazon S3 Bucket Image URI**"}`

* The screen driver listens to display commands containing the image URIs that the camera sends. These commands are sent to **Screen Thing Name**/display. It displays each image on the screen.

When you deploy the flow in [Creating a Flow with Devices](https://docs.aws.amazon.com/thingsgraph/latest/ug/iot-tg-gs-thing-sample.html) to your AWS IoT Greengrass group, AWS IoT Things Graph mediates the communications between the devices. After the motion sensor sends its message, AWS IoT Things Graph sends the capture command to the camera. After the camera indicates that the image upload is complete, AWS IoT Things Graph sends the image URI to the screen.


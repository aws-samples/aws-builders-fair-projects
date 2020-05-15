# smartgarden2020
Codes to SmartGarden 2020 -> ESP32, Lex, Alexa and Timelapse

Install Greengrass on Raspberry
Create a Thing in IoT with right IOT and Greengrass IAM permissions in the cert:
https://docs.aws.amazon.com/greengrass/latest/developerguide/gg-sec.html

Use Moongose to flash ESP32 board:
https://aws.amazon.com/pt/blogs/aws-brasil/aws-iot-com-mongoose-os-rodando-em-esp8266-e-esp32/

Put ESP32 in a sleep mode if you are going to use battery:
https://lastminuteengineers.com/esp32-sleep-modes-power-consumption/

The Greengrass raspberry local IP will be the gateway ESP32 will connect to.
You can also choose send data from ESP32 directly to the internet.

You can buy a Higrow solution:
https://hackaday.io/project/25253-higrow-plants-monitoring-sensor
https://flashgamer.com/blog/comments/review-of-higrow-esp32-moisture-and-temperature-sensor

Or you can put sensors directly on Raspberry or buy another board/create your own board.

You will need a pump and a relay to control when pump are going to be activated (circuit on).
The sensors we are using are DHT11/DHT22 and soil moisture sensor (https://www.amazon.com/Gikfun-Capacitive-Corrosion-Resistant-Detection/dp/B07H3P1NRM/ref=pd_sbs_86_t_0/142-0621292-0310020?_encoding=UTF8&pd_rd_i=B07H3P1NRM&pd_rd_r=0c49ea67-c4b8-486f-abfb-d6b73929fad7&pd_rd_w=tQoz7&pd_rd_wg=s5m8a&pf_rd_p=5cfcfe89-300f-47d2-b1ad-a4e27203a02a&pf_rd_r=X4CGG55Q19BJY2A485G5&psc=1&refRID=X4CGG55Q19BJY2A485G5)
You can choose a simple soil moisture sensor if you want to, or add another kind of sensors.

To generate timelapse, you need to use this code to put FFMPEG into a Lambda Layer:
https://github.com/serverlesspub/ffmpeg-aws-lambda-layer
So your python code can refer this layer.

To use the Lex iframe you need to launch this stack (2nd one) and later change the link int the website index.html file to insert the iframe generated here:
https://aws.amazon.com/blogs/machine-learning/deploy-a-web-ui-for-your-chatbot/

To use Alexa skills you need to create the Alexa skill in your Alexa developer account, this lambda is the backend of the skill.
https://developer.amazon.com/alexa/console/ask

There's Alexa and Lex interactions you can use to create the tenets of the solution (same mentioned in backend lambdas).

The Lambdas to run in the edge (Raspberry PI running Greengrass) can be found in lambdasGreengrass-Edge or in this git: https://github.com/tibernardinelli/plant-watering

Other helpful content:

ESP32 is the thing you ar going to Connect into Greengrass.

You can use FreeRTOS or Mooongose to program ESP32: https://aws.amazon.com/pt/freertos/
https://github.com/mongoose-os-libs/aws

To test the relay using Python in Raspberry PI: https://github.com/skiwithpete/relaypi/blob/master/4port/script4.py
 

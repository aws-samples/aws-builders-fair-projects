# IoT Racer #

IoT Racer is an IoT and Serverless project that displays long-distance command and control capabilities via a 4 player game of tag.

## Overview ##
This project contains a set of code and an AWS Cloud Development Kit (CDK) script that can be used to create the entire project.

## Architecture ##
[Architecture Diagram](./Architecture.png)

### Further Information ###
Additional READMEs can be found in the folders for each of the microservices and controllers used for the project.

- [Vehicle Microservice](./VehicleMicroservice/README.md)
- [Board Microservice](./BoardMicroservice/README.md)
- [Game Microservice](./GameMicroservice/README.md)
- [Web UI](./IoT_Web/README.md)
- [Joysticks](./pi_joysticks/README.md)
- [Game Board](./game-board/README.md)

## Running the CDK Script ##
To be created

## IOT Controller Device and Certificate Setup ##
In order for the game controller to connect to AWS IOT Core it requires 3 items:  
Device  
Certificate  
Policy  
A [wizard](https://docs.aws.amazon.com/iot/latest/developerguide/register-device.html) is available within the AWS Console for creating all 3 objects as well as attaching the policy to the certificate.  
Note that on step 6 you must download all 3 files as well as activate the device.  If you may also follow the link provided to download the AWS IOT Root CA if you have not already done so.  
It is also recommended that you rename the certificate and key files to designate which device they should be deployed to.  (ex. joystick1-certificate.pem.crt)  
Please store the files in a safe place as the certificate must be replaced if the key files are lost.  

## FAQ ##
__Q: What language(s) were used for this project?__   
Python was the only language used.

__Q: What AWS Services were used for this project?__  
AWS Cloud9, AWS CodeCommit, Amazon DynamoDB, AWS IoT, AWS Lambda, and Amazon SNS.

__Q: What development enviroment and libraries were used for this project?  What was AWS Cloud9 used for?__  
All AWS development was done using AWS Cloud9 environments with AWS CodeCommit repositories.  Chalice was used for Lambda development.  

__Q: What is Amazon SNS used for?__  
Amazon SNS is used to trigger different events for the game play.  Uses of SNS are:
* Triggering the BoardMicroservice Lambda function, which validates and orders the moves for each round
* Triggering the VehicleMicroservice Lambda function, which sends commands to the vehicles on the LED board
* Triggering the VehicleMicroservice Lambda functio, which sends commands to the joysticks to unlock them due to the next round or invalid moves
* Triggering the GameMicroservice Lambda function, which performs scoring

__Q: What is AWS IoT used for?__  
AWS IoT is used for all communication between the AWS Cloud and the Raspberry Pis.  This includes messages to and from the joysticks and LED Board.

__Q: How is Amazon DynamoDB used?__  
A single DynamoDB Table is used for the entire application.  This table tracks all the moves, where the vehicles are, and game status.

__Q: Why AWS Lambda and not AWS Step Functions?__   
We did not need the extra features that Step Functions provides for this project at this time.  Additionally, Step Functions would have driven more cost into the solution.

__Q: What is running on the Pi?__  
We have two types of Pis running for the event.  The joysticks are running on Raspberry Pi 3 B+ and the LED board is running on Raspberry Pi 4.  Both of these are using Python 3.7 and the AWSIoTPythonSDK library to communicate with the IoT Core service.

__Q: What is long distance about this project?__  
For re:Invent 2019, joysticks are setup in both Aria and MGM hotels for Builders Fair.  The gameboard exists in Detroit.  AWS IoT Core is used to send moves from the Joysticks to us-east-1.  Further commands are sent from us-east-1 to Detroit to "move" the Vehilces on a virtual board and to the Joysticks to signal when additional moves can be made.

__Q: What are the base rules of the game?__  
For the player that is It, the goal is to tag a player who is not It.  For players who are not It, the goal is to stay away from the player who is It.  The game is played in terms of rounds, where all 4 players must submit moves before a round is processed.

__Q: How does a player get tagged to be it?__  
Players get tagged at the end of a turn if the Player who is it is one space, either horizontally or vertically, from the player who is It.  Diagonal spaces do not count.

__Q: How are scores calculated?__  
Scores per round are zero based, meaning the sum of all players scores will be 0.  Scores are calculated based on the state of a player (It or Not It) and the distance increase or decrease from the Player who is It.  

Players who are not It gain or lose points based on the number of spaces they are further from or closer to the Player who is It.  A Player who gets tagged loses 20 points.  

Players who are it receive the inverse of the sum of all Player scores.  They also gain 20 points if they tag a player.  

__Q: What data does this game collect per round?__  
Each move from every round is kept in an Amazon DynamoDB table.  This includes game, round, car, coordinates, score, and who is It.  

__Q: What will be done with this data?__  
We are interested in seeing if this data can be used to generate Machine Learning models that can be used to created AI controlled players.  We do not currently have a timeline for this analysis/work.

__Q: What other game ideas can be done with this base architecture?__  
Other Games can be added to this architecture.  Currently, only a single game of Tag is implemented.  Follow the Leader and Keep Away are two additional thoughts that were explored.

__Q: Do I need to use 2 joysticks on each Pi?__  
No.  The Joysticks and Python code that runs on the two Pis for this example could be deployed to 1 - 4 Pis.  The color of the car being controlled is based on the port being used.  See the [README](./pi_joysticks/README.md) for the Joysticks to understand how this can be implemented.

__Q: Do I need to use the same type of Joystick as was used?__  
No.  We tested the code with a standard Playstation 3 controller.  If you want to use other controllers, this is possible and may require some analysis to determine the type of controller reported to the Pi and which button you want to use to submit moves.

## Authors ##
- Tim Bruce brucetim@amazon.com
- Dave Crumbacher davecrum@amazon.com
- Joy Fasnacht joyf@amazon.com
- Alex Jantz ajantz@amazon.com
- Walker Miller walkmlr@amazon.com
- Josh Ragsdale joragsda@amazon.com
- Brad Staszcuk staszcuk@amazon.com

# License #

This library is licensed under the Apache 2.0 License.

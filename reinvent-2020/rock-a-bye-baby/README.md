# Rock-a-bye-baby - Smart Baby Sleep Assistant

## Features
1. Monitoring
2. Automation
3. Analytics

## Hardware Resources
1. Raspberry Pi (eg: https://www.amazon.com/s?k=raspberry+pi)
2. PIR Motion Sensor (eg: https://www.amazon.com/Aukru-Pyroelectricity-Raspberry-Microcontrollers-Electronic/dp/B019SX734A)
3. Raspberry Pi Camera Module (eg: https://www.amazon.com/Raspberry-Pi-Camera-Module-Megapixel/dp/B01ER2SKFS)
4. USB Microphone
5. External Speaker


## Raspberry Pi Setup

To run the workflow with real devices, you need to set up your Raspberry Pi with those devices.

1. Attach your motion sensor to Raspberry Pi
2. Attach the camera by following the instructions in the Raspberry Pi camera board documentation.
3. Download and install the drivers from /device-drivers/ThingsGraphPrototypeDevices/. To install the drivers, follow the instructions in the README.
4. Download and run the Play Music python app. Follow the instructions on the README

Now you've configured your Raspberry Pi for the smart assistant.

## Create Things

Open the AWS IoT console and create two things: one thing for your motion sensor and the other for the camera.

For instructions on how to create things in the registry, see https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html. Be sure to create and activate certificates for each thing.

## Create AWS IoT Things Graph Device Models

The flow for this project has 5 custom device models to call the Lambda functions.
The TDM for the device models are under iot/tg-models. Replace the Region and Account ID on all files.

## Create and deploy AWS IoT Things Graph Flow

AWS IoT Things Graph Data Model (TDM) code, contains the definition of the flow, is under iot/tg-flow.
Replace the Region and Account ID with appropriate values

Use the instructions here to create and deploy the flow through CLI - https://docs.aws.amazon.com/thingsgraph/latest/ug/iot-tg-workflows-gs-cloud-cli.html

## Create Amazon S3 bucket

S3 is used for storing the video recordings of baby's sleep events. Once the S3 bucket is created, note down the name. You will provide this as an argument, when running the device driver on Raspberry Pi

Here are the instructions: https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html

## Create Amazon TimeStream Database and Table

Amazon Timestream is used to store the Baby's sleep events. This project requires a database "eventsDB" and a table named "sleepEvents".

AWS CLI command for db and table creation - database/create-timestream-db-cli.txt

## Create Amazon DynamoDB Table

This project creates 3 DynamoDB tables -
1. for tracking the sleep event escalations/alerts
2. for showing event history with video recordings
3. storing sleep assistant configurations

AWS CLI command for #1 is here - database/create-dynamodb-table-cli.txt

The other two will be created through AWS Amplify

## Create AWS Lambda functions

This project uses 7 Lambda functions to call API based actions and interact with Step Functions. All the Lambda functions are under lambda-functions/ folder

## Create AWS Step Functions

We are using Step Functions to track and call Lambda functions to stop the sleep assistant after configurable period

The step functions state machine definition is in /step-functions

## Use Amazon SageMaker for Audio Detection

The cry sound detection is done with a custom audio classification model using Amazon SageMaker Pytorch framework.

Details of the model here: https://github.com/aws-samples/amazon-sagemaker-audio-classification-pytorch

## Build Mobile App using AWS Amplify

AWS Amplify can be used to build and deploy secure, scalable, full-stack web and mobile applications quickly. For this prototype, I used AWS Amplify to build an app with React.js as front-end, AWS AppSync(a fully managed GraphQL service) as the backend and DynamoDB as the database.

There are 2 features - one for setting the assistant configuration and the other for viewing the sleep history.

Code is in /mobile-app  

## Generate Daily Insights Report using Amazon Quicksight

For this prototype, Amazon Quicksight is used to generate reports and dashboard on baby's sleep patterns. Quicksight can pull data directly from Amazon Timestream Database.

- Documentation on how to connect Quicksight to Timestream - https://docs.aws.amazon.com/timestream/latest/developerguide/Quicksight.html
- Create Analysis and Dashboard with Quicksight - https://docs.aws.amazon.com/quicksight/latest/user/example-analysis.html

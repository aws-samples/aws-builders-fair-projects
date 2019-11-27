# AI/ML Blackjack Challenge #

AI/ML Blackjack Challenge is an Amazon SageMaker, IoT, and Serverless project that uses edge compute and cameras to detect playing card rank and suit using computer vision, displays the results real-time, and provides player guidance recommendations and probabilities for the game of blackjack.

## Overview ##
This project contains an architecture diagram and FAQ for the project. Source-code and deployment mechanisms will be soon-to-follow after re:Invent 2019.

## Architecture ##
[Architecture Diagram](./Architecture.png)

### Further Information ###
Under construction.

## Deploying the project ##
Under construction


## FAQ ##
__Q: What language(s) were used for this project?__
Python was the only language used.

__Q: What AI/ML techniques are used?__
Amazon SageMaker was used to train and deploy a custom deep learning object detection model (YOLOv3) for detecting 52 classes (king of heart, ace of spade, and so on.). A distance-based algorithm for object tracking (Euclidean distance) tracks previously seen cards to avoid tracking the same card more than once. Finally, reinforcement learning (Q-learning) is used to provide player guidance based on simulated blackjack games.

__Q: What are the base rules of blackjack?__
Reference the [Blackjack (Wikipedia)](https://en.wikipedia.org/wiki/Blackjack) page for a deep dive in blackjack rules. Note: In this project, you cannot split your hand into two hands when your first two cards hve the same value.

__Q: How are photos processed from the edge?__
A Greengrass Lambda Function calls the camera device to take a still of the entire table, and crops player and dealer regions based on prior calibration. Each cropped photo is uploaded to S3 using S3 Transfer Acceleration. An S3 Event triggers a Lambda function which sends the image to an Amazon SageMaker Endpoint for inference of rank and suit.

__Q: How are card predictions and probabilities displayed real-time?__
Throughout the system, messages are published into AWS IoT Core and contain metadata about the predictions, counts, probabilities, and Amazon S3 URIs to update the web frontend. The web frontend uses the AWS Amplify PubSub module and subscribes to the messages in AWS IoT Core using MQTT over WebSocket.

__Q: How are you tracking transitions between rounds?__
The web frontend provides manual buttons when the dealer shuffles the deck to reset counts, and a button to specify a new round has begun. In the future, we are investigating using activity detection and/or pose estimation of the card dealer to detect these activities automatically with machine learning and computer vision. We do not provide a timeline for these feature enhancements.

__Q: What data does this game collect per round?__
At the moment, we are not saving round results. In the future, we will seek options to store final round results such as player hand worth and whether a player "bust" or defeated the dealer. These can further inform machine learning models to provide better player guidance. We do not provide a timeline for these feature enhancements.

## Authors ##
- Laith Al-Saadoon lalsaado@amazon.com
- Chris Burns burnsca@amazon.com

# License #

This library is licensed under the Apache 2.0 License.

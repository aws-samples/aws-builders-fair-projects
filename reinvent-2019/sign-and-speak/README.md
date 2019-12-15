# Sign & Speak - AI-powered Communication

<p align="center"><img src="img/sign-and-speak-logo-small.png" /></p>

## 1. Project Overview

This repository provides the resources and instructions required to create your own version of the Sign & Speak project, which was on display at the Builder's Fair during re:Invent 2019. Sign & Speak uses machine learning to build a communication tool for users of sign language and users of spoken language.

## 2. Project Abstract

Sign & Speak facilitates communication between users of spoken language and users of sign language. By applying AI models trained to transcribe speech and interpret sign language, combined with a camera and a microphone, the tool enables two-way conversation in situations where communication was previously challenging.

## 3. Participant Experience

The Sign & Speak demo allows two participants to complete two scripted conversations, where one participant uses Auslan (Australian sign language) and one participant uses English. The Auslan user stands in front of a webcam, with a white background behind them, and is shown the 'Sign' page of the UI. The English user stands in front of a directional microphone, and is shown the 'Speak' page of the UI. Both UI components allow the participants to record their interaction through start/stop buttons.

The table below shows the two scripted conversations supported in the demo, where *A* is the Auslan user and *E* is the English user.

| Conversation #1 | Conversation #2 |
| ------------- | ------------- |
| A: Hello. | A: Pleased to meet you. |
| E: Hi! How are you? | E: Likewise. How are you? |
| A: Good. How are you? | A: Good. How are you? |
| E: I'm doing well. What are you planning tonight? | E: I'm doing well. What are you up to tonight? |
| A: Going to the pub. | A: Going to a restaurant. |
| E: Oh cool, I'd love to join you. What time are you going? | E: Sound great, I'd love to join you. At what time are you going? |
| A: At 20:00 | A: At 20:00 |
| E: See you there! | E: See you there! |
| A: Goodbye | A: Goodbye |

In addition to the two-way conversation, the demo allows for individual participants to test the Auslan transcription model seperately. When testing the Auslan model, participants can choose from the following list of supported words and phrases:

* Cat
* Friend
* Grandfather
* Grandmother
* Hello
* Goodbye
* Pleased to meet you
* Good! How are you?
* Thank you
* Eight 'o clock
* Restaurant
* Pub

## 4. Architecture

The image below shows the full architecture for the two-way communication demo.

1. A video recording is made of the Auslan user signing a word or phrase. This video is uploaded to an Amazon S3 bucket.
1. The video upload triggers an AWS Lambda function which transforms the video into an image (a grid of frames). 
1. A second AWS Lambda function sends the image to an Amazon SageMaker inference endpoint and waits for the response. It stores the resulting message in Amazon DynamoDB.
1. TODO - continue describing the process

<p align="center"><img src="img/sign-and-speak-architecture.png" /></p>

## 5. User Guide

This section describes how to set up the project on your own AWS account.

### 5.1 Hardware and Equipment

Below is a list of hardware and equipment used during the demo, in combination with the laptop running the demo itself.

* Webcam with USB connector
* Directional microphone with USB connector
* White canvas background + stand
* Height-adjustable tripods for webcam and microphone
* Additional monitor (*optional*)
* Softbox lighting kit (*optional*)

### 5.2 Machine Learning Model

The sign language machine learning model is created using [PyTorch](https://pytorch.org/) in [Amazon SageMaker](https://aws.amazon.com/sagemaker/). This section describes the process of training a new model from scratch.

#### 5.2.1 Creating a data set

First, you need to decide on a set of words and short phrases which the demo should support. We used the list of 12 words and phrases listed in section 3. The model performs better on signs which are visually distinct, but with enough training data, it can distinguish between similar signs such as grandfather and grandmother.

Second, you need to determine the audience for your demo. At re:Invent, we expected to see adult participants, with no prior knowledge of Auslan, and various nationalities, genders, clothing styles, and other visual features. To create a robust model for our expected audience, we asked 64 colleagues from different AWS offices to help us create training data. 

We controlled for factors such as background and lighting by choosing to only support a white background with even lighting. After completing the recording sessions with volunteers, and discarding unsuitable recordings, we were left with 42-72 videos per word or phrase. 

#### 5.2.2. Video preprocessing

Each video recording of a word or phrase is transformed into an image representation for the purpose of performing image classification with the machine learning model. This processing is done through a combination of Bash and Python scripts executed by AWS Lambda. This section explains how the preprocessing generates an image from a video, and describes how to set up your own AWS Lambda function to support the process.

To capture the movement (or time) element of signing a word or phrase, the image representation of a video is created as a 3x3 grid of video frames. [FFmpeg](https://ffmpeg.org/) is used to extract the key (non-blurry) frames from the video, then a Python script selects 9 key frames evenly spread across the length of the video, and FFmpeg is used to arrange these frames into the final grid structure. By selecting the frames according to the length of the video, this method is more robust to different speeds of signing. The image below illustrates the concept (blurred for anonymization only). 

<p align="center"><img src="img/grid_concept.png" /></p>

The stable release of FFmpeg at time of writing (4.2.1) does not contain all the features required to complete the preprocessing. We recommend downloading a [nightly build](https://johnvansickle.com/ffmpeg/) to access the latest features and bug fixes. We used the build from 26/08/2019, but would expect any later build or release to support the required functionality.

TODO - explain how to create a Lambda layer for FFmpeg

#### 5.2.3 Training and deploying a model

First, ensure that all training videos have been preprocessed into 3x3 grid images. Upload these images to an Amazon S3 bucket, organizing the images into folders based on their label (e.g. a folder for 'cat', a folder for 'pub', etc).

Follow [these instructions](https://docs.aws.amazon.com/sagemaker/latest/dg/gs-setup-working-env.html) to set up an Amazon SageMaker instance on the smallest instance type (`ml.t3.medium`). If you want to pre-load the Sign & Speak scripts, simply add the URL to this GitHub repository in the 'Git repositories' section of the setup process. 

If you forgot to pre-load the Sign & Speak project, simply wait for the instance to show status `InService`, then click 'Open Jupyter'. In the new tab which opens, click on the 'New' drop-down menu in the top right corner, and choose 'Terminal' at the bottom of the list. From the terminal, you can `git clone` this repository onto the instance.

Follow the instructions in `scripts/ML Instructions.ipynb` to train and deploy a model with your training data. Once you have an Amazon SageMaker endpoint, follow the instructions below to connect it to the UI.

### 5.3 User Interface

TODO

## 6. FAQ

**Q: There is more than one sign language?**

**A:** Yes! By some estimates there are perhaps [300 sign languages](https://en.wikipedia.org/wiki/List_of_sign_languages). Although ASL (American Sign Language) is probably the most well-known of these languages, the Sign & Speak project was built to support [Auslan](https://en.wikipedia.org/wiki/Auslan) (Australian Sign Language).

**Q: Will this method work for sign languages other than Auslan?**

**A:** We believe our method can be applied to any sign language. All you need is the training data to train a new model for the sign language of your choice. We describe our approach for collecting training data in the User Guide section of this document.

**Q: Can you share your Auslan data set and/or model?**

**A:** To protect the privacy of the volunteers who helped us build our Auslan model, we will not release the data or the model. However, with the code made available in this repository, you can train a new model on your own data.

**Q: What are the limitations of this method?**

**A:** The method only works for individual signs, or short combinations of signs (e.g. 'pleased to meet you' consists of three signs). Due to the limit of 9 frames it will not support full sentences. Additionally, the demo performed well with 12 different labels, but would require significantly more training data to scale to larger numbers of supported labels. Finally, this method does not capture all the nuances of sign language, such as expression and context. 

**Q: What are the future plans for this project?**

**A:** There are many ideas for improving and extending this project; below is a short, but incomplete list.
* Add support for full sign language sentences
* Add support for continuous sign language recognition
* Add a 3D avatar to turn text into sign language

**Q: What is the animal in your logo?**

**A:** It's a [quokka](https://duckduckgo.com/?q=quokka&t=ffnt&atb=v176-1&iax=images&ia=images), a marsupial found only in Australia. We are not professional artists. ;)

## 7. Authors

Sara 'Moose' van de Moosdijk, AWS ([GitHub](https://github.com/moose-in-australia/) | [LinkedIn](https://www.linkedin.com/in/saravandemoosdijk/))

Eshaan Anand, AWS (GitHub | [LinkedIn](https://sg.linkedin.com/in/eshaan-anand-03396456))

## 8. License

This library is licensed under the Apache 2.0 License.
# Project Overview
   Doodle Challenge is a multi-player game enabling you to compete against your fellow players, to see who can create the best doodles of a given subject.  You will need 1 host and at least 2 players to enjoy the game. The host and the players should be in the physical room to play.


# Project Abstract
   Players are invited to sketch various objects (e.g. a bird, a pair of spectacles, a car) against the clock, and each effort is automatically analysed and scored out of 100. The highest total score at the end of six rounds wins. The hub of the project is AWS Rekognition, the AWS service used to identify and classify images, based on a branch of Artificial Intelligence (AI) called Machine Learning (ML). The score given for each doodle is an indicator of Rekognition's confidence in its identification of the doodle. The project was implemented using entirely serverless technologies from AWS.


# Architecture
   <link>

# Environment setup
Doodle Challenge uses a number of libraries to work properly:
* [AWS Amplify] - Unified toolchain to create, integrate, and manage the AWS cloud services.
* [Node.js] - Event-driven JavaScript runtime.
* [React] - A JavaScript library for building user interfaces.
* [Material-ui] - React components
* [AWS SDK] - Command Line Interface to manage your AWS services.

# Installation
Install Nodejs version 8.x or greater and npm version 5.x.
> Verify that you are running at least Node.js version 8.x or greater and npm version 5.x or greater by running node -v and npm -v in a terminal/console window.

Install and configure the amplify cli
```sh
$ npm install -g @aws-amplify/cli
$ amplify configure
```

Go into the Doodle Challenge repo directory
```
$ cd doodlechallenge
```

Install the depedencies
```
$ npm install
```

You will need to deploy services on AWS
```
$ amplify push
```

Run locally
```
$ npm start
```

This should open your browser to http://localhost:3000

# FAQ
Q:  Do I need to be able to draw?
A:  No, you do not need to be able to draw. If your sketch is of low quality, it may still be recognized, and given a low score. All part of the fun.

Q:  How does it do it?
A:  Now that’s a big question! Short answer: through Machine Learning. See the next Q/A.

Q:  What is Machine Learning?
A:  Machine Learning is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention.

Q:  How long did it take to produce Google Challenge?
A:  The developers spent around six weeks conceptualizing and implementing Google Challenge.

Q:  Is Doodle Challenge open-source? Can I get access to all the code? Can I reuse it in my own project?
A:  Yes, yes, and yes. 


# Authors
Howard Tran, Enterprise Solutions Architect, AWS
Jeff Richards, Solutions Architect, AWS

[AWS Amplify]: <https://aws-amplify.github.io/docs/>
[Node.js]: <https://nodejs.org/en/>
[React]: <https://reactjs.org/>
[Material-ui]: <https://material-ui.com/>
[AWS SDK]: <https://aws.amazon.com/cli/>
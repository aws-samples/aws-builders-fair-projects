RhythmCloud 2.0 - Learn to play the drums and learn AWS IoT and Robotics!

This project is broken into its components as follows:

- cloudformation: this sets up IoT, DynamoDB, IAM users, S3 Buckets, and associated keys
- pi: python code that runs locally on the PI
- web: this is the static html files for the web UI
- lambda: lambda functions for UI and Greengrass
- esp32s: code for flashing individual drum controllers
- Build documentation - https://public-ryan.s3.amazonaws.com/RhythmCloudv2BuildInstructions.pdf
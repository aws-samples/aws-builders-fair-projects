# DeepPens Backend

A simple REST endpoint that allows the application to work with the IOT Device.

## Installation

To run locally you can run:

```bash
npm install
npm start
```

As the application communicates with Amazon Greengrass MQTT it requires the IOT_ENDPOINT value to be set before it will run. 

## Files

The application expects your SVG's to be in images folder and onces added there to be referenced from images.json. 
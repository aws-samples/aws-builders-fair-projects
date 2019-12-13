const express = require('express');

const fs = require('fs');
const cors = require('cors');
const AWS = require('aws-sdk');
const images = require('./images.json');
const customImages = require('./customImages.json');

const port = 8080;

const iot = new AWS.IotData({ endpoint: process.env.IOT_ENDPOINT });
const cw = new AWS.CloudWatch({ apiVersion: '2010-08-01' });

const apiMode = process.env.API_MODE || false;
const app = express();
app.use(cors());
app.use(express.json());
const getPath = param => images.find(x => x.word === param);

app.get('/img', (req, res) => {
  console.log('/img called');
  const fileData = getPath(req.query.file);
  if (fileData) {
    fs.readFile(`./src/images/${fileData.pngFilePath}`, (err, png) => {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.write('<html><body><img src="data:image/png;base64,');
      res.write(Buffer.from(png).toString('base64'));
      res.end('"/></body></html>');
    });
  } else {
    res.send('err');
  }
});

app.get('/', async (req, res) => {
  console.log('/ called');
  res.send('DeepPens');
});

const sendImageToAWSIoT = async (svg, boardPort, offset) => {
  console.log('Running sendImageToAWSIoT');
  const params = {
    id: '1',
    action: 'post',
    url: `http://127.0.0.1:${boardPort}/print/`,
    data: {
      svg,
      offset_x: offset.offset_x || 123.00237190055073,
      offset_y: offset.offset_y || 4.078080711935077,
      scale_x: offset.scale_x || 0.44548469836062077,
      scale_y: offset.scale_y || 0.44548469836062077,
      mode: 'once',
    },
  };
  const iotParams = {
    topic: 'http_python/request',
    payload: JSON.stringify(params),
  };

  console.log('--IOT Payload--');
  console.log(iotParams);

  iot.publish(iotParams, () => {
    console.log('Publishing to IoT topic...');
  });
};


app.post('/upload', async (req, res) => {
  console.log('/upload called');
  const offset = {
    offset_x: req.body.offset_x || 123.00237190055073,
    offset_y: req.body.offset_y || 123.00237190055073,
    scale_x: req.body.scale_x || 123.00237190055073,
    scale_y: req.body.scale_y || 123.00237190055073,
  };

  await sendImageToAWSIoT(req.body.textblock, req.body.port, offset);
  res.send('sent');
});


const sendMetric = (metric) => {
  const params = {
    MetricData: [
      {
        MetricName: 'Drawing',
        Dimensions: [
          {
            Name: 'Image',
            Value: metric,
          },
        ],
        Unit: 'None',
        Value: 1,
      },
    ],
    Namespace: 'DRAW/Image',
  };

  cw.putMetricData(params, (err, data) => {
    if (err) {
      console.log('Error', err);
    } else {
      console.log('Success', JSON.stringify(data));
    }
  });
};

app.get('/send-drawing', async (req, res) => {
  console.log('/send-drawing called');

  const imageArray = req.query.imageArray || 'default';
  let randomImg = req.query.imageNo || Math.floor(Math.random() * images.length);

  if (imageArray === 'custom') {
    randomImg = req.query.imageNo || Math.floor(Math.random() * customImages.length);
  }

  const now = Date.now();
  sendMetric(images[randomImg].word[0]);

  let img = images[randomImg];
  let offset = {};
  if (imageArray === 'custom') {
    img = customImages[randomImg];
    if (img.offset) {
      offset = img.offset;
    }
  }

  const filename = img.svgFilePath;
  fs.readFile(`./src/images/${img.svgFilePath}`, (err, svg) => {
    if (err) {
      console.log(err);
    }
    const boardPort = req.query.port || 8080;

    sendImageToAWSIoT(Buffer.from(svg).toString(), boardPort, offset);

    res.send({
      filename, img: img.word, startTime: now, apiMode,
    });
  });
});


app.listen(port, () => console.log(`DeepPens app listening on port ${port}!`));

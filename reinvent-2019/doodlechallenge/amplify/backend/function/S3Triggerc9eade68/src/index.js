/* Amplify Params - DO NOT EDIT
You can access the following resource attributes as environment variables from your Lambda function
var environment = process.env.ENV
var region = process.env.REGION

Amplify Params - DO NOT EDIT */

const AWS = require('aws-sdk');
const path = require('path');
const gql = require('graphql-tag');
const rek = new AWS.Rekognition();
const AWSAppSyncClient = require('aws-appsync').default;
let client;
const {createGameMessage} = require('./mutation.message');
global.fetch = require('node-fetch');
exports.handler = async function (event, context) { //eslint-disable-line
  // Get the object from the event and show its content type
  const bucket = event.Records[0].s3.bucket.name; //eslint-disable-line
  const key = event.Records[0].s3.object.key; //eslint-disable-line
  //console.log(`Bucket: ${bucket}`, `Key: ${key}`);
  const extension = path.extname(key);
  const justFileName = path.basename(key, extension);
  const fileNameWithExtension = path.basename(key);
  let directories = key.split("/");
  directories.pop();

  // let iotData = new AWS.IotData({
  //   endpoint: process.env["AWS_IOT_ENDPOINT"],
  //   region: process.env["REGION"]
  // });

  // console.log(directories);
  // console.log("extension:",extension);
  // console.log("justFileName:",justFileName);
  // console.log("fileNameWithExtension:",fileNameWithExtension);
  if(directories && directories.length > 1 && directories[1] === "doodles" && extension === ".jpg"){
    let doodleName = directories[directories.length-1].toLowerCase();
    let filePartitions = justFileName.split("_");
    let room = filePartitions[0];
    let playerUUID = filePartitions[1];
    
    console.log("Doodle: ", doodleName,", room: ",room,", playerUUID: ",playerUUID);
    const params = {
      Image: {
        S3Object: {
          Bucket: bucket,
          Name: key,
        },
      },
      MaxLabels: 100,
      MinConfidence: 10,
    };
    try {
      const data = await rek.detectLabels(params).promise();
      var score = 0;
      console.log("Labels:", data.Labels);
      data.Labels.find((value)=> {
        if(value.Name.toLowerCase() === doodleName){
          console.log("Found it");
          score = value.Confidence;
          return true;
        }
      });
      const topic = room+"/submitDoodle";
      // The web app needs to key path without the "public" folder
      let myKey = key.split("/");
      myKey.shift();
      let newFile = myKey.join("/");
      let topLabels = data.Labels.slice(data.Labels.length-10);
      topLabels = topLabels.map(label =>{
        return {name:label.Name, confidence:label.Confidence};
      });
      let payload = JSON.stringify({score:score, url:newFile, playerUUID:playerUUID, topLabels:topLabels});
      console.log("Payload: ", payload);
      
      client = new AWSAppSyncClient({
        url: process.env.AWS_APPSYNC_ENDPOINT,
        region: process.env.REGION,
        auth: {
          type: "AWS_IAM",
          credentials: AWS.config.credentials
        },
        disableOffline: true
      });
      const myMessage = await client.mutate({ 
        mutation: gql`${createGameMessage}`,
        variables: { input: {room, action: "submitDoodle", data:payload }},
        fetchPolicy: 'no-cache'
      });
      console.log(myMessage);
      // const iotParams = {
      //   payload: payload,
      //   topic,
      //   qos: 0
      // };
      // await iotData.publish(iotParams).promise();

      context.done(null, 'Successfully processed S3 event'); // SUCCESS with message
      //return data.Labels;
    } catch (err) {
      console.log(err);
      console.log('Cannot recognize image');
      context.done(null, 'Successfully processed S3 event'); // SUCCESS with message
    }
  }else{
    console.log("Not a doodle.");
    context.done(null, 'Successfully processed S3 event'); // SUCCESS with message
  }
};

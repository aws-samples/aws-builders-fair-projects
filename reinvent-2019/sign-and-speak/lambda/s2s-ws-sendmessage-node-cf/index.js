"use strict";

const AWS = require("aws-sdk");
const wsclientstable = process.env.wsclientstable;
const wssurl = process.env.wssurl;


require("aws-sdk/clients/apigatewaymanagementapi");

exports.handler = async (event) => {
    var record = event["Records"];    
    var eventName = record[0]["eventName"];    
    if(eventName == "INSERT")
    {        
    var dynamodbItem = record[0]["dynamodb"];
    var newItem = dynamodbItem["NewImage"];
    var sign = newItem["msg"]["S"];
    var confidence = newItem["confidence"]["S"];
    var isSign = newItem["isSign"]["BOOL"];   
    var finalMesage = isSign + "|" +   confidence + "|" + sign ;
    var dynamoClient = new AWS.DynamoDB.DocumentClient();
    let connectionData;
    try {
        connectionData = await dynamoClient.scan({ TableName: wsclientstable,
            ProjectionExpression: 'connectionId' }).promise();
        } 
    catch (e) {
        console.log(e.stack);
        return { statusCode: 500, body: e.stack };
        }
    const apigwManagementApi = new AWS.ApiGatewayManagementApi({
        apiVersion: '2018-11-29',
        endpoint: wssurl
    });
    const postCalls = connectionData.Items.map(async ({ connectionId }) => {
    try {
          await apigwManagementApi.postToConnection({ ConnectionId: connectionId, Data: finalMesage }).promise();
        } catch (e) {
          if (e.statusCode === 410) {
            console.log('Found stale connection, deleting ${connectionId}');
            await dynamoClient.delete({ TableName: wsclientstable, Key: { connectionId } }).promise();
          } else {
            throw e;
          }
        }
      });
      try {
        await Promise.all(postCalls);
      } catch (e) {
        return { statusCode: 500, body: e.stack };
      }
    }
    const response = {
        statusCode: 200,
        body: JSON.stringify('DDB Stream Message processed'),
    };
    return response;
};
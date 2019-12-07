require('dotenv').config();
const AlexaResponse = require("./response.js");
const AWS = require('aws-sdk');

const iotdata = new AWS.IotData({endpoint: process.env.IOT_ENDPOINT});
const thingName = process.env.IOT_THING_NAME;
const alexaDeviceName = process.env.ALEXA_DEVICE_NAME;
const topic = `dt/smart-garage/${thingName}/control`;

exports.handler = async function (event, context) {
  // console.log(JSON.stringify(event));
  const namespace = event.directive.header.namespace.toLowerCase();
  const directiveName = event.directive.header.name.toLowerCase();
  console.log(`namespace is ${namespace}  -  directive name: ${directiveName}`);

  switch(namespace) {
    case 'alexa.authorization': return handleAuth();
    case 'alexa.discovery': return handleDiscovery();
    case 'alexa.lockcontroller': return handleLockController(event);
    case 'alexa':
      if (directiveName === 'reportstate') return handleReportState(event);
    default: console.log('Unknown namespamce: ', namespace);
  }
};

function handleAuth() {
  const ar = new AlexaResponse({ namespace: "Alexa.Authorization", name: "AcceptGrant.Response"});

  return ar.get();
}

function handleDiscovery() {
  const adr = new AlexaResponse({namespace: "Alexa.Discovery", name: "Discover.Response"});
  const capability_alexa = adr.createPayloadEndpointCapability();

  const lock = adr.createPayloadEndpointCapability({
    interface: "Alexa.LockController",
    supported: [{name: "lockState"}],
    proactivelyReported: true,
    retrievable: true
  });

  const health = adr.createPayloadEndpointCapability({
    interface: "Alexa.EndpointHealth",
    supported: [{name: "connectivity"}],
    proactivelyReported: true,
    retrievable: true
  });

  adr.addPayloadEndpoint({
    friendlyName: alexaDeviceName,
    endpointId: thingName,
    capabilities: [capability_alexa, lock, health]
  });

  return adr.get();
}

async function handleLockController(event) {
  const desiredState = event.directive.header.name.toLowerCase(); // lock | unlock
  const endpointId = event.directive.endpoint.endpointId;
  const token = event.directive.endpoint.scope.token;
  const correlationToken = event.directive.header.correlationToken;

  const payload = JSON.stringify({
    device_name: thingName,
    desired_state: desiredState,
    timestamp: Math.floor(new Date() / 1000)
  });

  const params = { topic, payload, qos: 1 };
  const pubRes = await iotdata.publish(params).promise();
  // console.log('publish res ', pubRes);

  const ar = new AlexaResponse({ correlationToken, token, endpointId });
  const alexaDesiredState = {
    lock: 'locked',
    unlock: 'unlocked'
  };
  // TODO: async slow lock response:
  ar.addContextProperty({namespace: "Alexa.LockController", name: "lockState", value: alexaDesiredState[desiredState]});

  return ar.get();
}

async function handleReportState(event) {
  const endpointId = event.directive.endpoint.endpointId;
  const token = event.directive.endpoint.scope.token;
  const correlationToken = event.directive.header.correlationToken;
  const deviceState = await getDeviceShadowState(thingName);
  console.log('deviceState ', deviceState);
  const ar = new AlexaResponse({ correlationToken, token, endpointId, name: "StateReport" });
  ar.addContextProperty({namespace: "Alexa.LockController", name: "lockState", value: deviceState.toUpperCase()});

  console.log('handle report state ', ar.get());
  return ar.get();
}

async function getDeviceShadowState(thingName) {
  let shadowState = await iotdata.getThingShadow({thingName}).promise();
  shadowState = JSON.parse(shadowState.payload);

  if (shadowState.state.reported && shadowState.state.reported.is_open)
    return 'unlocked';

  return 'locked';
}

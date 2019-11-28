import sys
import boto3
from botocore.exceptions import ClientError
from botocore.vendored import requests
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

policyDocument = {
  'Version': '2012-10-17',
  'Statement': [
      {
          'Effect': 'Allow',
          'Action': 'iot:*',
          'Resource': '*'
      },
      {
          'Effect': 'Allow',
          'Action': 'greengrass:*',
          'Resource': '*'
      }
  ]
}
def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))


def handler(event, context):
  responseData = {}
  try:
      logger.info('Received event: {}'.format(json.dumps(event)))
#      result = cfnresponse.FAILED
      client = boto3.client('iot')
      s3client = boto3.client('s3')
      BUCKET_NAME = event['ResourceProperties']['s3bucketname']
      print("BUCKET_NAME=",BUCKET_NAME)
      thingName=event['ResourceProperties']['ThingName']
      if event['RequestType'] == 'Create':
          thing = client.create_thing(
              thingName=thingName
          )
          response = client.create_keys_and_certificate(
              setAsActive=True
          )
          certId = response['certificateId']
          certArn = response['certificateArn']
          certPem = response['certificatePem']
          privateKey = response['keyPair']['PrivateKey']
          s3_response = s3client.put_object(Bucket=BUCKET_NAME, Key="rhythmcloud-cert.pem.crt", Body=certPem)
          s3_response = s3client.put_object(Bucket=BUCKET_NAME, Key="rhythmcloud-prvt.pem.key", Body=privateKey)
          client.create_policy(
              policyName='{}-full-access'.format(thingName),
              policyDocument=json.dumps(policyDocument)
          )
          response = client.attach_policy(
              policyName='{}-full-access'.format(thingName),
              target=certArn
          )
          response = client.attach_thing_principal(
              thingName=thingName,
              principal=certArn,
          )
          logger.info('Created thing: %s, cert: %s and policy: %s' %
              (thingName, certId, '{}-full-access'.format(thingName)))
          result = "SUCCESS"
          responseData['certificateId'] = certId
          responseData['certificatePem'] = certPem
          responseData['privateKey'] = privateKey
          responseData['certArn'] = certArn
          responseData['iotEndpoint'] = client.describe_endpoint(endpointType='iot:Data-ATS')['endpointAddress']
      elif event['RequestType'] == 'Update':
          logger.info('Updating thing: %s' % thingName)
          result = "SUCCESS"
      elif event['RequestType'] == 'Delete':
          logger.info('Deleting thing: %s and cert/policy' % thingName)
          response = client.list_thing_principals(
              thingName=thingName
          )
          for i in response['principals']:
              response = client.detach_thing_principal(
                  thingName=thingName,
                  principal=i
              )
              response = client.detach_policy(
                  policyName='{}-full-access'.format(thingName),
                  target=i
              )
              response = client.update_certificate(
                  certificateId=i.split('/')[-1],
                  newStatus='INACTIVE'
              )
              response = client.delete_certificate(
                  certificateId=i.split('/')[-1],
                  forceDelete=True
              )
              response = client.delete_policy(
                  policyName='{}-full-access'.format(thingName),
              )
              response = client.delete_thing(
                  thingName=thingName
              )
          result = "SUCCESS"
  except ClientError as e:
      logger.error('Error: {}'.format(e))
      result = "FAILED"
  logger.info('Returning response of: {}, with result of: {}'.format(result, responseData))
  sys.stdout.flush()
  send(event, context, result, responseData)

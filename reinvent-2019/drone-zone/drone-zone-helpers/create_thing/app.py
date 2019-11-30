from __future__ import print_function
from crhelper import CfnResource
import logging
import boto3
import os
import json

logger = logging.getLogger(__name__)
# Initialise the helper, all inputs are optional, this example shows the defaults
helper = CfnResource(json_logging=False, log_level='DEBUG',
                     boto_level='CRITICAL')

try:
    ## Init code goes here
    GG_CONFIGS_BUCKET = os.environ['GG_CONFIGS_BUCKET']

    configFile = {
      "coreThing": {
        "caPath": "root.ca.pem",
        "certPath": "core.cert.pem",
        "keyPath": "core.private.key",
        "thingArn": "",
        "iotHost": "",
        "ggHost": "greengrass-ats.iot.{}.amazonaws.com".format(os.environ['AWS_REGION']),
        "keepAlive": 600
      },
      "runtime": {
        "cgroup": {
          "useSystemd": "yes"
        }
      },
      "managedRespawn": False,
      "crypto": {
        "principals": {
          "SecretsManager": {
            "privateKeyPath": "file:///greengrass/certs/core.private.key"
          },
          "IoTCertificate": {
            "privateKeyPath": "file:///greengrass/certs/core.private.key",
            "certificatePath": "file:///greengrass/certs/core.cert.pem"
          }
        },
        "caPath": "file:///greengrass/certs/root.ca.pem"
      }
    }

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
    pass

except Exception as e:
    helper.init_failure(e)


@helper.create
def create(event, context):
    logger.info("Got Create")
    # Optionally return an ID that will be used for the resource PhysicalResourceId,
    # if None is returned an ID will be generated. If a poll_create function is defined
    # return value is placed into the poll event as event['CrHelperData']['PhysicalResourceId']
    #
    # To add response data update the helper.Data dict
    # If poll is enabled data is placed into poll event as event['CrHelperData']
    client = boto3.client('iot')
    s3_client = boto3.client('s3')
    thingName=event['ResourceProperties']['ThingName']
    
    thing = client.create_thing(
        thingName=thingName
    )
    response = client.create_keys_and_certificate(
        setAsActive=True
    )
    json_configs_response = response
    certId = response['certificateId']
    certArn = response['certificateArn']
    certPem = response['certificatePem']
    privateKey = response['keyPair']['PrivateKey']
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

    iotEndpoint = client.describe_endpoint(endpointType='iot:Data-ATS')['endpointAddress']

    configFile['coreThing']['thingArn'] = thing['thingArn']
    configFile['coreThing']['thingName'] = thingName
    configFile['coreThing']['iotHost'] = iotEndpoint

    json_configs_response['configFile'] = configFile

    response = s3_client.put_object(
        Bucket=GG_CONFIGS_BUCKET,
        Key='bootstrap.json',
        Body=json.dumps(json_configs_response,indent=4)
    )

    helper.Data.update({"certificateId": certId})
    helper.Data.update({"certificatePem": certPem})
    helper.Data.update({"privateKey": privateKey})
    helper.Data.update({"iotEndpoint": iotEndpoint})

    # # To return an error to cloudformation you raise an exception:
    # if not helper.Data.get("test"):
    #     raise ValueError(
    #         "this error will show in the cloudformation events log and console.")

    return thingName


@helper.update
def update(event, context):
    logger.info("Got Update")
    # If the update resulted in a new resource being created, return an id for the new resource.
    # CloudFormation will send a delete event with the old id when stack update completes


@helper.delete
def delete(event, context):
    logger.info("Got Delete")
    # Delete never returns anything. Should not fail if the underlying resources are already deleted.
    # Desired state.
    client = boto3.client('iot')
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(GG_CONFIGS_BUCKET)
    bucket.objects.all().delete()

    thingName=event['ResourceProperties']['ThingName']
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


def handler(event, context):
    logger.info('Received event: {}'.format(json.dumps(event)))
    helper(event, context)

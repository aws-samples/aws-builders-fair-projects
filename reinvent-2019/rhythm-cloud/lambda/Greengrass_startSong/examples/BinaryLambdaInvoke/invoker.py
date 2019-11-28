#
# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# This example demonstrates invoking a lambda with 'binary' encoding type. In
# order to run this example, remember to mark your 'invokee' lambda as a binary
# lambda. You can configure this on the lambda configuration page in the
# console. After the lambdas get deployed to your Greengrass Core, you should
# be able to see 'Invoked successfully' returned by 'invokee' lambda. A lambda
# function can support non-json payload, which is a new feature introduced in
# GGC version 1.5.
#
import sys
import base64
import logging
import json
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client('lambda')


def handler(event, context):
    client_context = json.dumps({
        'custom': 'custom text'
    })

    try:
        response = client.invoke(
            ClientContext=base64.b64encode(bytes(client_context)),
            FunctionName='arn:aws:lambda:<region>:<accountId>:function:<targetFunctionName>:<targetFunctionQualifier>',
            InvocationType='RequestResponse',
            Payload='Non-JSON Data',
            Qualifier='1'
        )

        logger.info(response['Payload'].read())
    except Exception as e:
        logger.error(e)

# Copyright 2014. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from boto.exception         import JSONResponseError
from boto.dynamodb2.fields  import KeysOnlyIndex
from boto.dynamodb2.fields  import GlobalAllIndex
from boto.dynamodb2.fields  import HashKey
from boto.dynamodb2.fields  import RangeKey
from boto.dynamodb2.layer1  import DynamoDBConnection
from boto.dynamodb2.table   import Table

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import json

def getDynamoDBConnection(config=None, endpoint=None, port=None, local=False, use_instance_metadata=False):
    if local:
        db = DynamoDBConnection(
            host=endpoint,
            port=port,
            aws_secret_access_key='ticTacToeSampleApp',
            aws_access_key_id='ticTacToeSampleApp',
            is_secure=False)
    else:
        params = {
            'is_secure': True
            }

        # Read from config file, if provided
        if config is not None:
            if config.has_option('dynamodb', 'region'):
                params['region'] = config.get('dynamodb', 'region')
            if config.has_option('dynamodb', 'endpoint'):
                params['host'] = config.get('dynamodb', 'endpoint')

            if config.has_option('dynamodb', 'aws_access_key_id'):
                params['aws_access_key_id'] = config.get('dynamodb', 'aws_access_key_id')
                params['aws_secret_access_key'] = config.get('dynamodb', 'aws_secret_access_key')

        # Use the endpoint specified on the command-line to trump the config file
        if endpoint is not None:
            params['host'] = endpoint
            if 'region' in params:
                del params['region']

        # Only auto-detect the DynamoDB endpoint if the endpoint was not specified through other config
        if 'host' not in params and use_instance_metadata:
            response = urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document').read()
            doc = json.loads(response);
            params['host'] = 'dynamodb.%s.amazonaws.com' % (doc['region'])
            if 'region' in params:
                del params['region']

        db = DynamoDBConnection(**params)
    return db

def createGamesTable(db):

    try:
        hostStatusDate = GlobalAllIndex("HostId-StatusDate-index",
                                        parts=[HashKey("HostId"), RangeKey("StatusDate")],
                                        throughput={
                                            'read': 1,
                                            'write': 1
                                        })
        opponentStatusDate  = GlobalAllIndex("OpponentId-StatusDate-index",
                                        parts=[HashKey("OpponentId"), RangeKey("StatusDate")],
                                        throughput={
                                            'read': 1,
                                            'write': 1
                                        })

        #global secondary indexes
        GSI = [hostStatusDate, opponentStatusDate]

        gamesTable = Table.create("Games",
                    schema=[HashKey("GameId")],
                    throughput={
                        'read': 1,
                        'write': 1
                    },
                    global_indexes=GSI,
                    connection=db)

    except JSONResponseError as jre:
        try:
            gamesTable = Table("Games", connection=db)
        except Exception as e:
            print("Games Table doesn't exist.")
    finally:
        return gamesTable

#parse command line args for credentials and such
#for now just assume local is when args are empty

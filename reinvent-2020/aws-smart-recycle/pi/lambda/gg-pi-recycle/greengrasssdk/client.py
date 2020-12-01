#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#


def client(client_type, *args, **kwargs):
    if client_type == 'lambda':
        from .Lambda import Client
    elif client_type == 'iot-data':
        from .IoTDataPlane import Client
    elif client_type == 'secretsmanager':
        from .SecretsManager import Client
    elif client_type == 'streammanager':
        from .stream_manager import StreamManagerClient as Client
    else:
        raise Exception('Client type {} is not recognized.'.format(repr(client_type)))

    return Client(*args, **kwargs)

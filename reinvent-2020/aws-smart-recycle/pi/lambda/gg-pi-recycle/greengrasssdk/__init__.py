#
# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

from .client import client
# .Lambda imports greengrass_common, which only applies within Greengrass Core.
# Try-except as below to make sure the SDK is able to be imported outside of Greengrass Core
try:
    from .Lambda import StreamingBody
except:
    pass

__version__ = '1.6.0'
INTERFACE_VERSION = '1.5'

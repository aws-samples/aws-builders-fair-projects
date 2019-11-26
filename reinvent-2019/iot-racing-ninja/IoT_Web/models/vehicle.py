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
from boto.dynamodb2.items import Item
from datetime             import datetime

class Vehicle:
    """
    This Game class acts as a wrapper on top of an item in the BF_Vehicle_State table.
    Each of the fields in the table is of a String type.
    GameId is the primary key.
    HostId-StatusDate, Opponent-StatusDate are Global Secondary Indexes that are Hash-Range Keys.
    The other attributes are used to maintain game state.
    """
    def __init__(self, item):
        self.item = item
        self.vehicleId   = item["vehicleId"]
        self.facing      = item["facing"]
        self.x           = item["x"]
        self.y           = item["y"]

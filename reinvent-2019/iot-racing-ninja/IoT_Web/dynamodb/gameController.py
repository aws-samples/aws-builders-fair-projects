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
import json
import requests

class GameController:
    """
    This GameController hits the API Gateway to get game status json and stashed that json to be used to draw the board
    """

    def __init__(self):
        self.gameIdStr = ""
        self.round = ""
        self.it = ""
        self.playerState = ["","","",""]
        self.score = ["","","",""]
        self.vehicles = [0, 1, 2, 3]
        self.vehicleIdStr = ['white', 'red', 'blue', 'black']


    def getRound(self):
        return int(float(self.round))

    def getIt(self):
        return self.it

    def getGameId(self):
        return self.gameIdStr

    def getScore(self, vehicleIdx):
        return int(float(self.score[vehicleIdx]))

    def getGameStatus(self):
        """
        Calls API Gateway to get JSON representation of game status.  All vehicles' x, y, facing, and score, and it
        status, as well as the game ID and found
        """

        api_url_base = ' https://game-api.iotracer.ninja/game/status'
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.get(api_url_base, headers=headers)

            if response.status_code == 200:
                response_str = json.loads(response.content.decode('utf-8'))
                if response_str is not None:
                    self.gameIdStr = response_str['gameid']
                    self.round = response_str['round']
                    for vehicleIdx in self.vehicles:

                        player_x = str(int(response_str['Scores'][vehicleIdx][self.vehicleIdStr[vehicleIdx]]['x']))
                        player_y = str(int(response_str['Scores'][vehicleIdx][self.vehicleIdStr[vehicleIdx]]['y']))
                        player_facing = response_str['Scores'][vehicleIdx][self.vehicleIdStr[vehicleIdx]]['facing']
                        player_it = str(response_str['Scores'][vehicleIdx][self.vehicleIdStr[vehicleIdx]]['it'])
                        player_score = str(response_str['Scores'][vehicleIdx][self.vehicleIdStr[vehicleIdx]]['score'])
                        self.score[vehicleIdx] = player_score
                        player_data = {}
                        player_data['x'] = player_x
                        player_data['y'] = player_y
                        player_data['facing'] = player_facing
                        player_data['it'] = player_it
                        player_data['score'] = player_score
                        self.playerState[vehicleIdx] = json.dumps(player_data)
                else:
                    print('[!] Request Failed')

            else:
                return None

        except JSONResponseError as jre:
            return None
        except IOError as ioe:
            """
            eat any io errors
            """
            return None

        return None

    def getVehicle(self, color):
        """
        Gets the representation of the named (color) vehicle that was retrieved from the above API call
        """
        idx = 0

        for colors in self.vehicleIdStr:
            if (color == self.vehicleIdStr[idx]):
                return self.playerState[idx]
            else:
                idx = idx +1


    def getImgNameIt(self, facing):
        """
        Gets the name of the vehicle icon if it is 'it'
        """
        return {
            'E': '_east_it.png',
            'W': '_west_it.png',
            'N': '_north_it.png',
            'S': '_south_it.png'
        } [facing]

    def getImgNameNoIt(self, facing):
        """
        Gets the name of the vehicle icon if it is not 'it'
        """

        return {
            'E': '_east.png',
            'W': '_west.png',
            'N': '_north.png',
            'S': '_south.png'
        }[facing]

    def getBoardState(self, blackVehicleState, blueVehicleState, whiteVehicleState, redVehicleState):
        """
        Puts the state of the board into a list, putting a blank space for
        spaces that are not occupied.
        """

        strVals = ["One", "Two", "Three", "Four", "Five", "Six"]

        # got my x's and y's mixed up on horizontal & vertical - sorry gang
        blackVehicleState_x = blackVehicleState['y']
        blackVehicleState_y = blackVehicleState['x']
        blackVehicleDir = blackVehicleState['facing']
        blackVehicleIt = blackVehicleState['it']
        blueVehicleState_x = blueVehicleState['y']
        blueVehicleState_y = blueVehicleState['x']
        blueVehicleDir = blueVehicleState['facing']
        blueVehicleIt = blueVehicleState['it']
        whiteVehicleState_x = whiteVehicleState['y']
        whiteVehicleState_y = whiteVehicleState['x']
        whiteVehicleDir = whiteVehicleState['facing']
        whiteVehicleIt = whiteVehicleState['it']
        redVehicleState_x = redVehicleState['y']
        redVehicleState_y = redVehicleState['x']
        redVehicleDir = redVehicleState['facing']
        redVehicleIt = redVehicleState['it']

        blackVehicleSquareName = strVals[int(blackVehicleState_x)]+strVals[int(blackVehicleState_y)]
        blueVehicleSquareName = strVals[int(blueVehicleState_x)] + strVals[int(blueVehicleState_y)]
        whiteVehicleSquareName = strVals[int(whiteVehicleState_x)] + strVals[int(whiteVehicleState_y)]
        redVehicleSquareName = strVals[int(redVehicleState_x)] + strVals[int(redVehicleState_y)]

        squares = ["OneOne", "OneTwo", "OneThree", "OneFour", "OneFive", "OneSix",  \
                    "TwoOne", "TwoTwo", "TwoThree", "TwoFour", "TwoFive", "TwoSix",  \
                    "ThreeOne", "ThreeTwo", "ThreeThree", "ThreeFour", "ThreeFive", "ThreeSix", \
                    "FourOne", "FourTwo", "FourThree", "FourFour", "FourFive", "FourSix", \
                    "FiveOne", "FiveTwo", "FiveThree", "FiveFour", "FiveFive", "FiveSix", \
                    "SixOne", "SixTwo", "SixThree", "SixFour", "SixFive", "SixSix",]
        state = []

        for square in squares:
            if square == blackVehicleSquareName:
                if blackVehicleIt == 'True':
                    imgName = self.getImgNameIt(blackVehicleDir)
                    self.it = "Black"
                else:
                    imgName = self.getImgNameNoIt(blackVehicleDir)
                state.append('<img class="imgsq" src="/static/images/black'+imgName+'">')
            else:
                if square == blueVehicleSquareName:
                    if blueVehicleIt == 'True':
                        imgName = self.getImgNameIt(blueVehicleDir)
                        self.it = "Blue"
                    else:
                        imgName = self.getImgNameNoIt(blueVehicleDir)
                    state.append('<img class="imgsq" src="/static/images/blue'+imgName+'"/>')
                else:
                    if square == whiteVehicleSquareName:
                        if whiteVehicleIt == 'True':
                            self.it = "White"
                            imgName = self.getImgNameIt(whiteVehicleDir)
                        else:
                            imgName = self.getImgNameNoIt(whiteVehicleDir)
                        state.append('<img class="imgsq" src="/static/images/white'+imgName+'"/>')
                    else:
                        if square == redVehicleSquareName:
                            if redVehicleIt == 'True':
                                self.it = "Red"
                                imgName = self.getImgNameIt(redVehicleDir)
                            else:
                                imgName = self.getImgNameNoIt(redVehicleDir)
                            state.append('<img class="imgsq" src="/static/images/red'+imgName+'"/>')
                        else:
                            state.append(" ")

        return state

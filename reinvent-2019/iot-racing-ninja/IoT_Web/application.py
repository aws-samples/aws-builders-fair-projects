#!flask/bin/python
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
from dynamodb.gameController        import GameController
from uuid                           import uuid4
from flask                          import Flask, render_template, request, session, flash, redirect, jsonify, json
from configparser                   import ConfigParser
import os, time, sys, argparse

application = Flask(__name__)
application.debug = True
application.secret_key = str(uuid4())

"""
   Configure the application according to the command line args and config files
"""

cm = None

parser = argparse.ArgumentParser(description='Run the IoT Racer sample app', prog='application.py')
parser.add_argument('--config', help='Path to the config file containing application settings. Cannot be used if the CONFIG_FILE environment variable is set instead')
parser.add_argument('--serverPort', help='The port for this Flask web server to listen on.  Defaults to 5000 or whatever is in the config file. If the SERVER_PORT ' \
                    'environment variable is set, uses that instead.', type=int)
args = parser.parse_args()

configFile = args.config
config = None
if 'CONFIG_FILE' in os.environ:
    if configFile is not None:
        raise Exception('Cannot specify --config when setting the CONFIG_FILE environment variable')
    configFile = os.environ['CONFIG_FILE']
if configFile is not None:
    config = ConfigParser()
    config.read(configFile)

# Don't need the DynamoDB connection for our IoT Racer game; only hitting an API Gateway endpoint, not using any sort of local mode
# cm = ConnectionManager(mode=args.mode, config=config, endpoint=args.endpoint, port=args.port, use_instance_metadata=use_instance_metadata)
controller = GameController()

serverPort = args.serverPort
if config is not None:
    if config.has_option('flask', 'secret_key'):
        application.secret_key = config.get('flask', 'secret_key')
    if serverPort is None:
        if config.has_option('flask', 'serverPort'):
            serverPort = config.get('flask', 'serverPort')

# Default to environment variables for server port - easier for elastic beanstalk configuration
if 'SERVER_PORT' in os.environ:
    serverPort = int(os.environ['SERVER_PORT'])

if serverPort is None:
    serverPort = 5000

"""
   Define the urls and actions the app responds to
"""

@application.route('/', methods=["GET"])
def root():
    session["username"] = "BuildersFair2019"
    return redirect('/game')

@application.route('/index', methods=["GET", "POST"])
def index():
    """
    Method associated to both routes '/' and '/index' and accepts
    post requests for when a user logs in.  Updates the user of
    the session to the person who logged in.  Also populates 3 tables for game invites, games in progress, and
    games finished by the logged in user (if there is one).
    """

    if session == {} or session.get("username", None) == None:
        session["username"] = "BuildersFair2019"

    return redirect('/game')

@application.route('/game')
def game():
    """
    Method associated the with the '/game=<gameId>' route where the
    gameId is in the URL.

    Validates that the gameId actually exists.

    Checks to see if the game has been finished.

    Gets the state of the board and updates the visual representation
    accordingly.

    Displays a bit of extra information like turn, status, and gameId.
    """

    controller.getGameStatus()
    blackVehicleState = controller.getVehicle('black')
    blueVehicleState = controller.getVehicle('blue')
    redVehicleState = controller.getVehicle('red')
    whiteVehicleState = controller.getVehicle('white')
    gameId = controller.getGameId()
    round = controller.getRound()
    blackScore = controller.getScore(3)
    blueScore = controller.getScore(2)
    redScore = controller.getScore(1)
    whiteScore = controller.getScore(0)

    try:
        boardState = controller.getBoardState(json.loads(blackVehicleState), json.loads(blueVehicleState),
                                             json.loads(whiteVehicleState), json.loads(redVehicleState))
        # non-obvious dependency - it is found during the getBoardState call
        it = controller.getIt()
    except Exception as e:
        print(e)

    return render_template("board.html",
                            username=session.get("username"),
                            gameId=gameId,
                            round=round,
                            it=it,
                            blackScore=blackScore,
                            blueScore=blueScore,
                            redScore=redScore,
                            whiteScore=whiteScore,
                            OneOne=boardState[0],
                            OneTwo=boardState[1],
                            OneThree=boardState[2],
                            OneFour=boardState[3],
                            OneFive=boardState[4],
                            OneSix=boardState[5],
                            TwoOne=boardState[6],
                            TwoTwo=boardState[7],
                            TwoThree=boardState[8],
                            TwoFour=boardState[9],
                            TwoFive=boardState[10],
                            TwoSix=boardState[11],
                            ThreeOne=boardState[12],
                            ThreeTwo=boardState[13],
                            ThreeThree=boardState[14],
                            ThreeFour=boardState[15],
                            ThreeFive=boardState[16],
                            ThreeSix=boardState[17],
                            FourOne=boardState[18],
                            FourTwo=boardState[19],
                            FourThree=boardState[20],
                            FourFour=boardState[21],
                            FourFive=boardState[22],
                            FourSix=boardState[23],
                            FiveOne=boardState[24],
                            FiveTwo=boardState[25],
                            FiveThree=boardState[26],
                            FiveFour=boardState[27],
                            FiveFive=boardState[28],
                            FiveSix=boardState[29],
                            SixOne=boardState[30],
                            SixTwo=boardState[31],
                            SixThree=boardState[32],
                            SixFour=boardState[33],
                            SixFive=boardState[34],
                            SixSix=boardState[35]
                           )

@application.route('/gameData')
def gameData():
    """
    Method associated the with the '/gameData=' route to get a fresh version of the game data for board.html

    Returns a JSON representation of the game
    """
    controller.getGameStatus()
    blackVehicleState = controller.getVehicle('black')
    blueVehicleState = controller.getVehicle('blue')
    redVehicleState = controller.getVehicle('red')
    whiteVehicleState = controller.getVehicle('white')
    gameId = controller.getGameId()
    round = controller.getRound()
    blackScore = controller.getScore(3)
    blueScore = controller.getScore(2)
    redScore = controller.getScore(1)
    whiteScore = controller.getScore(0)

    try:
        boardState = controller.getBoardState(json.loads(blackVehicleState), json.loads(blueVehicleState),
                                             json.loads(whiteVehicleState), json.loads(redVehicleState))
        # non-obvious dependency - it is found during the getBoardState call
        it = controller.getIt()
    except Exception as e:
        print(e)

    return jsonify(username=session.get("username"),
                                gameId=gameId,
                                round=round,
                                it=it,
                                blackScore=blackScore,
                                blueScore=blueScore,
                                redScore=redScore,
                                whiteScore=whiteScore,
                                OneOne=boardState[0],
                               OneTwo=boardState[1],
                               OneThree=boardState[2],
                               OneFour=boardState[3],
                               OneFive=boardState[4],
                               OneSix=boardState[5],
                               TwoOne=boardState[6],
                               TwoTwo=boardState[7],
                               TwoThree=boardState[8],
                               TwoFour=boardState[9],
                               TwoFive=boardState[10],
                               TwoSix=boardState[11],
                               ThreeOne=boardState[12],
                               ThreeTwo=boardState[13],
                               ThreeThree=boardState[14],
                               ThreeFour=boardState[15],
                               ThreeFive=boardState[16],
                               ThreeSix=boardState[17],
                               FourOne=boardState[18],
                               FourTwo=boardState[19],
                               FourThree=boardState[20],
                               FourFour=boardState[21],
                               FourFive=boardState[22],
                               FourSix=boardState[23],
                               FiveOne=boardState[24],
                               FiveTwo=boardState[25],
                               FiveThree=boardState[26],
                               FiveFour=boardState[27],
                               FiveFive=boardState[28],
                               FiveSix=boardState[29],
                               SixOne=boardState[30],
                               SixTwo=boardState[31],
                               SixThree=boardState[32],
                               SixFour=boardState[33],
                               SixFive=boardState[34],
                               SixSix=boardState[35]
                            )

if __name__ == "__main__":
     application.run(debug = os.getenv('FLASK_DEBUG',False), port=serverPort, host='0.0.0.0')

import app
import base64
import boto3
from boto3.dynamodb.conditions import Key, Attr
import decimal
import json
import os
import requests
import time
import unittest

class SimulateGame(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.region = os.getenv('region','us-east-1')
        self.iot_table = os.getenv('iot_table','iot_game')
        self.vehicles = int(os.getenv('vehicles','4'))
        self.vehicle_list = os.getenv('vehicle_list',['red', 'blue', 'white', 'black'])
        self.dynamodb_table = boto3.resource('dynamodb', 
            region_name=self.region).Table(self.iot_table)
        self.vehicle_data = [{'itemid':'red', 'x':'0', 'y':'0', 'facing':'S', 
            'score':0, 'type':'vehicle', 'vehicleid':1, 'it':True },
            {'itemid':'blue', 'x':'0', 'y':'5', 'facing':'N', 
            'score':0, 'type':'vehicle', 'vehicleid':2, 'it': False}, 
            {'itemid':'white', 'x':'5', 'y':'0', 'facing':'S', 
            'score':0, 'type':'vehicle', 'vehicleid':3, 'it': False},
            {'itemid':'black', 'x':'5', 'y':'5', 'facing':'N',
            'score':0, 'type':'vehicle', 'vehicleid':4, 'it': False}]
        self.rounds = []
        self.rounds.append({'round':'1', 'moves':[{'car':'red', 'move':'forward'}, 
            {'car':'black', 'move':'forward'},{'car':'blue', 'move':'forward'}, 
            {'car':'white', 'move':'forward'}]})
        self.rounds.append({'round':'2', 'moves':[{'car':'red', 'move':'left'}, 
            {'car':'black', 'move':'forward'},{'car':'blue', 'move':'forward'}, 
            {'car':'white', 'move':'forward'}]})
        self.rounds.append({'round':'3', 'moves':[{'car':'red', 'move':'right'}, 
            {'car':'black', 'move':'left'},{'car':'blue', 'move':'right'}, 
            {'car':'white', 'move':'right'}]})
        self.rounds.append({'round':'4', 'moves':[{'car':'red', 'move':'right'}, 
            {'car':'black', 'move':'forward'},{'car':'blue', 'move':'forward'}, 
            {'car':'white', 'move':'right'}]})
        self.rounds.append({'round':'5', 'moves':[{'car':'red', 'move':'left'}, 
            {'car':'black', 'move':'left'},{'car':'blue', 'move':'left'}, 
            {'car':'white', 'move':'forward'}]})
        self.rounds.append({'round':'6', 'moves':[{'car':'red', 'move':'left'}, 
            {'car':'black', 'move':'left'},{'car':'blue', 'move':'forward'}, 
            {'car':'white', 'move':'left'}]})
        self.rounds.append({'round':'7', 'moves':[{'car':'red', 'move':'forward'}, 
            {'car':'black', 'move':'forward'},{'car':'blue', 'move':'forward'}, 
            {'car':'white', 'move':'left'}]})
        self.rounds.append({'round':'8', 'moves':[{'car':'red', 'move':'forward'}, 
            {'car':'black', 'move':'right'},{'car':'blue', 'move':'left'}, 
            {'car':'white', 'move':'left'}]})
        self.rounds.append({'round':'9', 'moves':[{'car':'red', 'move':'forward'}, 
            {'car':'black', 'move':'forward'},{'car':'blue', 'move':'left'}, 
            {'car':'white', 'move':'forward'}]})
        self.rounds.append({'round':'10', 'moves':[{'car':'red', 'move':'forward'}, 
            {'car':'black', 'move':'left'},{'car':'blue', 'move':'left'}, 
            {'car':'white', 'move':'left'}]})
        self.rounds.append({'round':'11', 'moves':[{'car':'red', 'move':'right'}, 
            {'car':'black', 'move':'left'},{'car':'blue', 'move':'forward'}, 
            {'car':'white', 'move':'left'}]})


        self.board_url = 'https://tokr9dryqf.execute-api.us-east-1.amazonaws.com/api'
        self.game_url = 'https://9xwedz01kj.execute-api.us-east-1.amazonaws.com/api'
        self.game_status_uri = '/game/status'
        self.game_new_uri = '/game/new'
        self.board_move_uri = '/joysticks/'
        self.region='us-east-1'
        self.iot_dp = boto3.client('iot-data', region_name=self.region)
        self.dynamodb_table = boto3.resource('dynamodb', region_name=self.region).Table('iot_game')
        self.sleep_amount = 5
        self.gamestatus_url = self.game_url + self.game_status_uri

    def test_simulated_game(self):
        """run a simulated game"""
        #post to start the game
        response = requests.post(url = self.game_url + self.game_new_uri)
        print(response.text)
        getgamestatus(self)
        #send move for rounds
        print(self.rounds)
        for game_round in self.rounds:
            for move in game_round['moves']:
                moveurl = self.board_url + self.board_move_uri + move['car'] +'/' + move['move']
                response = requests.post(url = moveurl)
                print('vehicle {}: {}'.format(move['car'], move['move']))
            #need to return iot messages, give a few seconds for state
            sleeptime(self)          
            #brute force messaging
            while True:
                moves = self.dynamodb_table.query(IndexName='movestatus-vehicleid-index',
                    KeyConditionExpression=Key('movestatus').eq('moverequested'))
                for move in moves['Items']:
                    acktopic = 'vehicle/physical/ack/' + str(move['vehicleid'])
                    print('sending {}'.format(acktopic))
                    message = {}
                    message['physical']=base64.b64encode(b'123,R,')
                    self.iot_dp.publish(topic=acktopic, qos=1, payload=json.dumps(message))
                sleeptime(self)
                if moves['Count']==0:
                    break
            #check the game status
            getgamestatus(self)
            
def sleeptime(self):
    print('sleeping....')
    time.sleep(self.sleep_amount)

def getgamestatus(self):
    print('getting game status')
    response = requests.get(url=self.gamestatus_url)
    print('Game status: {}'.format(response.text))


if __name__ == '__main__':
    unittest.main()
import app
import boto3
import decimal
import os
import unittest
import requests


class GameTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.region = os.getenv('region','us-east-1')
        self.iot_table = os.getenv('iot_table','iot_game_2')
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

    def test_generate_new_game(self):
        game_id = app.generate_new_game()
        self.assertEqual(self.get_game_id(), game_id)
    
    def test_reset_players(self):
        app.reset_players()
        for vehicle in self.vehicle_data:
            key = {}
            key['itemid'] = vehicle['itemid']
            key['status'] = 'meta'
            dbresult = self.dynamodb_table.get_item(Key=key)
            self.assertEqual(dbresult['Item']['itemid'],vehicle['itemid'])
            self.assertEqual(dbresult['Item']['x'],vehicle['x'])
            self.assertEqual(dbresult['Item']['y'],vehicle['y'])
            self.assertEqual(dbresult['Item']['facing'],vehicle['facing'])
            self.assertEqual(dbresult['Item']['score'],vehicle['score'])
            self.assertEqual(dbresult['Item']['type'],vehicle['type'])
            self.assertEqual(dbresult['Item']['vehicleid'],vehicle['vehicleid'])
            self.assertEqual(dbresult['Item']['it'],vehicle['it'])

    def test_new_round(self):
        game_id = self.get_game_id()
        game_round = self.get_round(game_id) + 1
        new_round = app.new_round()
        self.assertEqual(int(new_round['newround']), game_round)
        
    def get_game_id(self):
        meta_response = self.dynamodb_table.get_item(Key={'itemid':'game', 'status':'meta'})
        game_response = self.dynamodb_table.get_item(Key={'itemid': meta_response['Item']['gameid'], 'status':'active'})
        return game_response['Item']['itemid']

    def get_round(self, game_id):
        game_response = self.dynamodb_table.get_item(Key={'itemid': game_id, 'status':'active'})
        return int(game_response['Item']['round'])
        
if __name__ == '__main__':
    unittest.main()
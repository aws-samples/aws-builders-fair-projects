import boto3
from boto3.dynamodb.conditions import Key, Attr
from chalice import Chalice
import decimal
import json
import os
import unittest
import uuid

app = Chalice(app_name='GameMicroservice')

aws_account_id = boto3.client('sts').get_caller_identity().get('Account')
region = os.getenv('region','us-east-1')
iot_table = os.getenv('iot_table','iot_racer')
vehicles = int(os.getenv('vehicles','4'))
newround = os.getenv('next_round', 'new_round')
vehicle_list = ['red', 'blue', 'white', 'black']
sns_base = 'arn:aws:sns:us-east-1:'
topic_unlock_arn = sns_base + aws_account_id + os.getenv('topic_unlock', ':vehicle_unlock')
topic_vehicle_location = sns_base + aws_account_id + os.getenv('vehicle_location', ':vehicle_location' )
app.debug = os.getenv('DEBUG', True)

vehicle_home = {'red':{'x': '0', 'y':'0', 'facing':'S', 'vehicleid':1, 'it':True},
    'blue':{'x':'0', 'y':'5', 'facing':'N', 'vehicleid':2, 'it':False}, 
    'white':{'x':'5', 'y':'0', 'facing':'S', 'vehicleid': 3, 'it':False},
    'black':{'x':'5', 'y':'5', 'facing':'N', 'vehicleid': 4, 'it':False}}

dynamodb_table = boto3.resource('dynamodb', region_name=region).Table(iot_table)
sns = boto3.client('sns', region_name=region)

@app.route('/game/status')
def game_status():
    #return gameid, rounds, and current scores
    game_status = {}
    game_status['gameid'], game_status['round'] = get_game_and_round()
    pe = "itemid, score, x, y, facing, it"
    player_response = dynamodb_table.query(
        IndexName='status-type-index',
        ProjectionExpression=pe,
        KeyConditionExpression=Key('status').eq('meta') & Key('type').eq('vehicle'),
        ConsistentRead=True
        )
    game_scores = []
    for player in player_response['Items']:
        game_scores.append({player['itemid']:{'score':player['score'], 'x':player['x'],
            'y':player['y'], 'facing':player['facing'], 'it':player['it']}})
    game_status['Scores'] = game_scores
    return game_status
    
@app.route('/game/new', methods=['POST'])
def new_game():
    """trigger new game"""
    #change to SNS message
    gameid = generate_new_game()
    reset_players()
    trigger_players('New Game')
    return {'newgame':gameid}
    
#@app.route('/round/new', methods=['POST'])
def trigger_round():
    #TODO remove when no longer needed
    return handle_sns_message('')

@app.on_sns_message(topic=newround)
def handle_sns_message(event):  
    """trigger new round of the current game"""
    return new_round()
    
def new_round():
    app.log.debug('new round triggered')
    if duplicate_request():
        app.log.debug('this is a duplicate round request - aborting')
        return
    score_and_udpate_players()
    meta_response = dynamodb_table.get_item(Key={'itemid':'game', 'status':'meta'},
        ConsistentRead=True)
    update_response = dynamodb_table.update_item(Key={
        'itemid':meta_response['Item']['gameid'],'status':'active'},
        UpdateExpression='set #f1 = #f1 + :v1',
        ExpressionAttributeValues={':v1': decimal.Decimal(1)},
        ExpressionAttributeNames={'#f1': 'round'},
        ReturnValues='UPDATED_NEW'
        )
    trigger_players('New Round')
    return {'newround':update_response['Attributes']['round']}

def duplicate_request():
    gameid, round = get_game_and_round()
    status = gameid + "_" + str(round)
    player_response = dynamodb_table.query(
        IndexName='status-type-index',
        KeyConditionExpression=Key('status').eq(status) & Key('type').eq('vehicle'),
        ConsistentRead=True
        )
    if player_response['Count']==4:
        return False
    return True

def trigger_players(subject):
    #todo update to sending an SNS message
    for vehicle in vehicle_list:
        app.log.debug('unlock triggered for ' + vehicle)
        sns_response = sns.publish(TopicArn=topic_unlock_arn,Subject=subject,Message=vehicle)

def generate_new_game():
    """create a new game"""
    newgame=str(uuid.uuid4())
    put_response = dynamodb_table.put_item(Item={'itemid':newgame, 'status':'active', 'round':1})
    update_response = dynamodb_table.update_item(Key={'itemid':'game', 'status':'meta'},
        UpdateExpression='set #f1 = :v1',
        ExpressionAttributeValues={':v1': newgame},
        ExpressionAttributeNames={'#f1': 'gameid'},
        ReturnValues='UPDATED_NEW'
        )
    return update_response['Attributes']['gameid']

def reset_players():
    """reset virtual vehicles only to home"""
    #TODO: need to calculate route back to home
    for vehicle in vehicle_list:
        item = {}
        item['itemid'] = vehicle
        item['status'] = 'meta'
        item['x'] = vehicle_home[vehicle]['x']
        item['y'] = vehicle_home[vehicle]['y']
        item['score'] = 0
        item['type'] = 'vehicle'
        item['facing'] = vehicle_home[vehicle]['facing']
        item['vehicleid'] = vehicle_home[vehicle]['vehicleid']
        item['it'] = vehicle_home[vehicle]['it']
        result = dynamodb_table.put_item(Item=item)
        message = {}
        message['vehicle'] = item['itemid']
        message['x'] = int(item['x'])
        message['y'] = int(item['y'])
        message['facing'] = item['facing']
        subject='Move Vehicle'
        app.log.debug('Sending %s', json.dumps(message))
        sns_response = sns.publish(TopicArn=topic_vehicle_location,Subject=subject,Message=json.dumps(message))

def get_game_and_round():
    meta_response = dynamodb_table.get_item(Key={'itemid':'game', 'status':'meta'},
        ConsistentRead=True)
    game_response = dynamodb_table.get_item(Key={'itemid': meta_response['Item']['gameid'], 'status':'active'}, 
        ConsistentRead=True)
    return game_response['Item']['itemid'], game_response['Item']['round']

#@app.route('/score', methods=['POST'])        
def score_and_udpate_players():
    """score and update records for vehicles for next round"""
    #query by status & type, meta and vehicle
    gameid, round = get_game_and_round()
    app.log.debug("%s_%s", gameid, str(round))
    pe = "itemid, #s, score, x, y, facing, new_x, new_y, new_facing, it"
    player_response = dynamodb_table.query(
        IndexName='status-type-index',
        ProjectionExpression=pe,
        KeyConditionExpression=Key('status').eq(gameid + "_" + str(round)) & Key('type').eq('vehicle'),
        ExpressionAttributeNames={'#s' : 'status'},
        ConsistentRead=True
        )
    meta_response = dynamodb_table.query(
        IndexName='status-type-index',
        ProjectionExpression=pe,
        KeyConditionExpression=Key('status').eq('meta') & Key('type').eq('vehicle'),
        ExpressionAttributeNames={'#s' : 'status'},
        ConsistentRead=True
        )
    it_meta = None
    it = {}
    for player in meta_response['Items']:
        if player['it']:
            it_meta = player['itemid']
            app.log.debug('who is it? %s', it_meta)
    if not it_meta:
        #no one is it, a little easter egg :)
        app.log.debug('No one is it! %s', player_response)
    else:
        for player in player_response['Items']:
            if player['itemid'] == it_meta:
                it = player
                app.log.debug('Inner: %s %s', it, player)
                break
    app.log.debug('IT: %s', it)
    rolling = 0
    new_it = False
    for player in player_response['Items']:
        app.log.debug('Iterating through players')
        app.log.debug(player)
        player['score'], player['delta'] = score(player, it)
        rolling += player['score']
        key = {}
        key['itemid'] = player['itemid']
        key['status'] = player['status']
        if player['delta'] == 1 and not new_it:
            new_it = True
            #penalize new it score
            player['score']-=20
            update_player(key, player['score'], True, player['new_x'], player['new_y'], player['new_facing'])
        else:
            update_player(key, player['score'], False, player['new_x'], player['new_y'], player['new_facing'])
    rolling *= -1
    if new_it:
        rolling += 20
    key['itemid'] = it['itemid']
    key['status'] = it['status']
    update_player(key, rolling, not new_it)

def update_player(key, score, it, x = None, y = None, nf = None):
    player_update = dynamodb_table.update_item(Key=key,
        UpdateExpression='set score = :v1, it = :v2',
        ExpressionAttributeValues={
        ':v1': decimal.Decimal(score),
        ':v2': it
        },
        ReturnValues="UPDATED_NEW"
        )
    key['status']='meta'
    if not (x == None and y == None):
        meta_update = dynamodb_table.update_item(Key=key,
            UpdateExpression='set score = score + :v1, it = :v2, x = :v3, y = :v4, facing = :v5',
            ExpressionAttributeValues={
            ':v1': decimal.Decimal(score),
            ':v2': it,
            ':v3': x,
            ':v4': y,
            ':v5': nf
            },
            ReturnValues="UPDATED_NEW"
            )
    else:
        meta_update = dynamodb_table.update_item(Key=key,
            UpdateExpression='set score = score + :v1, it = :v2',
            ExpressionAttributeValues={
            ':v1': decimal.Decimal(score),
            ':v2': it
            },
            ReturnValues="UPDATED_NEW"
            )

def score(player, it):
    app.log.debug('scoring player %s', player['itemid'])
    app.log.debug('player %s', player)
    app.log.debug('it %s', it)
    old_value = abs(int(player['x']) - int(it['x'])
        ) + abs(int(player['y']) - int(it['y']))
    new_value = abs(int(player['new_x']) - int(it['new_x'])
        ) + abs(int(player['new_y']) - int(it['new_y']))
    flag = -1 if new_value < old_value else 1
    score = abs(old_value - new_value) * flag
    app.log.debug('score: %d and delta: %d', score, new_value)
    return score, new_value


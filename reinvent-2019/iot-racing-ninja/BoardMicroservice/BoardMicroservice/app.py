import boto3
from boto3.dynamodb.conditions import Key, Attr
from chalice import Chalice
import json
import os
import unittest


app = Chalice(app_name='BoardMicroservice')
app.debug=os.getenv('DEBUG', True)

aws_account_id = boto3.client('sts').get_caller_identity().get('Account')
region = os.getenv('region','us-east-1')
topic_vehiclemoved = os.getenv('topic_vehiclemoved', 'vehicle_moved')
sns_base = 'arn:aws:sns:us-east-1:'
topic_unlock_arn = sns_base + aws_account_id + os.getenv('topic_unlock', ':vehicle_unlock')
topic_round_arn = sns_base + aws_account_id + os.getenv('topic_round', ':round_reset')
move_arn = sns_base + aws_account_id + os.getenv('topic_move', ':moves_to_process')
vehicles = int(os.getenv('vehicles', 4))

iot_table = os.getenv('iot_game_table', 'iot_racer')

dynamodb_table = boto3.resource('dynamodb', region_name=region).Table(iot_table)
iot_dp = boto3.client('iot-data', region_name=region)
sns = boto3.client('sns', region_name=region)

@app.route('/joysticks/{vehicle}/{move}', methods=['POST'])
def vehicle_move(vehicle, move):
    message = {}
    message['joystick']=vehicle
    message['move']=move
    iot_response = iot_dp.publish(
            topic='joystick/move/' + vehicle,
            qos=1,
            payload=json.dumps(message)
        )          

    return (iot_response)

@app.route('/vehicles')
def get_vehicles():
    """return the entire list of vehicles and positions on root"""
    pe = "itemid, x, y, facing"
    app.log.debug('get_vehicles: getting all vehicle locations')
    result = dynamodb_table.query(
        IndexName='status-type-index',
        ProjectionExpression=pe,
        KeyConditionExpression=Key('status').eq('meta') & Key('type').eq('vehicle'),
        ConsistentRead=True
    )
    #iterate through the results and build json
    data = {}
    app.log.debug(result)
    for item in result['Items']:
        data[item['itemid']]={'facing': item['facing'], 'x': str(item['x']),'y': str(item['y'])}
    json_data = json.dumps(data)
    return (json_data)

@app.route('/vehicles/{id}')
def get_vehicle(id):
    """return status for a single vehicle"""
    result = dynamodb_table.get_item(Key={'itemid':id,'status':'meta'},
        ConsistentRead=True)
    data = {}
    data[result['Item']['itemid']]={'facing': result['Item']['facing'], 'x': str(result['Item']['x']),'y': str(result['Item']['y'])}
    return (json.dumps(data))

@app.on_sns_message(topic=topic_vehiclemoved)
def handle_sns_message(event):
    """Process SNS messages and move vehicles if all vehicles have made a move"""
    gamemeta_response = dynamodb_table.get_item(Key={'itemid':'game','status':'meta'},
        ConsistentRead=True)
    game_response = dynamodb_table.get_item(Key={'itemid':gamemeta_response['Item']['gameid'],'status':'active'},
        ConsistentRead=True)
    curr_round = game_response['Item']['itemid'] + '_' + str(game_response['Item']['round'])
    moves = dynamodb_table.query(IndexName='status-type-index',
        KeyConditionExpression=Key('status').eq(curr_round) & Key('type').eq('vehicle'),
        ConsistentRead=True)
    app.log.debug(moves['Items'])
    if moves['Count']==vehicles:
        moves_good = True
        for move in moves['Items']:
            app.log.debug('processing moves_good for %s', move)
            is_valid_move = True
            (new_facing, new_x, new_y, is_valid_move) = do_move(
                    move['move'], move['facing'], int(move['x']), int(move['y']))
            if is_valid_move:
                move['movestatus']='accepted'
                move['new_x']=new_x
                move['new_y']=new_y
                move['new_facing']=new_facing
                app.log.debug('%s move accpeted', move)
            else:
                moves_good = False
                move['movestatus'] = 'rejected'
                app.log.debug('%s move rejected', move)
        if moves_good == False:
            delete_bad_moves(moves['Items'])
            return{'bad moves':'true'}
        if same_spot_check(moves['Items']):
            #set move order and update all recordsc
            #TODO: check for vehicle collision
            if order_moves(moves['Items']):
                sns_response = sns.publish(TopicArn=move_arn,Subject='Moves Queued',Message=curr_round)
                return{'bad moves':'false'}
            else:
                return{'bad moves':'true'}
        else:
            delete_bad_moves(moves['Items'])
            return{'bad moves':'true'}

def do_move (move, facing, x, y):
    """calculate new move location"""
    valid_move = True
    if facing == 'N':
        if move == 'forward' and y > 0:
            y -= 1
        elif move == 'left' and x > 0:
            x -= 1
            facing = 'W'
        elif move == 'right' and x < 5:
            x += 1
            facing = 'E'
        else:
            valid_move = False
    elif facing == 'S':
        if move == 'forward' and y < 5:
            y += 1
        elif move == 'left' and x < 5:
            x += 1
            facing = 'E'
        elif move == 'right' and x > 0:
            x -= 1
            facing = 'W'
        else:
            valid_move = False
    elif facing == 'E':
        if move == 'forward' and x < 5:
            x += 1
        elif move == 'left' and y > 0:
            y -= 1
            facing = 'N'
        elif move == 'right' and y < 5:
            y += 1
            facing = 'S'
        else:
            valid_move = False
    elif facing == 'W':
        if move == 'forward' and x > 0:
            x -= 1
        elif move == 'left' and y < 5:
            y += 1
            facing = 'S'
        elif move == 'right' and y > 0:
            y -= 1
            facing = 'N'
        else:
            valid_move = False
    return (facing, x, y, valid_move)

def same_spot_check(moves):
    """validate that two cars are not going to the same spot"""
    movesaccepted = True
    for move in moves:
        if move['movestatus']=='rejected':
            continue
        for other_move in moves:
            if (other_move['movestatus']=='rejected') or (
                other_move['itemid'] == move['itemid']):
                continue
            if (move['new_x']==other_move['new_x']) and (
                move['new_y']==other_move['new_y']):
                #two moves to the same spot
                move['movestatus']='rejected'
                other_move['movestatus']='rejected'
                movesaccepted = False
    return movesaccepted

def delete_bad_moves(moves):
    """remove bad moves from the table"""
    for move in moves:
        if move['movestatus']=='rejected':
            key = {}
            key['itemid'] = move['itemid']
            key['status'] = move['status']
            #delete item to be rejected
            delete_response = dynamodb_table.delete_item(Key=key)
            sns_response = sns.publish(TopicArn=topic_unlock_arn,Subject='Invalid Move',Message=key['itemid'])

def order_moves(moves):
    """order the moves and update records"""
    x = len(moves) - 1
    order = 1
    while x > -1:
        for other_moves in moves:
            #find out if this car can move    
            can_move = True
            if moves[x]['itemid'] != other_moves['itemid'] and (
                moves[x]['new_x']==other_moves['x'] and moves[x]['new_y']==other_moves['y']):
                #this is the case where a vehicle cannot move until the prior has
                app.log.info('someone is in my way %s %s', moves[x]['itemid'], other_moves['itemid'])
                can_move = False
                break
        if can_move:
            #update the record to include the move order
            moves[x]['movestatus'] = 'readytomove'
            moves[x]['order'] = order
            key = {}
            key['itemid'] = moves[x]['itemid']
            key['status'] = moves[x]['status']
            app.log.info('moving %s', moves[x]['itemid'])
            update_response = dynamodb_table.update_item(Key=key,
                UpdateExpression='set #ord = :v1, #st = :v2, #nx = :v3, #ny = :v4, #nf = :v5',
                ExpressionAttributeValues={':v1': order, ':v2':moves[x]['movestatus'],
                    ':v3':moves[x]['new_x'],':v4':moves[x]['new_y'], ':v5':moves[x]['new_facing']
                },
                ExpressionAttributeNames={'#ord': 'order', '#st':'movestatus', '#nx':'new_x', '#ny':'new_y', '#nf':'new_facing'}
                )
            app.log.debug('move made by %s to %s, %s', moves[x]['itemid'], moves[x]['new_x'], moves[x]['new_y'])
            #remove move made from list, no need to compare to old location
            del moves[x]
            x = len(moves) - 1
            order = order + 1
        else:
            #try the next move
            app.log.debug('move not made for %s to %s, %s', moves[x]['itemid'], moves[x]['new_x'], moves[x]['new_y'])
            x-=1
    if len(moves) > 0:
        #there are some bad moves due to ordering - just delete those and reset joysticks
        for move in moves:
            move['movestatus'] = 'rejected'
        print(moves)
        delete_bad_moves(moves)
        return False
    else:
        #all moves ordered
        return True

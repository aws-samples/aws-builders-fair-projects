from chalice import Chalice
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

# Setup Chalice
app = Chalice(app_name='VehicleMicroservice')
app.debug = True

# Environment setup
region = os.getenv('region', 'us-east-1')
table_name = os.getenv('table_name', 'iot_racer')
num_vehicles = int(os.getenv('num_vehicles', "4"))
dynamodb_table = boto3.resource('dynamodb', region_name=region).Table(table_name)
sns = boto3.client('sns')
iot_dp = boto3.client('iot-data', region_name=region)
aws_account_id = boto3.client('sts').get_caller_identity().get('Account')
sns_arn_prefix = 'arn:aws:sns:{0}:{1}'.format(region, aws_account_id)

# SNS topic ARNs (for publishing)
vehicle_moved_topic_arn = '{0}:{1}'.format(sns_arn_prefix, os.getenv('vehicle_moved_topic', 'vehicle_moved'))
new_round_topic_arn = '{0}:{1}'.format(sns_arn_prefix, os.getenv('new_round_topic', 'new_round'))
moves_to_process_topic_arn = '{0}:{1}'.format(sns_arn_prefix, os.getenv('moves_to_process_topic', 'moves_to_process'))

# SNS topic names (for subscribing)
moves_topic = os.getenv('moves_topic', 'moves_to_process')
unlock_topic = os.getenv('unlock_topic', 'vehicle_unlock')
vehicle_location_topic = os.getenv('vehicle_location_topic', 'vehicle_location')

# Vehicles can only move in these directions
VALID_MOVES = ('forward', 'left', 'right',)

# New vehicle location
@app.on_sns_message(topic=vehicle_location_topic)
def handle_vehicle_location_sns_message(event):
    app.log.debug('Handle SNS: Vehicle Location')
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)

    if event.subject == 'Move Vehicle' and len(event.message) > 0:
        payload = json.loads(event.message)
        app.log.debug('Publish to vehicle/physical/location/{0}'.format(payload['vehicle']))
        iot_response = iot_dp.publish(
            topic='vehicle/physical/location/{0}'.format(payload['vehicle']),
            qos = 1,
            payload = event.message
        )

# Unlock joystick
@app.on_sns_message(topic=unlock_topic)
def handle_unlock_sns_message(event):
    app.log.debug('Handle SNS: Joystick Unlock')
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)

    if (event.subject == 'New Round' or event.subject == 'New Game' or event.subject == "Invalid Move") and len(event.message) > 0:
        vehicle_color = event.message
        app.log.debug('Publish "{0}" to joystick/status/{1}'.format(event.subject, vehicle_color))
        iot_response = iot_dp.publish(
            topic='joystick/status/{0}'.format(vehicle_color),
            qos = 1,
            payload = json.dumps({'joystick': vehicle_color, 'reason': event.subject})
        )

# Process moves
@app.on_sns_message(topic=moves_topic)
def handle_moves_sns_message(event):
    app.log.debug('Handle SNS: Moves Queued')
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)

    if event.subject == 'Moves Queued' and len(event.message) > 0:
        moves = dynamodb_table.query(IndexName='status-type-index',
            KeyConditionExpression=Key('status').eq(event.message) & Key('type').eq('vehicle'))
        
        if moves['Count'] == num_vehicles:
            # Okay to make the moves
            app.log.debug("Number of vehicles in query match expected number (%d), so proceeding", num_vehicles)
            round_number = event.message.split("_")[1]
            sorted_moves = sorted(moves['Items'], key=lambda k: k['order'])
            all_moves_made = True
            for move in sorted_moves:
                vehicle_color = move['itemid']
                vehicle_id = move['vehicleid']
                if move['movestatus'] == 'moverequested':
                    app.log.debug('Duplicate message... abort')
                    return
                if move['movestatus'] != 'readytomove':
                    continue
                all_moves_made = False
                direction = move['move']
                app.log.debug("Move vehicle '%s' %s", vehicle_color, move['move'])
                iot_response = iot_dp.publish(
                    topic='vehicle/physical/move/' + vehicle_color,
                    qos = 1,
                    payload = json.dumps({'vehicle': vehicle_color, 'move': direction})
                )
                ddb_response = dynamodb_table.update_item(
                    Key={'itemid': vehicle_color, 'status': event.message},
                    UpdateExpression='SET movestatus = :val1',
                    ExpressionAttributeValues={
                        ':val1': 'moverequested'
                    }
                )
                break
            if all_moves_made:
                app.log.debug('Publish to new_round SNS topic')
                sns_response = sns.publish(
                    TopicArn=new_round_topic_arn,
                    Message="all moves made",
                )
                app.log.debug("All moves made. new_round SNS topics notified.")
        else:
            app.log.debug("Number of vehicles in query (%d) match expected number (%d), so aborting", moves['Count'], num_vehicles)

@app.lambda_function(name='iot_handler')
def iot_handler(event, context):
    app.log.debug('Handle IoT')
    app.log.debug('Event: %s', event)

    # Setup game record structure
    game_meta = {}
    game_meta['itemid'] = 'game'
    game_meta['status'] = 'meta'
    gamemeta_response = dynamodb_table.get_item(Key=game_meta, ConsistentRead=True)
    app.log.debug('game_meta='+repr(gamemeta_response))

    game = {}
    game['itemid']=gamemeta_response['Item']['gameid']
    game['status']='active'
    game_response = dynamodb_table.get_item(Key=game, ConsistentRead=True)
    game_status = game_response['Item']['itemid']+"_"+str(game_response['Item']['round'])
    app.log.debug('game_response status='+repr(game_status))

    # Joystick move on IoT topic = joystick/move/{color}
    if ('joystick' in event) and ('move' in event):
        move = event['move']
        if move not in VALID_MOVES:
            app.log.debug('"{0}" not a valid move'.format(move))
            return
        vehicle_color = event['joystick']

        item = {}
        item['itemid'] = vehicle_color
        item['status'] = 'meta'
        meta_response = dynamodb_table.get_item(Key=item, ConsistentRead=True)
        meta_item = meta_response['Item']
        vehicle_id = meta_item['vehicleid']
        current_x = meta_item['x']
        current_y = meta_item['y']
        facing = meta_item['facing']

        # Register move and send SNS message for board controller
        response = dynamodb_table.put_item(Item={
            'itemid': vehicle_color, 'vehicleid': vehicle_id, 'status': game_status, 'move': move,
            'x': current_x, 'y': current_y, 
            'type':'vehicle', 'facing': facing,
            'movestatus':'registered'
        })
        response = dynamodb_table.put_item(Item=meta_item)

        app.log.debug('Publish to vehicle_moved SNS topic')
        response = sns.publish(
            TopicArn=vehicle_moved_topic_arn,
            Message=vehicle_color + " moved.",
        )

    # Ack from device moved on IoT topic = vehicle/physical/ack/{color}
    elif ('physical' in event):
        if len(event['physical']) > 0:
            payload = event['physical']
            app.log.debug('payload='+repr(payload))
            app.log.debug('topic='+repr(event['topic']))
            try:
                vehicle_color = payload['vehicle']
                app.log.debug('vehicle_color='+repr(vehicle_color))
            except:
                app.log.error('ERROR: Could not find vehicle color')

            ddb_response = dynamodb_table.update_item(
                Key={'itemid': vehicle_color, 'status': game_status},
                UpdateExpression='SET movestatus = :val1',
                ExpressionAttributeValues={
                    ':val1': 'movecompleted'
                }
            )

            app.log.debug('Publish to moves_to_process SNS topic')
            response = sns.publish(
                TopicArn=moves_to_process_topic_arn,
                Subject='Moves Queued',
                Message=game_status
            )
        else:
            app.log.error('ERROR: Physical payload is empty')
    else:
        app.log.error('ERROR: unknown event: {}'.format(event))
    return
# Vehicle Microservice #

The Vehicle Microservice handles communication with both the joysticks and the physical vehicles.

## Framework ##
Chalice is used as the framework for this microservice. The single Python file (app.py) has 
multiple handlers, depending on the source of the event (IoT or SNS). When deploying the 
code, Chalice creates multiple Lambda functions from the same source (app.py). For IoT 
and SNS events, it creates Lambda functions with the appropriate triggers.

## Joystick Communication ##
When a joystick makes a move, an IoT message is published to the topic `joystick/move/{color}`, 
where {color} is one of \[black, blue, red, white\]. An IoT rule is configured to invoke the 
Lambda function `VechicleMicroservice-dev-iot_handler`. This function queries DynamoDB 
to get the current game and round information and then updates the appropriate vehicle item 
in DynamoDB with the requested move and also publishes "{color} moved." to the vehicle_moved 
SNS topic.

When the joysticks need to be unlocked for a next move, an SNS message is published to an 
unlock topic, which this microservice is subscribed to. When triggered, it publishes a 
message to the appropriate IoT topic (`joystic/status/{color}`), which allows the joystick 
controllers to set the appropriate status.

## Physical Map Communication ##
When all moves are ready to be processed (after the board microservice does its work), a 
message is published to the `moves_to_process` SNS topic with the game ID and round number. 
This microservice iterates through each move for the associated game and round, in order, 
and publishes a message to the `vehicle/physical/move/{color}` topic for the physical map 
to be updated.

After the physical map is updated for each move, an acknowledgement is published back to 
`vehicle/physical/ack/{color}`, which this microservice is subscribed to. It then updates 
the movestatus attribute in DynamoDB to `movecompleted`. After all vehicles are updated, 
a final  message is published to the `new_round` SNS topic to indicate a new round.
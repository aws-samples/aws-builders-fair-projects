# Board Microservice #

The Board Microservice handles communications from and to the Vehicle Microservice.  Board handles the validation of moves on the defined space and triggers appropriate events based on the state of the moves.  Each of the access points to Board are discussed below.

## SNS Message Integration ##
The following APIs are triggered via SNS messages

### Topic : vehicle_moved ###
This entry point checks to see if there are moves registered from all vehicles.  Once all four moves are validated, the order of moves is calculated, and a message is posted to the SNS topic 'moves_to_process'

This entry point will exit if there are less than 4 moves registered from the Vehicle microservice, as this is not a full round.

This entry point will also send out commands to unlock joysticks related to invalid moves, which are moves off the board or when 2 or more cars try to enter the same space.  In this case, an SNS message will be posted to vehicle_unlock with the color of the vehicle that needs to be unlocked.  In cases where multiple cars make invalid moves, multiple messages will be sent.  Invalid moves are also deleted from the DynamoDB table at this point.

## API Gateway ##
The following APIs are triggered via the API gateway endpoint

### /joysticks/{vehicle}/{move} [POST] ###
This is a testing entry point for sending moves without using the physical joysticks.  Valid values for each are below:

| Vehicle |
|-|
| Red |
| Blue |
| Black |
| White |

| Move |
|-|
| Forward |
| Left |
| Right |


# Validating for delete #

Access Patterns
1) /vehicles - Get the meta records for the vehicles
    - status = meta & type = vehicle

2) /vehicle/id - get the meta for a single vehicle 
    - item = color & status = meta
    
3) vehiclemoved
    - item = game & status = meta
    - item = gameid & status = active
    - status = game_current_round & status = vehicle
    
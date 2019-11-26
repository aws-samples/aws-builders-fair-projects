# Game Microservice #

The Game Microservice is responsible for handling the game rules for IoTRacer.Ninja.  The game that is presented here is a game of tag, in which one player is defined as "It."  The player who is It can tag another player, who then becomes It.

## Player Goals : It ##
The goal of the player who is It is to get closer to the players who are not It and to tag another player so they become it.  The player who is It gains scores for getting closer to the other players during a move.  If the player tags someone else, they receive a bonus of 20 points to their score.  A player tags another by moving into a space either horizantally or vertically next to another player.

## Player Goals : Not It ##
The goal of the players who are not it is to move further from the player who is it.  Players who are not it lose points for getting closer to the player who is It and gain points for moving further from the player who is it.  Players who get tagged and become it lose 20 points.

## SNS ##

### Message from new_round ###
Triggers the scoring calculations and updates from all the moves, once accomplished.  Score is calculated by user, updated to DynamoDB, and a message is sent to vehicle_unlock to signify the closing of the current round and unlock the joysticks for input for the next round.

## API Gateway ##

### /game/status [GET] ###
Retrieves the current game's status, including game id, round, player locations, and player scores.

### /game/new [POST] ###
Starts a new game and resets player positions to their home locations.  This sends an SNS message to vehicle_unlock to unlock the joysticks and to vehicle_location to reset the real vehicle locations.


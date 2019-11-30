export const HubEvents = {
    BECOME_PLAYER: "becomePlayer",
    BECOME_HOST: "becomeHost"
};
export const PubSubEvents = {
    CHALLENGER_JOIN: "challengerJoin", // When a player joins
    GAME_PLAYERS: "gamePlayers",
    REQUEST_GAME_CODE_CHECK: "requestGameCodeCheck", // Request to verify game code
    RESPOND_GAME_CODE_CHECK_SUCCESS: "respondGameCodeCheckSuccess", // Response of the verify game code
    RESPOND_GAME_CODE_CHECK_FAIL: "respondGameCodeCheckFail", // Response of the verify game code
    CANCEL_GAME: "cancelGame", // Host cancels game
    START_GAME: "startGame", // Host starts the game
    SUBMIT_DOODLE: "submitDoodle", // Player submits their drawing
    NEXT_ROUND: "nextRound", // Host signals a new round
    END_GAME: "endGame", // Host signals the entire game has ended
    NEW_GAME: "newGame", // Host will start a new game, this will include the updated gamecode so existing players can auto join without typnig it in again
    REMOVE_FROM_GAME: "removeFromGame", // Host kicked player out. Either due to capacity or they just felt like it.
    LEAVE_GAME: "leaveGame" // The player has left the game
};
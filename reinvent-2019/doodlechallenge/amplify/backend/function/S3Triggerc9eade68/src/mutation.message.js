const createGameMessage = `mutation CreateGameMessage($input: CreateGameMessageInput!) {
  createGameMessage(input: $input) {
    id
    room
    action
    data
    message
    createdAt
  }
}
`;
module.exports = {
  createGameMessage,
}  
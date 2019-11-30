/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createGame = `mutation CreateGame($input: CreateGameInput!) {
  createGame(input: $input) {
    id
    room
    players {
      uuid
      room
      name
      avatar
      doodles {
        name
        score
        url
      }
    }
  }
}
`;
export const updateGame = `mutation UpdateGame($input: UpdateGameInput!) {
  updateGame(input: $input) {
    id
    room
    players {
      uuid
      room
      name
      avatar
      doodles {
        name
        score
        url
      }
    }
  }
}
`;
export const deleteGame = `mutation DeleteGame($input: DeleteGameInput!) {
  deleteGame(input: $input) {
    id
    room
    players {
      uuid
      room
      name
      avatar
      doodles {
        name
        score
        url
      }
    }
  }
}
`;
export const createGameMessage = `mutation CreateGameMessage($input: CreateGameMessageInput!) {
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
export const updateGameMessage = `mutation UpdateGameMessage($input: UpdateGameMessageInput!) {
  updateGameMessage(input: $input) {
    id
    room
    action
    data
    message
    createdAt
  }
}
`;
export const deleteGameMessage = `mutation DeleteGameMessage($input: DeleteGameMessageInput!) {
  deleteGameMessage(input: $input) {
    id
    room
    action
    data
    message
    createdAt
  }
}
`;

/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getGame = `query GetGame($id: ID!) {
  getGame(id: $id) {
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
export const listGames = `query ListGames(
  $filter: ModelGameFilterInput
  $limit: Int
  $nextToken: String
) {
  listGames(filter: $filter, limit: $limit, nextToken: $nextToken) {
    items {
      id
      room
      players {
        uuid
        room
        name
        avatar
      }
    }
    nextToken
  }
}
`;
export const getGameMessage = `query GetGameMessage($id: ID!) {
  getGameMessage(id: $id) {
    id
    room
    action
    data
    message
    createdAt
  }
}
`;
export const listGameMessages = `query ListGameMessages(
  $filter: ModelGameMessageFilterInput
  $limit: Int
  $nextToken: String
) {
  listGameMessages(filter: $filter, limit: $limit, nextToken: $nextToken) {
    items {
      id
      room
      action
      data
      message
      createdAt
    }
    nextToken
  }
}
`;

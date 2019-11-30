/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const onCreateGame = `subscription OnCreateGame {
  onCreateGame {
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
export const onUpdateGame = `subscription OnUpdateGame {
  onUpdateGame {
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
export const onDeleteGame = `subscription OnDeleteGame {
  onDeleteGame {
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
export const onCreateGameMessage = `subscription OnCreateGameMessage {
  onCreateGameMessage {
    id
    room
    action
    data
    message
    createdAt
  }
}
`;
export const onUpdateGameMessage = `subscription OnUpdateGameMessage {
  onUpdateGameMessage {
    id
    room
    action
    data
    message
    createdAt
  }
}
`;
export const onDeleteGameMessage = `subscription OnDeleteGameMessage {
  onDeleteGameMessage {
    id
    room
    action
    data
    message
    createdAt
  }
}
`;

const defaultState = {
    username: "guest",
    connectionId: "",
    matchId: "",
    score: 0
}

const UserReducer = (state = defaultState, action) => {
    switch(action.type) {
        case 'SET_CONN_ID':
                return { ...state, connectionId: action.connectionId}
        case 'SET_MATCH_ID':
                return { ...state, matchId: action.matchId}
        case 'SET_USERNAME':
                return {...state, username: action.username}
        case 'INC_SCORE':
                return {...state, score: state.score + 1}
        default:
            return state
    }
}

export default UserReducer
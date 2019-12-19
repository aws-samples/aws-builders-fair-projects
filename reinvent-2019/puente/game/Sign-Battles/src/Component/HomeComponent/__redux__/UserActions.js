const UserActions = dispatch => {
    return {
        setUsername: (username) =>  {
            dispatch({
                type: 'SET_USERNAME',
                username: username
            })
        },
        setConnId: connectionId => {
            dispatch({
                type: 'SET_CONN_ID',
                connectionId: connectionId
            })
        },
        setMatchId: matchId =>  {
            dispatch({
                type: 'SET_MATCH_ID',
                matchId: matchId
            })
        },
        incScore: () => {
            dispatch({
                type: 'INC_SCORE'
            })
        },
        incTimer: () => {
            dispatch({
                type: "INC_TIMER"
            })
        },
        startMatch: () =>   {
            dispatch({
                type: "START_MATCH"
            })
        },
        setResults: (result) => {
            dispatch({
                type: 'SET_RESULT',
                result: result
            })
        }
    }
}

export default UserActions
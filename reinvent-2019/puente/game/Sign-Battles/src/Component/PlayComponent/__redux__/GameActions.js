const GameActions = dispatch => {
    return {
        logResult: result => {
            dispatch({
                type: 'LOG_RESULT',
                result: result
            });
        },
        changeWord: word => {
            dispatch({
                type: 'CHANGE_WORD',
                word: word
            })
        },
        updateInput: letter => {
            dispatch({
                type: 'UPDATE_INPUT',
                letter: letter
            })
        },
        updateWord: (word) => {
            dispatch({
                type: 'UPDATE_WORD',
                word: word
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
        reset: () => {
            dispatch({
                type: 'RESET'
            })
        },
        setMatchResults: (result) => {
            dispatch({
                type: 'SET_MATCH_RESULT',
                result: result
            })
        },
        setGameOver: () =>  {
            dispatch({
                type: 'GAMEOVER'
            })
        }
    }
}

export default GameActions
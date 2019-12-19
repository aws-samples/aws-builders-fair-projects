const defaultState = {
    gameOver: false,
    startMatch: false,
    matchResult: "lose",
    input: "",
    words: ["abc", "cba", "def", "fed", "aba"],
    time: 0,
    results: [],
    classMap: ["A", "B", "C", "D", "E", "F", "G", "H"],
    videoConstraints: {
        width: 512,
        height: 512,
        facingMode: "environment"
    }
}

const GameReducer = (state = defaultState, action) => {
    switch (action.type) {
        case 'UPDATE_WORD':
            return {...state, word: action.word }
        case 'LOG_RESULT':
            return {...state, results: [...state.results, action.result ]}
        case 'UPDATE_INPUT':
            return {...state, input: state.input + action.letter }
        case 'RESET':
            return {...state, input: ""}
        case 'INC_TIMER':
            return {...state, time: ++state.time }
        case 'START_MATCH':
            return {...state, startMatch: true}
        case 'SET_MATCH_RESULT':
            return {...state, matchResult: action.result}
        case 'GAMEOVER':
            return {...state, gameOver: true }
        default:
            return state
    }
}

export default GameReducer
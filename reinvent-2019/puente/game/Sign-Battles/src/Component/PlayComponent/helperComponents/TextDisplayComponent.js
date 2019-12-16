import React from 'react';
import { connect } from 'react-redux'

function TextDisplay(props)  {
    return (
        <React.Fragment>
            <p>Time: {props.time}</p>
            <p>Word: {props.words[props.score]}</p>
            <p>Current: {props.input}</p>
        </React.Fragment>
    )
}

const mapStateToProps = (state) =>  {
    return  {
        time: state.game.time,
        input: state.game.input,
        words: state.game.words,
        score: state.user.score
    }
}

export default connect(mapStateToProps, null)(TextDisplay);
import React from 'react';
import { connect } from 'react-redux';

function PredictionResult(props){
    return (
        <p>{props.result === undefined ? null : props.result.pop()}</p>
    )
}

function mapStateToProps(state)  {
    return{
        result: state.game.results
    }
}

export default connect(mapStateToProps, null)(PredictionResult);

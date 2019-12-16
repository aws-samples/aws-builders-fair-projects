import React from 'react'
import { connect } from 'react-redux';
import GameActions from '../PlayComponent/__redux__/GameActions';

class Waiting extends React.Component   {

    render()    {
        return  (
            <React.Fragment>
                {this.props.matchResult === 'win' ? <p> You Win! </p> : <p> You Lose! </p> }
            </React.Fragment>
        )
    }
}

const mapStateToProps = (state) => {
    return  {
        matchResult: state.game.matchResult
    }
}

export default connect(mapStateToProps, GameActions)(Waiting);
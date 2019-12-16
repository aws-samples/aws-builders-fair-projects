import React from 'react'
import { connect } from 'react-redux'

import UserActions from './__redux__/UserActions'

class Home extends React.Component {
    constructor(props)  {
        super(props)
        this.state = {
            username: ""
        }
    }

    startMatch = () => {
        this.props.setUsername(this.state.username)
        this.props.history.push({
            pathname: "/play"
          })
    }

    handleChange = (event) =>   {
        this.setState({username: event.target.value});
    }

    render() {
        return (
            <React.Fragment>
                <input onChange={this.handleChange} value={this.state.username}></input>
                <button onClick={this.startMatch}>Start Match</button>
            </React.Fragment>
        )
    }
}


export default connect(null, UserActions)(Home)
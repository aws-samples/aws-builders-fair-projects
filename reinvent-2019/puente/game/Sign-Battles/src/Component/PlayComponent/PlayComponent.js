import React from 'react';
import { connect } from 'react-redux';

import UserActions from '../HomeComponent/__redux__/UserActions';

import Camera from './helperComponents/CameraComponent'
import PredictionResult from './helperComponents/PredictionResultComponent';
import TextDisplay from './helperComponents/TextDisplayComponent';


class Play extends React.Component {
    constructor(props) {
        super(props)

        this.websocket = null
        this.time = 0;

        this.state = {
            isOpen: false,
            WS_URL: "wss://aeheisl368.execute-api.us-east-2.amazonaws.com/alpha",
            timeInterval: null
        }
    }

    componentDidMount() {
        this.initSocket()
        this.waitForSocketConnection(() => {
            this.sendMessage("JoinMatch", { username: this.props.username })
        })
    }

    componentWillUnmount() {
        clearInterval(this.state.timeInterval)
    }

    waitForSocketConnection(callback) {
        setTimeout(
            () => {
                if (this.websocket.readyState === 1) {
                    console.log("Connection is made")
                    if (callback != null) {
                        callback();
                    }
                } else {
                    console.log("wait for connection...")
                    this.waitForSocketConnection(callback);
                }

            }, 5);
    }

    /**
    *  Set up WebSocket connection for a new user and
    *  basic listeners to handle events
    */
    initSocket = () => {
        this.websocket = new WebSocket(this.state.WS_URL);
        this.websocket.onopen = this.onConnOpen;
        this.websocket.onmessage = this.onMessage;
        this.websocket.onclose = this.onConnClose;
    }

    onConnOpen = () => {
        this.setState({ isOpen: true });
        console.log('Websocket connected!');
    }

    /**
     *  Log lost connection for now
     */
    onConnClose = () => {
        console.log('Websocket closed!');
        this.initSocket()
    }

    onMessage = (data) => {
        console.log("before: ", data)
        if (data) {
            let parsedData = JSON.parse(data.data)
            console.log("data: ", parsedData)
            switch (parsedData.route) {
                case 'JOIN_MATCH':
                    this.props.setConnId(parsedData.connectionId)
                    this.props.setMatchId(parsedData.matchId)
                    break;
                case 'INC_SCORE':
                    console.log(parsedData)
                    break;
                case 'PLAYER_JOINED':
                    console.log("Num of players in match: ", Object.keys(parsedData.players).length)
                    if (Object.keys(parsedData.players).length >= 2)   {
                        this.props.startMatch()
                        if ( this.state.timeInterval !== null)  {
                            this.setState({
                                    timeInterval: setInterval(() => { this.props.incTimer() }, 1000)
                            })
                        }
                    }
                    break;
                case 'GAME_OVER':
                    console.log("gameover")
                    this.props.history.push({
                        pathname: "/results"
                    })
                    break;
                default:
                    console.log("default: ", data)
            }
        }
    }

    sendMessage = (routeKey, message) => {
        if (this.websocket && this.state.isOpen) {
            this.websocket.send(JSON.stringify({
                action: routeKey,
                data: message
            }));
        } else {
            console.log(`Websocket connection not found!!`);
        }
    }

    render() {
        return (
            <React.Fragment>
                {!this.props.startMatchBool ?
                    <React.Fragment>
                        <p>Waiting for player</p>
                    </React.Fragment> :
                    <React.Fragment>
                        <Camera sendMessage={this.sendMessage} history={this.props.history} />
                        <PredictionResult />
                        <TextDisplay></TextDisplay>
                        <button onClick={this.test}>test</button>
                    </React.Fragment>}
            </React.Fragment>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        username: state.user.username,
        startMatchBool: state.game.startMatch
    }
}

export default connect(mapStateToProps, UserActions)(Play);
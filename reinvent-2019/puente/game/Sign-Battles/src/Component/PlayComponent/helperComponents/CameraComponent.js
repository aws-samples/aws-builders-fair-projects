import React from 'react';
import Webcam from 'react-webcam';
import { connect } from 'react-redux';

import _ from 'lodash';
import { PuenteAdapter } from '../../../Adapters/PuenteAdapter'
import GameActions from '../__redux__/GameActions'

class Camera extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            intervalId: null,
            currentWord: ""
        }
    }

    componentDidMount = () => {
        this.setState({
            interval: setInterval(this.videoPredict, this.props.interval !== undefined ? this.props.interval : 1000)
        })
    };

    componentWillUnmount = () => {
        clearInterval(this.state.intervalId);
    };

    webcamRef = webcam => {
        this.webcam = webcam;
    };

    // Captures screenshot and sends it to Puente API. It then filters the result to extract the highest prediction rate.
    videoPredict = (imgString) => {
        if(!this.webcam)    {
            return
        }
        if (imgString === undefined) {
            imgString = this.webcam.getScreenshot()
        }
        PuenteAdapter.classify(imgString)
            .then(res => {
                if(res.indexOf) {
                    // console.log(res)
                    let maxKey = res.indexOf(_.max(res));
                    this.props.logResult(this.props.classMap[maxKey])

                    // console.log("predictions: ", res);
                    // console.log("max: ", maxKey);

                    this.addLetter(this.props.classMap[maxKey])
                }
            })
    };

    addLetter = letter =>   {
        //DEBUG
        // console.log("letter: ", letter)
        // console.log("word: ", this.props.word)
        // console.log("last letter: ", this.state.currentWord)

        
            //Check if letter signed is correct
            if (letter.toLowerCase() === this.props.words[this.props.score][this.props.input.length])  {
                this.props.updateInput(letter)
            }
            
            //Check if entire word is correct
            if (this.props.input.toLowerCase() === this.props.words[this.props.score] )   {
                console.log("word complete")
                this.props.reset()
                this.props.sendMessage("IncScore", {
                    word: this.props.words[this.props.score],
                    connectionId: this.props.connectionId,
                })
                this.props.incScore()
            }

            if (this.props.score === 1 ) {
                this.props.setGameOver()
                this.props.setMatchResults('win')
                this.props.sendMessage("GameOver", {
                    matchId: this.props.matchId
                })
                console.log("hereeee: ", this.props.matchId)
            }
        }
    

    render() {
        return (
            <React.Fragment>
                <Webcam
                    id="webcam"
                    ref={this.webcamRef}
                    audio={false}
                    height={512}
                    width={512}
                    screenshotFormat="image/jpeg"
                    videoConstraints={this.props.videoConstraints}
                />
            </React.Fragment>
        )
    }
}

const mapStateToProps = state => {
    return {
        videoConstraints: state.game.videoConstraints,
        classMap: state.game.classMap,
        words: state.game.words,
        input: state.game.input,
        connectionId: state.user.connectionId,
        score: state.user.score,
        matchId: state.user.matchId,
        gameOver: state.game.gameOver
    }
}

export default connect(mapStateToProps, GameActions)(Camera);
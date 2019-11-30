import React from 'react';
import {Grid} from '@material-ui/core';
import {NEXT_DOODLE_DELAY} from '../../../../constants';
import ModuleRoundResultsItem from './item';
import ModuleCountDown from './countDown';
import './index.css';

export default class Welcome extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentPlayer:0,
      show:true,
      countDown:false
    };
  }
  componentDidMount(){
    this.timer = setInterval(this.tickTock.bind(this), NEXT_DOODLE_DELAY);
  }
  componentWillMount(){
    clearInterval(this.timer);
  }
  tickTock(){
    if(this.state.currentPlayer < this.props.players.length-1){
      this.setState(prevState=>{
        return {show:false}
      }, ()=>{
        setTimeout(()=>{
          this.setState(prevState => {
            return {currentPlayer: prevState.currentPlayer + 1, show:true}
          });
        }, 500);
      });
    }else{
      clearInterval(this.timer);
      if(this.props.round < this.props.doodles.length-1){
        this.setState(prevState=>{
          return {countDown:true}
        }, ()=>{
          setTimeout(()=>{
            this.props.handleNextRound();
          }, NEXT_DOODLE_DELAY);
        });
      }else{
        this.props.handleNextRound();
      }
    }
  }
  getChallenge(player){
    if(player.doodles.length > 0 && (this.props.round === player.doodles.length-1)){
      return player.doodles[player.doodles.length-1];
    }
    return null;
  }
  isWinner(player){
    if(!this.props.endRound){ return false; }
    let highest = 0;
    
    for(let i = 0; i < this.props.players.length; i++){
      if(this.props.players[i].doodles[this.props.round] && highest < this.props.players[i].doodles[this.props.round].score){
        highest = this.props.players[i].doodles[this.props.round].score;
      }
    }
    return (player.doodles[this.props.round].score >= highest);
  }
  
  componentDidUpdate(){
    // console.log("InGame Progress Component Did Update");
    // if(this.props.endRound){
    //   console.log("Round completed");
    //   setTimeout(()=>{
    //     this.props.handleNextRound();
    //   }, NEXT_ROUND_DELAY);
    //   //this.props.handleNextRound();
    // }
  }
  render (){
    let doodle = this.getChallenge(this.props.players[this.state.currentPlayer]);
    let winner = this.isWinner(this.props.players[this.state.currentPlayer]);
    return (
      <Grid className="Screen_Host_RoundResults"
      container
      spacing={2}
      direction="column"
      alignItems="center"
      justify="center"
      >
        {this.props.players && this.props.players.length > 0 && 
          <Grid className="InGameProgress_GridPlayer_Item" item xs={12}>
            <ModuleRoundResultsItem show={this.state.show} doodle={doodle} winner={winner} player={this.props.players[this.state.currentPlayer]}></ModuleRoundResultsItem>
          </Grid>
        }
        {this.state.countDown && 
          <ModuleCountDown/>
        }
      </Grid>
    );
  }
}
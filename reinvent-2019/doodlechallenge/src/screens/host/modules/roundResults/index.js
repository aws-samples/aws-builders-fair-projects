import React from 'react';
import {Typography, Grid} from '@material-ui/core';
import ComponentLeaderBoard from '../../../../components/leaderboard';
import ModuleAnimateResultItems from './animateResultItems';
import {NEXT_ROUND_DELAY} from '../../../../constants';
import './index.css';

export default class Welcome extends React.Component {
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
  removePlayer(player){
    if(window.confirm("Are you sure you want to remove this player?")){
      this.props.removePlayer(player);
    }
  }
  render (){
    // We only want to go as small as 3 per row
    let itemColumnSize = (this.props.players.length > 3) ? 4:Math.ceil(12/this.props.players.length);
    if(itemColumnSize > 6){
      itemColumnSize = 6;
    }
    return (
      <div>
        <Typography variant="h2" component="h2" style={{color:"#FFF", textAlign:"center", marginBottom:"20px", paddingTop:"50px", paddingBottom:"20xp"}}>
          draw <strong>'{this.props.doodles[this.props.round].object.toUpperCase()}'</strong> on your device now!
        </Typography>
        <ComponentLeaderBoard removePlayer={this.removePlayer.bind(this)} players={this.props.players}></ComponentLeaderBoard>
        {this.props.endRound &&
          <ModuleAnimateResultItems endRound={this.props.endRound} handleNextRound={this.props.handleNextRound} doodles={this.props.doodles} round={this.props.round} players={this.props.players}/>
        }
      </div>
    );
  }
}
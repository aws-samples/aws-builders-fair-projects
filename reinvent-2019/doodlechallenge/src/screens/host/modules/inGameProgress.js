import React from 'react';
import {Typography, Grid} from '@material-ui/core';
import ModuleInGameProgressPlayer from './inGameProgressPlayer';
import {DOODLES, NEXT_ROUND_DELAY} from '../../../constants';
import '../index.css';

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
    console.log("highest: ",highest, "- Your score: ", player.doodles[this.props.round].score);
    return (player.doodles[this.props.round].score >= highest);
  }
  removePlayer(player){
    if(window.confirm("Are you sure you want to remove this player?")){
      this.props.removePlayer(player);
    }
  }
  componentDidUpdate(){
    if(this.props.endRound){
      setTimeout(()=>{
        this.props.handleNextRound();
      }, NEXT_ROUND_DELAY);
      //this.props.handleNextRound();
    }
  }
  render (){
    // We only want to go as small as 3 per row
    let itemColumnSize = (this.props.players.length > 3) ? 4:Math.ceil(12/this.props.players.length);
    if(itemColumnSize > 6){
      itemColumnSize = 6;
    }
    return (
      <Grid className="Screen_Host_InGame_Progress"
      container
      spacing={2}
      direction="column"
      alignItems="center"
      justify="center"
      style={{ minHeight: '100vh' }}
      >
        <Grid item xs={12}>
          <Typography variant="h2" component="h2" style={{color:"#FFF", textAlign:"center", marginBottom:"20px", paddingTop:"50px", paddingBottom:"20xp"}}>
            draw <strong>'{DOODLES[this.props.round].object.toUpperCase()}'</strong> on your device now!
          </Typography>
          <Grid container className="InGameProgress_GridPlayer" spacing={3}
          direction="row"
          alignItems="center"
          justify="center">
          {this.props.players.map((player,index)=>{
            let doodle = this.getChallenge(player);
            let winner = this.isWinner(player);
            console.log("doodle: ", doodle);
            console.log("winner: ", winner);
            console.log("Column size: ", itemColumnSize);
            return(
              <Grid className="InGameProgress_GridPlayer_Item" key={index} item xs={itemColumnSize}>
                <button className="button-remove" onClick={()=>{this.removePlayer(player);}}>X</button>
                <ModuleInGameProgressPlayer endRound={this.props.endRound} player={player} doodle={doodle} winner={winner}/>
              </Grid>
            )
          })}
          </Grid>
        </Grid>
      </Grid>
    );
  }
}
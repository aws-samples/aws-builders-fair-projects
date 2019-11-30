import React from 'react';
import { Grid } from '@material-ui/core';
import ModuleRoundResults from './roundResults';
import ComponentLeaderBoard from '../../../components/leaderboard';
//import ModuleInGameProgress from './inGameProgress';
import ModuleWinner from './winner';
import '../index.css';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    
  }
  render(){
    let view;
    if(this.props.endGame){
      view = <div className="Screen_Winner"><ComponentLeaderBoard players={this.props.players}></ComponentLeaderBoard><ModuleWinner newGame={this.props.newGame} players={this.props.players} round={this.props.round}/></div>;
    }else{
      view = <ModuleRoundResults removePlayer={this.props.removePlayer} handleNextRound={this.props.handleNextRound} endRound={this.props.endRound} players={this.props.players} round={this.props.round} doodles={this.props.doodles}/>;
    }
    return (
      <Grid className="Screen_Host_Game"
          container
          spacing={0}
          justify="center"
          style={{ minHeight: '100vh' }}
          >
          {view}
      </Grid> 
    )
  }
}
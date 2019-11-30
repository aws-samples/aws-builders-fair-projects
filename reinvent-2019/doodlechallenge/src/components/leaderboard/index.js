import React from 'react';
import { Grid } from '@material-ui/core';
import {getPlayerScore} from '../../helper';
import ComponentLeaderboardItem from './item';
import ComponentLeaderboardEmtpyItem from './emptyItem';
import {MAX_PLAYERS} from '../../constants';
import './index.css';


export default class App extends React.Component {
  getEmptyItemsView(){
    let view = [];
    for(let i = this.props.players.length; i < MAX_PLAYERS; i++){
      view.push(<Grid key={i} item xs={2}><ComponentLeaderboardEmtpyItem/></Grid>);
    }
    return view;
  }
  render (){
    return (
      <Grid container justify="center" className="Leaderboard" spacing={2}>
        {this.props.players && this.props.players.map((player, index) => {
            let totalScore = getPlayerScore(player);
            return (
              <Grid key={player.uuid} item xs={2}>
                <ComponentLeaderboardItem removePlayer={this.props.removePlayer} player={player} score={totalScore}/>
              </Grid>
            )
          })}
          {this.getEmptyItemsView()}
      </Grid>
    );
  }
}
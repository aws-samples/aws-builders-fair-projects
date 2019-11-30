import React from 'react';
import {Typography, Grid, Button} from '@material-ui/core';
import {getScoreLeader} from '../../../helper';
import ComponentPlayer from '../../../components/player';
//import {EVENTS} from '../../../events';
import '../index.css';

export default class Welcome extends React.Component {
  getWinner(players){
    return getScoreLeader(players);
  }
  reloadPage(){
    window.location.reload(false); 
  }
  render (){
    let player = this.getWinner(this.props.players);
    return (
      <Grid className="Screen_Host_Winner"
      container
      spacing={0}
      direction="column"
      alignItems="center"
      justify="center"
      >
        <Grid item xs={12}>
          <Typography variant="h2" component="h2" style={{color:"#FFF", textAlign:"center", paddingBottom:"50px"}}>
            The winner is
          </Typography>
          <div className="Winner_Player"><ComponentPlayer player={player}/></div>
          <Button size="large" variant="contained" color="secondary" onClick={this.reloadPage}>Continue</Button>
        </Grid>
      </Grid>
    );
  }
}
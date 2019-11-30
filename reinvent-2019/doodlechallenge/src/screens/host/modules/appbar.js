import React from 'react';
import { Hub } from 'aws-amplify';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import {MIN_PLAYERS, MAX_PLAYERS} from '../../../constants';
//import {EVENTS} from '../../../events';
import '../index.css';

export default class App extends React.Component {
  render(){
    return(
        <AppBar className="App_Bar" position="static">
        <Toolbar>
        <Grid container spacing={3}>
            <Grid item xs={2}>
            <Button size="medium" variant="contained" onClick={this.props.cancelGame}>Cancel</Button>
            </Grid>
            <Grid item xs={8}>
            <Typography variant="h5" component="h2" style={{textAlign:"center"}}>
                Game Room: <span className="font-legible">{this.props.gameCode}</span>
            </Typography>
            </Grid>
            <Grid item xs={2} style={{textAlign:"right"}}>
              {this.props.players && this.props.players.length >= MIN_PLAYERS && this.props.players.length <= MAX_PLAYERS &&
                <Button size="large" variant="contained" color="secondary" onClick={this.props.startGame}>Start Game</Button>
              }
            </Grid>
        </Grid>
        </Toolbar>
        </AppBar>
    )
  }
}
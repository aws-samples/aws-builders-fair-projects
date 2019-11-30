import React from 'react';
import { Grid } from '@material-ui/core';
import ModuleAppBar from './appbar';
import ModulePlayerList from './playerList';
import ModuleCountDown from './countDown';
import '../index.css';
export default class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      startCountDown: false
    }
  }
  handleStartCountDown(){
    this.setState({
      startCountDown: true
    })
  }
  render(){
    let view;
    if(!this.state.startCountDown){
      view = <Grid item xs={12}><ModuleAppBar startGame={this.handleStartCountDown.bind(this)} cancelGame={this.props.cancelGame} players={this.props.players} gameCode={this.props.gameCode}></ModuleAppBar><ModulePlayerList removePlayer={this.props.removePlayer} players={this.props.players}/></Grid>;
    }else{
      view = <Grid item xs={12}><ModuleCountDown handleCountDown={this.props.startGame}/></Grid>;
    }
    return(
      <Grid className="Screen_Host"
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
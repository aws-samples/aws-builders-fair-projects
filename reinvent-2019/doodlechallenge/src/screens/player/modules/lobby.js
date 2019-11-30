import React from 'react';
import Amplify, { API, Auth, Hub, PubSub, graphqlOperation } from 'aws-amplify';
import {Paper, Typography, Button, Grid, Card, CardContent, TextField} from '@material-ui/core';
import {ReactComponent as AssetBackground} from '../../../assets/backgrounds/Schedule.svg';
import {getPublishOperation} from '../../../helper';
import {PubSubEvents} from '../../../events';
import * as subscriptions from '../../../graphql/subscriptions';
import * as mutations from '../../../graphql/mutations';

import '../index.css';
export default class App extends React.Component{
  constructor(props) {
    super(props);
    this.textInput = React.createRef();
    this.requestMessage = null;
    this.state = {
      gameCode:null,
      error:""
    }
  }
  componentDidMount(){
    //this.listenToMessages();
  }
  componentWillUnmount(){
    //this.unlistenToMessages();
    clearTimeout(this.countDown);
  }
  unlistenToMessages(){
    if(this.subscriptionMessage){
      this.subscriptionMessage.unsubscribe();
      this.subscriptionMessage = null;
    }
  }
  handleJoinGame(){
    let gameCode = this.textInput.current.value;
    if(gameCode === ""){
      window.alert("Please enter a game code");
    }else{
      this.setState((prevState, prop)=>{
        return {gameCode:gameCode.toUpperCase()};
      }, ()=>{
        this.checkGameCode(gameCode.toUpperCase());
      });
    }
  }
  reset(){
    this.setState({gameCode:null, error:"Game room not found"});
  }
  async checkGameCode(gameCode){
    this.props.checkGameCode(gameCode);
    this.countDown = setTimeout(this.reset.bind(this), 4000);
  }

  render(){
    return (
      <Grid className="Lobby"
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: '100vh' }}
        >
        <AssetBackground alt="Doodle Challenge" className="Background"></AssetBackground>
        <Grid item xs={12}>
          <Typography className="Game_Title" variant="h1" component="h1" style={{color:"#FFF", textAlign:"center"}}>
            DOODLE CHALLENGE
          </Typography>
          <Paper className="Welcome_Box">
              <Card>
                <CardContent>
                  <Typography variant="h6" component="h6">
                    Enter Game Code To Join
                  </Typography>
                  {this.state.error !== "" ? (
                  <TextField className="Welcome_Input_Code"
                    id="outlined-full-width"
                    label=""
                    error
                    required
                    placeholder="Game Code"
                    fullWidth
                    label={this.state.error}
                    margin="normal"
                    variant="outlined"
                    inputRef={this.textInput}
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                  ):(
                  <TextField className="Welcome_Input_Code"
                    id="outlined-full-width"
                    label=""
                    required
                    placeholder="Game Code"
                    fullWidth
                    label=""
                    margin="normal"
                    variant="outlined"
                    inputRef={this.textInput}
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                  )}
                  {this.state.gameCode ? (
                    <Button disabled fullWidth={true} size="large" variant="contained" color="primary">
                      Please wait...
                    </Button>
                  ):(
                    <Button fullWidth={true} size="large" variant="contained" color="primary" onClick={this.handleJoinGame.bind(this)} >
                    Join Game
                  </Button>
                  )}
                </CardContent>
                <CardContent className="Button_Host">
                  <Button variant="contained" color="default" onClick={this.props.hostGame} >
                    Host Game
                  </Button>
                </CardContent>
              </Card>
          </Paper>
        </Grid>   

    </Grid> 
    )
  }
}
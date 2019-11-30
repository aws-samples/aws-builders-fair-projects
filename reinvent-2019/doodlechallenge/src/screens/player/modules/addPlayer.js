import React from 'react';
import Amplify, { API, Hub } from 'aws-amplify';
import {Grid, Paper, Button, Card, CardContent, CardActions, Typography, Divider, TextField, Fade} from '@material-ui/core';
import {HubEvents} from '../../../events';
import * as mutations from '../../../graphql/mutations';
import * as queries from '../../../graphql/queries';
import {getAvailableAvatar} from '../../../helper';
import uuid from 'uuidv4';
import '../index.css';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.textInput = React.createRef();
    this.state = {
      playerName:null
    };
  }
  playNow(){
    let playerName = this.textInput.current.value;
    if(playerName === ""){
      window.alert("Please enter your name");
    }else{
      this.setState({playerName:playerName});
    }
  }
  async addPlayerToGame(playerName){
    let playersQuery = await API.graphql({
      query: queries.listPlayers,
      variables: {
        filter: {
          room: { eq: this.props.gameCode }
        }
      },
      authMode: 'AWS_IAM'
    });
    let players = playersQuery.data.listPlayers.items;
    let myDate = new Date();
    let newPlayer = {
      id: uuid(),
      name: playerName,
      room: this.props.gameCode,
      avatar:getAvailableAvatar(players),
      doodles:[],
      createdAt: myDate.toISOString()
    };
    console.log(newPlayer);
    let player = await API.graphql({query:mutations.createPlayer, variables:{input:newPlayer}, authMode: 'AWS_IAM'});
    console.log("Your player, ", player);
    this.props.addedPlayer(player.data.createPlayer);
  }
  componentDidUpdate(){
    if(this.state.playerName){
      this.addPlayerToGame(this.state.playerName);
    }
  }
  cancel(){
    if(window.confirm("Are you sure you want to leave the game?")){
      this.props.cancel();
      //Hub.dispatch(EVENTS.CLEARED_GAME_CODE, { event: 'buttonClick', data: null, message:'' });  
    }
  }
  render(){
    return(
      <Grid className="Screen_Challenger"
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: '100vh', color:'#FFF' }}
        >

          <Paper className="Component-join">
            <Fade in={true}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1">
                  Game Room: <strong>{this.props.gameCode}</strong>
                </Typography>
                <Divider />
                <Divider />
                <br/>
                <Typography variant="h6" component="h6">
                  Enter your name
                </Typography>
                <TextField
                  id="outlined-full-width"
                  label=""
                  required
                  style={{ margin: "8px auto", color: "#FFF" }}
                  placeholder="Your name"
                  fullWidth
                  margin="normal"
                  variant="outlined"
                  inputRef={this.textInput}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </CardContent>
              <CardActions>
              <Grid container spacing={3}>
                <Grid item xs={12} style={{textAlign:"center"}}>
                  <Button style={{marginRight:"5px"}} size="medium" variant="contained" color="default" onClick={this.cancel.bind(this)}>Cancel</Button>
                  {this.state.playerName ? (
                    <Button disabled size="medium" variant="contained" color="primary" onClick={this.playNow.bind(this)}>Please wait</Button>
                  ):(
                    <Button size="medium" variant="contained" color="primary" onClick={this.playNow.bind(this)}>Play Now!</Button>
                  )}
                </Grid>
              </Grid>
              </CardActions>
            </Card>
            </Fade>
        </Paper>
      </Grid>
    )
  }
}
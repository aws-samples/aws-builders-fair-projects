import React from 'react';
import Amplify, { API, Storage } from 'aws-amplify';
import {AppBar, Toolbar, Container, Grid, Paper, Button, Card, CardContent, CardActions, Typography, Divider, TextField, Fade} from '@material-ui/core';
import CanvasDraw from 'react-canvas-draw';
import CompontentsAvatar from '../../../components/avatar';
import * as mutations from '../../../graphql/mutations';
import * as queries from '../../../graphql/queries';
import {getAvailableAvatar, getImageByteData} from '../../../helper';
import { uuid } from 'uuidv4';
import '../index.css';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.textInput = React.createRef();
    this.myAvatar = React.createRef();
    this.state = {
      id:uuid(),
      hasAvatar:false
    };
  }
  componentWillMount(){
    this.interval = setInterval(()=>{
      let doodled = this.myAvatar.current.hasAvatar();
      if(doodled && !this.state.hasAvatar){
        this.setState({hasAvatar:true});
      }else if(!doodled && this.state.hasAvatar){
        this.setState({hasAvatar:false});
      }
    }, 500);
  }
  componentWillUnmount(){
    if(this.interval){
      clearInterval(this.interval);
    }
  }
  playNow(){
    let doodled = this.myAvatar.current.hasAvatar();
    if(!doodled){
      window.alert("Please enter your name");
    }else{
      let imageBytes = getImageByteData("canvas", 0.5);
      let file = "AVATARS/"+this.props.gameCode+'/'+this.state.id+'.jpg';
      this.uploadToS3(file,imageBytes);
    }
  }
  uploadToS3(file,data){
    Storage.put(file, data)
    .then (result => {
      console.log("uploaded");
      console.log(result);
      this.addPlayerToGame(result.key);
      //this.getScore({bytes:data}, result.key);
    }) // {key: "gameid/playerindex.txt"}
    .catch(err => {
      console.log(err)
    });
  }
  async addPlayerToGame(avatar){
    let newPlayer = {
      uuid: this.state.id,
      name: avatar,
      room: this.props.gameCode,
      avatar:this.props.avatar,
      doodles:[]
    };
    //let player = await API.graphql({query:mutations.createPlayer, variables:{input:newPlayer}, authMode: 'AWS_IAM'});
    //console.log("Your player, ", player);
    this.props.addedPlayer(newPlayer);
  }
  componentDidUpdate(){
    if(this.state.playerName){
      this.addPlayerToGame(this.state.playerName);
    }
  }
  clear(){
    this.myAvatar.current.clear();
  }
  cancel(){
    if(window.confirm("Are you sure you want to leave the game?")){
      this.props.cancel();
      //Hub.dispatch(EVENTS.CLEARED_GAME_CODE, { event: 'buttonClick', data: null, message:'' });  
    }
  }
  render(){
    return(
      <Grid className="Screen_Challenger Screen_Hello_MyName"
        container
        spacing={0}
        direction="row"
        alignItems="center"
        justify="center"
        style={{ minHeight: '100vh', color:'#FFF' }}
        >
          <AppBar className="App_Bar_Hello_MyName" position="absolute">
            <Toolbar>
            <Grid container spacing={3} direction="row">
                <Grid item xs={4} style={{textAlign:"left"}}>
                  <Button style={{marginRight:"5px"}} size="small" variant="contained" color="default" onClick={this.cancel.bind(this)}>Quit</Button>
                </Grid>
                <Grid item xs={4}>
                  <Grid container direction="row">
                    <Container align="center">
                      <Typography variant="subtitle1">
                        Game Room: <strong>{this.props.gameCode}</strong>
                      </Typography>
                    </Container>
                  </Grid> 
                </Grid>
                <Grid item xs={4} style={{textAlign:"right"}}>
                  <Button size="small" variant="contained" onClick={this.clear.bind(this)} style={{marginRight:"10px"}}>Clear</Button>&nbsp;
                  {!this.state.hasAvatar ? (
                    <Button disabled size="small" variant="contained" color="primary" alt="Write your name" onClick={this.playNow.bind(this)}>Play Now!</Button>
                  ):(
                    <Button size="small" variant="contained" color="primary" onClick={this.playNow.bind(this)}>Play Now!</Button>
                  )}
                </Grid>
            </Grid>
            </Toolbar>
          </AppBar>
          <CompontentsAvatar color={this.props.avatar} ref={this.myAvatar}/>
      </Grid>
    )
  }
}
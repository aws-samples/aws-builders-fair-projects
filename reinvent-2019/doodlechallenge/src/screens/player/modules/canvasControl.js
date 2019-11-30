import React from 'react';
import {Button, Grid, Typography, AppBar, Container, Toolbar} from '@material-ui/core';
import { S3Image } from 'aws-amplify-react';
import '../index.css';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      done:false
    }
  }
  formatTime(d){
    d = Number(d);
    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);

    //var hDisplay = h < 10 ? "0"+h+":" : h+":";
    var mDisplay = m < 10 ? "0"+m+":" : m+":";
    var sDisplay = s < 10 ? "0"+s : s;
    return  mDisplay + sDisplay; 
  }
  handleDone(){
    this.setState(()=>{
      return {
        done:true
      }
    }, ()=>{
      this.props.done();
    })
  }
  render(){
    let formattedTime = this.formatTime(this.props.time);
    return (
      <AppBar className="App_Bar" position="fixed" style={{backgroundColor:"#282c34"}}>
        <Toolbar>
        <Grid container spacing={3} direction="row">
            <Grid item xs={4} style={{textAlign:"left"}} className="Player_Draw_App_Bar">
              <S3Image className="InGame_Image" imgKey={this.props.player.name} />
              <Typography className="App_Bar_Title" variant="body1">Draw {this.props.draw}</Typography>  
            </Grid>
            <Grid item xs={4}>
              <Grid container direction="row">
                <Container align="center">
                  <Typography display="inline" align="left" style={{ color: '#FFF'}}>Time:&nbsp;</Typography>  
                  <Typography className={(this.props.time<=5)? "Draw_Timer expiring":"Draw_Timer"} component="div" display="inline">
                    {formattedTime}
                  </Typography>
                </Container>
              </Grid> 
            </Grid>
            <Grid item xs={4} style={{textAlign:"right"}}>
              <Button size="small" variant="contained" onClick={this.props.clear} style={{marginRight:"10px"}}>Clear</Button>&nbsp;
              {this.state.done ? (
                <Button size="small" disabled variant="contained">Done</Button>
              ):(
                <Button size="small" color="primary" variant="contained" onClick={this.handleDone.bind(this)}>Done</Button>
              )}
            </Grid>
        </Grid>
        </Toolbar>
      </AppBar>
    );
  }
}


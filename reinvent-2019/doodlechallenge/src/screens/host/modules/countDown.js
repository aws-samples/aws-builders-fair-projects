import React from 'react';
import { Hub } from 'aws-amplify';
import { Grid, Typography, Fade } from '@material-ui/core';

import '../index.css';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        ticktock:5
    };
  }
  componentWillUnmount(){
    if(this.timer){
      clearInterval(this.timer);
    }
  }
  componentDidMount(){
    this.timer = setInterval(
      () => this.countDown(),
      1000
    );
  }
  countDown(){
    this.setState({
      ticktock: this.state.ticktock-1
    });
    if(this.state.ticktock === 0){
      clearInterval(this.timer);
      this.props.handleCountDown();
      //Hub.dispatch(EVENTS.START_GAME, { event: 'buttonClick', data: null, message:'' });
    }
  }
  
  render(){
    return(
      <Grid className="Screen_CountDown"
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: '100vh', color:'#FFF' }}
        >
          <Grid item xs={12}>
            <Fade in={true}>
            <Typography variant="subtitle1" gutterBottom>
              Get Ready!!!
              <br/>
              {this.state.ticktock}
            </Typography>
            </Fade>
          </Grid>
      </Grid> 
    )
  }
}
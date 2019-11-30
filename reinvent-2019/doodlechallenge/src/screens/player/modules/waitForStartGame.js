import React from 'react';
import {Grid, Typography, Fade } from '@material-ui/core';
import '../index.css';

export default class App extends React.Component {
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
          <Grid item xs={6}>
            <Fade in={true}>
            <Typography variant="subtitle1" gutterBottom>
              <br/>
              Waiting for host to start the game
            </Typography>
            </Fade>
          </Grid>
      </Grid> 
    )
  }
}
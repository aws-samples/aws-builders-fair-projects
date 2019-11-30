import React from 'react';
import {Typography, Grid, Button} from '@material-ui/core';
import ComponentPlayer from '../../../components/player';

import '../index.css';

export default class App extends React.Component {
  reloadPage(){
    window.location.reload(false); 
  }
  render(){
    return (
      <Grid className="Screen_Challenger_Winner"
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justify="center"
          style={{ minHeight: '100vh' }}
          >
          <Grid item xs={12}>
            <Typography variant="h4" component="h4" style={{color:"#FFF", textAlign:"center"}}>
              The winner is
            </Typography>
            <div className="Winner_Player">
              <ComponentPlayer player={this.props.player}/>
              <Button size="large" variant="contained" color="secondary" onClick={this.reloadPage}>Continue</Button>
            </div>
          </Grid>   

      </Grid> 
    );
  }
}


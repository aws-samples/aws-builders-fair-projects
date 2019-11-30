import React from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import LinearProgress from '@material-ui/core/LinearProgress';

import '../index.css';

export default class App extends React.Component {
  
  render(){
    return (
      <Grid className="Screen_Challenger_Loading"
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justify="center"
          style={{ minHeight: '100vh' }}
          >
          <Grid item xs={12}>
            <Typography variant="h4" component="h4" style={{color:"#FFF", textAlign:"center"}}>
              Great job!
            </Typography>
            <Typography variant="h4" component="h4" style={{color:"#FFF", textAlign:"center"}}>
              Waiting for other players to tally up the score!
            </Typography>
            <br/>
            <LinearProgress />
          </Grid>   

      </Grid> 
    );
  }
}


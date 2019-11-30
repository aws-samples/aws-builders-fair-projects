import React from 'react';
import { Button, Grid, Typography, Container } from '@material-ui/core';
import {ReactComponent as AssetBackground} from '../../../assets/backgrounds/Schedule.svg';
import {DRAWTIME} from '../../../constants';
import '../index.css';
export default class App extends React.Component{
  constructor(props) {
    super(props);
  }
  render(){
    return(
      <Grid className="Screen_Host"
            container
            spacing={0}
            direction="column"
            alignItems="center"
            justify="center"
            style={{ minHeight: '100vh' }}
            >
            <AssetBackground className="Background"></AssetBackground>
            <Grid item xs={12}>
              <Typography className="Game_Title" variant="h1" component="h1" style={{color:"#FFF", textAlign:"center"}}>
                DOODLE CHALLENGE
              </Typography>
              <Typography variant="h4" component="h4" style={{color:"#FFF", textAlign:"center"}}>
                Compete to see who can doodle better!
              </Typography>
              <br/>
              <Typography variant="h4" component="h4" style={{color:"#FFF", textAlign:"center"}}>
                Your doodles will be ranked using Machine Learning!
              </Typography>
              <br/>
              <Container style={{textAlign:"center"}}>
                <Button variant="contained" color="primary" onClick={this.props.createGame} >
                  Let's Begin
                </Button>
              </Container>
            </Grid>   

        </Grid> 
    )
  }
}
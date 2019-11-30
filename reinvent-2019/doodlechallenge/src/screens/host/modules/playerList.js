import React from 'react'
import {Grid, Typography, Container, Zoom, Paper, Card, CardContent} from '@material-ui/core';
import ComponentPlayer from '../../../components/player';
import {MAX_PLAYERS} from '../../../constants';
export default class App extends React.Component {
  removePlayer(player){
    if(window.confirm("Are you sure you want to remove this player?")){
      this.props.removePlayer(player);
    }
  }
  renderPlayers(){
    let view = [];
    for(let i = 0; i < MAX_PLAYERS; i++){
      if(this.props.players && this.props.players[i]){
        let player = this.props.players[i];
        view.push(
            <Grid className="Host_Player_List_Item" key={i} item xs={4}>
              <Paper className="Host_Player_List_Paper">
                <Card>
                  <CardContent>
                    <Container style={{textAlign:"center"}}>
                      <button className="button-remove" onClick={()=>{this.removePlayer(player);}}>X</button>
                      <ComponentPlayer player={player}/>
                    </Container>
                  </CardContent>
                </Card>
              </Paper>
            </Grid>
        );
      }else{
        view.push(
          <Grid key={i} className="Host_Player_List_Item Empty" item xs={4}>
            <Paper className="Host_Player_List_Paper">
              <Card>
                <CardContent>
                  <Container style={{textAlign:"center"}}>
                    <Typography variant="body1">
                      Waiting for player to join
                    </Typography>
                  </Container>
                </CardContent>
              </Card>
            </Paper>
          </Grid>
        );
      }
    }
    return view;
  }
  render() {
    return (
      <Grid
        container
        spacing={0}
        direction="row"
        alignItems="center"
        justify="center"
        className="Host-PlayerList"
        >
          <Container>
            <Typography variant="h3" component="h2" style={{color:"#FFF", textAlign:"center"}}>Enter game room and your name on your device</Typography>
          </Container>
          {this.renderPlayers()}
      </Grid>
    )
  }
}
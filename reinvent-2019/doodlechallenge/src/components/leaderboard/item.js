import React from 'react';
import Paper from '@material-ui/core/Paper';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { S3Image } from 'aws-amplify-react';
import IconButton from '@material-ui/core/IconButton';
import HighlightOffIcon from '@material-ui/icons/HighlightOff';

import './index.css';


export default class App extends React.Component {
  render (){
    
    return (
      <Card className={"Component-Player"}>
        <CardContent>
          <Container style={{textAlign:"center"}}>
            <IconButton onClick={()=>{ if(this.props.removePlayer) {this.props.removePlayer(this.props.player);}}} className="button-remove" color="primary" aria-label="upload picture" component="span">
              <HighlightOffIcon></HighlightOffIcon>
            </IconButton>
            <Paper className="Avatar_Container">
              <Card className="Avatar_Card" style={{backgroundColor:this.props.player.avatar}}>
                <CardContent className="Avatar_Content_Title">
                  <Typography variant="subtitle2">
                    HELLO
                  </Typography>
                  <Typography variant="body1">
                    my name is
                  </Typography>
                </CardContent>
                <CardContent className="Avatar_Content_Canvas">
                  <S3Image className="InGame_Image" imgKey={this.props.player.name} />
                </CardContent>
                <CardContent className="Avatar_Content_Score">
                  <Typography variant="body1">
                    Points: {this.props.score}
                  </Typography>
                </CardContent>
              </Card>
            </Paper>
          </Container>
        </CardContent>
      </Card>
    );
  }
}
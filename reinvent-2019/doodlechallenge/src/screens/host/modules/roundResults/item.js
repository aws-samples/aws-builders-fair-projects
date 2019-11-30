import React from 'react';
import {Paper, Card, CardContent, Container, Typography, Grid, Zoom, Grow} from '@material-ui/core';
import {ReactComponent as AssetBackground} from '../../../../assets/icons/medal_stars.svg';
import { S3Image } from 'aws-amplify-react';
import {getFormattedScore} from '../../../../helper';
import './index.css';

export default class Welcome extends React.Component {
  render (){
    let doodleView;
    if(this.props.doodle){
      doodleView = <Container className="challenger_doodle_container">
        <S3Image className="InGame_Image" imgKey={this.props.doodle.url} />
        <Typography variant="h6" className="InGame_Score" gutterBottom>Score: {getFormattedScore(this.props.doodle.score)}</Typography>
        </Container>
    }
    let winnerView;
    if(this.props.winner && this.props.doodle && this.props.doodle.score > 0){
      winnerView = <Container className="InGame_Player_Winner" style={{textAlign:"center"}}>
      <AssetBackground></AssetBackground>
      <Typography variant="h4" style={{textAlign:"center"}} gutterBottom>
        WINNER!
      </Typography>
    </Container>
    }
    let winnerClass = "InGame_Grow";
    if(this.props.winner && this.props.doodle && this.props.doodle.score > 0){
      winnerClass += " winner";
    }else if(this.props.doodle){
      winnerClass += " has-doodled";
    }
    
    let alsoLooksLike;
    if(this.props.doodle && this.props.doodle.labels){
      let labels = this.props.doodle.labels.map((label, index) =>{
        return label.name
      });
      alsoLooksLike = <Typography variant="body1" className="InGame_Label" gutterBottom>This also looks like: <b>{labels.join(", ")}</b></Typography>
    }
    return (
      <Zoom in={this.props.show} timeout={100}>
        <div className={"InGame_Grow "+winnerClass}>
          <Paper className={"InGameProgressPlayer "+winnerClass}>
            <Card>
              <CardContent className="InGameProgress_CardContent">
                <Container className="InGame_Player_Image" style={{textAlign:"center", borderColor:this.props.player.avatar}}>
                  <S3Image className="InGame_Image" imgKey={this.props.player.name} />
                </Container>
                {doodleView}

                {alsoLooksLike}
              </CardContent>
            </Card>
          </Paper>
          {winnerView}
        </div>
      </Zoom>
    );
  }
}
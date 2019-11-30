import React from 'react';
import {Paper, Card, CardContent, Container, Typography, Grid, Zoom, Grow} from '@material-ui/core';
import {ReactComponent as AssetBackground} from '../../../assets/icons/medal_stars.svg';
import ComponentPlayer from '../../../components/player';
import { S3Image } from 'aws-amplify-react';
import {AVATARS} from '../../../constants';
import {DOODLES} from '../../../constants';
import '../index.css';

export default class Welcome extends React.Component {
  constructor(props) {
    super(props);
    //this.finishRound = this.finishRound.bind(this);
    this.myCanvas = React.createRef();
    
  }
  
  componentDidMount(){
    document.addEventListener("keydown", this._handleKeyDown);
  }
  componentWillUnmount(){
    document.removeEventListener("keydown", this._handleKeyDown);
  }
  render (){
    let doodleView;
    if(this.props.doodle){
      doodleView = <Container className="challenger_doodle_container">
        <S3Image className="InGame_Image" imgKey={this.props.doodle.url} />
        <Typography variant="h6" className="InGame_Score" gutterBottom>Score: {this.props.doodle.score}</Typography>
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
    console.log("rendering ingameprogress player: ",this.props.player.avatar);
    return (
      <div className={"InGame_Grow "+winnerClass}>
        <Paper className={"InGameProgressPlayer "+winnerClass}>
          <Card>
            <CardContent className="InGameProgress_CardContent">
              <Container className="InGame_Player_Image" style={{textAlign:"center", borderColor:this.props.player.avatar}}>
                <S3Image className="InGame_Image" imgKey={this.props.player.name} />
              </Container>
              {doodleView}
            </CardContent>
          </Card>
        </Paper>
        {winnerView}
      </div>
    );
  }
}
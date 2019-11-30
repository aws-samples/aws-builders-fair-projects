import React from 'react';
import {Paper, Card, CardContent, Typography, Fade} from '@material-ui/core';
import CanvasDraw from 'react-canvas-draw';
import './index.css';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.myCanvasDraw = React.createRef();
  }
  clear(){
    this.myCanvasDraw.current.clear();
  }
  hasAvatar(){
    let drawing = JSON.parse(this.myCanvasDraw.current.getSaveData());
    return drawing.lines.length > 0;
  }
  render(){
    let styles = {};
    if(this.props.color){
      styles = {
        backgroundColor: this.props.color
      }
    }
    return(
      <Fade in={true}>
        <Paper className="Avatar_Container">
          <Card className="Avatar_Card" style={styles}>
            <CardContent className="Avatar_Content_Title">
              <Typography variant="h2">
                HELLO
              </Typography>
              <Typography variant="h6" component="h6">
                my name is
              </Typography>
            </CardContent>
            <CardContent className="Avatar_Content_Canvas">
              <CanvasDraw className="Avatar_Canvas" ref={this.myCanvasDraw} lazyRadius={0} brushRadius={5} hideGrid={true} catenaryColor="#FFFFFF" brushColor="#000000" canvasWidth="100%" canvasHeight="100%"/>    
            </CardContent>
          </Card>
        </Paper>
      </Fade>
    )
  }
}
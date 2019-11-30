import React from 'react';
import Amplify, { API, Storage, Predictions, PubSub } from 'aws-amplify';
import ModuleCanvas from './canvas';
import ModuleLoading from './loading';
import ModuleWinner from './winner';
import {DRAWTIME, DOODLES} from '../../../constants';
import {getImageByteData} from '../../../helper';
import {PubSubEvents} from '../../../events';
import * as mutations from '../../../graphql/mutations';
import { AmazonAIPredictionsProvider } from '@aws-amplify/predictions';
import './index.css';

Amplify.addPluggable(new AmazonAIPredictionsProvider());
export default class App extends React.Component {
  constructor(props) {
    super(props);
    //this.finishRound = this.finishRound.bind(this);
    this.myCanvas = React.createRef();
    this.state = {
      time:DRAWTIME,
    };
  }
  componentDidMount(){
    console.log("Game: Comp did mount");
    this.startTimer();
    //Hub.listen(EVENTS.FINISHED_DRAWING, this.finishRound);
  }
  componentDidUpdate(prevProps) {
    if(prevProps.doodle && this.props.doodle && prevProps.doodle.object !== this.props.doodle.object){
      this.startTimer();
    }
  }
  startTimer(){
    if(this.timer){
      clearInterval(this.timer);
    }
    this.timer = setInterval(() => this.countDown(),1000);
  }
  countDown(){
    let myRemaining = this.state.time-1;
    if(myRemaining === 0){
      this.finishRound();
    }else{
      this.setState({ time: myRemaining });
    }
  }
  finishRound(){
    console.log("finished Round");
    clearInterval(this.timer);
    let imageBytes = getImageByteData("canvas", 0.5); //this.myCanvas.current.getImageByteData(0.5);
    let file = "doodles/"+this.props.doodle.object.toLocaleLowerCase()+"/"+this.props.player.room+'_'+this.props.player.uuid+'.jpg';
    this.uploadToS3(file,imageBytes);
    //this.uploadToAPI(imageBytes);
  }
  // async uploadToAPI(data){
  //   let myDoodle = DOODLES[this.props.round].object.toLocaleLowerCase();
  //   let drawing = await API.graphql({query:mutations.createDrawing, variables:{name:myDoodle, imageData:data}, authMode: 'AWS_IAM'});
  //   console.log("I've called the new API");
  //   console.log(drawing);
  //   //this.props.addedPlayer(player.data.createPlayer);
  // }
  uploadToS3(file,data){
    Storage.put(file, data)
    .then (result => {
      this.props.handleFinishedDrawing();
      this.setState({time:DRAWTIME});
      //this.getScore({bytes:data}, result.key);
    }) // {key: "gameid/playerindex.txt"}
    .catch(err => {
      window.alert("Failed to upload doodle: ", err);
      console.log(err)
    });
  }
  render(){
    let view;
    if(this.props.winner){
      view = <ModuleWinner player={this.props.winner}/>;
    }else if(this.props.roundEnded){
      view = <ModuleLoading/>;
    }else{
      view = <ModuleCanvas ref={this.myCanvas} finishRound={this.finishRound.bind(this)} time={this.state.time} player={this.props.player} doodle={this.props.doodle}/>
    }
    return(
      <div>
        {view}
      </div>
    )
  }
}
import React from 'react';
import Amplify, { Hub, API } from 'aws-amplify';
import { Container } from '@material-ui/core';
import ScreenHost from './screens/host';
import ScreenPlayer from './screens/player';
import './App.css';
import awsconfig from './aws-exports';
import * as subscriptions from './graphql/subscriptions';
import {HubEvents} from './events';

Amplify.configure(awsconfig);

export default class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      player:true
    }
    Hub.listen(HubEvents.BECOME_PLAYER,(data) => {
      this.playGame();
    })
  }
  
  componentDidMount(){
    //window.LOG_LEVEL = 'DEBUG';
    document.title = 'Doodle Challenge';
    this.listenToMessages();
  }
  componentWillUnmount(){
    if(this.subscriptionMessage){
      this.subscriptionMessage.unsubscribe();
      this.subscriptionMessage = null;
    }
  }
  listenToMessages(){
    this.subscriptionMessage = API.graphql({
      query: subscriptions.onCreateGameMessage,
      variables: null,
      authMode: 'AWS_IAM'
    }).subscribe({
      next: event => {
        if (event){
          let payload = event.value.data.onCreateGameMessage;
          Hub.dispatch(payload.action, {
            id: payload.id,
            room: payload.room,
            message: payload.message,
            data: payload.data ? JSON.parse(payload.data): payload.data,
            createdAt: payload.createdAt
          });
        }
      },
      error: error =>{
        console.log("subscription main error, will resubscribe:", error);
        this.subscriptionMessage.unsubscribe();
        this.listenToMessages();
      },
      complete: data=>{
        console.log("subscription main complete will resubscribe:",data);
        this.subscriptionMessage.unsubscribe();
        this.listenToMessages();
      }
    });
  }
  hostGame(){
    this.setState({player:false});
  }
  playGame(){
    this.setState({player:true});
  }
  render(){
    return (
      <Container fixed={true} className="App">
        {this.state.player ? <ScreenPlayer hostGame={this.hostGame.bind(this)}/>:<ScreenHost playGame={this.playGame.bind(this)}/>}
      </Container>
    );
  }
}

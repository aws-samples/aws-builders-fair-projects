import React from 'react';
import Amplify, { API, Auth, Hub, PubSub, Cache, graphqlOperation } from 'aws-amplify';
import { Container } from '@material-ui/core';
import ModuleLobby from './modules/lobby';
import ModuleAddPlayer from './modules/addPlayerCanvas';
import ModuleWaitForStartGame from './modules/waitForStartGame';
import ModuleGame from './modules/game';
import {PubSubEvents} from '../../events'; 
import * as mutations from '../../graphql/mutations';
import './index.css';
export default class App extends React.Component{
  constructor(props) {
    super(props);
    this.requestMessage = null;
    this.handleBrowserLeaving = this.handleBrowserLeaving.bind(this);
    this.handleCancelGame = this.handleCancelGame.bind(this);
    this.handleGameCodeCheckFail = this.handleGameCodeCheckFail.bind(this);
    this.handleGameCodeCheckSuccess = this.handleGameCodeCheckSuccess.bind(this);
    this.handleRemoveFromGame = this.handleRemoveFromGame.bind(this);
    this.handleStartGame = this.handleStartGame.bind(this);
    this.handleNextRound = this.handleNextRound.bind(this);
    this.handleEndGame = this.handleEndGame.bind(this);
    this.handleNewGame = this.handleNewGame.bind(this);

    this.state = {
      gameCode:null,
      avatar:null,
      player:null,
      startGame:false,
      doodle:null,
      roundEnded:false,
      winner:null,
      gameCodeError:false
    }
  }
  componentDidMount(){
    this.addListeners();
    window.addEventListener('beforeunload', this.handleBrowserLeaving);
  }
  componentWillUnmount(){
    this.removeListeners();
    window.removeEventListener('beforeunload', this.handleBrowserLeaving);
  }
  addListeners(){
    Hub.listen(PubSubEvents.CANCEL_GAME, this.handleCancelGame);
    Hub.listen(PubSubEvents.RESPOND_GAME_CODE_CHECK_SUCCESS, this.handleGameCodeCheckSuccess);
    Hub.listen(PubSubEvents.RESPOND_GAME_CODE_CHECK_FAIL, this.handleGameCodeCheckFail);
    Hub.listen(PubSubEvents.REMOVE_FROM_GAME, this.handleRemoveFromGame);
    Hub.listen(PubSubEvents.START_GAME, this.handleStartGame);
    Hub.listen(PubSubEvents.NEXT_ROUND, this.handleNextRound);
    Hub.listen(PubSubEvents.END_GAME, this.handleEndGame);
    Hub.listen(PubSubEvents.NEW_GAME, this.handleNewGame);
  }
  removeListeners(){
    Hub.remove(PubSubEvents.CANCEL_GAME, this.handleCancelGame);
    Hub.remove(PubSubEvents.RESPOND_GAME_CODE_CHECK_SUCCESS, this.handleGameCodeCheckSuccess);
    Hub.remove(PubSubEvents.RESPOND_GAME_CODE_CHECK_FAIL, this.handleGameCodeCheckFail);
    Hub.remove(PubSubEvents.REMOVE_FROM_GAME, this.handleRemoveFromGame);
    Hub.remove(PubSubEvents.START_GAME, this.handleStartGame);
    Hub.remove(PubSubEvents.NEXT_ROUND, this.handleNextRound);
    Hub.remove(PubSubEvents.END_GAME, this.handleEndGame);
    Hub.remove(PubSubEvents.NEW_GAME, this.handleNewGame);
  }
  async handleBrowserLeaving(event){
    if(this.state.player){
      let message = {
        room: this.state.gameCode,
        action: PubSubEvents.LEAVE_GAME,
        data: JSON.stringify(this.state.player)
      };
      this.requestGameCodeCheck = await API.graphql({query:mutations.createGameMessage, variables:{input: message}, authMode: 'AWS_IAM' });
    }
  }

  // Host removed player from game
  handleRemoveFromGame(data){
    const payload = data.payload;
    if(payload.data && payload.data.player && this.state.player){
      if(payload.data.player.uuid === this.state.player.uuid){
        console.log("handle remove from game: ",payload);
        if(payload.message){
          window.alert(payload.message);
        }
        this.exitGame();
      }
    }
  }

  // Host Cancelled the game
  handleCancelGame(data){
    const payload = data.payload;
    if(payload.room === this.state.gameCode){
      this.exitGame();
    }
  }

  // No game exist or the game is full
  handleGameCodeCheckFail(data){
    if(this.requestGameCodeCheck){
      const payload = data.payload;
      const request = this.requestGameCodeCheck.data.createGameMessage;
      if(payload.data && payload.data.messageId && request.id === payload.data.messageId){
        window.alert(payload.message);
        this.setState({gameCodeError:true});
      }
    }
  }
  
  // Gamecode is valid and has room for players. Play on!
  handleGameCodeCheckSuccess(data){
    if(this.requestGameCodeCheck){
      const payload = data.payload;
      const request = this.requestGameCodeCheck.data.createGameMessage;
      if(payload.data && payload.data.messageId && request.id === payload.data.messageId){
        this.setState({
          gameCode:payload.room,
          avatar:payload.data.avatar,
          gameCodeError:false
        })
      }
    }
  }

  // Game started. Lets get it going.
  handleStartGame(data){
    const payload = data.payload;
    if(payload.room === this.state.gameCode){
      const doodles = payload.data.doodles;
      const doodle = payload.data.doodle;
      this.setState({startGame:true, doodle:doodle});
    }
  }

  // Host started new round in the game.
  handleNextRound(data){
    const payload = data.payload;
    if(payload.room === this.state.gameCode){
      const doodle = payload.data.doodle;
      this.setState({
        doodle:doodle,
        roundEnded:false
      })
    }
  }

  // Host ended the game
  handleEndGame(data){
    const payload = data.payload;
    if(payload.room === this.state.gameCode){
      const player = payload.data.winner;
      this.setState({winner:player});
    }
  }

  // Host wants to play a new game
  handleNewGame(data){
    const payload = data.payload;
    const gameCode = payload.data.gameCode;
    const oldGameCode = payload.data.oldGameCode;
    if(this.state.gameCode && this.state.gameCode === oldGameCode){
      this.setState((prevState, props) => {
        return {
          gameCode:gameCode,
          player:null,
          startGame:false,
          doodle:null,
          roundEnded:false,
          winner:null
        }
      }, ()=>{
        //console.log("removing listeners");
        // this.removeListeners();
  
        // // Due to amplify issue with unsub to sub, we need to patch the race condition by using a settime
        // //https://github.com/aws-amplify/amplify-js/issues/4064
        // setTimeout( async()=>{
        //   this.addListeners(gameCode);
        // }, 1000);
      })
    }
  }

  // Send message to hosts to confirm gamecode exists.
  // If it does exist a new message will be sent and need to match against the caller so not every client responds but only the callee.
  async checkGameCode(gameCode){
    let message = {
      room: gameCode.toUpperCase(),
      action: PubSubEvents.REQUEST_GAME_CODE_CHECK,
      createdAt: new Date().toISOString()
    };
    this.requestGameCodeCheck = await API.graphql({query:mutations.createGameMessage, variables:{input: message}, authMode: 'AWS_IAM' });
  }
  
  // Send a request to the host to join the game.
  async addedPlayer(player){
    let message = {
      room: this.state.gameCode,
      action: PubSubEvents.CHALLENGER_JOIN,
      data:JSON.stringify(player)
    };  
    await API.graphql({query:mutations.createGameMessage, variables:{input: message}, authMode: 'AWS_IAM' });
    this.setState({player:player});
  }
  exitGame(){
    this.setState({gameCode:null, avatar:null, player:null, startGame:false, winner:null});
  }
  
  handleFinishedDrawing(){
    this.setState({roundEnded:true});
  }
  render(){
    let view;
    if(this.state.gameCode && this.state.player && this.state.startGame){
      view = <ModuleGame winner={this.state.winner} handleFinishedDrawing={this.handleFinishedDrawing.bind(this)} roundEnded={this.state.roundEnded} doodle={this.state.doodle} gameCode={this.state.gameCode} player={this.state.player}/>
    }else if(this.state.gameCode && !this.state.player && !this.state.startGame){
      view = <ModuleAddPlayer addedPlayer={this.addedPlayer.bind(this)} cancel={this.exitGame.bind(this)} avatar={this.state.avatar} gameCode={this.state.gameCode}/>
    }else if(this.state.gameCode && this.state.player && !this.state.startGame){
      view = <ModuleWaitForStartGame player={this.state.player} gameCode={this.state.gameCode}/>
    }else{
      view = <ModuleLobby checkGameCode={this.checkGameCode.bind(this)} hostGame={this.props.hostGame}/>
    }
    return (
      <Container className="Screen_Player">
      {view}
      </Container>
    )
  }
}
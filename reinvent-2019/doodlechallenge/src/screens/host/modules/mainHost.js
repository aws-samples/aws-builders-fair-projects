import React from 'react';
import { API, Hub, PubSub, graphqlOperation } from 'aws-amplify';
import { Grid, Container } from '@material-ui/core';
import {ReactComponent as AssetBackground} from '../../../assets/backgrounds/Schedule.svg';
import ModuleIntro from './intro';
import ModuleLobby from './lobby';
import ModuleGame from './game';
import * as mutations from '../../../graphql/mutations';
import {PubSubEvents} from '../../../events';
import { ROUNDS_PER_GAME, AVATARS, MAX_PLAYERS, getRandomDoodles} from '../../../constants';
import {isRoundCompleted, getScoreLeader, getGameCode, getPlayerNumber} from '../../../helper';
import '../index.css';
export default class App extends React.Component{
  constructor(props) {
    super(props);
    this.responseToGameChecks = 0;
    this.handleRespondToGameRoomCheck = this.handleRespondToGameRoomCheck.bind(this);
    this.handlePlayersJoining = this.handlePlayersJoining.bind(this);
    this.handlePlayersLeaving = this.handlePlayersLeaving.bind(this);
    this.handleSubmittedDoodles = this.handleSubmittedDoodles.bind(this);
    this.state = {
      gameCode:null,
      players:[],
      round:0,
      doodles: [],
      maxRounds:ROUNDS_PER_GAME,
      //maxRounds:1,
      startGame:false,
      endRound:false,
      endGame:false
    }
    
  }
  componentDidMount(){
    this.addListeners();
  }
  componentDidUpdate(prevProps, prevState){
    //this.addListeners();
  }
  componentWillUnmount(){
    this.removeListeners();
  }
  addListeners(){
    Hub.listen(PubSubEvents.REQUEST_GAME_CODE_CHECK, this.handleRespondToGameRoomCheck);
    Hub.listen(PubSubEvents.CHALLENGER_JOIN, this.handlePlayersJoining);
    Hub.listen(PubSubEvents.LEAVE_GAME, this.handlePlayersLeaving);
    Hub.listen(PubSubEvents.SUBMIT_DOODLE, this.handleSubmittedDoodles);
  }
  removeListeners(){
    Hub.remove(PubSubEvents.REQUEST_GAME_CODE_CHECK, this.handleRespondToGameRoomCheck);
    Hub.remove(PubSubEvents.CHALLENGER_JOIN, this.handlePlayersJoining);
    Hub.remove(PubSubEvents.LEAVE_GAME, this.handlePlayersLeaving);
    Hub.remove(PubSubEvents.SUBMIT_DOODLE, this.handleSubmittedDoodles);
  }
  
  // Players left. Either by quiting or their browser closing.
  handlePlayersLeaving(data){
    let player = data.payload.data;
    
    let playerIndex = getPlayerNumber(this.state.players, player);
    if(playerIndex !== null){
      let players = this.state.players;
      players.splice(playerIndex,1);
      this.setState({players:players});
    }
  }

  // New players joined the game. This happens after the signed their hello my name card.
  // We can block them from joining if we already have a max amount.
  async handlePlayersJoining(data){
    const payload = data.payload;
    if(payload.room === this.state.gameCode){
      let player = payload.data;
      if(this.state.players.length < MAX_PLAYERS){
        let players = this.state.players;
        players.push(player);
        this.setState({players:players});
      }else{
        let message = {
          room:this.state.gameCode,
          action: PubSubEvents.REMOVE_FROM_GAME,
          data: JSON.stringify({player:player, messageId: payload.id}),
          message: "The room is full"
        };
        await API.graphql({query:mutations.createGameMessage, variables:{input: message}});
      }
    }
  }

  // A player submitted their doodle. Lets store it and check if all players are done.
  handleSubmittedDoodles(data){
    const payload = data.payload;
    if(payload.room === this.state.gameCode){
      let players = this.state.players;
      const playerUUID = payload.data.playerUUID;
      const doodle = {score:payload.data.score, url:payload.data.url, labels:payload.data.topLabels};
      players = players.map((p, i) =>{
        if(p.uuid === playerUUID){
          p.doodles.push({
            name: this.state.doodles[this.state.round].object,
            score: doodle.score,
            url: doodle.url,
            labels: doodle.labels
          });
        }
        return p;
      });
      
      if(isRoundCompleted(players, this.state.round)){
        this.setState({
          players: players,
          endRound:true
        });
      }else{
        this.setState({
          players: players,
          endRound:false
        });
      }
    }
  }

  // New players want to check for the game room.
  // Only verify if the room matches current game and less than max allowed players.
  async handleRespondToGameRoomCheck(data){
    let payload = data.payload;
    let gameCode = payload.room;
    if(gameCode == this.state.gameCode){
      let avatarColor = AVATARS[this.responseToGameChecks];
      let message = {
        room: gameCode,
        action: PubSubEvents.RESPOND_GAME_CODE_CHECK_SUCCESS,
        data: JSON.stringify({avatar:avatarColor, messageId: payload.id})
      };
      if(this.state.players.length < MAX_PLAYERS){
        this.responseToGameChecks++;
        if(this.responseToGameChecks >= AVATARS.length-1){
          this.responseToGameChecks = 0;
        }
      }
      else{
        message.action = PubSubEvents.RESPOND_GAME_CODE_CHECK_FAIL;
        message.message = "The room is full";
      }
      await API.graphql({query:mutations.createGameMessage, variables:{input: message}});
    }
  }
  createGame(){
    this.setState({
      gameCode: getGameCode()
    });
  }
  async saveGame(){
    let game = {
      room: this.state.gameCode,
      players: this.state.players
    }
    let savedGame = await API.graphql({query:mutations.createGame, variables:{input:game}});
  }
  async endGame(){
    let winner = getScoreLeader(this.state.players);
    this.saveGame();

    let message = {
      room: this.state.gameCode,
      action: PubSubEvents.END_GAME,
      data: JSON.stringify({winner:winner})
    };
    await API.graphql({query:mutations.createGameMessage, variables:{input: message}});
    this.setState({round:0, endRound:true, endGame:true});
  }
  async cancelGame(){
    let message = {
      room: this.state.gameCode,
      action: PubSubEvents.CANCEL_GAME
    };
    await API.graphql({query:mutations.createGameMessage, variables:{input: message}});
    this.responseToGameChecks = 0;
    this.setState({gameCode:null, players:[], round:0, startGame:false, endGame:false, endRound:true});
  }
  async startGame(){
    let doodles = getRandomDoodles(ROUNDS_PER_GAME);
    let message = {
      room: this.state.gameCode,
      action: PubSubEvents.START_GAME,
      data: JSON.stringify({doodles:doodles, doodle:doodles[this.state.round]})
    };
    await API.graphql({query:mutations.createGameMessage, variables:{input: message}});
    this.setState({startGame:true, endRound:false, doodles:doodles});
  }
  async handleNextRound(){
    let nextRound = this.state.round + 1;
    if(nextRound >= this.state.maxRounds){
      // No more rounds
      this.endGame();
    }else{
      let message = {
        room: this.state.gameCode,
        action: PubSubEvents.NEXT_ROUND,
        data: JSON.stringify({doodle:this.state.doodles[nextRound]})
      };
      await API.graphql({query:mutations.createGameMessage, variables:{input: message}});
      //await PubSub.publish(this.state.gameCode+"/"+PubSubEvents.NEXT_ROUND, nextRound);
      this.setState({round:nextRound, endRound:false});
    }
  }
  async newGame(){
    let oldGameCode;
    let newGameCode = getGameCode();
    // Reset game to start anew
    this.setState((prevState, props) => {
      oldGameCode = prevState.gameCode;
      return {
        gameCode:newGameCode,
        players:[],
        round:0,
        startGame:false,
        endRound:false,
        endGame:false
      }
    }, async ()=>{
      let message = {
        room: this.state.gameCode,
        action: PubSubEvents.NEW_GAME,
        data: JSON.stringify({gameCode:newGameCode, oldGameCode: oldGameCode})
      };
      await API.graphql({query:mutations.createGameMessage, variables:{input: message}});
    })
  }
  async removePlayer(player){
    let playerIndex = getPlayerNumber(this.state.players, player);
    if(playerIndex !== null){
      let players = this.state.players;
      players.splice(playerIndex,1);

      let message = {
        room:this.state.gameCode,
        action: PubSubEvents.REMOVE_FROM_GAME,
        data: JSON.stringify({player:player}),
        message: "The host booted you from the game!"
      };
      await API.graphql({query:mutations.createGameMessage, variables:{input: message}});

      this.setState(prevState=>{
        return {players:players};
      }, ()=>{
        if(isRoundCompleted(players, this.state.round)){
          this.setState({
            players: players,
            endRound:true
          });
        }
      });
    }
  }
  render(){
    let view;
    if(this.state.gameCode && !this.state.startGame){
      view = <ModuleLobby removePlayer={this.removePlayer.bind(this)} gameCode={this.state.gameCode} players={this.state.players} startGame={this.startGame.bind(this)} cancelGame={this.cancelGame.bind(this)}/>
    }else if(this.state.gameCode && this.state.startGame){
      view = <ModuleGame removePlayer={this.removePlayer.bind(this)} newGame={this.newGame.bind(this)} endGame={this.state.endGame} handleNextRound={this.handleNextRound.bind(this)} endRound={this.state.endRound} round={this.state.round} doodles={this.state.doodles} gameCode={this.state.gameCode} players={this.state.players}/>
    }else{
      view = <ModuleIntro createGame={this.createGame.bind(this)}/>
    }
    return(
      <Container maxWidth={false}>
        <Grid className="Screen_Host"
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: '100vh' }}
        >
          {view}
        </Grid> 
      </Container>
    )
  }
}
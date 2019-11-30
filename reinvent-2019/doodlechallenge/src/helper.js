import {AVATARS} from './constants';
export const handleConnectionError = (error) => {
  window.alert("Error connecting to socket. Please check your internet.");
}
export const handleConnectionClosed = () => {
  window.alert("Connection closed to socket. Please check your connection.");
}
// Gets a standardized PubSub.publish object for the app to use.
export const getPublishOperation = (event, data) =>{
  return {
    event:event,
    data:data
  }
}
export const getAvailableAvatar = (players) =>{
  // Max 30 avatars
  let usedAvatars = players.map((player)=>{
    return player.avatar;
  });
  return generateRandom(0,AVATARS.length-1, usedAvatars);
}
// Checks whether all players have completed the challenge
export const isRoundCompleted = (players, round) => {
  if(!players || players.length <= 0){ return false;}
  for(let i=0; i < players.length; i++){
    if( (players[i].doodles.length - 1) < round){
      return false;
    }
  }
  return true;
}
// Gets the player index, this is their player number. The only mechanism to track in addition to their name which has to be unique.
export const getPlayerNumber = (players, player) => {
  console.log("Looking for player index");
  if(players.length){
    
    return players.findIndex(function(element) {
      console.log(element.uuid, "===", player.uuid);
      return element.uuid === player.uuid;
    })
  }
  return null;
}
// Gets the total score for the player
export const getPlayerScore = (player) => {
  let score = 0;
  for(let i = 0; i < player.doodles.length; i++){
    score = score + player.doodles[i].score;
  }
  return getFormattedScore(score);
}
// Gets formatted score
export const getFormattedScore = (score) =>{
  return Math.round(score * 100) / 100;
}
// Gets the score leader
export const getScoreLeader = (players) => {
  let player = null;
  let highScore = -1;
  for(let i = 0; i < players.length; i++){
    let score = getPlayerScore(players[i]);
    if(score > highScore){
      highScore = score;
      player = players[i];
    }
  }
  return player;
}
export const getSanitizedPlayerObject = (player) =>{
  let doodles = player.doodles.map((doodle)=>{
    return {
      name: doodle.name,
      score: doodle.score,
      url: doodle.url
    }
  });
  return {
    name:player.name,
    avatar:player.avatar,
    doodles:doodles
  }
}
export const getGameCode = () =>{
  var result           = '';
  var characters       = 'ABCDEFGHJKMNPQRSTWXYZ23456789';
  var charactersLength = 4;
  for ( var i = 0; i < charactersLength; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}
// Updates the player in the array.
export const updatePlayer = (player, players) => {
  let myPlayers = players.map((value,index)=>{
    if(value.uuid === player.uuid){
      return player;
    }else{
      return value;
    }
  });
  return myPlayers;
}
export const hasGameStarted = (game) => {
  return game.locked;
}
export const hasGameEnded = (game) => {
  return !game.active;
}
export const create_UUID = () => {
  var dt = new Date().getTime();
  var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = (dt + Math.random()*16)%16 | 0;
      dt = Math.floor(dt/16);
      return (c=='x' ? r :(r&0x3|0x8)).toString(16);
  });
  return uuid;
}
function generateRandom(min, max, failOn) {
  failOn = Array.isArray(failOn) ? failOn : [failOn]
  var num = Math.floor(Math.random() * (max - min + 1)) + min;
  return failOn.includes(num) ? generateRandom(min, max, failOn) : num;
}

export const getBinary = (base64Image) => {
  var binaryImg = atob(base64Image);
  var length = binaryImg.length;
  var ab = new ArrayBuffer(length);
  var ua = new Uint8Array(ab);
  for (var i = 0; i < length; i++) {
    ua[i] = binaryImg.charCodeAt(i);
  }

  return ab;
}
export const getImageByteData = (elementTag, quality)=>{
  let canvas = document.getElementsByTagName(elementTag);
  
  let localImages = []
  for(let c of canvas) {
    //localImages.push(c.toDataURL('image/png'));
    localImages.push(canvasToImage(c, "#FFFFFF", quality));
  }
  // convert base64 content to binary data object
  var base64Image = localImages[1].replace(/^data:image\/(png|jpeg|jpg);base64,/, '');
  return getBinary(base64Image);
}
export const canvasToImage = (c,backgroundColor, quality)=>{

  var context = c.getContext('2d');
  
  let canvas = context.canvas;
  //cache height and width        
  var w = canvas.width;
  var h = canvas.height;
  
  var data;
  
  //get the current ImageData for the canvas.
  data = context.getImageData(0, 0, w, h);
  
  //store the current globalCompositeOperation
  var compositeOperation = context.globalCompositeOperation;
  
  //set to draw behind current content
  context.globalCompositeOperation = "destination-over";
  
  //set background color
  context.fillStyle = backgroundColor;
  
  //draw background / rect on entire canvas
  context.fillRect(0,0,w,h);
  
  //get the image data from the canvas
  var imageData = canvas.toDataURL("image/jpeg", quality);
  
  //clear the canvas
  context.clearRect (0,0,w,h);
  
  //restore it with original / cached ImageData
  context.putImageData(data, 0,0);
  
  //reset the globalCompositeOperation to what it was
  context.globalCompositeOperation = compositeOperation;
  
  //return the Base64 encoded data url string
  return imageData;
}
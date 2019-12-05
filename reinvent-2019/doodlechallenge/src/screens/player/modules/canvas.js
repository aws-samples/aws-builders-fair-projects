import React from 'react';
import { Hub } from 'aws-amplify';
import CanvasDraw from 'react-canvas-draw';
import ComponentControls from './canvasControl';
import {ReactComponent as AssetBackground} from '../../../assets/icons/canvas_bg.jpg';
//import {EVENTS} from '../../../events';
import '../index.css';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.myCanvasDraw = React.createRef();
  }
  clear(){
    this.myCanvasDraw.current.clear();
  }
  async finishedDrawing(){
    // Hub.dispatch(EVENTS.FINISHED_DRAWING, { 
    //   event: 'buttonClick', 
    //   data: null, 
    //   message:'' 
    // });
  }
  
  render(){
    return (
      <div className="Component-canvas">
        <ComponentControls player={this.props.player} done={this.props.finishRound} time={this.props.time} draw={this.props.doodle.object} clear={this.clear.bind(this)} />
        <CanvasDraw className="canvas" imgSrc={AssetBackground} ref={this.myCanvasDraw} lazyRadius={0} brushRadius={5} hideGrid={true} canvasWidth="100%"/>          
      </div>
    )
  }
}
import React from 'react';
import { Fade, Typography } from '@material-ui/core';

import './index.css';

export default class Welcome extends React.Component {
  render (){
    return (
      <Fade in={true} timeout={100}>
        <div className="InGame_CountDown">
          <Typography variant="h2" className="InGame_CountDown_Label" gutterBottom>Get ready for next round</Typography>
        </div>
      </Fade>
    );
  }
}
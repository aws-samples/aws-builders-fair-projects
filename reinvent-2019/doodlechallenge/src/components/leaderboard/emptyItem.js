import React from 'react';
import Paper from '@material-ui/core/Paper';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { S3Image } from 'aws-amplify-react';
import IconButton from '@material-ui/core/IconButton';
import HighlightOffIcon from '@material-ui/icons/HighlightOff';

import './index.css';


export default class App extends React.Component {
  render (){
    return (
      <Card className="Component-Player Empty">
        
      </Card>
    );
  }
}
import React from 'react';
// import logo from './logo.svg';
import './App.css';
import Amplify from 'aws-amplify';
import awsconfig from './aws-exports';
import Dashboard from './dashboard/dashboard'
import { withAuthenticator } from 'aws-amplify-react';
import { SemanticToastContainer } from 'react-semantic-toasts';
import 'react-semantic-toasts/styles/react-semantic-alert.css';

Amplify.configure(awsconfig);

function App() {
  return (
    <div className="App">
      <SemanticToastContainer />
      {/* <Dashboard thingName="dz-drone0" /> */}
      {/* <Dashboard thingName="dz-drone1" /> */}
      {/* <Dashboard thingName="dz-drone2" /> */}
      {/* <Dashboard thingName="dz-drone3" /> */}
      <Dashboard thingName="dz-drone4" />
    </div>
  );
}

export default withAuthenticator(App, true);
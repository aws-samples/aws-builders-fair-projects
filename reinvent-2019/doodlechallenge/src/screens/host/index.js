import React from 'react';
import Amplify, { Hub } from 'aws-amplify';
import { withAuthenticator, SignIn, Greetings, RequireNewPassword, ForgotPassword, Loading, VerifyContact } from 'aws-amplify-react';
import { Button } from '@material-ui/core';
import ModuleMainHost from './modules/mainHost';
import {HubEvents} from '../../events';
import './index.css';

const goBack = () => {
  Hub.dispatch(HubEvents.BECOME_PLAYER);
}
const MyTheme = {
  navBar: {"backgroundColor":"initial", "border":"0px"},
  navRight:{"textAlign":"center"}
}
const message =  <Button fullWidth={true} size="large" variant="contained" color="primary" onClick={goBack} >Go Back</Button>;    
export default withAuthenticator(ModuleMainHost, false, [
    <Greetings inGreeting={(username) => 'Hello ' + username} outGreeting={message}/>,
    <SignIn />,
    <RequireNewPassword/>,
    <VerifyContact/>,
    <ForgotPassword/>,
    <Loading/>,
], null, MyTheme);
import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from "react-router-dom";
import Play from './Component/PlayComponent'
import Home from './Component/HomeComponent'
import Results from './Component/ResultsComponent/ResultsComponent'

function App() {
  return (
    <Router>
      <React.Fragment>
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/results" component={Results} />
          <Route path="/play" component={Play} />
        </Switch>
      </React.Fragment>
    </Router>
  );
}

export default App;

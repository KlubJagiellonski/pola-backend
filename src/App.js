import React from 'react';
import Search from './pages/serach/Search'
import ModalPage from './pages/serach/Modal'
import {
  HashRouter,
  Switch,
  Route,
} from "react-router-dom";


function App() {
  return (
    <div>
      <HashRouter>
        <Search />
        <Switch>
          <Route exact path="/:ean" component={ModalPage} />
        </Switch>
      </HashRouter>
    </div>
  );
}

export default App;

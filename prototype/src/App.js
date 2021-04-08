import React from 'react';
import Search from './pages/serach/Search'
import ModalPage from './pages/serach/Modal'
import {
  HashRouter,
  Switch,
  Route,
} from "react-router-dom";
import { AppStyled } from './App.css'


function App() {
  return (
    <AppStyled>
      <HashRouter>
        <Search />
        <Switch>
          <Route exact path="/ean/:ean" component={ModalPage} />
        </Switch>
      </HashRouter>
    </AppStyled>
  );
}

export default App;

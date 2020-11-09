import React from 'react';
import Search from './pages/serach/Search'
import ModalPage from './pages/serach/Modal'
import {
  BrowserRouter,
  Switch,
  Route,
} from "react-router-dom";


function App() {
  return (
    <div>
      <BrowserRouter>
        <Search />
        <Switch>
          <Route exact path="/:ean" component={ModalPage} />
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;

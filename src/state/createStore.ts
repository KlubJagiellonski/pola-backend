import { composeWithDevTools } from 'redux-devtools-extension';
//import combinedReducers from './reducers/root-reducer';
import { load, save } from 'redux-localstorage-simple';
import { createStore, applyMiddleware, combineReducers } from 'redux';
import todosCustomMiddleware from './middlewares/todosCustomMiddleware';
import loginCustomMiddleware from './middlewares/loginCustomMiddleware';
import { IPolaState } from './types';

import loginReducer, { ILoginState } from './reducers/login';
import todosReducer, { ITodosState } from './reducers/todos';
import { appReducer } from './app/app-reducer';
import { searchReducer } from './search/search-reducer';
import thunk from 'redux-thunk';

const middleware = [thunk];

const reducers = combineReducers({
  // loginReducer,
  // todosReducer,
  app: appReducer,
  search: searchReducer,
});

export default (preloadedState: IPolaState) => {
  return createStore(
    reducers,
    //getLoadedState(preloadedState),
    composeWithDevTools(
      applyMiddleware(thunk) // save({ states: ['loginReducer'] }), todosCustomMiddleware(), loginCustomMiddleware())
    )
  );
};

const getLoadedState = (preloadedState: IPolaState | any) => {
  if (typeof window !== 'undefined')
    return {
      ...preloadedState,
      ...load({ states: ['loginReducer'], disableWarnings: true }),
    };

  return {
    ...preloadedState,
  };
};

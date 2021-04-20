import { AnyAction, Reducer } from 'redux';
import { appReducer, IAppState } from './app/app-reducer';
import { searchReducer, ISearchState } from './search/search-reducer';

export interface IPolaState {
  app: IAppState;
  search: ISearchState;
}

export const reducers = {
  app: appReducer,
  search: searchReducer,
};

export interface IAction extends AnyAction {
  type: string;
  payload?: any;
  meta?: any;
}

export interface IActionReducer<TState> {
  [actionName: string]: Reducer<TState, IAction>;
}

import { AnyAction, Reducer } from 'redux';
import { IAppState } from './app/app-reducer';
import { IArticlesState } from './articles/articles-reducer';
import { ISearchState } from './search/search-reducer';
import { IFriendsState } from './friends/friends-reducer'

export interface IPolaState {
  app: IAppState;
  search: ISearchState;
  articles: IArticlesState;
  friends: IFriendsState;
}

export interface IAction extends AnyAction {
  type: string;
  payload?: any;
  meta?: any;
}

export interface IActionReducer<TState> {
  [actionName: string]: Reducer<TState, IAction>;
}

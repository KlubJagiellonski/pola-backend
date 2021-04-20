import { AnyAction, Reducer } from 'redux';
import { actionTypes } from './search-actions';
import * as actions from './search-actions';
import { IAction, IActionReducer } from '../types';

export interface ISearchState {
  isSearchLoading: boolean;
  searchPhrase?: string;
  results?: string[];
}

const initialState: ISearchState = {
  isSearchLoading: false,
};

const reducers: IActionReducer<ISearchState> = {
  [actionTypes.INVOKE_PHRASE]: (state: ISearchState, action: ReturnType<typeof actions.InvokePhrase>) => {
    return {
      ...state,
      isSearchLoading: true,
      searchPhrase: action.payload.searchPhrase,
    };
  },

  [actionTypes.LOAD_RESULTS]: (state: ISearchState, action: ReturnType<typeof actions.LoadResults>) => {
    return {
      ...state,
      isSearchLoading: false,
      results: action.payload.results,
    };
  },
};

export const searchReducer: Reducer<ISearchState, AnyAction> = (
  state: ISearchState = initialState,
  action: IAction
) => {
  const reducer: any = reducers[action.type];
  return reducer ? reducer(state, action) : state;
};

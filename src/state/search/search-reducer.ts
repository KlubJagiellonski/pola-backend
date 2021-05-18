import { AnyAction, Reducer } from 'redux';
import { actionTypes } from './search-actions';
import * as actions from './search-actions';
import { IAction, IActionReducer } from '../types';
import { IProductData } from '../../domain/products';

export interface ISearchState {
  isLoading: boolean;
  phrase?: string;
  products?: IProductData[];
  token?: string;
  error?: unknown;
}

const initialState: ISearchState = {
  isLoading: false,
};

const reducers: IActionReducer<ISearchState> = {
  [actionTypes.INVOKE_SEARCH]: (state: ISearchState, action: ReturnType<typeof actions.InvokePhrase>) => {
    return {
      ...state,
      isLoading: true,
      phrase: action.payload.phrase,
      token: undefined,
    };
  },

  [actionTypes.LOAD_RESULTS]: (state: ISearchState, action: ReturnType<typeof actions.LoadResults>) => {
    return {
      ...state,
      isLoading: false,
      products: action.payload.products,
      token: action.payload.token,
    };
  },

  [actionTypes.SEARCH_FAILED]: (state: ISearchState, action: ReturnType<typeof actions.SearchFailed>) => {
    return {
      ...state,
      isLoading: false,
      error: action.payload.error,
      token: undefined,
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

import { AnyAction, Reducer } from 'redux';
import { actionTypes } from './search-actions';
import * as actions from './search-actions';
import { IAction, IActionReducer } from '../types';
import { IProductData, IProductEAN } from '../../domain/products';

export enum SearchStateName {
  INITIAL = 'initial',
  LOADING = 'loading',
  LOADED = 'loaded',
  SELECTED = 'selected',
}

export type SearchState =
  | {
      stateName: SearchStateName.INITIAL;
    }
  | {
      stateName: SearchStateName.LOADING;
      phrase: string;
      error?: unknown;
    }
  | {
      stateName: SearchStateName.LOADED;
      phrase: string;
      token: string;
      products: IProductData[];
      error?: unknown;
    }
  | {
      stateName: SearchStateName.SELECTED;
      phrase: string;
      token: string;
      products: IProductData[];
      selectedProduct: IProductEAN;
      error?: unknown;
    };

const initialState: SearchState = {
  stateName: SearchStateName.INITIAL,
};

const reducers: IActionReducer<SearchState> = {
  [actionTypes.INVOKE_SEARCH]: (state: SearchState, action: ReturnType<typeof actions.InvokePhrase>) => {
    return {
      ...state,
      stateName: SearchStateName.LOADING,
      phrase: action.payload.phrase,
      token: undefined,
    };
  },

  [actionTypes.LOAD_RESULTS]: (state: SearchState, action: ReturnType<typeof actions.LoadResults>) => {
    return {
      ...state,
      stateName: SearchStateName.LOADED,
      phrase: action.payload.phrase,
      token: action.payload.token,
      products: action.payload.products,
    };
  },

  [actionTypes.CLEAR_RESULTS]: (state: SearchState, action: ReturnType<typeof actions.ClearResults>) => {
    return initialState;
  },

  [actionTypes.SEARCH_FAILED]: (state: SearchState, action: ReturnType<typeof actions.SearchFailed>) => {
    return {
      ...state,
      error: action.payload.error,
    };
  },

  [actionTypes.SHOW_PRODUCT_DETAILS]: (state: SearchState, action: ReturnType<typeof actions.ShowProductDetails>) => {
    return {
      ...state,
      stateName: SearchStateName.SELECTED,
      selectedProduct: action.payload.product,
    };
  },

  [actionTypes.UNSELECT_PRODUCT]: (state: SearchState, action: ReturnType<typeof actions.ShowProductDetails>) => {
    return {
      ...state,
      stateName: SearchStateName.LOADED,
      selectedProduct: undefined,
    };
  },
};

export const searchReducer: Reducer<SearchState, AnyAction> = (state: SearchState = initialState, action: IAction) => {
  const reducer: any = reducers[action.type];
  return reducer ? reducer(state, action) : state;
};

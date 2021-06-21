import { AnyAction, Reducer } from 'redux';
import { actionTypes } from './search-actions';
import * as actions from './search-actions';
import { IAction, IActionReducer } from '../types';
import { IProductData, IProductEAN } from '../../domain/products';

export interface ISearchState {
  isLoading: boolean;
  phrase?: string;
  token?: string;
  products?: IProductData[];
  selectedProduct?: IProductEAN;
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

  [actionTypes.CLEAR_RESULTS]: (state: ISearchState, action: ReturnType<typeof actions.ClearResults>) => {
    return {
      ...state,
      isLoading: false,
      products: undefined,
      token: undefined,
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

  [actionTypes.SHOW_PRODUCT_DETAILS]: (state: ISearchState, action: ReturnType<typeof actions.ShowProductDetails>) => {
    return {
      ...state,
      selectedProduct: action.payload.product,
    };
  },

  [actionTypes.UNSELECT_PRODUCT]: (state: ISearchState, action: ReturnType<typeof actions.ShowProductDetails>) => {
    return {
      ...state,
      selectedProduct: undefined,
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

import { AnyAction, Reducer } from 'redux';
import { actionTypes } from './search-actions';
import * as actions from './search-actions';
import { IAction, IActionReducer } from '../types';
import { IProductData, Product } from '../../domain/products';
import { ErrorHandler } from '../../services/api-errors';

export interface ISearchResultPage {
  pageIndex: number;
  products: IProductData[];
}

export enum SearchStateName {
  INITIAL = 'initial',
  LOADING = 'loading',
  LOADED = 'loaded',
  SELECTED = 'selected',
  ERROR = 'error',
}

export type SearchState =
  | {
      stateName: SearchStateName.INITIAL;
    }
  | {
      stateName: SearchStateName.LOADING;
      phrase: string;
    }
  | {
      stateName: SearchStateName.LOADED;
      phrase: string;
      nextPageToken: string;
      resultPages: ISearchResultPage[];
      totalItems: number;
    }
  | {
      stateName: SearchStateName.SELECTED;
      phrase: string;
      nextPageToken: string;
      resultPages: ISearchResultPage[];
      totalItems: number;
      selectedProduct: Product;
    }
  | {
      stateName: SearchStateName.ERROR;
      phrase?: string;
      nextPageToken?: string;
      resultPages?: ISearchResultPage[];
      totalItems?: number;
      selectedProduct?: Product;
      error: ErrorHandler;
    };

const initialState: SearchState = {
  stateName: SearchStateName.INITIAL,
};

const reducers: IActionReducer<SearchState> = {
  [actionTypes.INVOKE_SEARCH]: (state: SearchState = initialState, action: ReturnType<typeof actions.InvokeSearch>) => {
    return {
      ...state,
      stateName: SearchStateName.LOADING,
      phrase: action.payload.phrase,
      pageToken: undefined,
      nextPageToken: undefined,
    };
  },

  [actionTypes.LOAD_RESULTS]: (state: SearchState = initialState, action: ReturnType<typeof actions.LoadResults>) => {
    if (state.stateName === SearchStateName.LOADING) {
      return {
        ...state,
        stateName: SearchStateName.LOADED,
        //phrase: action.payload.phrase,
        nextPageToken: action.payload.token,
        totalItems: action.payload.totalItems,
        resultPages: [
          {
            pageIndex: 1,
            products: action.payload.pageProducts,
          },
        ],
      };
    }

    return state;
  },

  [actionTypes.LOAD_NEXT_PAGE]: (
    state: SearchState = initialState,
    action: ReturnType<typeof actions.LoadNextPage>
  ) => {
    if (state.stateName === SearchStateName.LOADED) {
      return {
        ...state,
        stateName: SearchStateName.LOADED,
        resultPages: [
          ...state.resultPages,
          {
            pageIndex: state.resultPages.length + 1,
            products: action.payload.pageProducts,
          },
        ],
      };
    }

    return state;
  },

  [actionTypes.CLEAR_RESULTS]: (state: SearchState = initialState) => {
    return initialState;
  },

  [actionTypes.SEARCH_FAILED]: (state: SearchState = initialState, action: ReturnType<typeof actions.SearchFailed>) => {
    return {
      ...state,
      stateName: SearchStateName.ERROR,
      error: action.payload.error,
    };
  },

  [actionTypes.SHOW_PRODUCT_DETAILS]: (
    state: SearchState = initialState,
    action: ReturnType<typeof actions.ShowProductDetails>
  ) => {
    if (state.stateName === SearchStateName.LOADED) {
      return {
        ...state,
        stateName: SearchStateName.SELECTED,
        selectedProduct: action.payload.product,
      };
    }

    return state;
  },

  [actionTypes.UNSELECT_PRODUCT]: (state: SearchState = initialState) => {
    if (state.stateName === SearchStateName.SELECTED) {
      return {
        ...state,
        stateName: SearchStateName.LOADED,
        selectedProduct: undefined,
      };
    }

    return state;
  },
};

export const searchReducer: Reducer<SearchState, AnyAction> = (state: SearchState = initialState, action: IAction) => {
  const reducer: any = reducers[action.type];
  return reducer ? reducer(state, action) : state;
};

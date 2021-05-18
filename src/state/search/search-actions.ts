import { IProductData, IProductEAN } from '../../domain/products';
import { IAction } from '../types';

export const actionTypes = {
  INVOKE_SEARCH: 'SEARCH:INVOKE_SEARCH',
  LOAD_RESULTS: 'SEARCH:LOAD_RESULTS',
  SEARCH_FAILED: 'SEARCH:SEARCH_FAILED',
  SHOW_PRODUCT_DETAILS: 'SEARCH:SHOW_PRODUCT_DETAILS',
  UNSELECT_PRODUCT: 'SEARCH:UNSELECT_PRODUCT',
};

export const InvokePhrase = (phrase: string): IAction => ({
  type: actionTypes.INVOKE_SEARCH,
  payload: {
    phrase,
  },
});

export const LoadResults = (products: IProductData[], token: string): IAction => ({
  type: actionTypes.LOAD_RESULTS,
  payload: {
    products,
    token,
  },
});

export const SearchFailed = (error: unknown): IAction => ({
  type: actionTypes.SEARCH_FAILED,
  payload: {
    error,
  },
});

export const ShowProductDetails = (product: IProductEAN): IAction => ({
  type: actionTypes.SHOW_PRODUCT_DETAILS,
  payload: {
    product,
  },
});

export const UnselectProduct = (): IAction => ({
  type: actionTypes.UNSELECT_PRODUCT,
});

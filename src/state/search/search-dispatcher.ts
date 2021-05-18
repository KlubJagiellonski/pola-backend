import { Dispatch } from 'redux';
import { ProductService } from '../../domain/products/product-service';
import { IPolaState } from '../types';
import * as actions from './search-actions';

export const searchDispatcher = {
  invokeSearch: (phrase: string) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      await dispatch(actions.InvokePhrase(phrase));
      const service = ProductService.getInstance();
      const response = await service.searchProducts(phrase);
      const products = response.products;
      await dispatch(actions.LoadResults(products, response.nextPageToken));
    } catch (error) {
      await dispatch(actions.SearchFailed(error));
    }
  },

  invokeLoadMore: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      const state = getState();
      if (state.search.phrase && state.search.token) {
        const service = ProductService.getInstance();
        const response = await service.searchProducts(state.search.phrase, state.search.token);
        const products = response.products;
        await dispatch(actions.LoadResults(products, response.nextPageToken));
      }
    } catch (error) {
      await dispatch(actions.SearchFailed(error));
    }
  },
};

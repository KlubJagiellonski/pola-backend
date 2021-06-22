import { Dispatch } from 'redux';
import { ProductEANService } from '../../domain/products/ean-service';
import { ProductService } from '../../domain/products/search-service';
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
      console.error('cannot search', error);
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
      console.error('cannot load more products', error);
      await dispatch(actions.SearchFailed(error));
    }
  },

  clearResults: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      dispatch(actions.ClearResults());
    } catch (error) {
      console.error('cannot clear results', error);
      await dispatch(actions.SearchFailed(error));
    }
  },

  selectProduct: (code: string, id: string) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      const service = ProductEANService.getInstance();
      const ean = await service.getProduct(code, id);
      const product = getState().search.products?.find((p) => p.id === id);
      await dispatch(
        actions.ShowProductDetails({
          ...ean,
          data: product,
        })
      );
    } catch (error) {
      console.error('cannot select product', error);
      await dispatch(actions.SearchFailed(error));
    }
  },

  unselectProduct: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      await dispatch(actions.UnselectProduct());
    } catch (error) {
      console.error('cannot unselect product', error);
      await dispatch(actions.SearchFailed(error));
    }
  },
};

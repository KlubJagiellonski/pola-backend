import { Dispatch } from 'redux';
import { EAN, IProductEAN, Product } from '../../domain/products';
import { ProductEANService } from '../../domain/products/ean-service';
import { ProductService } from '../../domain/products/search-service';
import { ErrorHandler } from '../../services/api-errors';
import { IPolaState } from '../types';
import { ProductSelectors } from './product-selectors';
import * as actions from './search-actions';
import { SearchStateName } from './search-reducer';

export const searchDispatcher = {
  /**
   * Gets first page of results for specified phrase.
   * Used by Home page.
   * @param phrase Text from search input.
   */
  invokeSearch: (phrase: string) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      const {
        search: { stateName },
      } = getState();

      if (stateName !== SearchStateName.LOADING) {
        if (stateName !== SearchStateName.INITIAL) {
          await dispatch(actions.ClearResults());
        }
        await dispatch(actions.InvokeSearch(phrase));

        const service = ProductService.getInstance();
        const response = await service.searchProducts(phrase);
        const { products, totalItems, nextPageToken } = response;
        await dispatch(actions.LoadResults(products, totalItems, nextPageToken));
      }
    } catch (error: unknown) {
      if (error instanceof ErrorHandler) {
        console.error('[Product search error]:', error);
        await dispatch(actions.SearchFailed(error));
      } else {
        console.error('[Unhandled error]:', error);
        throw error;
      }
    }
  },

  /**
   * Loads next page of results for phrase stored in the reducer.
   * Used by Products list page.
   */
  invokeLoadMore: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      const { search } = getState();

      if (search.stateName === SearchStateName.LOADED) {
        const { phrase, nextPageToken } = search;
        const service = ProductService.getInstance();
        const response = await service.searchProducts(phrase, nextPageToken);

        if (response) {
          const { products } = response;

          await dispatch(actions.LoadNextPage(phrase, products));
        } else {
          throw new Error('Search response is empty');
        }
      }
    } catch (error) {
      console.error('cannot load more products', error);
      await dispatch(actions.SearchFailed(error));
    }
  },

  /**
   * Set search reducer to its initial state.
   * No products loaded, no search phrase stored.
   */
  clearResults: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      dispatch(actions.ClearResults());
    } catch (error) {
      console.error('cannot clear results', error);
      await dispatch(actions.SearchFailed(error));
    }
  },

  /**
   * Stores which product from retrieved search results is selected.
   * Loads detailed product data from EAN service.
   * @param code EAN code of selected product
   */
  selectProduct: (code: EAN) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      const { search } = getState();
      if (search.stateName === SearchStateName.LOADED) {
        const service = ProductEANService.getInstance();
        const productEntityEAN: IProductEAN = await service.getProduct(code);
        const prod = ProductSelectors.findProduct(productEntityEAN.code, search);
        if (prod) {
          const product = new Product(prod.name, productEntityEAN);
          await dispatch(actions.ShowProductDetails(product));
        } else {
          throw new Error('Cannot find product');
        }
      }
    } catch (error) {
      console.error('cannot select product', error);
      await dispatch(actions.SearchFailed(error));
    }
  },

  /**
   * Clears selected product data.
   */
  unselectProduct: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      const {
        search: { stateName },
      } = getState();

      if (stateName === SearchStateName.SELECTED) {
        await dispatch(actions.UnselectProduct());
      }
    } catch (error) {
      console.error('cannot unselect product', error);
      await dispatch(actions.SearchFailed(error));
    }
  },
};

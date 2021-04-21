import { Dispatch } from 'redux';
import { Product } from '../../products';
import { SearchService } from '../../services/search-service';
import { IPolaState } from '../types';
import * as actions from './search-actions';

export const searchDispatcher = {
  invokeSearch: (phrase: string) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      await dispatch(actions.InvokePhrase(phrase));
      const productData = await SearchService.getProducts(10);
      const products = productData.results.map(
        data => new Product(data.title, data.description, data.category, data.image)
      );
      await dispatch(actions.LoadResults(products));
    } catch (error) {
      await dispatch(actions.SearchFailed(error));
    }
  },
};

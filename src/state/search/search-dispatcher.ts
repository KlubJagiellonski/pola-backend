import { Dispatch } from 'redux';
import { SearchService } from '../../services/search-service';
import { IPolaState } from '../types';
import * as actions from './search-actions';

export const searchDispatcher = {
  invokeSearch: (phrase: string) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    try {
      await dispatch(actions.InvokePhrase(phrase));
      const products = await SearchService.getProducts(10);
      await dispatch(actions.LoadResults(products));
    } catch (error) {
      await dispatch(actions.SearchFailed(error));
    }
  },
};

import { Dispatch } from 'redux';
import { SearchService } from '../../services/search-service';
import { IPolaState } from '../types';
import * as actions from './search-actions';

export const searchDispatcher = {
  invokePhrase: (text: string) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.InvokePhrase(text));
    const products = await SearchService.getProducts(10);
    await dispatch(actions.LoadResults(products.map(x => x.name.last)));
  },
  loadResults: (results: string[]) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.LoadResults(results));
  },
};

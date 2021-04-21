import { ,Dispatch } from 'redux';
import { BrowserHistoryInstance } from '../../utils/routing/browser-history';
import { IPolaState } from '../types';
import * as actions from './app-actions';

export const appDispatcher = {
  initialize: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.Initialize());
  },

  loadBrowserLocation: (location: Location) => async (dispatch: any, getState: () => IPolaState) => {
    BrowserHistoryInstance.setHistory(history);
    await dispatch(actions.LoadBrowserLocation(location));
  },
};

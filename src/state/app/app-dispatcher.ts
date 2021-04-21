import { Dispatch } from 'redux';
import { IPolaState } from '../types';
import * as actions from './app-actions';

export const appDispatcher = {
  initialize: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.Initialize());
  },

  loadBrowserLocation: (location: Location) => async (dispatch: any, getState: () => IPolaState) => {
    await dispatch(actions.LoadBrowserLocation(location));
  },
};

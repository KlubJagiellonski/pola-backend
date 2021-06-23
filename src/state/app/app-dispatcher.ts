import { Dispatch } from 'redux';
import { PageType } from '../../domain/generic';
import { IPolaState } from '../types';
import * as actions from './app-actions';

export const appDispatcher = {
  initialize: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.Initialize());
  },

  loadBrowserLocation: (location: Location) => async (dispatch: any, getState: () => IPolaState) => {
    await dispatch(actions.LoadBrowserLocation(location));
  },

  selectActivePage: (type: PageType) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.SelectActivePage(type));
  },

  expandMenu: (expanded: boolean) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.ExpandMenu(expanded));
  },
};

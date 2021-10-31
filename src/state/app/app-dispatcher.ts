import { Dispatch } from 'redux';
import { PageType } from '../../domain/website';
import { SearchStateName } from '../search/search-reducer';
import { IPolaState } from '../types';
import * as actions from './app-actions';
import * as searchActions from '../search/search-actions';

export const appDispatcher = {
  initialize: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.Initialize());
  },

  loadBrowserLocation: (location: Location) => async (dispatch: any, getState: () => IPolaState) => {
    await dispatch(actions.LoadBrowserLocation(location));
  },

  selectActivePage: (type: PageType) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    const { search } = getState();
    if (search.stateName === SearchStateName.LOADED) {
      await dispatch(searchActions.ClearResults());
    }
    await dispatch(actions.SelectActivePage(type));
  },

  expandMenu: (expanded: boolean) => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.ExpandMenu(expanded));
  },

  /**
   * Toggles visibility of search info modal.
   *
   * [EXPLANATION]: inside app dispatcher as this operation is valid for all search states
   */
  toggleSearchInfo: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    await dispatch(actions.ToggleSearchInfo());
  },
};

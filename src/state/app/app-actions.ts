import { IAction } from '../types';

export const actionTypes = {
  INITIALIZE: 'APP:INITIALIZE',
  LOAD_BROWSER_LOCATION: 'APP:LOAD_BROWSER_LOCATION',
  SELECT_ACTIVE_PAGE: 'APP:SELECT_ACTIVE_PAGE',
  EXPAND_MENU: 'APP:EXPAND_MENU',
  TOGGLE_SEARCH_INFO: 'APP:TOGGLE_SEARCH_INFO',
};

export const Initialize = (): IAction => ({
  type: actionTypes.INITIALIZE,
});

export const LoadBrowserLocation = (location: Location): IAction => ({
  type: actionTypes.LOAD_BROWSER_LOCATION,
  payload: {
    location,
  },
});

export const SelectActivePage = (type: PageType): IAction => ({
  type: actionTypes.SELECT_ACTIVE_PAGE,
  payload: {
    type,
  },
});

export const ExpandMenu = (expanded: boolean): IAction => ({
  type: actionTypes.EXPAND_MENU,
  payload: {
    expanded,
  },
});

export const ToggleSearchInfo = (): IAction => ({
  type: actionTypes.TOGGLE_SEARCH_INFO,
});

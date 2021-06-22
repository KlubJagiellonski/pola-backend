import { IAction } from '../types';

export const actionTypes = {
  INITIALIZE: 'APP:INITIALIZE',
  LOAD_BROWSER_LOCATION: 'APP:LOAD_BROWSER_LOCATION',
  SELECT_ACTIVE_PAGE: 'APP:SELECT_ACTIVE_PAGE',
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

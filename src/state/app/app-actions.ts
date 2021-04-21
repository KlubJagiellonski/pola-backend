import { Context } from 'react';
import { ReactReduxContextValue } from 'react-redux';
import { AnyAction } from 'redux';
import { IAction } from '../types';

export const actionTypes = {
  INITIALIZE: 'APP:INITIALIZE',
  LOAD_BROWSER_LOCATION: 'APP:LOAD_BROWSER_LOCATION',
};

export const Initialize = (): IAction => ({
  type: actionTypes.INITIALIZE,
});

export const LoadBrowserLocation = (location: any): IAction => ({
  type: actionTypes.LOAD_BROWSER_LOCATION,
  payload: {
    location,
  },
});

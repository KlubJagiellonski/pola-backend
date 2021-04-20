import { IAction } from '../types';

export const actionTypes = {
  INITIALIZE: 'APP:INITIALIZE',
};

export const Initialize = (): IAction => ({
  type: actionTypes.INITIALIZE,
});

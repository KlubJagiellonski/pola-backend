import { IAction } from '../types';

export const actionTypes = {
  INVOKE_PHRASE: 'SEARCH:INVOKE_PHRASE',
  LOAD_RESULTS: 'SEARCH:LOAD_RESULTS',
};

export const InvokePhrase = (text: string): IAction => ({
  type: actionTypes.INVOKE_PHRASE,
  payload: {
    searchPhrase: text,
  },
});

export const LoadResults = (results: string[]): IAction => ({
  type: actionTypes.LOAD_RESULTS,
  payload: {
    results,
  },
});

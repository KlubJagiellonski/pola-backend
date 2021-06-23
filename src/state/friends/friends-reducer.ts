import { AnyAction, Reducer } from 'redux';

import { actionTypes } from './friends-actions';
import * as actions from './friends-actions';
import { IAction, IActionReducer } from '../types';
import { IFriend } from '../../domain/friends';

export interface IFriendsState {
  initialized: boolean;
  data?: IFriend[];
}

const initialState: IFriendsState = {
  initialized: false,
};

const reducers: IActionReducer<IFriendsState> = {
  [actionTypes.LOAD_FRIENDS]: (state: IFriendsState = initialState, action: ReturnType<typeof actions.LoadFriends>) => {
    return {
      ...state,
      initialized: true,
      data: action.payload.friends,
    };
  },
};

export const friendsReducer: Reducer<IFriendsState, AnyAction> = (
  state: IFriendsState = initialState,
  action: IAction
) => {
  const reducer: any = reducers[action.type];
  return reducer ? reducer(state, action) : state;
};

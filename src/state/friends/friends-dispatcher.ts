import { Dispatch } from 'redux';
import { Friend } from '../../domain/friends';
import { FriendsService } from '../../domain/friends/friend-service';
import { IPolaState } from '../types';
import * as actions from './friends-actions';

export const friendsDispatcher = {
  loadFriends: () => async (dispatch: Dispatch, getState: () => IPolaState) => {
    const friendsData = await FriendsService.getFriends();
    const friends = friendsData.results.map(data => new Friend(data.description, data.photo));
    await dispatch(actions.LoadFriends(friends));
  },
};

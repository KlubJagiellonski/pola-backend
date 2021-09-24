import React, { useEffect } from 'react'
import styled from 'styled-components'
import { Friend } from '../../domain/friends'
import { margin, Device } from '../../styles/theme'
import SingleFriend from './SingleFriend'
import Friends from './Friends'
import { hash } from '../../domain/website'
import { StringParam, useQueryParams } from 'use-query-params';
import { useState } from 'react'
import { getFriendBySlug } from '../../utils/friends'

const Wrapper = styled.div`
  margin: ${margin.small} 0;

  .friends_wrapper{
    .friends_title{
      display: none;
    }
  }

  @media ${Device.mobile} {
    margin: ${margin.small} 0;
  }
`
interface IFriendsSection {
  friends?: Friend[]
}

const FriendsSection: React.FC<IFriendsSection> = ({ friends }) => {
  const [query] = useQueryParams({
    value: StringParam
  });
  const [friend, setFriend] = useState<Friend>()

  useEffect(() => {
    if (friends && query.value) {
      const friend = getFriendBySlug(query.value, friends);
      if (friend != undefined) {
        setFriend(friend);
      }
    }
  }, [friends, query]);

  return (
    <Wrapper id={hash.friends.friend.id}>
      <Friends friends={friends} />
      {friend && friends && <SingleFriend {...friend} />}
    </Wrapper>
  )
}

export default FriendsSection
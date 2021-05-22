import React from 'react';
import { Wrapper, Item, Items, Title } from './SocialMedia.css';
import SocialImg from './../assets/social.png';
import { color } from '../styles/theme';

const SocialMedia = () => {
  return (
    <Wrapper color={color.background.white}>
      <Title>Social Media</Title>
      <Items>
        <Item>
          <img src={SocialImg} />
        </Item>
        <Item>
          <img src={SocialImg} />
        </Item>
        <Item>
          <img src={SocialImg} />
        </Item>
        <Item>
          <img src={SocialImg} />
        </Item>
      </Items>
    </Wrapper>
  );
};

export default SocialMedia;

import React from 'react';
import { Wrapper, ImageWrapper, Title } from './Friends.css';
import Friend from './../assets/friend.png';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import { color } from '../styles/theme';

const friends = [
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
  { img: Friend },
];

const Friends = () => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: friends.length > 10 ? 10 : friends.length,
    slidesToScroll: friends.length > 10 ? 10 : friends.length,
    arrows: false,
    responsive: [
      {
        breakpoint: 1400,
        settings: {
          slidesToShow: friends.length > 6 ? 6 : friends.length,
          slidesToScroll: friends.length > 6 ? 6 : friends.length,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: friends.length > 3 ? 3 : friends.length,
          slidesToScroll: friends.length > 3 ? 3 : friends.length,
        },
      },
    ],
  };

  return (
    <Wrapper color={color.primary}>
      <Title>Przyjaciele Poli</Title>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <ImageWrapper amountElements={friends.length}>
          <Slider {...settings}>
            {friends.map((el, id) => (
              <div key={`friend_${id}`}>
                <img src={el.img} />
              </div>
            ))}
          </Slider>
        </ImageWrapper>
      </div>
    </Wrapper>
  );
};

export default Friends;

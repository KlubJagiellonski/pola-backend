import React from 'react';
import styled from 'styled-components';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

import { TitleSection, WrapperSection } from '../styles/GlobalStyle.css';
import { Device, color, margin, padding } from './../styles/theme'
import { IFriend } from '../domain/friends';
import { ResponsiveImage } from './responsive-image';

const Wrapper = styled(WrapperSection)`
  width: 100%;
  padding-top: ${padding.small};
  padding-bottom: ${padding.big};
  text-align: center;
  grid-area: friends;
  overflow: hidden;

  @media ${Device.mobile} {
    background-color: white;
    padding: ${padding.big} 0;
  }
`;

const ImageWrapper = styled.div`
  width: 100%;
  margin-top: ${margin.normal};
`;

const FriendsSlider = styled(Slider)`
    height: 6em;

  .slick-dots li.slick-active button:before {
    color: ${color.button.red} !important;
  }
`

const Image = styled.div`
  height: 5.6em;

  div{
    width: 100%;
    height: 100%;

    picture{
      img{
        object-fit: contain !important;
      }
    }
  }
`

interface IFriends {
  friends?: IFriend[];
}

const Friends: React.FC<IFriends> = ({ friends }) => {

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 5,
    adaptiveHeight: true,
    slidesToScroll: 5,
    arrows: false,
    responsive: [
      {
        breakpoint: 1272,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
        },
      },
    ]
  }

  return (
    <Wrapper color={color.background.white}>
      <TitleSection>Przyjaciele Poli</TitleSection>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        {friends &&
          <ImageWrapper>
            <FriendsSlider {...settings}>
              {friends.map((el, id) => (
                <div key={`friend_${id}`}>
                  <Image>
                    {el.image && <ResponsiveImage imageSrc={el.image}/>}
                  </Image>
                </div>
              ))}
            </FriendsSlider>
        </ImageWrapper>}
      </div>
    </Wrapper>
  );
};

export default Friends;

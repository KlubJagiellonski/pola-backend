import React from 'react';
import styled from 'styled-components';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

import { TitleSection, WrapperSection } from '../../styles/GlobalStyle.css';
import { Device, color, margin, padding, fontSize, width } from './../../styles/theme';
import { Friend } from '../../domain/friends';
import { ResponsiveImage } from './../images/ResponsiveImage';
import { AnchorLink } from "gatsby-plugin-anchor-links";
import { buildFriendUrl } from './friends-url-service';
import { hash } from '../../domain/website';

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
  .slick-dots li.slick-active button:before {
    color: ${color.button.red} !important;
  }
`;

const Image = styled.div`
  height: 5.6em;

  div {
    width: 100%;
    height: 100%;

    picture {
      img {
        object-fit: contain !important;
      }
    }
  }
`;

const FriendLink = styled(AnchorLink)`
  font-size: ${fontSize.small};
  position: relative;
  bottom: 0;
  color: ${color.text.secondary};
  opacity: 0.6;
`

interface IFriends {
  friends?: Friend[];
  rows?: number
}

const Friends: React.FC<IFriends> = ({ friends, rows }) => {
  const rowsSettingsDesktop = rows && rows > 1 ? { rows, slidesPerRow: 4 } : {}
  const rowsSettingsMobile = rows && rows > 1 ? { rows, slidesPerRow: 3 } : {}
  const slidesSettingsDesktop = rows && rows > 1 ? {} : { slidesToShow: 5, slidesToScroll: 5 }
  const slidesSettingsMobile = rows && rows > 1 ? {} : { slidesToShow: 3, slidesToScroll: 3 }

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    adaptiveHeight: true,
    ...slidesSettingsDesktop,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 5000,
    ...rowsSettingsDesktop,
    responsive: [
      {
        breakpoint: width,
        settings: {
          ...slidesSettingsMobile,
          ...rowsSettingsMobile
        },
      },
    ],
  };

  return (
    <Wrapper className="friends_wrapper" color={color.background.white}>
      <TitleSection className="friends_title">Przyjaciele Poli</TitleSection>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        {friends && (
          <ImageWrapper>
            <FriendsSlider {...settings}>
              {friends.map((el, id) => (
                <div className="friend-item" key={`friend_${id}`}>
                  <Image>{el.image && <ResponsiveImage imageSrc={el.image} />}</Image>
                  {el.slug &&
                    <FriendLink to={buildFriendUrl(el.slug, hash.friends.friend.id)}>
                      Zobacz {'>'}
                    </FriendLink>
                  }
                </div>
              ))}
            </FriendsSlider>
          </ImageWrapper>
        )}
      </div>
    </Wrapper>
  );
};

export default Friends;

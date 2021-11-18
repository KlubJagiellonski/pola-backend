import React from 'react';
import styled from 'styled-components';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

import { TitleSection, WrapperSection } from './../styles/GlobalStyle.css';
import { Device, color, margin, padding, fontSize, width } from './../styles/theme';
import { AnchorLink } from 'gatsby-plugin-anchor-links';

const Wrapper = styled(WrapperSection)`
  width: 100%;
  height: 100%;
  padding-top: ${padding.small};
  padding-bottom: ${padding.big};
  text-align: center;

  @media ${Device.mobile} {
    background-color: white;
    padding: ${padding.big} 0;
  }
`;

const ImageWrapper = styled.div`
  width: 100%;
  margin-top: ${margin.normal};
`;

const SliderStyled = styled(Slider)`
  .slick-dots li button::before {
    font-size: 0.5rem;
  }

  .slick-dots li.slick-active button:before {
    color: ${color.button.red} !important;
  }
`;

const SliderLink = styled(AnchorLink)`
  font-size: ${fontSize.small};
  position: relative;
  bottom: 0;
  color: ${color.text.secondary};
  height: 100%;
`;

const SliderItem = styled.div`
  height: 100%;
`;

interface ISliderElement {
  to: string;
  children?: React.ReactNode | React.ReactNode[];
}

export const SliderElement: React.FC<ISliderElement> = ({ to, children }) => {
  return (
    <SliderItem>
      <SliderLink to={to}>{children}</SliderLink>
    </SliderItem>
  );
};

interface ISliderContainer {
  title?: string;
  rows?: number;
  children?: React.ReactNode | React.ReactNode[];
}

export const SliderContainer: React.FC<ISliderContainer> = ({ rows, children, title }) => {
  const rowsSettingsDesktop = rows && rows > 1 ? { rows, slidesPerRow: 4 } : {};
  const rowsSettingsMobile = rows && rows > 1 ? { rows, slidesPerRow: 3 } : {};
  const slidesSettingsDesktop = rows && rows > 1 ? {} : { slidesToShow: 5, slidesToScroll: 5 };
  const slidesSettingsMobile = rows && rows > 1 ? {} : { slidesToShow: 3, slidesToScroll: 3 };

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
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
          ...rowsSettingsMobile,
        },
      },
    ],
  };

  return (
    <Wrapper color={color.background.white}>
      <TitleSection>{title}</TitleSection>
      <ImageWrapper>
        <SliderStyled {...settings}>{children}</SliderStyled>
      </ImageWrapper>
    </Wrapper>
  );
};

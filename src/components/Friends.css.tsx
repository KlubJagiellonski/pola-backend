import styled from 'styled-components';
import { WrapperSection } from '../styles/GlobalStyle.css';
import { Device, color, margin, padding } from './../styles/theme'
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

export const Wrapper = styled(WrapperSection)`
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

export const ImageWrapper = styled.div`
  width: 100%;
  margin-top: ${margin.normal};
`;

export const FriendsSlider = styled(Slider)`
  height: 110px;

  .slick-dots li.slick-active button:before {
    color: ${color.red} !important;
  }
`

export const Image = styled.div`
  height: 100px;

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

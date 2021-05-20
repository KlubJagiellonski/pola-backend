import styled from 'styled-components';
import { WrapperSection, Text } from '../../styles/GlobalStyle.css';
import {Device} from '../../styles/theme'
import {SecondaryButton } from '../buttons/SecondaryButton';

export const Wrapper = styled(WrapperSection)`
  display: flex;
  flex-direction: row;
  min-height: 220px;
  margin-bottom: 15px;

  @media only screen and (min-width: 1900px) {
    min-height: 250px;
  }

  @media only screen and (min-width: 2500px) {
    min-height: 280px;
  }

  @media ${Device.mobile}{
    min-height: 120px;
  }
`;

export const ArticleImage = styled.div<{ img?: string }>`
  width: 50%;
  height: auto;
  text-align: left;
  /* background: url(${({ img }) => img});
  background-repeat: no-repeat;
  background-size: cover; */

  @media ${Device.mobile} {
    width: 40%;
    background-size: contain;
    background-position: center;
  }
`;

export const ArticleSection = styled.div`
  width: 50%;
  margin: 0 15px;

  @media ${Device.mobile} {
    width: 60%;
  }
`;

export const ArticleButton = styled(SecondaryButton)`
  font-size: 14px;
  font-weight: 300;
  
  @media ${Device.mobile} {
    display: none;
  }
`;

export const ArticleDate = styled(Text)`
  @media ${Device.mobile} {
    display: none;
  }
`

import styled from 'styled-components';
import { WrapperSection, Text, TitleSection } from '../../styles/GlobalStyle.css';
import {Device, fontSize} from '../../styles/theme'
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
  font-size: ${fontSize.small};
  font-weight: 300;
  
  @media ${Device.mobile} {
    display: none;
    font-size: ${fontSize.tiny};
  }
`;

export const ArticleDate = styled(Text)`
  @media ${Device.mobile} {
    display: none;
  }
`

export const ArticleTitle = styled(TitleSection)`
  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`

export const ArticleText = styled(Text)`
  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`

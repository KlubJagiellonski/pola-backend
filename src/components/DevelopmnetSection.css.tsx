import styled from 'styled-components';
import { WrapperSection } from '../styles/GlobalStyle.css';
import {Device, fontSize, margin, color, padding} from './../styles/theme'
import { TitleSection, Text } from '../styles/GlobalStyle.css';

export const Wrapper = styled(WrapperSection)`
  display: flex;
  flex-direction: row;
  grid-area: development;
  min-height: 230px;
`;

export const Info = styled.p`
  font-size: ${fontSize.tiny};
  color: ${color.white};
  text-align: center;
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
`

export const TextSection = styled.div`
  margin-right: ${margin.normal};
  padding: 0 ${padding.normal};
  background-color: ${color.white};
  width: 50%;

  @media ${Device.mobile} {
    padding: 0 ${padding.small};
  }
`;

export const DevelopmentTitle = styled(TitleSection)`
  margin-bottom: ${margin.normal};

  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`

export const DevelopmentText = styled(Text)`
  margin-bottom: ${margin.big};

  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`
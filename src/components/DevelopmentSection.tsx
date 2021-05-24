import React from 'react';
import styled from 'styled-components';

import {Device, fontSize, margin, color, padding} from './../styles/theme'
import {SecondaryButton } from './buttons/SecondaryButton';
import {ButtonColor} from './buttons/Button'
import { WrapperSection } from '../styles/GlobalStyle.css';
import { TitleSection, Text } from '../styles/GlobalStyle.css';

const Wrapper = styled(WrapperSection)`
  display: flex;
  flex-direction: row;
  grid-area: development;
  min-height: 16.1em;

  @media ${Device.mobile} {
    min-height: 15em;
  }
`;

const Info = styled.p`
  font-size: ${fontSize.tiny};
  color: ${color.text.light};
  text-align: center;
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
`

const TextSection = styled.div`
  margin-right: ${margin.normal};
  padding: 0 ${padding.normal};
  background-color: ${color.background.white};
  width: 50%;

  @media ${Device.mobile} {
    padding: 0 ${padding.small};
  }
`;

const DevelopmentTitle = styled(TitleSection)`
  margin-bottom: ${margin.normal};

  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`

const DevelopmentText = styled(Text)`
  margin-bottom: ${margin.big};

  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`

const DevelopmentSection = () => {
  return (
    <Wrapper color={color.background.red}>
      <Info>Grafika Flat: Smutny koszyk zakupowy</Info>
      <TextSection>
        <DevelopmentTitle>Zobacz jak rozwija się Aplikacja Pola i wspomóż ją!</DevelopmentTitle>
        <DevelopmentText>Dowiedz się co możesz jeszcze zrobić, aby wspierać polskich producentów.</DevelopmentText>
        <SecondaryButton label='Czytaj dalej...' fontSize={fontSize.small} color={ButtonColor.Red}/>
      </TextSection>
    </Wrapper>
  );
};

export default DevelopmentSection;

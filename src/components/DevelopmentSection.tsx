import React from 'react';
import { Wrapper, TextSection, DevelopmentTitle,  DevelopmentText, Info} from './DevelopmnetSection.css';
import { color, fontSize } from '../styles/theme';
import {SecondaryButton } from './buttons/SecondaryButton';
import {ButtonColor} from './buttons/Button'

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

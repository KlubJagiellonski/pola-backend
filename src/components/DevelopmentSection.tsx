import React from 'react';
import { Wrapper, Image, TextSection } from './DevelopmnetSection.css';
import { color } from '../styles/theme';
import Rectangle from '../assets/Rectangle.png';
import { TitleSection, Text } from '../styles/GlobalStyle.css';

const DevelopmentSection = () => {
  return (
    <Wrapper color={color.primary}>
      <Image img={Rectangle} />
      <TextSection>
        <TitleSection>Zobacz jak rozwija się Aplikacja Pola i wspomóż ją!</TitleSection>
        <Text>Dowiedz się co możesz jeszcze zrobić, aby wspierać polskich producentów.</Text>
      </TextSection>
    </Wrapper>
  );
};

export default DevelopmentSection;

import React from 'react';
import { Wrapper, Image, TextSection, DevelopmentTitle,  DevelopmentText} from './DevelopmnetSection.css';
import { color } from '../styles/theme';
import Rectangle from '../assets/Rectangle.png';

const DevelopmentSection = () => {
  return (
    <Wrapper color={color.primary}>
      <Image img={Rectangle} />
      <TextSection>
        <DevelopmentTitle>Zobacz jak rozwija się Aplikacja Pola i wspomóż ją!</DevelopmentTitle>
        <DevelopmentText>Dowiedz się co możesz jeszcze zrobić, aby wspierać polskich producentów.</DevelopmentText>
      </TextSection>
    </Wrapper>
  );
};

export default DevelopmentSection;

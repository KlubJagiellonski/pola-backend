import React from 'react';
import styled from 'styled-components';

import { Device, fontSize, margin, color, padding } from './../styles/theme';
import { SecondaryButton } from './buttons/SecondaryButton';
import { ButtonColor } from '../styles/button-theme';
import { WrapperSection } from '../styles/GlobalStyle.css';
import { TitleSection, Text } from '../styles/GlobalStyle.css';
import { ResponsiveImage } from '../components/images/ResponsiveImage';

const Wrapper = styled(WrapperSection)`
  display: flex;
  flex-direction: row;
  grid-area: development;
  min-height: 16.1em;

  @media ${Device.mobile} {
    min-height: 15em;
  }
`;

const Info = styled.div`
  width: 50%;
  height: initial;
  position: relative;
`;

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
`;

const DevelopmentText = styled(Text)`
  margin-bottom: ${margin.big};

  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`;

const ImgSection = styled.div`
  position: absolute;
  left: 0;
  right: 0;
  margin: auto;
  top: 50%;
  transform: translateY(-50%);

  @media ${Device.mobile} and (min-width : 550px){
    top: 0;
    transform: translateY(0px);

    div {
    picture {
      img{
        width: auto !important;
        height: 15em !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
      }
    }
  }
  }  
`

const DevelopmentSection = () => {
  return (
    <Wrapper color={color.background.red}>
      <Info>
        <ImgSection>
          <ResponsiveImage imageSrc='smutny-2.png'/>
        </ImgSection>
      </Info>
      <TextSection>
        <DevelopmentTitle>Zobacz jak rozwija się Aplikacja Pola i wspomóż ją!</DevelopmentTitle>
        <DevelopmentText>Dowiedz się co możesz jeszcze zrobić, aby wspierać polskich producentów.</DevelopmentText>
        <SecondaryButton label="Czytaj dalej..." fontSize={fontSize.small} color={ButtonColor.Red} />
      </TextSection>
    </Wrapper>
  );
};

export default DevelopmentSection;

import React from 'react';
import styled from 'styled-components';
import styledContainerQuery from 'styled-container-query'

import { Device, fontSize, margin, color, padding } from './../styles/theme';
import { SecondaryButton } from './buttons/SecondaryButton';
import { ButtonColor } from '../styles/button-theme';
import { WrapperSection } from '../styles/GlobalStyle.css';
import { TitleSection, Text } from '../styles/GlobalStyle.css';
import { ResponsiveImage } from '../components/images/ResponsiveImage';

const Info = styled.div`
  width: 50%;
  height: initial;
  position: relative;

  @media ${Device.mobile} {
    width: 8em;
    height: 10em;
    margin: 0 auto;
  }
`;

const TextSection = styled.div`
  margin-right: ${margin.normal};
  padding: 0 ${padding.normal};
  background-color: ${color.background.white};

  @media ${Device.mobile} {
    padding: ${padding.normal};
    width: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
`;

const Texts = styled.div`
  width: 50%;
  background-color: ${color.background.white};
  margin-right: ${margin.small};

  @media ${Device.mobile} {
    margin-bottom: ${margin.small};
    margin-right: 0;
    width: 100%;
  }

`;

const DevelopmentTitle = styled(TitleSection)`
  margin-bottom: ${margin.normal};

`;

const DevelopmentText = styled(Text)`
  margin-bottom: ${margin.big};
`;

const ImgSection = styled.div`
  position: absolute;
  left: 0;
  right: 0;
  margin: auto;
  top: 50%;
  transform: translateY(-50%);

  @media ${Device.mobile}{
    top: 0;
    transform: translateY(0px);

    div {
    picture {
      img{
        width: auto !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
      }
    }
  }
}  
`

const Wrapper = styled(WrapperSection)``;

const Container = styledContainerQuery(Wrapper)`
  display: flex;
  flex-direction: row;
  grid-area: development;
  min-height: 16.1em;
  width: 100%;

  @media ${Device.mobile} {
    min-height: 0;
    display: flex;
    flex-direction: column;
  }

  &:container(max-width: 450px){
    min-height: 0;
    display: flex;
    flex-direction: column;

    ${Info}{
      width: 8em;
      height: 10em;
      margin: 0 auto;
    }

    ${TextSection}{
      padding: ${padding.normal};
      width: auto;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    ${Texts}{
      margin-bottom: ${margin.small};
      width: 100%;
    }

    ${ImgSection}{
      top: 0;
      transform: translateY(0px);

      div {
      picture {
        img{
          width: auto !important;
          left: 50% !important;
          transform: translateX(-50%) !important;
        }
      }
    }
    }
  }
`;

const DevelopmentSection = () => {
  return (
    <Container color={color.background.red}>
      <Info>
        <ImgSection>
          <ResponsiveImage imageSrc='smutny-2.png' />
        </ImgSection>
      </Info>
      <Texts>
        <TextSection>
          <DevelopmentTitle>Zobacz jak rozwija się Aplikacja Pola i wspomóż ją!</DevelopmentTitle>
          <DevelopmentText>Dowiedz się co możesz jeszcze zrobić, aby wspierać polskich producentów.</DevelopmentText>
          <div className='buttons'>
            <SecondaryButton label="Czytaj dalej..." fontSize={fontSize.small} color={ButtonColor.Red} />
          </div>
        </TextSection>
      </Texts>
    </Container>
  );
};

export default DevelopmentSection;

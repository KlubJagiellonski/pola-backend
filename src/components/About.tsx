import React from 'react';
import styled from 'styled-components';

import { padding, margin, color, fontSize } from '../styles/theme';
import { ButtonColor } from '../styles/button-theme';
import { WrapperSection, Text, TitleSection } from '../styles/GlobalStyle.css';
import { SecondaryButton } from './buttons/SecondaryButton';

const Wrapper = styled(WrapperSection)`
  min-height: 32.3em;
  grid-area: about;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column-reverse;
`;

const MockUp = styled.div`
  background-color: ${color.background.primary};
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;

  p {
    margin: 0;
    color: ${color.text.secondary};
    font-size: ${fontSize.small};
  }
`;

const Info = styled.div`
  background-color: ${color.background.dark};
  padding: ${padding.normal} ${padding.big};
`;

const AboutText = styled(Text)`
  color: ${color.text.light};
  margin-top: ${margin.normal};
`;

const AboutTitle = styled(TitleSection)`
  color: ${color.text.light};
`;
const AboutButton = styled(SecondaryButton)`
  margin: ${margin.normal} 0;
`;

const About = () => {
  return (
    <Wrapper color={color.background.dark}>
      <Info>
        <AboutTitle>O Poli</AboutTitle>
        <AboutText>
          Masz dość masówki globalnych koncernów? Szukasz lokalnych firm tworzących unikatowe produkty? Pola pomoże Ci
          odnaleźć polskie wyroby. Zabierając Polę na zakupy, odnajdujesz produkty „z duszą” i wspierasz polską
          gospodarkę.
        </AboutText>
        <AboutButton label="Dowiedz się więcej... " color={ButtonColor.White} fontSize={fontSize.small} />
      </Info>
      <MockUp>
        <p>Mock up telefonu z uruchomioną aplikacją</p>
      </MockUp>
    </Wrapper>
  );
};

export default About;

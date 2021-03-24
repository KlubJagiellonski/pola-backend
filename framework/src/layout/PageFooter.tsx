import React from 'react';
import styled from 'styled-components';
import Logo from './../assets/logo.png';
import SocialFooter from './../assets/SocialFooter.png';

import { theme } from '../styles/theme';

export const Footer = styled.footer`
  display: flex;
  flex-flow: row nowrap;
  width: 100%;
  background-color: ${theme.dark};
  padding: 20px 0px;
  justify-content: center;
`;

export const LogoImage = styled.img`
  margin-right: 100px;
`;

export const Section = styled.div`
  background-color: ${theme.primary};
  padding: 5px 70px 5px 40px;
  margin-right: 20px;

  .text {
    font-family: 'Roboto';
  font-size: 18px;
  font-weight: 400;
  line-height: 21px;
  }

  .title {
    font-family: Roboto;
  font-size: 18px;
  font-weight: 700;
  line-height: 21px;
  }

  .social-rows {
    display: flex;
  flex-direction: row;
  }

  .social-image {
    width: 20%;
  padding-right: 5px;
  }
`;

export const PageFooter = () => {
  return (
    <Footer>
      <div>
        <LogoImage src={Logo} />
      </div>
      <Section>
        <p className="title">Informacje</p>
        <p className="text">Home</p>
        <p className="text">Aktualności</p>
        <p className="text">O Poli</p>
      </Section>
      <Section>
        <p className="title">Działaj z nami</p>
        <p className="text">Wesprzyj aplikację</p>
        <p className="text">Klub przyjaciół Poli</p>
        <p className="text">Dołącz do zespołu</p>
      </Section>
      <Section>
        <p className="title">Jakieś pytania?</p>
        <p className="text">Kontakt</p>
        <p className="text">FAQ</p>
        <p className="text">Uzupełnij dane o firmie</p>
      </Section>
      <Section>
        <p className="title">Social media Title</p>
        <div className="social-rows">
          <img className="social-image" src={SocialFooter}></img>
          <img className="social-image" src={SocialFooter}></img>
          <img className="social-image" src={SocialFooter}></img>
          <img className="social-image" src={SocialFooter}></img>
        </div>
      </Section>
    </Footer>
  );
};

import React from 'react';
import styled from 'styled-components';

import SocialFooter from '../assets/SocialFooter.png';
import { PolaLogo } from './Pola-Logo';
import { color, Device, padding, pageWidth } from '../styles/theme';

export const FooterContainer = styled.footer`
  background-color: ${color.secondary};
  padding: ${padding.big};

  .footer-content {
    display: flex;
    flex-flow: row nowrap;
    margin: 0 auto;

    max-width: ${pageWidth};

    .sections {
      flex: 1 1 100%;
      display: flex;
      padding: 0;
      margin: 0;
    }
    @media ${Device.mobile} {
      .sections {
        flex-flow: column;
      }
    }

    @media ${Device.desktop} {
      .logo {
        min-width: 100px;
      }
      .sections {
        flex-flow: row nowrap;
        gap: ${padding.normal};
      }
    }
  }
`;

export const Section = styled.div`
  background-color: ${color.primary};
  flex: 1 1 25%;

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

  @media ${Device.mobile} {
    background-color: transparent;
    text-align: right;

    .title,
    .social-rows,
    .hide-mobile {
      display: none;
    }
  }

  @media ${Device.desktop} {
    padding: ${padding.normal};
    .hide-desktop {
      display: none;
    }
  }
`;

interface IFooterSection {
  title: string;
}

const FooterSection: React.FC<IFooterSection> = ({ title, children }) => (
  <Section>
    <p className="title">{title}</p>
    {children}
  </Section>
);

export const PageFooter = () => {
  return (
    <FooterContainer>
      <div className="footer-content">
        <div className="logo">
          <PolaLogo />
        </div>
        <div className="sections">
          <FooterSection title="Informacje">
            <p className="text">Home</p>
            <p className="text">Aktualności</p>
            <p className="text">O Poli</p>
          </FooterSection>
          <FooterSection title="Działaj z nami">
            <p className="text">Wesprzyj aplikację</p>
            <p className="text">Klub przyjaciół Poli</p>
            <p className="text">Dołącz do zespołu</p>
          </FooterSection>
          <FooterSection title="Jakieś pytania?">
            <p className="text">Kontakt</p>
            <p className="text">FAQ</p>
            <p className="text hide-desktop">Polityka prywatności</p>
            <p className="text hide-mobile">Uzupełnij dane o firmie</p>
          </FooterSection>
          <FooterSection title="Social media Title">
            <div className="social-rows">
              <img className="social-image" src={SocialFooter}></img>
              <img className="social-image" src={SocialFooter}></img>
              <img className="social-image" src={SocialFooter}></img>
              <img className="social-image" src={SocialFooter}></img>
            </div>
          </FooterSection>
        </div>
      </div>
    </FooterContainer>
  );
};

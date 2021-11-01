import React from 'react';
import styled from 'styled-components';

import LogoWhite from '../assets/logo/pola-white.svg';
import { color, Device, fontSize, padding, pageWidth, margin } from '../styles/theme';
import { Link } from 'gatsby';
import { urls } from '../domain/website';
import { AnchorLink } from 'gatsby-plugin-anchor-links';
import { Facebook, Instagram, Twitter } from '../components/social-media/Icons';

const FooterContainer = styled.footer`
  background-color: ${color.background.dark};
  color: ${color.text.light};
  margin: 0 auto;
  width: 100%;
  padding: ${padding.big} 0;

  .footer-content {
    display: flex;
    flex-flow: row nowrap;
    margin: 0 auto;

    @media ${Device.Desktop} {
      max-width: ${pageWidth};
    }

    .sections {
      flex: 1 1 100%;
      display: flex;
      padding: 0;
      margin: 0;
    }

    @media ${Device.mobile} {
      .sections {
        flex-flow: column;
        gap: 0;
      }
    }

    @media ${Device.desktop} {
      .sections {
        flex-flow: row nowrap;
        gap: ${padding.normal};
      }
    }
  }
`;

const Section = styled.div`
  flex: 1 1 25%;

  .link {
    text-decoration: none;
  }

  .text {
    font-size: ${fontSize.normal};
    font-weight: 400;
    line-height: 21px;
    color: ${color.text.light};
  }

  .title {
    font-size: ${fontSize.normal};
    font-weight: bold;
    line-height: 21px;
  }

  .social-rows {
    display: flex;
    flex-direction: row;
  }

  @media ${Device.mobile} {
    background-color: transparent;
    text-align: right;
    margin-right: ${margin.normal};

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
  title?: string;
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
        <FooterSection>
          <div className="logo">
            <img src={LogoWhite} />
          </div>
        </FooterSection>
        <div className="sections">
          <FooterSection title="Informacje">
            <Link className='link' to={urls.pola.home()}>
              <p className="text">Home</p>
            </Link>
            <Link className='link' to={urls.pola.news}>
              <p className="text">Aktualności</p>
            </Link>
            <Link className='link' to={urls.pola.about()}>
              <p className="text">O Poli</p>
            </Link>
          </FooterSection>
          <FooterSection title="Działaj z nami">
            <Link className='link' to={urls.pola.support}>
              <p className="text">Wesprzyj aplikację</p>
            </Link>
            <Link className='link' to={urls.pola.friends()}>
              <p className="text">Klub przyjaciół Poli</p>
            </Link>
            <Link className='link' to={urls.pola.team}>
              <p className="text">Dołącz do zespołu</p>
            </Link>
          </FooterSection>
          <FooterSection title="Jakieś pytania?">
            <AnchorLink className='link' to={urls.pola.home('contact')}>
              <p className="text">Kontakt</p>
            </AnchorLink>
            <AnchorLink className='link' to={urls.pola.about('faq')}>
              <p className="text">FAQ</p>
            </AnchorLink>
            <Link className='link' to={urls.pola.home()}>
              <p className="text hide-desktop">Polityka prywatności</p>
            </Link>
            <Link className='link' to={urls.pola.home()}>
              <p className="text hide-mobile">Uzupełnij dane o firmie</p>
            </Link>
          </FooterSection>
          <FooterSection title="Śledź nas na:">
            <div className="social-rows">
              <Facebook type='filled' />
              <Instagram type='filled' />
              <Twitter type='filled' />
            </div>
          </FooterSection>
        </div>
      </div>
    </FooterContainer>
  );
};

import React from 'react';
import styled from 'styled-components';

import { HamburgerMenu } from './nav/HamburgerMenu';
import { NavbarMenu } from './nav/NavbarMenu';
import { desktopHeaderHeight, Device, pageWidth, color } from '../styles/theme';
import { Link } from 'gatsby';

interface IPageHeader {
  siteTitle?: string;
}

const HeaderContainer = styled.header`
  display: flex;
  flex-flow: row nowrap;
  justify-content: center;
  position: absolute;
  top: 0;
  z-index: 10;
  width: 100%;
  background: ${color.primary};

  .header-content {
    display: flex;
    flex-flow: row nowrap;
    width: 100%;
    max-width: ${pageWidth};
  }

  @media ${Device.mobile} {
    .navbar-menu {
      display: none;
    }
  }
  @media ${Device.desktop} {
    height: ${desktopHeaderHeight};
    .hamburger-menu {
      display: none;
    }
  }
`;

const navItems = (
  <React.Fragment>
    <span className="nav-item">
      <Link to="/">Home</Link>
    </span>
    <span className="nav-item">
      <Link to="/news">Aktualności</Link>
    </span>
    <span className="nav-item">
      <Link to="/about">O Poli</Link>
    </span>
    <span className="nav-item">
      <Link to="/support">Wesprzyj aplikację</Link>
    </span>
    <span className="nav-item">
      <Link to="/friends">Klub przyjaciół Poli</Link>
    </span>
    <span className="nav-item">
      <Link to="/join">Dołącz do zespołu</Link>
    </span>
    <span className="nav-item">
      <Link to="/faq">FAQ</Link>
    </span>
    <span className="nav-item">
      <Link to="/contect">Kontakt</Link>
    </span>
  </React.Fragment>
);

export const PageHeader = (props: IPageHeader) => (
  <HeaderContainer>
    <div className="header-content">
      <NavbarMenu>{navItems}</NavbarMenu>
      <HamburgerMenu>{navItems}</HamburgerMenu>
    </div>
  </HeaderContainer>
);

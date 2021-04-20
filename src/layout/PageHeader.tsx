import React from 'react';
import styled from 'styled-components';

import { HamburgerMenu } from './nav/HamburgerMenu';
import { NavbarMenu } from './nav/NavbarMenu';
import { desktopHeaderHeight, Device, pageWidth, theme } from '../styles/theme';

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
  background: ${theme.border};

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
    <span className="nav-item">Home</span>
    <span className="nav-item">Aktualności</span>
    <span className="nav-item">O Poli</span>
    <span className="nav-item">Wesprzyj aplikację</span>
    <span className="nav-item">Klub przyjaciół Poli</span>
    <span className="nav-item">Dołącz do zespołu</span>
    <span className="nav-item">FAQ</span>
    <span className="nav-item">Kontakt</span>
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

import React from 'react';
import styled from 'styled-components';

import { HamburgerMenu } from './nav/HamburgerMenu';
import { NavbarMenu } from './nav/NavbarMenu';
import { desktopHeaderHeight, Device, pageWidth, color } from '../styles/theme';
import { Link } from 'gatsby';
import { NavItem } from './nav/NavItem';
import { PageType } from '../domain/generic';

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
  background: ${color.background.white};

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
    <NavItem type={PageType.HOME} label="Home" to="/" activePage={PageType.HOME} />
    <NavItem type={PageType.NEWS} label="Aktualności" to="/news" activePage={PageType.HOME} />
    <NavItem type={PageType.ABOUT} label="O Poli" to="/about" activePage={PageType.HOME} />
    <NavItem type={PageType.SUPPORT} label="Wesprzyj aplikację" to="/support" activePage={PageType.HOME} />
    <NavItem type={PageType.FRIENDS} label="Klub przyjaciół Poli" to="/friends" activePage={PageType.HOME} />
    <NavItem type={PageType.TEAM} label="Dołącz do zespołu" to="/join" activePage={PageType.HOME} />
    <NavItem type={PageType.FAQ} label="FAQ" to="/faq" activePage={PageType.HOME} />
    <NavItem type={PageType.CONTACT} label="Kontakt" to="/contect" activePage={PageType.HOME} />
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

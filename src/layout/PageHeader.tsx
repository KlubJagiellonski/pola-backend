import React from 'react';
import styled from 'styled-components';

import { HamburgerMenu } from './nav/HamburgerMenu';
import { NavbarMenu } from './nav/NavbarMenu';
import { desktopHeaderHeight, Device, pageWidth, color } from '../styles/theme';
import { NavItem } from './nav/NavItem';
import { pageLinks, PageType } from '../domain/website';

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

interface IPageHeader {
  siteTitle?: string;
  activePage: PageType;
  isMenuExpanded: boolean;

  onExpand: (expanded: boolean) => void;
}

export const PageHeader = (props: IPageHeader) => {
  const navItems = pageLinks.map((link) => <NavItem key={link.type} data={link} activePage={props.activePage} />);

  return (
    <HeaderContainer>
      <div className="header-content">
        <NavbarMenu>{navItems}</NavbarMenu>
        <HamburgerMenu expanded={props.isMenuExpanded} onExpand={props.onExpand}>
          {navItems}
        </HamburgerMenu>
      </div>
    </HeaderContainer>
  );
};

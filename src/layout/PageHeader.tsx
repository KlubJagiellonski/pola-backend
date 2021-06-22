import React from 'react';
import styled from 'styled-components';

import { HamburgerMenu } from './nav/HamburgerMenu';
import { NavbarMenu } from './nav/NavbarMenu';
import { desktopHeaderHeight, Device, pageWidth, color } from '../styles/theme';
import { NavItem } from './nav/NavItem';
import { PageLinkData, PageType } from '../domain/generic';

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
  onSelect: (type: PageType) => void;
}

export const PageHeader = (props: IPageHeader) => {
  const items: PageLinkData[] = [
    { type: PageType.HOME, label: 'Home', url: '/' },
    { type: PageType.NEWS, label: 'Aktualności', url: '/news' },
    { type: PageType.ABOUT, label: 'O Poli', url: '/about' },
    { type: PageType.SUPPORT, label: 'Wesprzyj aplikację', url: '/support' },
    { type: PageType.FRIENDS, label: 'Klub przyjaciół Poli', url: '/friends' },
    { type: PageType.TEAM, label: 'Dołącz do zespołu', url: '/join' },
    { type: PageType.CONTACT, label: 'Kontakt', url: '/contact' },
  ];
  const navItems = items.map((item) => <NavItem data={item} activePage={props.activePage} onClick={props.onSelect} />);

  return (
    <HeaderContainer>
      <div className="header-content">
        <NavbarMenu>{navItems}</NavbarMenu>
        <HamburgerMenu>{navItems}</HamburgerMenu>
      </div>
    </HeaderContainer>
  );
};

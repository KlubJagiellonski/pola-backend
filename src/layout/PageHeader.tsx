import React from 'react';
import styled from 'styled-components';

import { HamburgerMenu } from './nav/HamburgerMenu';
import { NavbarMenu } from './nav/NavbarMenu';
import { desktopHeaderHeight, Device, pageWidth, color } from '../styles/theme';
import { NavItem } from './nav/NavItem';
import { PageLinkData, PageType } from '../domain/generic';
import { urls } from '../utils/browser/urls';

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

  onSelect: (type: PageType) => void;
  onExpand: (expanded: boolean) => void;
}

export const PageHeader = (props: IPageHeader) => {
  const items: PageLinkData[] = [
    { type: PageType.HOME, label: 'Home', url: urls.pola.home },
    { type: PageType.NEWS, label: 'Aktualności', url: urls.pola.news },
    { type: PageType.ABOUT, label: 'O Poli', url: urls.pola.about },
    { type: PageType.SUPPORT, label: 'Wesprzyj aplikację', url: urls.pola.support },
    { type: PageType.FRIENDS, label: 'Klub przyjaciół Poli', url: urls.pola.friends },
    { type: PageType.TEAM, label: 'Dołącz do zespołu', url: urls.pola.team },
    { type: PageType.FAQ, label: 'FAQ', url: urls.pola.faq },
    { type: PageType.CONTACT, label: 'Kontakt', url: urls.pola.contact },
  ];
  const navItems = items.map((item) => (
    <NavItem key={item.type} data={item} activePage={props.activePage} onClick={props.onSelect} />
  ));

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

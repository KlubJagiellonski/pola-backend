import React, { createRef } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';

import { PolaLogo } from '../Pola-Logo';
import { Device, mobileHeaderHeight, padding, color } from '../../styles/theme';

interface IHamburgerMenu {}

const HamburgerLayout = styled.nav`
  background: ${color.button.disabled};
  @media ${Device.desktop} {
    display: none;
  }

  flex: 1 1 100%;

  height: 100%;

  .nav-items {
    display: flex;
    flex-flow: column;
    gap: ${padding.normal};
    align-items: center;
    justify-content: center;
    .nav-item {
      font-weight: bolder;
      cursor: pointer;
    }
  }
`;

const Navbar = styled.div`
  display: flex;
  justify-content: space-between;
  padding: ${padding.small};

  height: ${mobileHeaderHeight};

  .menu-icon {
    cursor: pointer;
  }
`;

const Items = styled.div`
  overflow: hidden;
  height: 0;
  transition: height 0.5s;
  &.open {
    height: 400px;
  }
`;

export const HamburgerMenu: React.FC<IHamburgerMenu> = ({ children }) => {
  const itemsRef = createRef<HTMLDivElement>();

  const handleOpen = (e: React.MouseEvent<SVGSVGElement, MouseEvent>) => {
    const items = itemsRef.current;
    items?.classList.toggle('open');
  };

  return (
    <HamburgerLayout className="hamburger-menu">
      <Navbar>
        <PolaLogo />
        <FontAwesomeIcon icon={faBars} onClick={handleOpen} className="menu-icon" />
      </Navbar>
      <Items ref={itemsRef} className="nav-items">
        {children}
      </Items>
    </HamburgerLayout>
  );
};

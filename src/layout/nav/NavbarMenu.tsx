import React from 'react';
import { Link } from 'gatsby';
import styled from 'styled-components';

import { PolaLogo } from '../PolaLogo';
import { Device } from '../../styles/theme';
import { urls } from '../../domain/website';

interface INavbarMenu {}

const NavbarLayout = styled.nav`
  @media ${Device.mobile} {
    display: none;
  }

  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;

  flex: 1 1 100%;
  align-items: center;
  height: 100%;
`;

export const NavbarMenu: React.FC<INavbarMenu> = ({ children }) => (
  <NavbarLayout className="navbar-manu">
    <Link to={urls.pola.home}>
      <PolaLogo />
    </Link>
    {children}
  </NavbarLayout>
);

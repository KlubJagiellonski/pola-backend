import React from 'react';
import styled from 'styled-components';
import { pageWidth, theme } from '../styles/theme';
import { NavigationBar } from './Navigationbar';
import { PolaLogo } from './Pola-Logo';

interface IPageHeader {
  siteTitle?: string
}

const HeaderContainer = styled.header`
  display: flex;
  flex-flow: row nowrap;
  justify-content: center;
  background: ${theme.dark};
  margin-bottom: 1.45rem;
  min-height: 6rem;

  .header-container {
    display: flex;
    flex-flow: row nowrap;
    width: 100%;
    max-width: ${pageWidth};
  }
`;

export const PageHeader = (props: IPageHeader) => (
  <HeaderContainer>
    <div className="header-container">
      <PolaLogo />
      <NavigationBar />
    </div>
  </HeaderContainer>
);
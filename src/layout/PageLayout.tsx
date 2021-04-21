import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import { useStaticQuery, graphql } from 'gatsby';

import { PageHeader } from './PageHeader';
import { PageFooter } from './PageFooter';
import { desktopHeaderHeight, Device, mobileHeaderHeight } from '../styles/theme';
import './PageLayout.css';
import { Initialize } from '../state/app/app-actions';

const LayoutContainer = styled.div``;

const PageContent = styled.main`
  width: 100%;
  margin: 0 auto;
  padding: 0;

  @media ${Device.mobile} {
    padding-top: ${mobileHeaderHeight};
  }
  @media ${Device.desktop} {
    padding-top: ${desktopHeaderHeight};
  }
`;

interface IPageLayout {}

export const PageLayout: React.FC<IPageLayout> = ({ children }) => {
  const dispatch = useDispatch();

  const bootApplication = () => {
    dispatch(Initialize());
  };

  useEffect(() => {
    bootApplication();
  }, []);

  const data1 = useStaticQuery(graphql`
    query SiteTitleQuery {
      site {
        siteMetadata {
          title
        }
      }
    }
  `);

  return (
    <LayoutContainer>
      <PageHeader siteTitle={data1.site.siteMetadata.title} />
      <PageContent>{children}</PageContent>
      <PageFooter />
    </LayoutContainer>
  );
};

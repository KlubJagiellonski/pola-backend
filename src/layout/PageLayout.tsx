import React, { useEffect } from 'react';
import { connect, ConnectedProps } from 'react-redux';
import styled from 'styled-components';
import { useStaticQuery, graphql } from 'gatsby';

import { PageHeader } from './PageHeader';
import { PageFooter } from './PageFooter';
import { IPolaState } from '../state/types';
import { articlesDispatcher } from '../state/articles/articles-dispatcher';
import { friendsDispatcher } from './../state/friends/friends-dispatcher';
import { appDispatcher } from '../state/app/app-dispatcher';
import { ProductModal } from '../search/product-modal/ProductModal';
import { searchDispatcher } from '../state/search/search-dispatcher';
import ErrorBoundary from '../utils/error-boundary';

import { desktopHeaderHeight, Device, mobileHeaderHeight } from '../styles/theme';
import '../styles/pola-web.css';

const connector = connect(
  (state: IPolaState) => ({
    selectedProduct: state.search.selectedProduct,
  }),
  {
    initApp: appDispatcher.initialize,
    loadArticles: articlesDispatcher.loadArticles,
    loadFriends: friendsDispatcher.loadFriends,
    unselectProduct: searchDispatcher.unselectProduct,
  }
);

type ReduxProps = ConnectedProps<typeof connector>;

type IPageLayout = ReduxProps & {};

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

const Layout: React.FC<IPageLayout> = ({
  children,
  initApp,
  loadArticles,
  loadFriends,
  selectedProduct,
  unselectProduct,
}) => {
  const bootApplication = async () => {
    await initApp();
    await loadArticles();
    await loadFriends();
  };

  useEffect(() => {
    bootApplication();
  }, []);

  const data = useStaticQuery(graphql`
    query SiteTitleQuery {
      site {
        siteMetadata {
          title
        }
      }
    }
  `);

  return (
    <ErrorBoundary scope="page-layout">
      <LayoutContainer>
        {selectedProduct && <ProductModal product={selectedProduct} onClose={unselectProduct} />}
        <PageHeader siteTitle={data.site.siteMetadata.title} />
        <PageContent>{children}</PageContent>
        <PageFooter />
      </LayoutContainer>
    </ErrorBoundary>
  );
};

export const PageLayout = connector(Layout);

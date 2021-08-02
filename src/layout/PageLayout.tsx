import React from 'react';
import { connect, ConnectedProps } from 'react-redux';
import styled from 'styled-components';
import { useStaticQuery, graphql } from 'gatsby';

import { PageHeader } from './PageHeader';
import { PageFooter } from './PageFooter';
import { IPolaState } from '../state/types';
import { appDispatcher } from '../state/app/app-dispatcher';
import { ProductModal } from '../search/product-modal';
import { searchDispatcher } from '../state/search/search-dispatcher';
import ErrorBoundary from '../utils/error-boundary';
import { desktopHeaderHeight, Device, mobileHeaderHeight } from '../styles/theme';
import { StateLoader } from './StateLoader';
import '../styles/pola-web.css';
import Download from '../components/Download';

const connector = connect(
  (state: IPolaState) => ({
    activePage: state.app.activePage,
    isMenuExpanded: state.app.isMenuExpanded,
    selectedProduct: state.search.selectedProduct,
  }),
  {
    selectPage: appDispatcher.selectActivePage,
    expandMenu: appDispatcher.expandMenu,
    unselectProduct: searchDispatcher.unselectProduct,
  }
);

type ReduxProps = ConnectedProps<typeof connector>;

type IPageLayout = ReduxProps & {};

const LayoutContainer = styled.div`
  display: flex;
  flex-flow: column;
  height: 100vh;
`;

const PageContent = styled.main`
  width: 100%;
  margin: 0 auto;
  padding: 0;
  flex: 1 1 auto;

  @media ${Device.mobile} {
    padding-top: ${mobileHeaderHeight};
  }
  @media ${Device.desktop} {
    padding-top: ${desktopHeaderHeight};
  }
`;

const Layout: React.FC<IPageLayout> = ({
  activePage,
  isMenuExpanded,
  selectedProduct,
  children,

  selectPage,
  expandMenu,
  unselectProduct,
}) => {
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
      <StateLoader />
      <LayoutContainer>
        {selectedProduct && <ProductModal product={selectedProduct} onClose={unselectProduct} />}
        <PageHeader
          siteTitle={data.site.siteMetadata.title}
          activePage={activePage}
          onSelect={selectPage}
          isMenuExpanded={isMenuExpanded}
          onExpand={expandMenu}
        />
        <PageContent>{children}</PageContent>
        <Download />
        <PageFooter />
      </LayoutContainer>
    </ErrorBoundary>
  );
};

export const PageLayout = connector(Layout);

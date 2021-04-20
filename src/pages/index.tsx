import React from 'react';
import { connect } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';
import './index.css';
import { SearchContainer } from '../components/search';
import Contents from '../components/Contents';
import { PageSection } from '../layout/PageSection';
import { Device, pageWidth, padding, theme } from '../styles/theme';
import { SearchService } from '../services/search-service';
import { IPolaState } from '../state/types';
import { searchDispatcher } from '../state/search/search-dispatcher';

const Content = styled.div`
  width: 100%;
  margin: 0 auto;
  @media ${Device.mobile} {
    padding: ${padding.normal};
  }
  @media ${Device.desktop} {
    padding: ${padding.normal} 0;
    max-width: ${pageWidth};
  }
`;

interface IMainPage {
  searchResults: string[];

  invokeSearch: (phrase: string) => void;
}

const MainPage = (props: IMainPage) => {
  const { searchResults } = props;

  const load = async () => {
    const products = await SearchService.getProducts(10);
  };

  React.useEffect(() => {
    load();
  }, []);

  return (
    <PageLayout>
      <SEO title="Pola Web" />
      <PageSection size="full" backgroundColor={theme.dark}>
        <Content>
          <SearchContainer searchResults={searchResults} onSearch={props.invokeSearch} />
        </Content>
      </PageSection>
      <PageSection>
        <Contents />
      </PageSection>
    </PageLayout>
  );
};

export default connect(
  (state: IPolaState) => ({
    searchResults: state.search.results,
  }),
  {
    invokeSearch: searchDispatcher.invokeSearch,
  }
)(MainPage);

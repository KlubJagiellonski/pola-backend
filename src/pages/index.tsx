import React from 'react';
import { connect, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';
import './index.css';
import { SearchContainer } from '../components/search';
import Contents from '../components/Contents';
import { PageSection } from '../layout/PageSection';
import { Device, pageWidth, padding, color } from '../styles/theme';
import { IPolaState } from '../state/types';
import { searchDispatcher } from '../state/search/search-dispatcher';
import { LoadBrowserLocation } from '../state/app/app-actions';
import { IProduct } from '../products';

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
  location: Location;
  searchResults: IProduct[];
  articles?: IArticle[];

  invokeSearch: (phrase: string) => void;
}

const MainPage = (props: IMainPage) => {
  const { searchResults, location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(LoadBrowserLocation(location));
  }, []);

  return (
    <PageLayout>
      <SEO title="Pola Web" />
      <PageSection size="full" backgroundColor={color.dark}>
        <Content>
          <SearchContainer searchResults={searchResults} onSearch={props.invokeSearch} />
        </Content>
      </PageSection>
      <PageSection>
        <Contents articles={props.articles} />
      </PageSection>
    </PageLayout>
  );
};

export default connect(
  (state: IPolaState) => ({
    searchResults: state.search.results,
    articles: state.articles.data,
  }),
  {
    invokeSearch: searchDispatcher.invokeSearch,
  }
)(MainPage);

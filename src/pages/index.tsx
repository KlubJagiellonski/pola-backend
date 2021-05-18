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
import { IProductData } from '../domain/products';
import { IArticle } from '../domain/articles';

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
  searchResults: IProductData[];
  token?: string;
  articles?: IArticle[];

  invokeSearch: (phrase: string) => void;
  invokeLoadMore: () => void;
  selectProduct: (code: string) => void;
}

const MainPage = (props: IMainPage) => {
  const { searchResults, location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(LoadBrowserLocation(location));
  }, []);

  return (
    <PageLayout>
      <SEO title="Pola Web | Strona główna" />
      <PageSection size="full" backgroundColor={color.dark}>
        <Content>
          <SearchContainer
            searchResults={searchResults}
            onSearch={props.invokeSearch}
            token={props.token}
            onLoadMore={props.invokeLoadMore}
            onSelect={props.selectProduct}
          />
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
    searchResults: state.search.products,
    token: state.search.token,
    articles: state.articles.data,
  }),
  {
    invokeSearch: searchDispatcher.invokeSearch,
    invokeLoadMore: searchDispatcher.invokeLoadMore,
    selectProduct: searchDispatcher.selectProduct,
  }
)(MainPage);

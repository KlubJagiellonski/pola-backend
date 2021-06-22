import React from 'react';
import { connect, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';
import { PageSection } from '../layout/PageSection';
import { padding, margin, color, fontSize } from '../styles/theme';
import { IPolaState } from '../state/types';
import { searchDispatcher } from '../state/search/search-dispatcher';
import { LoadBrowserLocation } from '../state/app/app-actions';
import { IProductData } from '../domain/products';
import { IArticle } from '../domain/articles';
import { IFriend } from '../domain/friends';
import { SearchResultsList } from '../search/results-list/SearchResultsList';
import { PrimaryButton } from '../components/buttons/PrimaryButton';
import { ButtonColor } from '../styles/button-theme';
import { Spinner } from '../components/spinner';
import { navigate } from 'gatsby';

interface IProductsPage {
  location: Location;
  phrase: string;
  searchResults: IProductData[];
  token?: string;
  isLoading?: boolean;
  articles?: IArticle[];
  friends?: IFriend[];

  invokeSearch: (phrase: string) => void;
  onLoadMore: () => void;
  clearResults: () => void;
  selectProduct: (code: string, id: string) => void;
}

const ProductsPage = (props: IProductsPage) => {
  const { phrase, isLoading, searchResults, location, onLoadMore } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(LoadBrowserLocation(location));
  }, []);

  const emptyResults = !searchResults || searchResults.length < 1;
  if (emptyResults) {
    return null;
  }

  const loadButton = isLoading ? (
    <PrimaryButton icon={<Spinner styles={{ size: 30, color: color.button.white }} />} color={ButtonColor.Red} />
  ) : (
    <PrimaryButton label="Doładuj" color={ButtonColor.Red} onClick={onLoadMore} />
  );

  return (
    <PageLayout>
      <SEO title="Pola Web | Znalezione produkty" />
      {searchResults && (
        <PageSection>
          <SearchResultsList
            phrase={phrase}
            results={searchResults}
            isLoading={props.isLoading}
            token={props.token}
            actions={loadButton}
            onSelect={props.selectProduct}
          />
        </PageSection>
      )}
    </PageLayout>
  );
};

export default connect(
  (state: IPolaState) => ({
    phrase: state.search.phrase,
    searchResults: state.search.products,
    token: state.search.token,
    isLoading: state.search.isLoading,
    articles: state.articles.data,
    friends: state.friends.data,
  }),
  {
    invokeSearch: searchDispatcher.invokeSearch,
    onLoadMore: searchDispatcher.invokeLoadMore,
    clearResults: searchDispatcher.clearResults,
    selectProduct: searchDispatcher.selectProduct,
  }
)(ProductsPage);

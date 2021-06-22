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
import { State } from '../state/search/search-reducer';
import { SearchResultsHeader } from '../search/results-list/SearchResultsHeader';

interface IProductsPage {
  location: Location;
  phrase: string;
  searchResults: IProductData[];
  token?: string;
  searchState: State;
  articles?: IArticle[];
  friends?: IFriend[];

  invokeSearch: (phrase: string) => void;
  onLoadMore: () => void;
  clearResults: () => void;
  selectProduct: (code: string, id: string) => void;
}

const ProductsPage = (props: IProductsPage) => {
  const { phrase, searchResults, location, onLoadMore, searchState } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(LoadBrowserLocation(location));
  }, []);

  const emptyResults = !searchResults || searchResults.length < 1;
  if (emptyResults) {
    navigate('/');
    return null;
  }

  const loadButton =
    searchState === State.LOADING ? (
      <PrimaryButton
        disabled={true}
        icon={<Spinner styles={{ size: 20, color: color.button.white }} />}
        color={ButtonColor.Red}
      />
    ) : (
      <PrimaryButton label="Doładuj" color={ButtonColor.Red} onClick={onLoadMore} />
    );

  return (
    <PageLayout>
      <SEO title="Pola Web | Znalezione produkty" />
      <SearchResultsHeader phrase={phrase} searchResults={searchResults} searchState={searchState} />
      {searchResults && (
        <PageSection>
          <SearchResultsList results={searchResults} actions={loadButton} onSelect={props.selectProduct} />
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
    searchState: state.search.stateName,
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

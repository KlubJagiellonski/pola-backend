import React from 'react';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { PageSection } from '../layout/PageSection';
import { color } from '../styles/theme';
import { IPolaState } from '../state/types';
import { searchDispatcher } from '../state/search/search-dispatcher';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { IProductData } from '../domain/products';
import { IArticle } from '../domain/articles';
import { IFriend } from '../domain/friends';
import { SearchResultsList } from '../search/results-list/SearchResultsList';
import { PrimaryButton } from '../components/buttons/PrimaryButton';
import { ButtonColor } from '../styles/button-theme';
import { Spinner } from '../layout/Spinner';
import { SearchStateName } from '../state/search/search-reducer';
import { SearchResultsHeader } from '../search/results-list/SearchResultsHeader';
import { navigateTo } from '../utils/browser';
import { urls } from '../utils/browser/urls';
import { DevelopmentPlaceholder } from '../layout/DevelopmentPlaceholder';
import { PageType } from '../domain/generic';

interface IProductsPage {
  location?: Location;
  phrase: string;
  searchResults: IProductData[];
  token?: string;
  searchState: SearchStateName;
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
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.PRODUCTS));
    }
  }, []);

  const emptyResults = searchState === SearchStateName.INITIAL && (!searchResults || searchResults.length < 1);
  if (emptyResults) {
    navigateTo(urls.pola.home);
    return null;
  }

  const loadButton =
    searchState === SearchStateName.LOADING ? (
      <PrimaryButton
        disabled={true}
        icon={<Spinner styles={{ size: 20, color: color.button.white }} />}
        color={ButtonColor.Red}
      />
    ) : (
      <PrimaryButton label="Wczytaj więcej" color={ButtonColor.Red} onClick={onLoadMore} />
    );

  return (
    <PageLayout>
      <SEOMetadata title="Pola Web | Znalezione produkty" />
      <DevelopmentPlaceholder text="Lista produktów" />
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
    location: state.app.location,
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

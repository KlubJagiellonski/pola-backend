import React from 'react';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { searchDispatcher } from '../state/search/search-dispatcher';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { EAN, IProductData } from '../domain/products';
import { SearchStateName } from '../state/search/search-reducer';
import { navigateTo } from '../utils/browser';
import { DevelopmentPlaceholder } from '../layout/DevelopmentPlaceholder';
import { PageType, urls } from '../domain/website';
import { reduceToFlatProductsList } from '../domain/products/search-service';
import { DynamicProductResults } from '../search/results-list/DynamicProductResults';

interface IProductsPage {
  location?: Location;
  searchState: SearchStateName;
  searchResults?: {
    phrase: string;
    token: string;
    pages: IProductData[];
    totalItems: number;
  };

  onLoadMore: () => void;
  selectProduct: (code: EAN) => void;
}

const ProductsPage = (props: IProductsPage) => {
  const { location, searchState, searchResults, onLoadMore } = props;

  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.PRODUCTS));
    }
  }, []);

  if (!searchResults) {
    navigateTo(urls.pola.home);
    return null;
  }

  return (
    <PageLayout>
      <SEOMetadata pageTitle="Znalezione produkty" />
      <DevelopmentPlaceholder text="Lista produktów" />
      <DynamicProductResults
        {...searchResults}
        state={searchState}
        onSelect={props.selectProduct}
        onLoadMore={onLoadMore}
      />
    </PageLayout>
  );
};

export default connect(
  (state: IPolaState) => {
    const { app, search } = state;
    return {
      location: app.location,
      searchState: search.stateName,
      searchResults:
        search.stateName !== SearchStateName.INITIAL && search.stateName !== SearchStateName.LOADING
          ? {
              phrase: search.phrase,
              pages: reduceToFlatProductsList(search.resultPages),
              totalItems: search.totalItems,
              token: search.nextPageToken,
            }
          : undefined,
    };
  },
  {
    onLoadMore: searchDispatcher.invokeLoadMore,
    selectProduct: searchDispatcher.selectProduct,
  }
)(ProductsPage);

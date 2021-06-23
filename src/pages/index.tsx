import React from 'react';
import { connect, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';
import { SearchForm } from '../search/form/SearchForm';
import Contents from '../components/Contents';
import { PageSection } from '../layout/PageSection';
import { Device, pageWidth, padding, margin, color, fontSize } from '../styles/theme';
import { IPolaState } from '../state/types';
import { searchDispatcher } from '../state/search/search-dispatcher';
import { LoadBrowserLocation } from '../state/app/app-actions';
import { IProductData } from '../domain/products';
import { IArticle } from '../domain/articles';
import { ResponsiveImage } from '../components/responsive-image';
import { IFriend } from '../domain/friends';
import Download from '../components/Download';
import { SearchResultsList } from '../search/results-list/SearchResultsList';
import { PrimaryButton } from '../components/buttons/PrimaryButton';
import { SecondaryButton } from '../components/buttons/SecondaryButton';
import { ButtonColor } from '../styles/button-theme';
import { SearchResultsHeader } from '../search/results-list/SearchResultsHeader';
import { urls } from '../utils/browser/urls';
import { openNewTab } from '../utils/browser';
import { SearchStateName } from '../state/search/search-reducer';

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

const Background = styled.div<{ img?: string }>`
  position: absolute;
  top: 0px;
  left: 0px;
  bottom: 0px;
  right: 0px;

  div {
    width: 100%;
    height: 100%;
  }
`;

const MissingProductInfo = styled.div`
  background-color: ${color.background.red};
  color: ${color.text.light};
  text-align: center;
  font-size: ${fontSize.big};
  padding: ${padding.normal};
  margin-top: ${margin.big};
`;

interface IHomePage {
  location: Location;
  phrase: string;
  searchResults?: IProductData[];
  token?: string;
  searchState: string;
  articles?: IArticle[];
  friends?: IFriend[];

  invokeSearch: (phrase: string) => void;
  invokeLoadMore: () => void;
  clearResults: () => void;
  selectProduct: (code: string, id: string) => void;
}

const HomePage = (props: IHomePage) => {
  const { phrase, searchResults, location, searchState } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(LoadBrowserLocation(location));
  }, []);

  const handleCancel = () => {
    props.clearResults();
  };

  const emptyResults = !searchResults || searchResults.length < 1;
  const isLoading = searchState === SearchStateName.LOADING;

  return (
    <PageLayout>
      <SEO title="Pola Web | Strona główna" />
      <PageSection size="full" styles={{ backgroundColor: color.background.primary }}>
        <Background>
          <ResponsiveImage imageSrc={'background.png'} />
        </Background>
        <Content>
          <SearchForm onSearch={props.invokeSearch} />
        </Content>
      </PageSection>
      <SearchResultsHeader phrase={phrase} searchResults={searchResults} searchState={searchState} />
      {!emptyResults && (
        <PageSection>
          <SearchResultsList
            results={searchResults}
            actions={
              <PrimaryButton color={ButtonColor.Gray} onClick={handleCancel}>
                <span>Anuluj</span>
              </PrimaryButton>
            }
            onSelect={props.selectProduct}
          />
          <MissingProductInfo>
            <p>Nie znalazłeś czego szukasz?</p>
            <SecondaryButton
              onClick={() => openNewTab(urls.external.openFoods)}
              color={ButtonColor.Red}
              fontSize={fontSize.small}>
              Zgłoś produkt do bazy
            </SecondaryButton>
          </MissingProductInfo>
        </PageSection>
      )}
      <PageSection>
        <Contents articles={props.articles} friends={props.friends} />
      </PageSection>
      <PageSection size="full" styles={{ backgroundColor: color.background.black }}>
        <Download />
      </PageSection>
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
    invokeLoadMore: searchDispatcher.invokeLoadMore,
    clearResults: searchDispatcher.clearResults,
    selectProduct: searchDispatcher.selectProduct,
  }
)(HomePage);

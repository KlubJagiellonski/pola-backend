import React from 'react';
import { connect, ConnectedProps, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { SearchForm } from '../search/form/SearchForm';
import { PageSection } from '../layout/PageSection';
import { Device, pageWidth, padding, color } from '../styles/theme';
import { IPolaState } from '../state/types';
import { searchDispatcher } from '../state/search/search-dispatcher';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { ResponsiveImage } from '../components/images/ResponsiveImage';
import { PageType, urls } from '../domain/website';
import { Article } from '../domain/articles';
import { reduceToFlatProductsList } from '../domain/products/search-service';
import { SearchStateName } from '../state/search/search-reducer';
import { FirstPageResults } from '../search/results-list/FirstPageResults';
import { EAN, ISearchResults } from '../domain/products';
import { Friend } from '../domain/friends';
import { appDispatcher } from '../state/app/app-dispatcher';
import DevelopmentSection from '../components/DevelopmentSection';
import SocialMedia from '../components/social-media/SocialMedia';
import Friends from '../components/friends/Friends';
import Teams from '../components/Teams';
import About from '../components/About';
import TeamsFriend from '../components/TeamsFriend';
import ArticlesListPreview from '../components/articles/list/ArticlesListPrewiev';
import { InfoBox } from '../components/InfoBox';
import { SearchResultsHeader } from '../search/results-list/SearchResultsHeader';

const connector = connect(
  (state: IPolaState) => {
    const { search, articles, friends } = state;
    return {
      searchState: search.stateName,
      searchResults:
        search.stateName === SearchStateName.LOADED || search.stateName === SearchStateName.SELECTED
          ? {
              phrase: search.phrase,
              products: reduceToFlatProductsList(search.resultPages),
              totalItems: search.totalItems,
              token: search.nextPageToken,
            }
          : undefined,
      articles: articles.data,
      friends: friends.data,
    };
  },
  {
    toggleSearchInfo: appDispatcher.toggleSearchInfo,
    invokeSearch: searchDispatcher.invokeSearch,
    invokeLoadMore: searchDispatcher.invokeLoadMore,
    clearResults: searchDispatcher.clearResults,
    selectProduct: searchDispatcher.selectProduct,
  }
);

type ReduxProps = ConnectedProps<typeof connector>;

const Content = styled.div`
  width: 100%;
  margin: 0 auto;
  box-sizing: border-box;

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
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;

  div {
    width: 100%;
    height: 100%;
  }

  opacity: 0.4;
`;

const WrapperContents = styled(PageSection)`
  @media ${Device.mobile} {
    padding: 0;
  }
`;

const Wrapper = styled.div`
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  overflow-x: hidden;
  padding-top: ${padding.normal};
  display: grid;
  grid-gap: 15px;
  grid-template-areas:
    'articles development'
    'articles social-media'
    'articles about'
    'friends friends'
    'teams-friend teams';

  @media ${Device.mobile} {
    margin: 0;
    padding: 0;
    grid-gap: 0px;
    grid-template-areas:
      'development'
      'articles'
      'about'
      'social-media'
      'friends'
      'teams-friend'
      'teams';
  }
`;

type IHomePage = ReduxProps & {
  location?: Location;
  searchState: SearchStateName;
  searchResults?: ISearchResults;
  articles?: Article[];
  activeTags: string[];
  friends?: Friend[];

  toggleSearchInfo: () => void;
  invokeSearch: (phrase: string) => void;
  invokeLoadMore: () => void;
  clearResults: () => void;
  selectProduct: (code: EAN) => void;
};

const HomePage = (props: IHomePage) => {
  const { location, searchState, searchResults } = props;
  const dispatch = useDispatch();
  const freshArticles = props.articles?.slice(0, 3);
  const isLoaded = searchState === SearchStateName.LOADED || searchState === SearchStateName.SELECTED;
  const isLoading = searchState === SearchStateName.LOADING;
  const isError = searchState === SearchStateName.ERROR;

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.HOME));
      props.clearResults();
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle="Strona główna" />
      <PageSection size="full" styles={{ backgroundColor: color.background.search }}>
        <Background>
          <ResponsiveImage imageSrc={'background2.jpg'} />
        </Background>
        <Content>
          <SearchForm
            onInfoClicked={props.toggleSearchInfo}
            onSearch={props.invokeSearch}
            onEmptyInput={props.clearResults}
            isLoading={isLoading}
          />
        </Content>
      </PageSection>
      <PageSection>
        {(isLoaded || isLoading) && (
          <SearchResultsHeader
            phrase={searchResults?.phrase}
            totalItems={searchResults?.totalItems}
            searchState={searchState}
            resultsUrl={searchResults && searchResults.totalItems > 0 ? urls.pola.products() : undefined}
          />
        )}
        {searchResults && (
          <FirstPageResults
            {...searchResults}
            isLoaded={isLoaded}
            isLoading={isLoading}
            onSelect={props.selectProduct}
            onClear={props.clearResults}
          />
        )}
        {isError && (
          <InfoBox>
            <h3>Błąd Wyszukiwania</h3>
            <p>Spróbuj wprowadzić inną frazę...</p>
          </InfoBox>
        )}
      </PageSection>
      <WrapperContents>
        <Wrapper>
          <ArticlesListPreview articles={freshArticles} />
          <DevelopmentSection />
          <SocialMedia />
          <About />
          <Friends friends={props.friends} />
          <Teams />
          <TeamsFriend />
        </Wrapper>
      </WrapperContents>
    </PageLayout>
  );
};

export default connector(HomePage);

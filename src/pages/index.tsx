import React from 'react';
import { connect, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';
import { SearchContainer } from '../search/form/SearchForm';
import Contents from '../components/Contents';
import { PageSection } from '../layout/PageSection';
import { Device, pageWidth, padding, margin, color, fontSize, lineHeight } from '../styles/theme';
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
import { ProductCounter } from '../search/results-list/ProductCounter';
import { Link } from 'gatsby';
import { Spinner } from '../components/spinner';

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

const Header = styled.header`
  font-size: ${fontSize.big};
  font-weight: bold;
  line-height: ${lineHeight.big};
`;

interface IMainPage {
  location: Location;
  phrase: string;
  searchResults?: IProductData[];
  token?: string;
  isLoading?: boolean;
  articles?: IArticle[];
  friends?: IFriend[];

  invokeSearch: (phrase: string) => void;
  invokeLoadMore: () => void;
  clearResults: () => void;
  selectProduct: (code: string, id: string) => void;
}

const MainPage = (props: IMainPage) => {
  const { phrase, searchResults, location, isLoading } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(LoadBrowserLocation(location));
  }, []);

  const redirectToOpenFoods = () => {
    window.location.href = 'https://pl.openfoodfacts.org/';
  };

  const handleCancel = () => {
    props.clearResults();
  };

  const emptyResults = !searchResults || searchResults.length < 1;

  return (
    <PageLayout>
      <SEO title="Pola Web | Strona główna" />
      <PageSection size="full" styles={{ backgroundColor: color.background.primary }}>
        <Background>
          <ResponsiveImage imageSrc={'background.png'} />
        </Background>
        <Content>
          <SearchContainer onSearch={props.invokeSearch} />
        </Content>
      </PageSection>
      <SearchResultsHeader phrase={phrase} searchResults={searchResults} isLoading={isLoading} />
      {!emptyResults && (
        <PageSection>
          <SearchResultsList
            phrase={phrase}
            results={searchResults}
            isLoading={props.isLoading}
            token={props.token}
            actions={
              <PrimaryButton color={ButtonColor.Gray} onClick={handleCancel}>
                <span>Anuluj</span>
              </PrimaryButton>
            }
            onSelect={props.selectProduct}
          />
          <MissingProductInfo>
            <p>Nie znalazłeś czego szukasz?</p>
            <SecondaryButton onClick={redirectToOpenFoods}>Zgłoś produkt do bazy</SecondaryButton>
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

interface ISearchResultsHeader {
  phrase: string;
  searchResults?: IProductData[];
  isLoading?: boolean;
}

const SearchResultsHeader: React.FC<ISearchResultsHeader> = ({ phrase, searchResults, isLoading }) => {
  const emptyResults = !searchResults || searchResults.length < 1;
  let header: React.ReactNode;
  if (!phrase && !searchResults && !isLoading) {
    return null;
  }

  if (isLoading) {
    header = <Spinner text="Wyszukiwanie produktów..." />;
  }

  if (emptyResults && !isLoading) {
    header = <Header>Nie znaleziono produktów</Header>;
  }

  if (!header) {
    header = (
      <>
        <Header>Uzyskano</Header>
        <Link to="/products">
          <ProductCounter phrase={phrase} amount={searchResults?.length || 0} />
        </Link>
      </>
    );
  }

  return <PageSection styles={{ textAlign: isLoading ? 'center' : 'left' }}>{header}</PageSection>;
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
    invokeLoadMore: searchDispatcher.invokeLoadMore,
    clearResults: searchDispatcher.clearResults,
    selectProduct: searchDispatcher.selectProduct,
  }
)(MainPage);

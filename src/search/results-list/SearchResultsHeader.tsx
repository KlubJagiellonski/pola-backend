import React from 'react';
import styled from 'styled-components';
import { PageSection } from '../../layout/PageSection';
import { IProductData } from '../../domain/products';
import { Spinner } from '../../components/Spinner';
import { ProductCounter } from './ProductCounter';
import { Link } from 'gatsby';
import { fontSize, lineHeight, margin } from '../../styles/theme';
import { SearchStateName } from '../../state/search/search-reducer';
import { PageType } from '../../domain/generic';

const Header = styled.header`
  font-size: ${fontSize.big};
  font-weight: bold;
  line-height: ${lineHeight.normal};
  margin: ${margin.normal} 0 ${margin.small} 0;
`;

interface ISearchResultsHeader {
  searchState: SearchStateName;
  phrase: string;
  searchResults?: IProductData[];
  resultsUrl?: string;

  setActivePage?: (type: PageType) => void;
}

export const SearchResultsHeader: React.FC<ISearchResultsHeader> = ({
  searchState,
  phrase,
  searchResults,
  resultsUrl,
  setActivePage,
}) => {
  const isLoading = searchState === SearchStateName.LOADING;
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
    const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
      if (setActivePage) {
        setActivePage(PageType.PRODUCTS);
      }
    };

    header = (
      <>
        <Header>Uzyskano</Header>
        {resultsUrl ? (
          <Link to={resultsUrl} onClick={handleClick}>
            <ProductCounter phrase={phrase} amount={searchResults?.length || 0} />
          </Link>
        ) : (
          <ProductCounter phrase={phrase} amount={searchResults?.length || 0} />
        )}
      </>
    );
  }

  return <PageSection styles={{ textAlign: isLoading ? 'center' : 'left' }}>{header}</PageSection>;
};

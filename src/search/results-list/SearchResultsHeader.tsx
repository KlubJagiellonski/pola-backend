import React from 'react';
import styled from 'styled-components';
import { PageSection } from '../../layout/PageSection';
import { IProductData } from '../../domain/products';
import { Spinner } from '../../layout/Spinner';
import { ProductCounter } from './ProductCounter';
import { Link } from 'gatsby';
import { fontSize, lineHeight, margin } from '../../styles/theme';
import { SearchStateName } from '../../state/search/search-reducer';

const Header = styled.header`
  font-size: ${fontSize.big};
  font-weight: bold;
  line-height: ${lineHeight.normal};
  margin-top: ${margin.normal};
`;

interface ISearchResultsHeader {
  searchState: SearchStateName;
  phrase: string;
  searchResults?: IProductData[];
  resultsUrl?: string;
}

export const SearchResultsHeader: React.FC<ISearchResultsHeader> = ({
  searchState,
  phrase,
  searchResults,
  resultsUrl,
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
    header = (
      <>
        <Header>Uzyskano</Header>
        {resultsUrl ? (
          <Link to={resultsUrl}>
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

import React from 'react';
import { PageSection } from '../../layout/PageSection';
import { IProductData } from '../../domain/products';
import { Spinner } from '../../components/spinner';
import { ProductCounter } from './ProductCounter';
import { Link } from 'gatsby';
import { fontSize, lineHeight } from '../../styles/theme';
import styled from 'styled-components';
import { State } from '../../state/search/search-reducer';

const Header = styled.header`
  font-size: ${fontSize.big};
  font-weight: bold;
  line-height: ${lineHeight.big};
`;

interface ISearchResultsHeader {
  searchState: State;
  phrase: string;
  searchResults?: IProductData[];
}

export const SearchResultsHeader: React.FC<ISearchResultsHeader> = ({ searchState, phrase, searchResults }) => {
  const isLoading = searchState === State.LOADING;
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

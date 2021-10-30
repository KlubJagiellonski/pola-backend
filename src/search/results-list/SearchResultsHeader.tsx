import React from 'react';
import styled from 'styled-components';
import { PageSection } from '../../layout/PageSection';
import { Spinner } from '../../components/Spinner';
import { ProductCounter } from './ProductCounter';
import { Link } from 'gatsby';
import { fontSize, lineHeight, margin } from '../../styles/theme';
import { SearchStateName } from '../../state/search/search-reducer';
import { PageType } from '../../domain/website';

const Header = styled.header`
  font-size: ${fontSize.big};
  font-weight: bold;
  line-height: ${lineHeight.normal};
  margin: ${margin.normal} 0 ${margin.small} 0;
`;

interface ISearchResultsHeader {
  searchState: SearchStateName;
  phrase: string;
  totalItems: number;
  resultsUrl?: string;

  setActivePage?: (type: PageType) => void;
}

export const SearchResultsHeader: React.FC<ISearchResultsHeader> = ({
  phrase,
  totalItems,
  resultsUrl,
  setActivePage,
}) => {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    if (setActivePage) {
      setActivePage(PageType.PRODUCTS);
    }
  };

  return (
    <PageSection styles={{ textAlign: 'left' }}>
      <Header>Uzyskano</Header>
      {resultsUrl ? (
        <Link to={resultsUrl} onClick={handleClick}>
          <ProductCounter phrase={phrase} amount={totalItems} />
        </Link>
      ) : (
        <ProductCounter phrase={phrase} amount={totalItems} />
      )}
    </PageSection>
  );
};

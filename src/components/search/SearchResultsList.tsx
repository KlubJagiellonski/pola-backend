import React from 'react';
import styled from 'styled-components';
import { IProduct } from '../../products';
import { SearchResultElement } from './SearchResultElement';

const ResultsList = styled.div`
  ul {
    list-style: none;
  }
`;

interface ISearchResultsList {
  results: IProduct[];
}

export const SearchResultsList: React.FC<ISearchResultsList> = ({ results }) => (
  <ResultsList>
    <header>
      <h2>Uzyskano</h2>
      <span>{`${results.length} wyniki`}</span>
    </header>
    <ul>
      {results.map((product: IProduct) => (
        <SearchResultElement product={product} key={product.id} />
      ))}
    </ul>
  </ResultsList>
);

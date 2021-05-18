import React from 'react';
import styled from 'styled-components';
import { IProductData } from '../../domain/products';
import { SearchResultElement } from './SearchResultElement';

const ResultsList = styled.div`
  ul {
    list-style: none;
  }
`;

interface ISearchResultsList {
  results: IProductData[];
  token?: string;

  onLoadMore?: () => void;
  onSelect: (code: string) => void;
}

export const SearchResultsList: React.FC<ISearchResultsList> = ({ results, token, onLoadMore, onSelect }) => {
  return (
    <ResultsList>
      <header>
        <h2>Uzyskano</h2>
        <span>{`${results.length} wyniki`}</span>
      </header>
      <ul>
        {results.map((product: IProductData, index: number) => (
          <SearchResultElement product={product} key={product.code} onSelect={onSelect} />
        ))}
      </ul>
      {token && <button onClick={onLoadMore}>Doładuj</button>}
    </ResultsList>
  );
};

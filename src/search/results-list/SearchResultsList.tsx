import React from 'react';
import styled from 'styled-components';
import { EAN, IProductData } from '../../domain/products';
import { margin } from '../../styles/theme';
import { SearchResultElement } from './ProductElement';

const ResultsList = styled.div`
  display: flex;
  flex-flow: column;
  align-items: center;

  .products-list {
    padding: 0;
    list-style: none;
    max-width: 50em;
  }

  .actions {
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;
    margin-bottom: ${margin.normal};
  }
`;

interface ISearchResultsList {
  results?: IProductData[];
  totalItems: number;
  actions?: React.ReactNode | React.ReactNode[];

  onSelect: (code: EAN) => void;
}

export const SearchResultsList: React.FC<ISearchResultsList> = ({ results, actions, onSelect }) => {
  if (!results) {
    return null;
  }

  return (
    <ResultsList>
      <ul className="products-list">
        {results.map((product: IProductData) => (
          <SearchResultElement product={product} key={product.code} onSelect={onSelect} />
        ))}
      </ul>
      {actions && <div className="actions">{actions}</div>}
    </ResultsList>
  );
};

import React from 'react';
import styled from 'styled-components';
import { IProductData } from '../../domain/products';
import { SearchResultElement } from './ProductElement';

const ResultsList = styled.div`
  .products-list {
    padding: 0;
    list-style: none;
  }

  .actions {
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;
  }
`;

interface ISearchResultsList {
  phrase: string;
  results?: IProductData[];
  token?: string;
  isLoading?: boolean;
  actions?: React.ReactNode | React.ReactNode[];

  onSelect: (code: string, id: string) => void;
}

export const SearchResultsList: React.FC<ISearchResultsList> = ({
  phrase,
  results,
  token,
  isLoading,
  actions,
  onSelect,
}) => {
  if (!results) {
    return null;
  }

  return (
    <ResultsList>
      <ul className="products-list">
        {results.map((product: IProductData, index: number) => (
          <SearchResultElement product={product} key={product.code} onSelect={onSelect} />
        ))}
      </ul>
      {actions && <div className="actions">{actions}</div>}
    </ResultsList>
  );
};

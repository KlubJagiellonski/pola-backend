import React from 'react';
import styled from 'styled-components';
import { IProductData } from '../../domain/products';
import { padding, color } from '../../styles/theme';
import { ProductScore } from '../ProductScore';

const ListElement = styled.li`
  margin-bottom: ${padding.normal};
  background-color: ${color.background.primary};
  box-shadow: 2px 2px 8px ${color.background.dark};
`;

const ResultElement = styled.div`
  display: flex;
  flex-flow: column;
  padding: ${padding.small} ${padding.normal};
  line-height: 1.7em;
  cursor: pointer;

  .company,
  .brand {
    font-size: 0.8em;
    line-height: 1.5em;
  }
`;

interface ISearchResultElement {
  product: IProductData;
  onSelect: (code: string, id: string) => void;
}

export const SearchResultElement: React.FC<ISearchResultElement> = ({ product, onSelect }) => (
  <ListElement onClick={e => onSelect(product.code, product.id)}>
    <ResultElement>
      <span className="name">
        {product.name} | {product.code}
      </span>
      {product.company && <span className="company">{product.company.name}</span>}
      {product.brand && <span className="brand">{product.brand.name}</span>}
    </ResultElement>
    <ProductScore value={product.score} />
  </ListElement>
);

import React from 'react';
import styled from 'styled-components';
import { IProductData } from '../../domain/products';
import { padding, color, fontSize, lineHeight } from '../../styles/theme';
import { ProductScore } from '../ProductScore';

const ListElement = styled.li`
  margin-bottom: ${padding.normal};
  background-color: ${color.background.gray};
`;

const ResultElement = styled.div`
  display: flex;
  flex-flow: column;
  padding: ${padding.small} ${padding.normal};
  cursor: pointer;

  .manufacturer {
    font-weight: bold;
    text-transform: uppercase;
  }
  .manufacturer,
  .brand,
  .name {
    font-size: ${fontSize.small};
    line-height: ${lineHeight.normal};
  }
`;

interface ISearchResultElement {
  product: IProductData;
  onSelect: (code: string, id: string) => void;
}

export const SearchResultElement: React.FC<ISearchResultElement> = ({ product, onSelect }) => (
  <ListElement onClick={e => onSelect(product.code, product.id)}>
    <ResultElement>
      {product.company && <span className="manufacturer">{product.company.name}</span>}
      {product.brand && <span className="brand">{product.brand.name}</span>}
      <span className="name">{product.name}</span>
    </ResultElement>
    <ProductScore value={product.score} />
  </ListElement>
);

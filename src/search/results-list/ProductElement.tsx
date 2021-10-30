import React from 'react';
import styled from 'styled-components';
import { EAN, IProductData } from '../../domain/products';
import { padding, color, fontSize, lineHeight } from '../../styles/theme';
import { ScoreBar } from '../../components/ScoreBar';

const ListElement = styled.li`
  max-width: 40em;
  margin-bottom: ${padding.normal};
  background-color: ${color.background.gray};
  cursor: pointer;
`;

const ResultElement = styled.div`
  display: flex;
  flex-flow: column;
  padding: ${padding.normal} ${padding.normal};

  .name {
    font-size: ${fontSize.normal};
    font-weight: bold;
    margin-bottom: 0.5em;
  }
  .manufacturer,
  .brand {
    font-size: ${fontSize.small};
    line-height: ${lineHeight.normal};
  }
`;

interface ISearchResultElement {
  product: IProductData;
  onSelect: (code: EAN) => void;
}

export const SearchResultElement: React.FC<ISearchResultElement> = ({ product, onSelect }) => (
  <ListElement onClick={(e) => onSelect(product.code)}>
    <ResultElement>
      <span className="name">{product.name}</span>
      {product.brand && <span className="brand">{product.brand.name}</span>}
      {product.company && <span className="manufacturer">{product.company.name}</span>}
    </ResultElement>
    <ScoreBar value={product.company?.score || 0} unit="pkt" animation={{ duration: 1, delay: 0.2 }} />
  </ListElement>
);

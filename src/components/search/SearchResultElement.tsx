import React from 'react';
import styled from 'styled-components';
import { IProduct } from '../../products';
import { padding, color } from '../../styles/theme';

const ListElement = styled.li`
  margin-bottom: ${padding.tiny};
  padding: ${padding.small} ${padding.normal};
  background-color: ${color.border};
`;

const ResultElement = styled.div`
  display: flex;
  flex-flow: column;
  line-height: 1.7em;

  .manufacturer {
    text-transform: uppercase;
  }
`;

interface ISearchResultElement {
  product: IProduct;
}

export const SearchResultElement: React.FC<ISearchResultElement> = ({ product }) => (
  <ListElement>
    <ResultElement>
      <span className="manufacturer">{product.category}</span>
      <span className="brand">{product.title}</span>
      <span className="name">{product.description}</span>
    </ResultElement>
  </ListElement>
);

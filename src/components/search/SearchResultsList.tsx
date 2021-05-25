import React from 'react';
import styled from 'styled-components';
import { IProductData } from '../../domain/products';
import { ButtonColor } from '../buttons/Button';
import { PrimaryButton } from '../buttons/PrimaryButton';
import { SearchResultElement } from './SearchResultElement';
import { color } from '../../styles/theme';
import { Spinner } from '../icons/spinner';

const ResultsList = styled.div`
  ul {
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
  results: IProductData[];
  token?: string;
  isLoading?: boolean;

  onLoadMore?: () => void;
  onSelect: (code: string, id: number) => void;
}

export const SearchResultsList: React.FC<ISearchResultsList> = ({
  results,
  token,
  isLoading,
  onLoadMore,
  onSelect,
}) => {
  const loadButton = isLoading ? (
    <PrimaryButton icon={<Spinner color={color.text.light} size={100} timeout={0} />} color={ButtonColor.Red} />
  ) : (
    <PrimaryButton label="Doładuj" color={ButtonColor.Red} onClick={onLoadMore} />
  );

  return (
    <ResultsList>
      <ProductCounter amount={results.length} />
      <ul>
        {results.map((product: IProductData, index: number) => (
          <SearchResultElement product={product} key={product.code} onSelect={onSelect} />
        ))}
      </ul>
      {token && <div className="actions">{loadButton}</div>}
    </ResultsList>
  );
};

interface IProductCounter {
  amount: number;
}

const ProductCounter: React.FC<IProductCounter> = ({ amount }) => {
  let text: string;
  switch (amount) {
    case 0:
      text = `Nie znaleziono produktów`;
      break;
    case 1:
      text = `Znaleziono 1 produkt`;
      break;
    case 2:
    case 3:
    case 4:
      text = `Znaleziono ${amount} produty`;
      break;
    default:
      text = `Znaleziono ${amount} produktów`;
  }

  return (
    <header>
      <h4>{text}</h4>
    </header>
  );
};

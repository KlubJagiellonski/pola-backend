import React from 'react';
import styled from 'styled-components';
import Loader from 'react-loader-spinner';
import { IProductData } from '../../domain/products';
import { ButtonColor, PrimaryButton } from '../buttons/PrimaryButton';
import { SearchResultElement } from './SearchResultElement';

const ResultsList = styled.div`
  ul {
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
  onSelect: (code: string) => void;
}

export const SearchResultsList: React.FC<ISearchResultsList> = ({
  results,
  token,
  isLoading,
  onLoadMore,
  onSelect,
}) => {
  const loadButton = isLoading ? (
    <PrimaryButton
      icon={
        <Loader
          type="Puff"
          color="#00BFFF"
          height={100}
          width={100}
          timeout={3000} //3 secs
        />
      }
      color={ButtonColor.Red}
    />
  ) : (
    <PrimaryButton label="Doładuj" color={ButtonColor.Red} onClick={onLoadMore} />
  );

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
      {token && <div className="actions">{loadButton}</div>}
    </ResultsList>
  );
};

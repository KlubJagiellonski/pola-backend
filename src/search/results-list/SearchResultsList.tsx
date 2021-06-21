import React from 'react';
import styled from 'styled-components';
import { IProductData } from '../../domain/products';
import { ButtonColor } from '../../styles/button-theme';
import { PrimaryButton } from '../../components/buttons/PrimaryButton';
import { SearchResultElement } from './ProductElement';
import { color, fontSize, lineHeight } from '../../styles/theme';
import { Spinner } from '../../components/spinner';
import { ProductCounter } from './ProductCounter';
import { Link } from 'gatsby';

const Header = styled.header`
  font-size: ${fontSize.big};
  font-weight: bold;
  line-height: ${lineHeight.big};
`;

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
  phrase: string;
  results: IProductData[];
  token?: string;
  isLoading?: boolean;

  onLoadMore?: () => void;
  onSelect: (code: string, id: string) => void;
}

export const SearchResultsList: React.FC<ISearchResultsList> = ({
  phrase,
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

  const emptyResults = results.length < 1;

  return (
    <ResultsList>
      {emptyResults ? (
        <Header>Nie znaleziono produktów</Header>
      ) : (
        <>
          <Header>Uzyskano</Header>
          <Link>
            <ProductCounter phrase={phrase} amount={results.length} />
          </Link>
          <ul>
            {results.map((product: IProductData, index: number) => (
              <SearchResultElement product={product} key={product.code} onSelect={onSelect} />
            ))}
          </ul>
        </>
      )}
    </ResultsList>
  );
};

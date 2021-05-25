import React from 'react';
import styled from 'styled-components';
import { SearchResultsList } from './SearchResultsList';
import { IProductData } from '../../domain/products';
import { SearchInput } from './SearchInput';
import ErrorBoundary from '../../utils/error-boundary';
import { Device } from '../../styles/theme';

export const Wrapper = styled.div`
  width: 100%;
  padding: 260px 0 70px 0;
  position: relative;

  @media ${Device.mobile} {
    padding: 100px 0 20px 0;
    display: flex;
    align-items: center;
    flex-direction: column;
  }
`;

interface ISearchContainer {
  searchResults: IProductData[];
  token?: string;
  isLoading?: boolean;

  onSearch: (phrase: string) => void;
  onLoadMore: () => void;
  onSelect: (code: string, id: number) => void;
}

export const SearchContainer: React.FC<ISearchContainer> = ({
  searchResults,
  token,
  isLoading,
  onSearch,
  onLoadMore,
  onSelect,
}) => {
  const handleLoad = () => onLoadMore();

  return (
    <ErrorBoundary scope="search-container">
      <Wrapper>
        <SearchInput onSearch={onSearch} />
        {searchResults && (
          <SearchResultsList
            results={searchResults}
            token={token}
            isLoading={isLoading}
            onLoadMore={handleLoad}
            onSelect={onSelect}
          />
        )}
      </Wrapper>
    </ErrorBoundary>
  );
};

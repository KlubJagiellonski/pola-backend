import React from 'react';
import styled from 'styled-components';
import { SearchInput } from './SearchInput';
import ErrorBoundary from '../../utils/error-boundary';
import { Device, fontSize, color } from '../../styles/theme';
import { TitleSection } from '../../styles/GlobalStyle.css';

const Container = styled.div`
  display: flex;
  flex-flow: column;
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

const Title = styled(TitleSection)`
  width: 20%;
  float: left;
  text-align: center;
  margin: 0;

  @media ${Device.mobile} {
    width: 100%;
    margin-bottom: 20px;
  }
`;

const Text = styled.div`
  display: flex;
  flex-flow: column;
  margin: 10px 0;
  padding: 0;
  font-family: 'Roboto';
  font-size: ${fontSize.small};
  text-align: left;
  line-height: 1rem;
  color: ${color.text.secondary};

  @media ${Device.mobile} {
    font-size: 12px;
  }

  a {
    color: ${color.text.red};
  }
`;

interface ISearchContainer {
  isLoading?: boolean;
  onSearch: (phrase: string) => void;
}

export const SearchContainer: React.FC<ISearchContainer> = ({ isLoading, onSearch }) => {
  return (
    <ErrorBoundary scope="search-container">
      <Container>
        <Title>Sprawdź informacje o produkcie</Title>
        <Text>
          <span>Wpisz tekst, podyktuj lub zeskanuj kod</span>
          <span>
            Nie znasz kodu?
            <a target="blank" href="https://pl.openfoodfacts.org/">
              Znajdź go w bazie
            </a>
          </span>
        </Text>
        <SearchInput onSearch={onSearch} isLoading={isLoading} />
      </Container>
    </ErrorBoundary>
  );
};

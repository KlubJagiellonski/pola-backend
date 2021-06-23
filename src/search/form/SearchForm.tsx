import React from 'react';
import styled from 'styled-components';
import { SearchInput } from './SearchInput';
import ErrorBoundary from '../../utils/error-boundary';
import { Device, fontSize, color, margin } from '../../styles/theme';
import { TitleSection } from '../../styles/GlobalStyle.css';
import { GooglePlayLink, AppStoreLink } from '../../components/links';
import { urls } from '../../utils/browser/urls';

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

const SearchWrapper = styled.div`
  margin-top: ${margin.normal};
  display: flex;
  flex-flow: column;
  gap: ${margin.small};

  @media ${Device.desktop} {
    flex-flow: row nowrap;
  }

  .mobile-apps {
    display: flex;
    flex-flow: row nowrap;
    gap: ${margin.small};
    justify-content: space-between;
  }
`;

interface ISearchForm {
  onSearch: (phrase: string) => void;
}

export const SearchForm: React.FC<ISearchForm> = ({ onSearch }) => {
  return (
    <ErrorBoundary scope="search-container">
      <Container>
        <Title>Sprawdź informacje o produkcie</Title>
        <Text>
          <span>Wpisz tekst, podyktuj lub zeskanuj kod</span>
          <span>
            Nie znasz kodu?&nbsp;
            <a target="blank" href={urls.external.openFoods.href}>
              Znajdź go w bazie
            </a>
          </span>
        </Text>
        <SearchWrapper>
          <SearchInput onSearch={onSearch} />
          <div className="mobile-apps">
            <AppStoreLink height={44} />
            <GooglePlayLink height={44} />
          </div>
        </SearchWrapper>
      </Container>
    </ErrorBoundary>
  );
};

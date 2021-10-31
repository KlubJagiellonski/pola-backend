import React from 'react';
import styled from 'styled-components';
import { SearchInput } from './SearchInput';
import ErrorBoundary from '../../utils/error-boundary';
import { Device, fontSize, color, margin, lineHeight } from '../../styles/theme';
import { TitleSection } from '../../styles/GlobalStyle.css';
import { GooglePlayLink, AppStoreLink } from '../../components/links';
import { urls } from '../../domain/website';

const Container = styled.div`
  display: flex;
  flex-flow: column;
  width: 100%;
  padding-top: 260px;
  padding-bottom: 70px;
  position: relative;
  text-align: left;

  @media ${Device.mobile} {
    padding: 100px 0 20px 0;
    display: flex;
    align-items: center;
    flex-direction: column;
  }
`;

const Title = styled(TitleSection)`
  font-size: ${fontSize.big};
  line-height: ${lineHeight.big};
  text-align: left;
  margin: 0;

  @media ${Device.mobile} {
    width: 100%;
    text-align: center;
    margin-bottom: ${margin.normal};
  }
`;

const Text = styled.div`
  display: flex;
  flex-flow: column;
  margin: ${margin.small} 0;
  padding: 0;
  font-size: ${fontSize.normal};
  text-align: left;
  line-height: ${lineHeight.big};
  color: ${color.text.secondary};

  @media ${Device.mobile} {
    text-align: center;
    font-size: ${fontSize.small};
    line-height: ${lineHeight.normal};
  }

  a {
    color: ${color.text.red};
  }
`;

const SearchWrapper = styled.div`
  margin-top: ${margin.normal};
  display: flex;
  flex-flow: column;
  gap: ${margin.normal};
  width: 100%;

  @media ${Device.desktop} {
    flex-flow: row nowrap;
    justify-content: center;
    width: 51rem;
  }
  @media ${Device.mobile} {
    max-width: 30rem;
  }

  .mobile-apps {
    width: 100%;
    display: flex;
    flex-flow: row nowrap;
    gap: ${margin.normal};

    @media ${Device.mobile} {
      margin-top: ${margin.normal};
      justify-content: space-evenly;
      gap: 0;
    }
  }
`;

interface ISearchForm {
  isLoading: boolean;
  onInfoClicked: () => void;
  onSearch: (phrase: string) => void;
  onEmptyInput: () => void;
}

export const SearchForm: React.FC<ISearchForm> = ({ isLoading, onInfoClicked, onSearch, onEmptyInput }) => {
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
          <SearchInput
            onInfoClicked={onInfoClicked}
            onSearch={onSearch}
            onEmptyInput={onEmptyInput}
            disabled={isLoading}
          />
          <div className="mobile-apps">
            <AppStoreLink height={56} />
            <GooglePlayLink height={56} />
          </div>
        </SearchWrapper>
      </Container>
    </ErrorBoundary>
  );
};

import React from 'react';
import {
  Wrapper,
  Title,
  Text,
  InputSection,
  InputText,
  InputIconSection,
  SubmitButton,
  FormSearch,
} from './Search.css';
import Kod from '../../assets/kod.svg';
import Microphone from '../../assets/microphone.svg';
import { SearchResultsList } from './SearchResultsList';
import { IProductData } from '../../domain/products';
import {ButtonColor} from './../buttons/Button';

interface ISearchContainer {
  searchResults: IProductData[];
  token?: string;
  isLoading?: boolean;

  onSearch: (phrase: string) => void;
  onLoadMore: () => void;
  onSelect: (code: string) => void;
}

export const SearchContainer: React.FC<ISearchContainer> = ({
  searchResults,
  token,
  isLoading,
  onSearch,
  onLoadMore,
  onSelect,
}) => {
  const [phrase, setPhrase] = React.useState<string>('');
  const hasPhrase = !!phrase && phrase.length > 0;

  const handlePhraseChange = (e: React.ChangeEvent<HTMLInputElement>) => setPhrase(e.currentTarget.value);
  const handleSearch = (e: React.MouseEventHandler<HTMLButtonElement>) => onSearch(phrase);
  const handleLoad = () => onLoadMore();

  return (
    <Wrapper>
      <div>
        <Title>Sprawdź informacje o produkcie</Title>
        <Text>
          Wpisz tekst, podyktuj lub zeskanuj kod
          <br />
          Nie znasz kodu?{' '}
          <a target="blank" href="https://pl.openfoodfacts.org/">
            Znajdź go w bazie
          </a>
        </Text>
        <FormSearch>
          <InputSection>
            <InputText placeholder="Nazwa produktu/producent/kod EAN" type="text" onChange={handlePhraseChange} />
            <InputIconSection>
              <div>
                <img src={Kod} />
              </div>
              <div>
                <img src={Microphone} />
              </div>
            </InputIconSection>
          </InputSection>
          <SubmitButton label='Sprawdź' color={ButtonColor.Red} disabled={!hasPhrase} onClick={handleSearch}/>
        </FormSearch>
      </div>
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
  );
};

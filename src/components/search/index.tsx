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
import { IUser } from '../../services/search-service';

interface ISearchContainer {
  searchResults: IUser[];
  onSearch: (phrase: string) => void;
}

export const SearchContainer: React.FC<ISearchContainer> = ({ searchResults, onSearch }) => {
  const [phrase, setPhrase] = React.useState<string>('');
  const hasPhrase = !!phrase && phrase.length > 0;

  const handlePhraseChange = (e: React.ChangeEvent<HTMLInputElement>) => setPhrase(e.currentTarget.value);

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
              <img src={Kod} />
              <img src={Microphone} />
            </InputIconSection>
          </InputSection>
          <SubmitButton disabled={!hasPhrase} onClick={e => onSearch(phrase)}>
            Sprawdź
          </SubmitButton>
        </FormSearch>
      </div>
      {searchResults && (
        <div className="results-list">
          <ul>
            {searchResults.map((user: IUser) => (
              <li key={user.email}>{`${user.name.first} ${user.name.last}`}</li>
            ))}
          </ul>
        </div>
      )}
    </Wrapper>
  );
};

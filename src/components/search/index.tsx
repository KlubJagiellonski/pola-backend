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
} from '../Search.css';
import Kod from '../../assets/kod.svg';
import Microphone from '../../assets/microphone.svg';
import { IUser, SearchService } from '../../services/search-service';

interface ISearchContainer {
  searchResults: string[];
  onSearch: (phrase: string) => void;
}

export const SearchContainer: React.FC<ISearchContainer> = ({ searchResults, onSearch }) => {
  const amount = 10;
  const [users, setUsers] = React.useState<IUser[]>([]);
  const [phrase, setPhrase] = React.useState<string>('');
  const hasPhrase = !!phrase && phrase.length > 0;

  const load = async () => {
    // fetch(`https://randomuser.me/api/?results=${amount}`)
    //   .then(response => response.json())
    //   .then((response: IUsersResponse) => {
    //     console.log('users', response.results.length);
    //     setUsers(response.results);
    //   });

    const products = await SearchService.getProducts(amount);

    console.log('users', products);
    setUsers(products);
  };

  React.useEffect(() => {
    load();
  }, []);

  const handlePhraseChange = (e: React.ChangeEvent) => setPhrase(e.currentTarget.value);

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
      <div className="results-list">
        <ul>
          {users.map((user: IUser) => (
            <li key={user.email}>{`${user.name.first} ${user.name.last}`}</li>
          ))}
        </ul>
      </div>
    </Wrapper>
  );
};

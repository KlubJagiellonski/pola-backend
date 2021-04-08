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
import Kod from './../assets/kod.svg';
import Microphone from './../assets/microphone.svg';

interface IUser {
  gender: string;
  name: {
    title: string;
    first: string;
    last: string;
  };
  email: string;
  phone: string;
  nat: string;
}

interface IUsersResponse {
  results: IUser[];
  info: {
    seed: string;
    results: number;
    page: number;
    version: number;
  };
}

const Search = () => {
  const [amount, setAmount] = React.useState<number>(10);
  const [users, setUsers] = React.useState<IUser[]>([]);

  const load = () => {
    fetch(`https://randomuser.me/api/?results=${amount}`)
      .then(response => response.json())
      .then((response: IUsersResponse) => {
        console.log('users', response.results.length);
        setUsers(response.results);
      });
  };

  React.useEffect(() => {
    load();
  }, []);

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
            <InputText placeholder="Nazwa produktu/producent/kod EAN" type="text" />
            <InputIconSection>
              <img src={Kod} />
              <img src={Microphone} />
            </InputIconSection>
          </InputSection>
          <SubmitButton onClick={e => load()}>Sprawdź</SubmitButton>
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

export default Search;

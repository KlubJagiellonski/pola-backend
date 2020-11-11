import React, { useState } from 'react'
import { SearchButton, SearchInput, SearchFormControl, Wrapper, Text } from './Search.css'
import { ImSearch } from 'react-icons/im'
import { useHistory } from "react-router-dom";

const Search = () => {
  const [ean, setEan] = useState("");
  let history = useHistory();

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(ean.length)
    if(ean.length > 0){
      history.push(`/ean/${ean.replace(/\s/g, '')}`);
    }
  }

  return (
    <Wrapper>
      <Text>
        Sprawdź informacje o produkcie.<br />
        Nie wiesz, jaki kod ma Twój produkt? <a href='https://pl.openfoodfacts.org/'>Sprawdź w bazie kodów</a>
      </Text>
      <SearchFormControl onSubmit={handleSubmit}>
        <SearchInput
          type='text'
          value={ean}
          onChange={e => setEan(e.target.value)}
          placeholder="Wpisz tutaj kod kreskowy (EAN)"
        />
        <SearchButton type='submit'>
          <ImSearch />
        </SearchButton>
      </SearchFormControl>
    </Wrapper>
  )
}

export default Search;
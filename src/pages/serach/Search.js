import React, { useState } from 'react'
import { SearchButton, SearchInput, SearchFormControl } from './Search.css'
import { ImSearch } from 'react-icons/im'

const Search = () => {
  const [ean, setEan] = useState("");

  return (
    <SearchFormControl>
      <SearchInput
        type='text'
        value={ean}
        onChange={e => setEan(e.target.value)}
        placeholder="Wpisz tutaj kod ean"
      />
      <SearchButton to={`/${ean}`}>
        <ImSearch />
      </SearchButton>
    </SearchFormControl>
  )
}

export default Search;
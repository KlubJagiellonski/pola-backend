import React from 'react';
import styled from 'styled-components';
import { ButtonColor } from '../../components/buttons/Button';

import { Device, fontSize, color, padding, margin } from '../../styles/theme';
import { SecondaryButton } from '../../components/buttons/SecondaryButton';
import Kod from '../../assets/kod.svg';
import Microphone from '../../assets/microphone.svg';



const InputSection = styled.div`
  position: relative;
  border: 1px solid ${color.border.grey};
  padding: 5px 100px 5px 10px;
  width: 320px;
  background-color: white;
  border-radius: 20px;

  @media ${Device.mobile} {
    width: 100%;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    padding: 5px 70px 5px 5px;
  }
`;

const InputText = styled.input`
  border: none;
  font-size: ${fontSize.small};
  width: 100%;
`;

const InputIconSection = styled.div`
  position: absolute;
  top: 0px;
  bottom: 0px;
  display: flex;
  align-items: center;
  right: 0px;
  padding: ${padding.tiny} 0;

  div {
    border-radius: 50%;
    background-color: ${color.background.red};
    height: 30px;
    width: 30px;
    margin-right: ${margin.tiny};
    display: flex;
    align-items: center;
    justify-content: center;

    img {
      height: 100%;
      max-height: 20px;
      max-width: 20px;
      cursor: pointer;
    }
  }
`;

const SubmitButton = styled(SecondaryButton)`
  margin-left: 15px;

  @media ${Device.mobile} {
    padding: 5px 0;
    margin-left: 0;
    margin-top: 5px;
    width: 100%;
  }
`;

const FormSearch = styled.div`
  display: flex;
  align-items: center;
  margin-top: 30px;

  @media ${Device.mobile} {
    flex-direction: column;
  }
`;

interface ISearchInput {
  isLoading?: boolean;
  onSearch: (phrase: string) => void;
}

export const SearchInput: React.FC<ISearchInput> = ({ isLoading, onSearch }) => {
  const [phrase, setPhrase] = React.useState<string>('');
  const hasPhrase = !!phrase && phrase.length > 0;

  const handlePhraseChange = (e: React.ChangeEvent<HTMLInputElement>) => setPhrase(e.currentTarget.value);
  const handleSearch = () => onSearch(phrase);
  const handleEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.keyCode === 13) {
      handleSearch();
    }
  };

  // return (
  //   <Container>
  //     <Title>Sprawdź informacje o produkcie</Title>
  //     <Text>
  //       Wpisz tekst, podyktuj lub zeskanuj kod
  //       <br />
  //       Nie znasz kodu?{' '}
  //       <a target="blank" href="https://pl.openfoodfacts.org/">
  //         Znajdź go w bazie
  //       </a>
  //     </Text>
  //     <FormSearch>
  //       <InputSection>
  //         <InputText
  //           placeholder="Nazwa produktu/producent/kod EAN"
  //           type="text"
  //           onChange={handlePhraseChange}
  //           onKeyDown={handleEnter}
  //         />
  //         <InputIconSection>
  //           <div>
  //             <img src={Kod} />
  //           </div>
  //           <div>
  //             <img src={Microphone} />
  //           </div>
  //         </InputIconSection>
  //       </InputSection>
  //       <SubmitButton label="Sprawdź" color={ButtonColor.Red} disabled={!hasPhrase} onClick={handleSearch} />
  //     </FormSearch>
  //   </Container>
  // );

  return (
    <FormSearch>
    <InputSection>
      <InputText
        placeholder="Nazwa produktu/producent/kod EAN"
        type="text"
        onChange={handlePhraseChange}
        onKeyDown={handleEnter}
        disabled={isLoading}
      />
      <InputIconSection>
        <div>
          <img src={Kod} />
        </div>
        <div>
          <img src={Microphone} />
        </div>
      </InputIconSection>
    </InputSection>
    <SubmitButton label="Sprawdź" color={ButtonColor.Red} disabled={!hasPhrase} onClick={handleSearch} />
  </FormSearch>
  )
};

import React from 'react';
import styled from 'styled-components';

import { ButtonColor } from '../../components/buttons/Button';
import { SecondaryButton } from '../../components/buttons/SecondaryButton';
import { Device, fontSize, color, padding, margin } from '../../styles/theme';
import Kod from '../../assets/kod.svg';
import Microphone from '../../assets/microphone.svg';

const InputSection = styled.div`
  padding: 5px 100px 5px 10px;
  position: relative;
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

  &:focus,
  &:active {
    border: none;
    outline: none;
  }
`;

const InputIconSection = styled.div`
  position: absolute;
  top: 0px;
  bottom: 0px;
  display: flex;
  align-items: center;
  right: 0px;
  padding: ${padding.tiny} 0;
`;

interface IInputIcon {
  imagePath: string;
}

const InputIcon = styled.div<IInputIcon>`
  border-radius: 50%;
  background-color: ${color.background.red};
  height: 30px;
  width: 30px;
  margin-right: ${margin.tiny};
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-image: url(${props => props.imagePath});
  background-position: center;
  background-repeat: no-repeat;
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
  const showSubmitButton = false;

  const handlePhraseChange = (e: React.ChangeEvent<HTMLInputElement>) => setPhrase(e.currentTarget.value);
  const handleSearch = () => onSearch(phrase);
  const handleEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.keyCode === 13) {
      handleSearch();
    }
  };

  return (
    <FormSearch>
      <InputSection>
        <InputText
          placeholder="nazwa produktu lub kod EAN"
          type="text"
          onChange={handlePhraseChange}
          onKeyDown={handleEnter}
          disabled={isLoading}
        />
        <InputIconSection>
          <InputIcon imagePath={Kod} />
          <InputIcon imagePath={Microphone} />
        </InputIconSection>
      </InputSection>
      {showSubmitButton && (
        <SubmitButton label="Sprawdź" color={ButtonColor.Red} disabled={!hasPhrase} onClick={handleSearch} />
      )}
    </FormSearch>
  );
};

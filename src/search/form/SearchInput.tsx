import React from 'react';
import styled from 'styled-components';
import debounce from 'lodash.debounce';

import { ButtonColor } from '../../styles/button-theme';
import { SecondaryButton } from '../../components/buttons/SecondaryButton';
import { Device, fontSize, color, padding, margin, px } from '../../styles/theme';
import Kod from '../../assets/kod.svg';
import Microphone from '../../assets/microphone.svg';

const FormSearch = styled.div`
  display: flex;
  align-items: center;

  @media ${Device.mobile} {
    flex-direction: column;
  }
`;

const InputSection = styled.div`
  padding: 0 1em 0 1em;
  position: relative;
  width: 100%;
  min-width: 28em;
  height: 2.5em;
  background-color: white;
  border-radius: 3em;

  @media ${Device.mobile} {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    padding-right: ${padding.normal};
    min-width: 24em;
  }
`;

const InputText = styled.input`
  border: none;
  font-size: ${fontSize.normal};
  width: 100%;
  height: 100%;

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

const InputIcon = styled.div<{ size: number; imagePath: string }>`
  border-radius: 50%;
  background-color: ${color.background.red};
  height: ${(props) => px(props.size)};
  width: ${(props) => px(props.size)};
  margin-right: ${margin.tiny};
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-image: url(${(props) => props.imagePath});
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

interface ISearchInput {
  disabled: boolean;
  onSearch: (phrase: string) => void;
}

export const SearchInput: React.FC<ISearchInput> = ({ disabled, onSearch }) => {
  const [phrase, setPhrase] = React.useState<string>('');
  const hasPhrase = !!phrase && phrase.length > 0;
  const showSubmitButton = false;

  const onPhraseChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.persist();
    setPhrase(e.currentTarget.value);
    onSearch(e.currentTarget.value);
  };

  const handlePhraseChange = debounce(onPhraseChange, 500, {
    leading: false,
    trailing: true,
  });

  const handleSearch = () => onSearch(phrase);
  const handleEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.keyCode === 13) {
      onSearch(phrase);
    }
  };

  return (
    <FormSearch>
      <InputSection>
        <InputText
          placeholder="nazwa produktu / producent / kod EAN"
          type="text"
          onChange={handlePhraseChange}
          onKeyDown={handleEnter}
          disabled={disabled}
        />
        <InputIconSection>
          <InputIcon imagePath={Kod} size={36} />
          <InputIcon imagePath={Microphone} size={36} />
        </InputIconSection>
      </InputSection>
      {showSubmitButton && (
        <SubmitButton label="Sprawdź" color={ButtonColor.Red} disabled={!hasPhrase} onClick={handleSearch} />
      )}
    </FormSearch>
  );
};

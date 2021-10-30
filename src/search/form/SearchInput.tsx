import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';
import debounce from 'lodash.debounce';

import { ButtonThemes, ButtonFlavor } from '../../components/buttons/Button';
import { SecondaryButton } from '../../components/buttons/SecondaryButton';
import { Device, fontSize, color, padding, margin, px } from '../../styles/theme';
import Kod from '../../assets/kod.svg';
import Microphone from '../../assets/microphone.svg';

const FormSearch = styled.div`
  display: flex;
  align-items: center;
  position: relative;

  @media ${Device.mobile} {
    flex-direction: column;
  }
`;

const InputElement = styled.div`
  padding-left: 0.25em;
  width: 100%;
  min-width: 28em;
  height: 56px;
  border-radius: 3em;
`;

const InputSection = styled(InputElement)`
  background-color: white;
  display: flex;
  justify-content: flex-end;

  @media ${Device.mobile} {
    min-width: 0;
  }
`;

const InputOverlay = styled(InputElement)`
  background-color: black;
  opacity: 0.33;
  position: absolute;
  z-index: 10;
`;

const InputText = styled.input`
  background-color: transparent;
  border: none;
  font-size: ${fontSize.normal};
  width: 100%;
  height: 100%;
  padding-right: ${padding.small};

  &:focus,
  &:active {
    border: none;
    outline: none;
  }

  @media ${Device.mobile} {
    max-width: none;
    width: 100%;
  }
`;

const InputIconSection = styled.div`
  display: flex;
  align-items: center;
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
  onEmptyInput: () => void;
}

const isNotEmpty = (value: string) => !!value && value.length && value.length > 0;

export const SearchInput: React.FC<ISearchInput> = ({ disabled, onSearch, onEmptyInput }) => {
  const [phrase, setPhrase] = React.useState<string>('');
  const hasPhrase = !!phrase && phrase.length > 0;
  const showSubmitButton = false;
  let inputRef = useRef<HTMLInputElement>(null);

  const onPhraseChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    handlePhraseChange(event.currentTarget.value);
  };

  const handlePhraseChange = debounce(
    (value: string) => {
      setPhrase(value);
      if (isNotEmpty(value)) {
        onSearch(value);
      } else {
        onEmptyInput();
      }
    },
    500,
    {
      leading: false,
      trailing: true,
    }
  );

  const handleSearch = () => onSearch(phrase);
  const handleEnter = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.keyCode === 13) {
      onSearch(phrase);
    }
  };

  useEffect(() => {
    if (inputRef && inputRef.current) {
      inputRef.current.focus();
    }
  }, [phrase, disabled]);

  return (
    <FormSearch>
      {disabled && <InputOverlay />}
      <InputSection>
        <InputIconSection>
          <InputIcon imagePath={Kod} size={48} />
        </InputIconSection>

        <InputText
          autoFocus
          ref={inputRef}
          placeholder="nazwa produktu / producent / kod EAN"
          type="text"
          onChange={onPhraseChange}
          onKeyDown={handleEnter}
          disabled={disabled}
        />
        <InputIconSection>
          <InputIcon imagePath={Kod} size={48} />
          <InputIcon imagePath={Microphone} size={48} />
        </InputIconSection>
      </InputSection>
      {showSubmitButton && (
        <SubmitButton
          label="Sprawdź"
          styles={ButtonThemes[ButtonFlavor.RED]}
          disabled={!hasPhrase}
          onClick={handleSearch}
        />
      )}
    </FormSearch>
  );
};

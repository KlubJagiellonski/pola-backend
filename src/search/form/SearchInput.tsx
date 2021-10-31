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
  flex-flow: row nowrap;
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
  padding: 0 ${padding.small} 0 ${padding.normal};

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
  width: ${(props) => px(props.size)};
  height: ${(props) => px(props.size)};
  margin-right: ${margin.tiny};
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-image: url(${(props) => props.imagePath});
  background-position: center;
  background-repeat: no-repeat;
`;

const InfoIcon = styled.div<{ width: number; height: number }>`
  display: flex;
  flex: 1 1 ${(props) => px(props.width)};
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-right: ${margin.tiny};
  background-color: ${color.background.red};
  width: ${(props) => px(props.width)};
  height: ${(props) => px(props.height)};
  color: ${color.text.light};
  cursor: pointer;

  h1,
  h2,
  h3,
  p,
  span {
    margin-top: 6px;
    line-height: 0;
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

interface ISearchInput {
  disabled: boolean;
  onInfoClicked: () => void;
  onSearch: (phrase: string) => void;
  onEmptyInput: () => void;
}

const isNotEmpty = (value: string) => !!value && value.length && value.length > 0;

export const SearchInput: React.FC<ISearchInput> = ({ disabled, onInfoClicked, onSearch, onEmptyInput }) => {
  const [phrase, setPhrase] = React.useState<string>('');
  const hasPhrase = !!phrase && phrase.length > 0;
  const showSubmitButton = false;
  const showBarcodeIcon = false;
  const showVoiceInputIcon = false;
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
          <InfoIcon width={50} height={48} onClick={onInfoClicked}>
            <h2>i</h2>
          </InfoIcon>
          {showBarcodeIcon && <InputIcon imagePath={Kod} size={48} />}
          {showVoiceInputIcon && <InputIcon imagePath={Microphone} size={48} />}
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

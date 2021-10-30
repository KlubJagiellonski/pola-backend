import React from 'react';
import { fontSize } from '../../styles/theme';
import { SecondaryButton } from '../../components/buttons/SecondaryButton';
import { ButtonThemes, ButtonFlavor } from '../../components/buttons/Button';
import { openNewTab } from '../../utils/browser';
import { urls } from '../../domain/website';
import { InfoBox } from '../../components/InfoBox';

export const MissingProductInfo = () => (
  <InfoBox>
    <p>Nie znalazłeś czego szukasz?</p>
    <SecondaryButton
      onClick={() => openNewTab(urls.external.openFoods)}
      styles={ButtonThemes[ButtonFlavor.RED]}
      fontSize={fontSize.small}>
      <p>Zgłoś produkt do bazy</p>
    </SecondaryButton>
  </InfoBox>
);

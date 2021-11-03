import React from 'react';
import { fontSize, padding } from '../../styles/theme';
import { SecondaryButton } from '../../components/buttons/SecondaryButton';
import { ButtonThemes, ButtonFlavor } from '../../components/buttons/Button';
import { openNewTab } from '../../utils/browser';
import { urls } from '../../domain/website';
import { InfoBox } from '../../components/InfoBox';
import { Title } from '../../components/Teams.css';
import { Text } from '../../styles/GlobalStyle.css';
import styled from 'styled-components';

const Content = styled.div`
  display: flex;
  flex-flow: row nowrap;
  gap: ${padding.big};
  width: 100%;
  justify-content: center;
`;

const buttonStyle = { ...ButtonThemes[ButtonFlavor.RED], fontSize: fontSize.small, lowercase: true };

export const MissingProductInfo = () => (
  <InfoBox>
    <Title>Nie znalazłeś czego szukasz?</Title>
    <Content>
      <div className="info-tile">
        <Text>Zgłoś brakującą firmę, produkt lub błąd w danych.</Text>
        <a href={urls.external.mail.Klub.href}>
          <SecondaryButton styles={buttonStyle}>
            <p>pola@klubjagiellonski.pl</p>
          </SecondaryButton>
        </a>
      </div>
      <div className="info-tile">
        <Text>Twojej firmy nie ma w bazie?</Text>
        <SecondaryButton onClick={() => openNewTab(urls.external.links.openFoods)} styles={buttonStyle}>
          <p>Wypełnij formularz</p>
        </SecondaryButton>
      </div>
    </Content>
  </InfoBox>
);

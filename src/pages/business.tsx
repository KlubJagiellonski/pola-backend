import React from 'react';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { PageType, urls } from '../domain/website';
import { PageSection } from '../layout/PageSection';
import { Text, TitleSection } from '../styles/GlobalStyle.css';
import { ResponsiveImage } from '../components/images/ResponsiveImage';
import styled from 'styled-components';
import { padding } from '../styles/theme';

const ImageContainer = styled.div`
  max-width: 40em;
  margin: 0 auto;
`;

interface IBusinessPage {
  location?: Location;
}

const BusinessPage = (props: IBusinessPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.BUSINESS));
    }
  }, []);

  return (
    <PageLayout styles={{ marginTop: padding.big }}>
      <SEOMetadata pageTitle="Oferta Biznesowa" />
      <PageSection>
         <TitleSection>Oferta biznesowa</TitleSection>
        <Text>
          Głównym celem działań biznesowych jest promocja oraz wsparcie polskich przedsiębiorstw. Będzie to możliwe
          dzięki stworzeniu silnego środowiska społeczno-biznesowego, które poprzez kooperację i wspólne działania
          przyczyni się do popularyzacji mody na patriotyzm gospodarczy.

           Stworzyliśmy narzędzia wsparcia biznesu, które odzwierciedlają aktualne nawyki konsumenckie i pozwalają
          uzyskać przewagę konkurencyjną.
        </Text>
        <TitleSection>Znak towarowy</TitleSection>
        <Text>
          Według badań nawet 90% Polaków chce kupować polskie produkty. Jak jednak rozpoznać polską firmę? Jakie
          kryteria należy wziąć pod uwagę? W odpowiedzi na te pytania powstała aplikacja Pola. Zabierz ją na zakupy. To
          proste narzędzie służące do weryfikowania firm. Aplikacja przyznaje punkty od 0 do 100. Maksymalną liczbę
          punktów uzyskuje firma, która produkuje w Polsce, jest tutaj zarejestrowana, ma polski kapitał i nie jest
          częścią zagranicznego koncernu. Ponieważ zdecydowana większość Polaków chce kupować polskie produkty, warto
          podkreślać ich pochodzenie na opakowaniu. Nasz znak towarowy jest skierowany do wszystkich firm, którym
          aplikacja Pola przyznaje maksymalną liczbę punktów.
          
          <p><strong><a href="https://klubjagiellonski.github.io/pola-web/business//">Członkowie Klubu Przyjaciół Poli posługujący się naszym znakiem towarowym</a></strong></p>
        </Text>
        <ImageContainer>
          <ResponsiveImage imageSrc="pola.jpg" />
        </ImageContainer>
      </PageSection>
      <PageSection>
        <TitleSection>Pola w sklepie internetowym</TitleSection>
        <Text>
          Aplikacje Pola pobrano już 750 tys. razy, a liczba zeskanowanych produktów zbliża się do 10 milionów.
        </Text>
        <Text>
          6 lat działania aplikacji, to także sześć lat analizy zachowań i nawyków konsumenckich. Wiemy jakich
          informacji potrzebują Polacy podczas codziennych zakupów i posiadamy odpowiednie narzędzia, by tych informacji
          dostarczać.{' '}
          <a href={urls.external.openSearch.href} target="__blank">
            91% Polaków chce znać pochodzenie produktów przed podjęciem decyzji zakupowej
          </a>
          . Posiadając liczne i zaangażowane grono odbiorców, znamy preferencje konsumentów i chętnie przeniesiemy swoje
          doświadczenia na rynek e-commerce.
        </Text>
        <ImageContainer>
          <ResponsiveImage imageSrc="pola-business.jpg" />
        </ImageContainer>
      </PageSection>
      <PageSection>
        <TitleSection>Udostępnianie danych</TitleSection>
        <Text>
          Chcemy dostarczać użytkownikom informacji, niezbędnych do podjęcia świadomych decyzji. Transparentność w
          zakresie udostępniania danych, to wzorcowa prokonsumencka postawa. Możemy dodać do bazy zgromadzoną przez
          Ciebie listę kodów EAN, listę marek własnych, lub zupełnie inne dane, których jeszcz e nie mamy. Budujmy razem
          świadomą konsumpcję.
        </Text>
      </PageSection>
      <PageSection>
        <TitleSection>Kontakt</TitleSection>
        <Text>Mateusz Perowicz</Text>
        <Text>mateusz.perowicz@klubjagiellonski.pl</Text>
        <Text>tel. 660 010 034</Text>
      </PageSection>
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({ location: state.app.location }), {})(BusinessPage);

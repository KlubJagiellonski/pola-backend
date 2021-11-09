import React from 'react';
import { connect, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { PageType, urls } from '../domain/website';
import { PageSection } from '../layout/PageSection';
import { Text, TitleSection } from '../styles/GlobalStyle.css';
import { ColumnsLayout, ContentColumn } from '../layout/ColumnsLayout';
import { margin, padding } from '../styles/theme';
import { ResponsiveImage } from '../components/images/ResponsiveImage';
import Faq from '../components/Faq';

const Image = styled.div`
  height: 100%;
  margin-left: 50%;
  transform: translateX(-50%);
  margin-bottom: ${margin.normal};

  .gatsby-image-wrapper {
    height: 100%;

    div {
      padding-bottom: 100% !important;
    }

    picture {
      img {
        width: auto !important;
      }
    }
  }
`;

interface IAboutPage {
  location?: Location;
}

const AboutPage = (props: IAboutPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.ABOUT));
    }
  }, []);

  return (
    <PageLayout styles={{ marginTop: padding.big }}>
      <SEOMetadata pageTitle="O Poli" />
      <ColumnsLayout>
        <ContentColumn fraction={60}>
          <PageSection>
            <TitleSection>O Poli</TitleSection>
            <Text>
              Masz dość masówki globalnych koncernów? Szukasz lokalnych firm tworzących unikatowe produkty? Pola pomoże
              Ci odnaleźć polskie wyroby. Zabierając Polę na zakupy, odnajdujesz produkty „z duszą” i wspierasz polską
              gospodarkę.
            </Text>
            <Text>
              Zeskanuj kod kreskowy z dowolnego produktu i dowiedz się więcej o firmie, która go wyprodukowała. Pola
              powie Ci, czy dany producent opiera się na polskim kapitale, ma u nas swoją produkcję, tworzy
              wykwalifikowane miejsca pracy, jest częścią zagranicznego koncernu.
            </Text>
            <Text>
              Jeśli znajdziesz firmę, której nie ma w naszej bazie, koniecznie zgłoś ją do nas. Pomożesz nam w ten
              sposób uzupełniać unikatową bazę polskich producentów.
            </Text>
          </PageSection>
          <PageSection>
            <TitleSection>Algorytm</TitleSection>
            <Text>
              Każdemu producentowi Pola przypisuje od 0 do 100 punktów. Pierwsze 35 punktów przyznaje proporcjonalnie do
              udziału polskiego kapitału w konkretnym przedsiębiorstwie. Dalsze 10 punktów otrzymuje ta firma, która
              jest zarejestrowana w Polsce, a kolejne 30, o ile produkuje w naszym kraju. Dalsze 15 punktów zależy od
              tego, czy zatrudnia w naszym kraju w obszarze badań i rozwoju. Wreszcie ostatnie 10 punktów otrzymują
              firmy, które nie są częścią zagranicznych koncernów.
            </Text>
            <Text>
              Liczba punktów zwizualizowana jest przy pomocy czerwonego paska. Dokładamy wszelkich starań aby dane w
              aplikacji zawsze odpowiadały rzeczywistości i były aktualizowane na bieżąco. Prosimy o zgłaszanie
              wszelkich uwag i niejasności.
            </Text>
          </PageSection>
          <PageSection>
            <TitleSection>Filozofia działania</TitleSection>
            <Text>
              Staramy się być maksymalnie przejrzyści w naszych działaniach. Całość kodu źródłowego serwisu udostępniamy
              na zasadach otwartego oprogramowania na{' '}
              <a href={urls.external.links.polaGitHub.href} target="__blank">
                koncie Klubu Jagiellońskiego
              </a>{' '}
              w serwisie GitHub. Wktórce planujemy udostępnić w Internecie całość bazy danych producentów wraz z
              historią zmian i źródłami, na podstawie których podejmujemy decyzję o liczbie punktów, które im
              przyznajemy. Działamy zgodnie z naszą{' '}
              <a href={urls.external.links.polaPrivacyPolicy.href} target="__blank">
                polityką prywatności
              </a>
              .
            </Text>
          </PageSection>
        </ContentColumn>
        <ContentColumn hideOnMobile={true} fraction={40}>
          <Image>
            <ResponsiveImage imageSrc="3-bez_loga.png" />
          </Image>
        </ContentColumn>
      </ColumnsLayout>
      <PageSection>
        <Faq />
      </PageSection>
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({}))(AboutPage);

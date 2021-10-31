import React from 'react';
import { connect, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { hash, PageType, urls } from '../domain/website';
import { Text, TitleSection, WrapperSection } from '../styles/GlobalStyle.css';
import { PageSection } from '../layout/PageSection';
import { margin, padding, Device, color, fontSize } from '../styles/theme';
import { ResponsiveImage } from '../components/images/ResponsiveImage';
import Placeholder from '../components/Placeholder';
import { Friend } from '../domain/friends';
import Card from '../components/Card';
import FriendsSection from '../components/friends/FriendsSection';

const Title = styled(TitleSection)`
  margin: ${margin.normal} 0;
  text-align: center;
`;

const FullWrapperInfo = styled(WrapperSection)`
  padding: 0 ${padding.small};
  display: flex;
  justify-content: center;
`;

const FullContentInfo = styled.div`
  width: 50%;

  @media ${Device.mobile} {
    width: 100%;
  }
`;

const UlSection = styled.ul`
  color: ${color.text.secondary};
  font-size: ${fontSize.small};
  margin: ${margin.small};
  padding: ${padding.small};
`;

const WrapperInfo = styled(PageSection)`
  display: flex;
  padding-bottom: 0;
  padding-top: 120px;
  margin-top: -120px;

  div {
    flex: 1;
  }

  @media ${Device.mobile} {
    flex-direction: column;
    padding-right: 0;
    padding-left: 0;
  }
`;

const Info = styled(WrapperSection)`
  padding: ${margin.normal} ${padding.big};
  margin: ${margin.normal} 0;

  @media ${Device.mobile} {
    padding: ${margin.big} ${padding.small};
    margin: ${margin.normal} 0;
  }
`;

const TitleInfo = styled(TitleSection)`
  @media ${Device.mobile} {
    text-align: center;
  }
`;

interface IFriendsPage {
  location?: Location;
  friends?: Friend[];
}

const FriendsPage = (props: IFriendsPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.FRIENDS));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle="Klub przyjaciół Poli" />
      <Placeholder text="Wspieramy polskie firmy - oto Przyjaciele Poli:" />
      <PageSection>
        <FriendsSection friends={props.friends} />
      </PageSection>
      <FullWrapperInfo color={color.background.transparencyGrey}>
        <FullContentInfo>
          <Title>Jak rozpoznać polską firmę?</Title>
          <Text>
            Można to ustalić weryfikując kilka czynników. Nasz program kierowany jest do przedsiębiorstw, które
            spełniają poniższe kryteria:
          </Text>
          <UlSection>
            <li>są zarejestrowane w Polsce;</li>
            <li>posiadają 100% polskiego kapitału;</li>
            <li>prowadzą produkcję na terenie naszego kraju;</li>
            <li>tworzą wykwalifikowane miejsca pracy;</li>
            <li>nie są częścią zagranicznego koncernu.</li>
          </UlSection>
          <Text>
            Ponadto przedsiębiorstwo musi charakteryzować się nieposzlakowaną opinią na swój temat oraz aktywnie
            angażować się w działania podejmowane na rzecz promocji patriotyzmu gospodarczego w Polsce.
          </Text>
        </FullContentInfo>
      </FullWrapperInfo>
      <WrapperInfo id={hash.friends.profit.id}>
        <Info color={color.background.white}>
          <TitleInfo>Czym jest Klub Przyjaciół Poli?</TitleInfo>
          <Text>
            Głównym celem Klubu Przyjaciół Poli jest promocja oraz wsparcie polskich przedsiębiorstw. Będzie to możliwe
            dzięki stworzeniu silnego środowiska społeczno-biznesowego, które poprzez kooperację i wspólne działania
            przyczyni się do popularyzacji mody na patriotyzm gospodarczy.
          </Text>
          <ResponsiveImage imageSrc="szproty.png" />
        </Info>
        <Info color={color.background.transparencyGrey}>
          <TitleInfo>Co zyskuje przyjaciel Poli?</TitleInfo>
          <UlSection>
            <li>Znak Towarowy Polski produkt - 100 pkt Pola</li>
            <Text>
              Stworzyliśmy własne oznaczenie Polski produkt - 100 pkt Pola przeznaczone wyłącznie dla produktów, które
              uzyskały w naszym algorytmie maksymalny wynik 100 punktów. Będzie to tym samym pierwszy znak towarowy,
              którego pojawienie się na etykiecie jest poparte merytoryczną analizą danego przedsiębiorstwa.
            </Text>
            <Text>
              Głównym powodem rozszerzenia naszej działalności są doświadczenia związane z oznaczeniami funkcjonującymi
              na polskim rynku spożywczym. W większości przypadków w sposób jednoznaczny sugerują one polskie
              pochodzenie produktów, chociaż po zweryfikowaniu ich producentów okazuje się, że są własnością
              zagranicznych podmiotów. Znak Polski produkt - 100 pkt Pola jest naszą odpowiedzią, która w formie
              prostego graficznego przekazu umożliwi szybką weryfikację produktu, co będzie szczególnie ważne dla osób
              niekorzystających z urządzeń mobilnych.
            </Text>
            <li> Ekspozycja informacji o firmie </li>
            <Text>
              Oprócz samego znaku towarowego status Przyjaciela Poli jest jednoznaczny z aktywnym udziałem w rozwoju
              aplikacji Pola. Zabierz ja na zakupy, którą używa już ponad 750 000 użytkowników. Informacja o firmie
              znajduje w specjalnych zakładkach w aplikacji oraz na naszej stronie internetowej, dzieki czemu każdy
              konsument może poznać historię oraz profil działalności wszystkich współpracujących z Klubem Jagiellońskim
              przedsiębiorstw. Dodatkowo po zeskanowaniu produktu należącego do Przyjaciela Poli użytkownik zostanie
              poinformowany o jego specjalnym statusie.
            </Text>
            <li>Działalność promocyjna oraz społeczna</li>
            <Text>
              Wszyscy Przyjaciele Poli mają możliwość aktywnego udziału w prowadzonych przez nas kampaniach społecznych
              oraz internetowych, mających na celu popularyzację polskich firm i patriotyzmu gospodarczego wśród
              obywateli.
            </Text>
          </UlSection>
        </Info>
      </WrapperInfo>
      <WrapperInfo>
        <Card
          title="Dołącz do Przyjaciół Poli"
          content="Lorem ipsum dolor sit amet."
          buttonLabel="KONTAKT"
          url={urls.pola.contact}
        />
      </WrapperInfo>
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({
  friends: state.friends.data,
}))(FriendsPage);

import React from 'react';
import { connect, useDispatch } from 'react-redux';
import { PageType, urls } from '../domain/website';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { IPolaState } from '../state/types';
import styled from 'styled-components';
import { PageLayout } from '../layout/PageLayout';
import { PageSection } from '../layout/PageSection';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { Link } from 'gatsby';
import { margin, padding } from '../styles/theme';

const Wrapper = styled.div`
  margin-top: ${margin.veryBig};
`;
const List = styled.ol`
  font-weight: 600;
  li {
    margin-bottom: ${margin.small};
  }
`;
const Title = styled.p``;
const Text = styled.p`
  font-weight: normal;
`;
const LetterList = styled.p`
  padding-left: ${padding.small};
`;

const PrivacyPolicy = (props: IContactPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.PRIVACY_POLICY));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle="Polityka prywatności" />
      <PageSection>
        <Wrapper>
          <List>
            <li>
              <Title>Jak analizujemy Twoje działania w aplikacji i na stronie?</Title>
              <Text>
                Projektując aplikację Pola zadbaliśmy o to, aby zbierała ona absolutne minimum potrzebnych nam danych i
                nie wykorzystywała ich nigdy w celach reklamowych. Chcemy pomóc naszym użytkownikom w zdobyciu
                informacji o producentach produktów, nie mamy zamiaru wykorzystać danych w żaden inny sposób niż w celu
                poprawy jakości działania aplikacji. Zbieramy jedynie podstawowe, niespersonalizowane dane dotyczące
                ruchu w aplikacji „Pola - zabierz ją na zakupy!” oraz na stronie pola-app.pl. Nie zbieramy danych
                pozwalających Cię zidentyfikować. Zebranych danych - takich jak adres IP - nie wykorzystujemy w celach
                komercyjnych i nie przekazujemy żadnym podmiotom, które mogłyby je wykorzystać do takich celów.
                Korzystamy jednak z Google Analytics, żeby wiedzieć które treści na naszej stronie przyciągają uwagę, a
                także z narzędzi pozwalających nam obserwować ruch i eliminować błędy w aplikacji mobilnej Pola
                (Logentries, Heroku, Sentry).
              </Text>
            </li>
            <li>
              <Title>W jaki sposób możesz zostawić nam więcej danych?</Title>
              <Text>
                Jedynie od Twoich świadomych decyzji zależy, czy zostawić nam więcej danych. Może się to zdarzyć w
                trzech przypadkach:
                <LetterList>
                  <br />
                  a. kiedy kontaktujesz się z nami lub zapisujesz na newsletter, przekazując nam swój adres e-mail,
                  <br />
                  b. kiedy przekazujesz nam darowiznę za pośrednictwem jednej z{' '}
                  <a href={urls.external.links.fundraising.href}>podstron takich jak ta</a>,
                  <br />
                  c. kiedy anonimowo prześlesz nam zdjęcie (np. w celu wskazania błędu identyfikacji produktu).
                </LetterList>
                Za każdym razem te dane są wykorzystywane do celów, które chcesz osiągnąć podejmując konkretne
                działanie!
              </Text>
            </li>
            <li>
              <Title>Co się dzieje z moimi danymi, kiedy kontaktuję się z wami lub zapisuję się na newsletter?</Title>
              <Text>
                <p>
                  Jeśli używasz formularza do kontaktu z nami, wykorzystujemy Twój adres email jedynie do odpowiedzi na
                  Twoją wiadomość. Nie będziemy kontaktować się z Tobą w innych kwestiach, chyba, że wyraźnie poprosisz
                  nas na przykład o dopisanie do newslettera.
                </p>
                Żeby skutecznie zapisać się na nasz newsletter nie wystarczy podać adresu e-mail na odpowiedniej
                podstronie albo w artykule, który czytasz. Musisz jeszcze zweryfikować swoją decyzję klikając
                potwierdzenie w mailu, który otrzymasz. Dopiero wtedy zaczynamy gromadzić i przetwarzać Twoje dane. Co
                się z nimi dzieje? Twój adres e-mail trafia na listę mailingową utrzymywaną przez polską platformę
                GetResponse. Tego, jak ta firma realizuję Politykę Prywatności dowiesz się{' '}
                <a href={urls.external.links.getresponsePrivacyPolicy.href}>tutaj</a>. Poza Twoim adresem e-mail
                zbieramy informacje na temat tego, czy zainteresowały Cię nasze newslettery i które treści okazały się
                szczególnie wartościowe. Może się zdarzyć, że z jakiegoś powodu będziemy musieli „zabrać” te dane z
                platformy tej konkretnej firmy i przenieść je do innego usługodawcy. Z pewnością jednak wybierając
                narzędzie do wysyłania maili będziemy kierowali się tym, by zewnętrzna firma w jak najmniejszym stopniu
                wykorzystywała Twoje dane do własnych celów. Zawsze możesz wypisać się z naszego newslettera klikając
                „rezygnacja” w stopce maila, którego od nas otrzymasz. Dane te przetrzymujemy do momentu zrezygnowania
                przez Ciebie z naszego newslettera.
              </Text>
            </li>
            <li>
              {' '}
              <Title>Co się dzieje z moimi danymi, kiedy przekazuję darowiznę? </Title>
              <Text>
                Kiedy zdecydujesz się przekazać nam darowiznę, to po wybraniu kwoty w nowym oknie przeniesiesz się do
                serwisu tpay.com prowadzonego przez polską firmę Krajowy Integrator Płatności S.A. Ich regulamin{' '}
                <a href={urls.external.links.amazonawsRegulamin.href}>znajdziesz tutaj</a>. Tam musisz pozostawić imię i
                nazwisko oraz e-mail – darowizny on-line muszą być nimi opatrzone. Przekazujemy te informacje firmie
                obsługującej księgowo Stowarzyszenie Klub Jagielloński w celu rozliczenia podatkowego. Te dane trafią
                również do nas, a my skorzystamy z nich, by podziękować Ci za wsparcie i poinformować o naszych
                działaniach. Zawsze możesz się wypisać z naszego newslettera klikając „rezygnacja” w stopce maila,
                którego od nas otrzymasz. Dane o Twojej darowiźnie przetrzymujemy przez okres wymagany z powodu
                rozliczeń podatkowych oraz w razie ewentualnej późniejszej kontroli.
              </Text>
            </li>
            <li>
              <Title>Co się dzieje z moimi danymi, kiedy wysyłam wam zdjęcie?</Title>
              <Text>
                Otrzymane od Ciebie zdjęcie wykorzystujemy jedynie w celu identyfikacji przedstawionego produktu,
                dodania go do bazy aplikacji Pola lub poprawy jego rekordu w przypadku błędu. Otrzymujemy od Ciebie
                jedynie zdjęcie oraz podstawowe informacje (metadane) powiązane z tym plikiem - nie jest możliwa więc
                identyfikacja Ciebie jako zgłaszającego nam dany produkt.
              </Text>
            </li>
            <li>
              <Title>Jak to się ma do RODO?</Title>
              <Text>
                Staramy się być możliwie najlepiej przystosowani do nowych przepisów. Stowarzyszenie Klub Jagielloński -
                wydawca aplikacji mobilnej Pola oraz strony <Link to={urls.pola.home()}>www.pola-app.pl</Link> - jest
                Administratorem Danych Osobowych w rozumieniu Rozporządzenia Ogólnego o Ochronie Danych Osobowych
                (RODO). Twoje dane gromadzimy i przetwarzamy na podstawie tzw. przesłanek legalizujących przetwarzanie
                danych osobowych, na przykład Twojej zgody albo potrzeby rozliczenia podatkowego w przypadku darowizn.
              </Text>
            </li>
            <li>
              <Title>Co mogę zrobić z moimi danymi?</Title>
              <Text>
                Masz do nich dostęp. Możesz żądać ich poprawienia. Możesz żądać ich usunięcia, zaprzestania lub
                ograniczenia przetwarzania. Masz prawo wycofać udzieloną przez Ciebie zgodę. Możesz żądać przeniesienia
                swoich danych do innego administratora. W każdej z tych spraw pisz na adres{' '}
                <a href={urls.external.mail.biuro.href}>biuro@klubjagiellonski.pl</a>. Jeśli uważasz, że przetwarzamy
                Twoje dane w sposób niewłaściwy, masz prawo wniesienia skargi do organu nadzorczego, Generalnego
                Inspektora Ochrony Danych Osobowych.
              </Text>
            </li>
          </List>
        </Wrapper>
      </PageSection>
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({}))(PrivacyPolicy);

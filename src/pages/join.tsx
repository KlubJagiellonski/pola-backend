import React from 'react';
import { connect, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { PageType, urls } from '../domain/website';
import { Text, TitleSection } from '../styles/GlobalStyle.css';
import { fontSize, margin, padding, Device, lineHeight } from '../styles/theme';
import { PageSection } from '../layout/PageSection';
import { ColumnsLayout, ContentColumn } from '../layout/ColumnsLayout';

interface ITeamPage {
  location?: Location;
}

const Wrapper = styled.div`
  margin: ${padding.veryBig} 0 ${margin.normal} 0;

  @media ${Device.mobile} {
    margin: ${padding.veryBig} ${margin.normal} ${margin.normal} ${margin.normal};
  }
`;

const List = styled.ul`
  padding: 0;
  margin: 0;
  list-style-type: none;

  li {
    font-size: ${fontSize.small};
  }
`;

const Section = styled.div`
  margin-top: ${margin.big};
`;

const Info = styled(Text)`
  line-height: ${lineHeight.normal};
`;

const TeamPage = (props: ITeamPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.TEAM));
    }
  }, []);

  return (
    <PageLayout>
      <Wrapper>
        <SEOMetadata pageTitle="Dołącz do zespołu" />
        <PageSection>
          <TitleSection>Zespół</TitleSection>
          <Text>
            Działamy razem dla dobra wspólnego. Tutaj wykorzystujemy nasze umiejętności, by tworzyć projekt pożyteczny
            społecznie. Całość prac programistycznych jest całkowicie transparentna i publicznie{' '}
            <a href={urls.external.links.github.href}>dostępna w serwisie GitHub</a>.
          </Text>
          <Text>
            Aplikacja Pola to dowód na to, że można programować inaczej. Nie pobieramy absolutnie żadnych informacji o
            naszych użytkownikach, nie wyświetlamy reklam, a każda linijka naszego kodu jest publicznie dostępna i każdy
            może ją zweryfikować. Staramy się realizować w ten sposób <b> ideę prospołecznego kodowania. </b>
          </Text>
          <Section>
            <TitleSection>Zespół aplikacji Pola:</TitleSection>
          </Section>
          <ColumnsLayout>
            <ContentColumn>
              <Section>
                <TitleSection>Programowanie</TitleSection>
                <List>
                  <li>Kamil Breguła</li>
                  <li>Rafał Gawlik</li>
                  <li>Marcin Stepnowski</li>
                  <li>Zuzanna Dudzińska</li>
                  <li>Julia Dudzińska</li>
                  <li>Jakub Kałamarz</li>
                  <li>Karol Kamiński</li>
                  <li>Mikołaj Rodkiewicz</li>
                  <li>Katarzyna Grudzień</li>
                  <li>Adam Walkowski</li>
                  <li>Damian Paśko</li>
                  <li>Marcin Murgas</li>
                  <li>Mateusz Śląski</li>
                  <li>Kuba Lipiński</li>
                  <li>Łukasz Rejman</li>
                  <li>Arek Banas</li>
                  <li>Paweł Janeczek</li>
                  <li>Grzesiek Kapusta</li>
                  <li>Jurek Kleszcz</li>
                  <li>Konrad Krakowiak</li>
                  <li>Antoni Kędracki</li>
                  <li>Michał Tajchert</li>
                </List>
              </Section>
              <Section>
                <TitleSection>Kontakt</TitleSection>
                <List>
                  <li>
                    <a href={urls.external.mail.Klub.href}>pola@klubjagiellonski.pl</a>
                  </li>
                  <li>tel. 660 010 034</li>
                </List>
              </Section>
            </ContentColumn>
            <ContentColumn>
              <Section>
                <TitleSection>algorytm:</TitleSection>
                <List>
                  <li>Piotr Dardziński</li>
                  <li>Michał Kot</li>
                  <li>Piotr Mieczkowski</li>
                  <li>Joanna Szalacha-Jarmużek</li>
                  <li>Leszek Wojdalski</li>
                </List>
              </Section>
              <Section>
                <TitleSection>projektowanie i design:</TitleSection>
                <List>
                  <li>Katarzyna Grudzień</li>
                  <li>Magdalena Karpińska</li>
                  <li>Tomasz Szczodrowski</li>
                  <li>Przemek Pomaski</li>
                </List>
              </Section>
              <Section>
                <TitleSection>koordynacja:</TitleSection>
                <List>
                  <li>Obecnie - Mateusz Perowicz</li>
                  <li>Bartosz Paszcza</li>
                  <li>Maciej Dulak</li>
                </List>
              </Section>
              <Section>
                <TitleSection>Redakcja:</TitleSection>
                <List>
                  <li>Bartek Ząbek</li>
                  <li>Piotr Kaźmierski</li>
                  <li>Arkadiusz Tomczyński</li>
                  <li>Mikołaj Dłubak</li>
                  <li>Łukasz Cader</li>
                  <li>Dawid Kiljański</li>
                  <li>Michał Wincel</li>
                  <li>Michał Kania</li>
                  <li>Maciek Dulak</li>
                  <li>Mateusz Mroczek</li>
                  <li>Mateusz Perowicz</li>
                  <li>Wojtek Skierski</li>
                </List>
              </Section>
            </ContentColumn>
          </ColumnsLayout>
        </PageSection>
      </Wrapper>
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({}))(TeamPage);

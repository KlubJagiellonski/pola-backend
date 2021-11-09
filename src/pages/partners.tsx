import React from 'react';
import { connect, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { PageType, urls } from '../domain/website';
import { PageSection } from '../layout/PageSection';
import { PartnerService } from '../domain/partners/partners-service';
import { PartnersList } from '../components/partners/PartnersList';
import { Device, margin, padding } from '../styles/theme';
import { ResponsiveImage } from '../components/images/ResponsiveImage';
import { Text } from '../styles/GlobalStyle.css';
import Placeholder from '../components/Placeholder';
import { ExternalLink } from '../utils/browser/links';

const Wrapper = styled.div`
  text-align: center;
  margin-top: ${margin.veryBig};
`;

const TextWrapper = styled.div`
  display: flex;
  justify-content: center;
`;

const TextSection = styled(Text)`
  margin: ${margin.big} 0;
  text-align: center;
`;

const ImageSection = styled.ul`
  display: flex;
  flex-flow: row nowrap;
  list-style: none;
  align-items: center;
  margin: 0 ${padding.veryBig};
  padding: 0 ${padding.veryBig};

  li {
    flex: 1;
    width: 100%;
    margin: 0 ${padding.veryBig};

    img {
      width: 100%;
    }
  }

  @media ${Device.mobile} {
    padding: 0;
    flex-flow: column;
    max-width: 20em;
    gap: ${padding.normal};
    margin: 0 ${margin.big};

    li {
      margin: 0 ${margin.normal};
    }
  }
`;

interface IPartnersPage {
  location?: Location;
}

const PartnersPage = (props: IPartnersPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.PARTNERS));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle="Partnerzy" />
      <Placeholder text="Partner aplikacji Pola" />
      <PageSection>
        <Wrapper>
          <ImageSection>
            <li>
              <ExternalLink url={urls.external.links.pge}>
                <ResponsiveImage imageSrc="PGE_logo.png" />
              </ExternalLink>
            </li>
            <li>
              <ExternalLink url={urls.external.links.polskieKupujeTo}>
                <ResponsiveImage imageSrc="polskie_kupuje.png" />
              </ExternalLink>
            </li>
          </ImageSection>
          <TextWrapper>
            <TextSection styles={{ maxWidth: '32rem' }}>
              Celem zainicjowanej przez Pracowników oraz Grupę Kapitałową PGE kampanii społecznej&nbsp;
              <ExternalLink url={urls.external.links.polskieKupujeTo}>
                <span>POLSKIE – KUPUJĘ TO!</span>
              </ExternalLink>
              &nbsp;jest zachęcanie Polaków do kupowania rodzimych produktów i usług. W ramach tego przedsięwzięcia PGE
              wspiera rozwój aplikacji Pola.
            </TextSection>
          </TextWrapper>
        </Wrapper>
      </PageSection>
      <PageSection>
        <PartnersList partners={PartnerService.getAll()} />
      </PageSection>
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({}))(PartnersPage);

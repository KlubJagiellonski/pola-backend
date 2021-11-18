import React from 'react';
import styled from 'styled-components';
import styledContainerQuery from 'styled-container-query';

import { Device, fontSize, margin, color, padding } from './../styles/theme';
import { ButtonFlavor, ButtonThemes } from './buttons/Button';
import { SecondaryButton } from './buttons/SecondaryButton';
import { WrapperSection } from '../styles/GlobalStyle.css';
import { TitleSection, Text } from '../styles/GlobalStyle.css';
import { ResponsiveImage } from '../components/images/ResponsiveImage';
import { openNewTab } from '../utils/browser';
import { urls } from '../domain/website';
import { ColumnsLayout, ContentColumn } from '../layout/ColumnsLayout';

const Info = styled.div`
  width: 100%;
  height: 12em;
  position: relative;
  margin: ${margin.small} 0;

  @media ${Device.mobile} {
    height: 10em;
  }
`;

const TextSection = styled.div`
  margin-right: ${margin.normal};
  padding: 0 ${padding.normal};
  background-color: ${color.background.white};
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  @media ${Device.mobile} {
    width: auto;
  }
`;

const Texts = styled.div`
  width: 100%;
  background-color: ${color.background.white};
  margin-right: ${margin.small};
`;

const Column = styled(ContentColumn)`
  align-items: center;
  justify-content: center;
`;

const Buttons = styled.div`
  text-align: center;
`;

const DevelopmentTitle = styled(TitleSection)`
  margin-bottom: ${margin.normal};
`;

const DevelopmentText = styled(Text)`
  margin-bottom: ${margin.big};
`;

const Columns = styled(ColumnsLayout)`
  gap: ${margin.normal};
`;

const ImgSection = styled.div`
  .gatsby-image-wrapper {
    picture {
      img {
        height: 12em !important;
        width: auto !important;
        left: 50% !important;
        transform: translateX(-50%) !important;

        @media ${Device.mobile} {
          height: 10em !important;
        }
      }
    }
  }
`;

const Wrapper = styled(WrapperSection)``;

const Container = styledContainerQuery(Wrapper)`
  display: flex;
  flex-direction: row;
  grid-area: development;
  min-height: 16.1em;
  width: 100%;

  @media ${Device.mobile} {
    min-height: 0;
    display: flex;
    flex-direction: column;
    border-bottom: 8px solid ${color.background.red};
    border-right: none;
    margin-top: ${margin.small};
  }

  &:container(max-width: 450px){
    min-height: 0;
    display: flex;
    flex-direction: column;
    border-bottom: 8px solid ${color.background.red};
    border-right: none;
    margin-top: ${margin.small};

    ${Texts}{
      width: 100%;
    }

    ${Info}{
      height: 10em;
    }

    ${Columns}{
      flex-direction: column;
    }

    ${Column}{
      width: 100%;
    }

    ${Info}{
      height: 10em;
    }

    ${ImgSection}{
      .gatsby-image-wrapper {
        picture {
          img {
            height: 10em !important;
          }
        }
      }
    }
  }
`;

const handleReadMore = () => {
  openNewTab(urls.external.links.polaSupport);
};

const DevelopmentSection = () => {
  return (
    <Container className="development-container" borderColor={color.background.red}>
      <Columns>
        <Column fraction={50}>
          <Buttons>
            <SecondaryButton
              label="Potrzebujemy 1 zł"
              styles={{ ...ButtonThemes[ButtonFlavor.RED], fontSize: fontSize.small }}
              onClick={handleReadMore}
            />
          </Buttons>
          <Info>
            <ImgSection>
              <ResponsiveImage imageSrc="smutny-2.png" />
            </ImgSection>
          </Info>
        </Column>
        <Column fraction={50}>
          <TextSection>
            <DevelopmentTitle>Zobacz jak rozwija się Aplikacja Pola i wspomóż ją!</DevelopmentTitle>
            <DevelopmentText>Dowiedz się co możesz jeszcze zrobić, aby wspierać polskich producentów.</DevelopmentText>
          </TextSection>
        </Column>
      </Columns>
    </Container>
  );
};

export default DevelopmentSection;

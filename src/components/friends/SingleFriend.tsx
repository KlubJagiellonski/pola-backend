import React from 'react';
import styled from 'styled-components';
import { Friend } from '../../domain/friends';
import { hash } from '../../domain/website';
import { PageSection } from '../../layout/PageSection';
import { color, Device, fontSize, margin } from '../../styles/theme';
import { ResponsiveImage } from '../images/ResponsiveImage';
import { TitleSection, Text } from '../../styles/GlobalStyle.css';
import { SecondaryButton } from '../buttons/SecondaryButton';
import { ButtonFlavor, ButtonThemes } from '../../components/buttons/Button';
import { AnchorLink } from 'gatsby-plugin-anchor-links';
import { buildFriendUrl } from './friends-url-service';
import { ColumnsLayout, ContentColumn } from '../../layout/ColumnsLayout';

const WrapperContents = styled(PageSection)`
  margin-top: ${margin.normal};

  @media ${Device.mobile} {
    padding: 0;
  }
`;

const RightColumn = styled(ContentColumn)`
  flex: 1;
  position: relative;
`;

const LeftColumn = styled(ContentColumn)`
  flex: 2;
`;

const ImageSection = styled.div`
  @media ${Device.mobile} {
    max-height: 15em;
    margin-bottom: ${margin.normal};

    .gatsby-image-wrapper {
      max-height: 15em;

      picture {
        img {
          max-height: 15em;
          width: auto !important;
          left: 50% !important;
          right: 50% !important;
          transform: translateX(-50%);
        }
      }
    }
  }

  @media ${Device.desktop} {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;

    .gatsby-image-wrapper {
      height: 100%;

      picture {
        img {
          width: auto !important;
          max-width: 100%;
          height: auto !important;
          max-height: 100%;
          left: 50% !important;
          right: 50% !important;
          top: 50% !important;
          transform: translate(-50%, -50%);
        }
      }
    }
  }
`;

const ButtonSection = styled.div`
  margin-top: ${margin.normal};
  display: flex;
  flex-direction: column;
  gap: ${margin.small};
`;

const Button = styled(SecondaryButton)`
  text-transform: capitalize;
  font-weight: bold;
  min-width: 300px;
`;

const ButtonWhiteRed = styled(Button)`
  border-color: ${color.border.grey};
`;

const ButtonRed = styled(Button)`
  border-color: ${color.background.red};
`;

const SingleFriend: React.FC<Friend> = ({ name, description, image, page, slug }) => {
  return (
    <WrapperContents>
      <ColumnsLayout>
        <RightColumn>
          <ImageSection>{image && <ResponsiveImage imageSrc={image} />}</ImageSection>
        </RightColumn>
        <LeftColumn>
          <TitleSection>{name}</TitleSection>
          <Text>{description}</Text>
          <ButtonSection>
            <a href={page} target="_blank">
              <ButtonRed
                label="Odwiedź stronę przyjaciela"
                styles={ButtonThemes[ButtonFlavor.RED]}
                fontSize={fontSize.small}
              />
            </a>
            {slug && (
              <AnchorLink to={buildFriendUrl(slug, hash.friends.profit.id)}>
                <ButtonWhiteRed
                  label="Wypromuj swoją firmę"
                  styles={ButtonThemes[ButtonFlavor.WHITE_RED]}
                  fontSize={fontSize.small}
                />
              </AnchorLink>
            )}
          </ButtonSection>
        </LeftColumn>
      </ColumnsLayout>
    </WrapperContents>
  );
};

export default SingleFriend;

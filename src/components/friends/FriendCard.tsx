import { Link } from 'gatsby';
import React from 'react';
import styled from 'styled-components';
import { Friend } from '../../domain/friends';
import { urls } from '../../domain/website';

import { TitleSection, WrapperSection, Text } from '../../styles/GlobalStyle.css';
import { color, padding, margin, fontSize } from '../../styles/theme';
import { SecondaryButton } from '../buttons/SecondaryButton';
import { ResponsiveImage } from '../images/ResponsiveImage';
import { ButtonThemes, ButtonFlavor } from '../../components/buttons/Button';

const Wrapper = styled(WrapperSection)`
  padding: ${padding.normal};
`;

const Content = styled(Text)`
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  margin: ${margin.normal} 0;
`;

const ImageSection = styled.div`
  .gatsby-image-wrapper {
    max-height: 8em;

    picture {
      img {
        width: auto !important;
        left: 50% !important;
        transform: translateX(-50%);
      }
    }
  }
`;

const Button = styled(SecondaryButton)`
  text-transform: capitalize;
  font-weight: bold;
  border-color: ${color.background.red};
  width: 100%;
`;

const ButtonSection = styled.div`
  padding: 0 ${padding.normal};
  display: flex;
  flex-direction: column;
  gap: ${margin.small};
`;

const FriendCard: React.FC<Friend> = (friend) => {
  return (
    <Wrapper color={color.background.transparencyGrey}>
      <TitleSection>Oto jeden Przyjaciel z wielu Przyjaciół Poli</TitleSection>
      {friend.image && (
        <ImageSection>
          <ResponsiveImage imageSrc={friend.image} />
        </ImageSection>
      )}
      <Content>{friend.description}</Content>
      <ButtonSection>
        {friend.slug && (
          <Link to={urls.pola.friends('friend', friend.slug)}>
            <Button label="Czytaj Więcej..." styles={ButtonThemes[ButtonFlavor.RED]} fontSize={fontSize.small} />
          </Link>
        )}
      </ButtonSection>
    </Wrapper>
  );
};

export default FriendCard;

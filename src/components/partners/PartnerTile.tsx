import React from 'react';
import styled from 'styled-components';
import { IPartner } from '../../domain/partners';
import { ResponsiveImage } from '../images/ResponsiveImage';

const Tile = styled.div`
  text-align: center;
  width: 100%;

  .title {
    width: 100%;
  }

  a {
    text-decoration: none;
    color: inherit;
  }
`;

const ImageContainer = styled.div`
  position: relative;
  padding: 0 2rem;
  margin-bottom: 1rem;
`;

export const PartnerTile: React.FC<IPartner> = ({ name, imageSrc, description, sourceUrl }) => (
  <Tile>
    <a href={sourceUrl} target="__blank">
      <ImageContainer>
        <ResponsiveImage imageSrc={imageSrc} />
      </ImageContainer>
      <p className="title">{description}</p>
    </a>
  </Tile>
);

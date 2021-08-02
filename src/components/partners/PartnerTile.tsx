import React from 'react';
import styled from 'styled-components';
import { IPartner } from '../../domain/website';
import { ResponsiveImage } from '../images/ResponsiveImage';

const Tile = styled.div`
  text-align: center;
  width: 100%;

  .title {
    width: 100%;
  }
`;

export const PartnerTile: React.FC<IPartner> = ({ name, imageSrc, description, sourceUrl }) => (
  <Tile>
    <a href={sourceUrl} target="__blank">
      <ResponsiveImage imageSrc={imageSrc} />
    </a>
    <p className="title">{description}</p>
  </Tile>
);

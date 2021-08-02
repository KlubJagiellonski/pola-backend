import React from 'react';
import styled from 'styled-components';
import { PartnerTile } from '../../components/partners/PartnerTile';
import { IPartner } from '../../domain/partners';
import { Device, padding } from '../../styles/theme';

interface IPartnersList {
  partners: IPartner[];
}

const List = styled.ul`
  display: flex;
  flex-flow: row nowrap;
  list-style: none;
  align-items: center;
  margin: 0 auto;
  padding: 0;
  gap: ${padding.big};

  li {
    flex: 1;
    width: 100%;

    img {
      width: 100%;
    }
  }

  @media ${Device.mobile} {
    padding: 0;
    flex-flow: column;
    max-width: 20em;
  }
`;

export const PartnersList: React.FC<IPartnersList> = ({ partners }) => (
  <List>
    {partners.map((partner) => (
      <li>
        <PartnerTile {...partner} />
      </li>
    ))}
  </List>
);

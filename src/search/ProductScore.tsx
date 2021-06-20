import React from 'react';
import styled from 'styled-components';
import { lighten } from 'polished';
import { color, padding } from '../styles/theme';

const Score = styled.div<{ value: number }>`
  width: 100%;
  background-color: ${color.background.primary};
  height: ${padding.small};

  .value {
    background-color: ${lighten(0.2)(color.background.red)};
    height: 100%;
    width: ${props => `${props.value}%`};
  }
`;

interface IProductScore {
  value: number;
}

export const ProductScore: React.FC<IProductScore> = ({ value }) => (
  <Score value={value}>
    <div className="value" />
  </Score>
);

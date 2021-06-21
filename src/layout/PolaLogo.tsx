import React from 'react';
import styled from 'styled-components';
import Logo from '../assets/logo/pola-color.svg';
import { padding, color, px } from '../styles/theme';

interface IPolaLogo {
  size?: number;
}

export const LogoColor = styled.div`
  background-color: ${color.background.white};
  border-radius: 50%;
  padding: ${padding.normal};
  margin-top: 60px;
`;

export const PolaLogo: React.FC<IPolaLogo> = ({ size = 80 }) => (
  <LogoColor>
    <img width={size} height={size} src={Logo} />
  </LogoColor>
);

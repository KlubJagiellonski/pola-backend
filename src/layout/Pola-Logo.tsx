import React from 'react';
import styled from 'styled-components';
import Logo from '../assets/logo.png';
import { color } from '../styles/theme';

export const LogoImage = styled.img``;

export const PolaLogo = () => <LogoImage src={Logo} />;

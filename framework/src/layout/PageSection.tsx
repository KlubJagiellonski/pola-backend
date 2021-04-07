import React from 'react';
import styled from 'styled-components';
import { Device, pageWidth, padding } from '../styles/theme';

export const PageSection = styled.section<{ size: 'narrow' | 'full' }>`
  width: 100%;
  margin: 0 auto;

  @media ${Device.mobile} {
    max-width: 'unset';
    padding: ${props => (props.size === 'narrow' ? padding : 0)};
  }
  @media ${Device.desktop} {
    max-width: ${props => (props.size === 'narrow' ? pageWidth : undefined)};
  }
`;

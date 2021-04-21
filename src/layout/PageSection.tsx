import React from 'react';
import styled from 'styled-components';
import { Device, pageWidth, padding, color } from '../styles/theme';

interface IPageSection {
  size?: 'narrow' | 'full';
  backgroundColor?: string;
}

export const PageSection = styled.section<IPageSection>`
  width: 100%;
  margin: 0 auto;
  background-color: ${props => props.backgroundColor || 'transparent'};
  @media ${Device.mobile} {
    padding: ${props => (props.size === 'full' ? 0 : padding.normal)};
  }
  @media ${Device.desktop} {
    max-width: ${props => (props.size === 'full' ? undefined : pageWidth)};
  }
`;

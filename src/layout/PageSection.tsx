import styled from 'styled-components';
import { Device, pageWidth, padding, color } from '../styles/theme';

interface IPageSection {
  size?: 'narrow' | 'full';
  styles?: {
    backgroundColor?: string;
    textColor?: string;
    textAlign?: string;
  };
}

export const PageSection = styled.section<IPageSection>`
  width: 100%;
  margin: 0 auto;
  background-color: ${({ styles }) => styles?.backgroundColor || 'transparent'};
  color: ${({ styles }) => styles?.textColor || color.text.primary};
  text-align: ${({ styles }) => styles?.textAlign || 'left'};
  position: relative;

  @media ${Device.mobile} {
    padding: 0;
  }
  @media ${Device.desktop} {
    max-width: ${(props) => (props.size === 'full' ? undefined : pageWidth)};
    padding: ${(props) => (props.size === 'full' ? 0 : padding.normal)};
  }
`;

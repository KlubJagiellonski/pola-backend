import styled from 'styled-components';
import { Device, pageWidth, padding} from '../styles/theme';

interface IPageSection {
  size?: 'narrow' | 'full';
  backgroundColor?: string;
}

export const PageSection = styled.section<IPageSection>`
  width: 100%;
  margin: 0 auto;
  background-color: ${props => props.backgroundColor || 'transparent'};
  position: relative;

  @media ${Device.mobile} {
    padding: 0;
  }
  @media ${Device.desktop} {
    max-width: ${props => (props.size === 'full' ? undefined : pageWidth)};
    padding: ${props => (props.size === 'full' ? 0 : padding.normal)};
  }
`;

import styled from 'styled-components';
import { color, fontSize, margin, evalPx, lineHeight } from './theme';

type IWrapperSection = {
  color?: string;
  borderColor?: string;
};

export const WrapperSection = styled.div<IWrapperSection>`
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  background: ${({ color }) => color};
  border-right: ${({ borderColor }) => (borderColor ? `8px solid ${borderColor}` : 'none')};
  width: 100%;
`;

export const TitleSection = styled.p`
  margin-top: ${margin.normal} 0;
  padding: 0;
  font-size: ${fontSize.normal};
  font-weight: 700;
  color: ${color.text.primary};
  line-height: ${lineHeight.normall};
`;

interface IText {
  styles?: {
    maxWidth?: number | string;
  };
}

export const Text = styled.p<IText>`
  margin-top: 5px;
  padding: 0;
  font-family: 'Merriweather';
  font-size: ${fontSize.small};
  color: ${color.text.secondary};
  line-height: ${lineHeight.normall};
  max-width: ${({ styles }) => evalPx(styles?.maxWidth)};

  font-feature-settings: 'kern', 'liga', 'clig', 'calt';

  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans',
    'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
`;

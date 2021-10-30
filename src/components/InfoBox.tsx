import styled from 'styled-components';
import { color, fontSize, padding, margin } from '../styles/theme';

export const InfoBox = styled.div`
  background-color: ${color.background.red};
  color: ${color.text.light};
  text-align: center;
  font-size: ${fontSize.big};
  padding: ${padding.normal};
  margin-top: ${margin.big};
`;

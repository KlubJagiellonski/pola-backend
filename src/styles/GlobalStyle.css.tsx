import styled from 'styled-components';
import { color, fontSize } from './theme';

type Color = {
  color: string;
};

export const WrapperSection = styled.div`
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  background: ${({ color }: Color) => color};
  width: 100%;
`;

export const TitleSection = styled.p`
  margin-top: 15px;
  margin-bottom: 10px;
  padding: 0;
  font-size: ${fontSize.normal};
  font-family: 'Ubuntu';
  font-weight: 700;
  line-height: 1rem;
  color: ${color.text.primary};
`;

export const Text = styled.p`
  margin-top: 5px;
  padding: 0;
  font-family: 'Merriweather';
  font-size: ${fontSize.small};
  color: ${color.text.secondary};
  line-height: 1rem;
`;

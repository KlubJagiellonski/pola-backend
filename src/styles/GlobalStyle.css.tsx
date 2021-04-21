import styled from 'styled-components';
import { color } from './theme';

export const Button = styled.button`
  font-family: 'Roboto';
  font-size: 14px;
  font-weight: 700;
  border: 1px solid ${color.border};
  background: ${color.primary};
  padding: 15px 0;
  text-align: center;
  cursor: pointer;
  color: ${color.border};
  text-transform: uppercase;
  width: 100%;
`;

type Color = {
  color: string;
};

export const WrapperSection = styled.div`
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  background: ${({ color }: Color) => color};
  width: 100%;
  margin-top: 15px;

  @media only screen and (max-width: 768px) {
    margin-top: 0;
  }
`;

export const TitleSection = styled.p`
  margin-top: 15px;
  margin-bottom: 10px;
  padding: 0;
  font-family: 'Roboto';
  font-size: 14px;
  font-weight: 700;

  @media only screen and (min-width: 1900px) {
    margin-top: 20px;
    margin-bottom: 15px;
    font-size: 16px;
  }
`;

export const Text = styled.p`
  margin-top: 5px;
  padding: 0;
  font-family: 'Roboto';
  font-size: 12px;
  color: ${color.text};

  @media only screen and (min-width: 1900px) {
    font-size: 14px;
    margin-top: 10px;
  }
`;

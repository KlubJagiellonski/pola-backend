import styled from 'styled-components';
import { color, padding } from '../../styles/theme';

export const Button = styled.button<{ theme: IButtonTheme }>`
  box-sizing: border-box;
  cursor: pointer;
  color: ${props => props.theme.color.text};
  background-color: ${props => props.theme.color.background};
  border: none;
  padding: ${padding.small} ${padding.normal};
  white-space: nowrap;
  font-weight: bold;
  transition-duration: 0.5s;
  font-size: ${props => props.theme.fontSize ? props.theme.fontSize: '18px'};

  &:hover {
    background-color: ${props => props.theme.color.hover};
  }

  &:focus {
    outline: none;
  }

  &.disabled {
    cursor: default;
    background-color: ${color.border};
    font-weight: 400;
  }
`;

interface IButtonColor {
  background: string;
  hover: string;
  text: string;
}

interface IButtonTheme {
  fontSize? :string
  color: IButtonColor
}

export const getButtonColor = (buttonColor?: ButtonColor): IButtonColor => {
  switch (buttonColor) {
    case ButtonColor.Red:
      return {
        background: color.red,
        hover: color.redLight,
        text: color.white,
      };
      case ButtonColor.LightGray:
        return {
          background: '#C4C4C430',
          hover: color.primary,
          text: color.text,
        };
    case ButtonColor.Gray:
    default:
      return {
        background: color.dark,
        hover: color.border,
        text: color.text,
      };
  }
};

export enum ButtonColor {
  Gray,
  LightGray,
  Red,
}
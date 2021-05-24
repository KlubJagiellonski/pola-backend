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
    background-color: ${color.button.disabled};
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
        background: color.button.red,
        hover: color.button.redLight,
        text: color.text.light,
      };
    case ButtonColor.White:
      return {
        background: color.button.white,
        hover: color.button.white,
        text: color.text.primary,
      };
    case ButtonColor.LightGray:
      return {
        background: color.button.lightGray,
        hover: color.button.white,
        text: color.text.primary,
      };
    case ButtonColor.Gray:
    default:
      return {
        background: color.button.gray,
        hover: color.button.disabled,
        text: color.text.primary,
      };
  }
};

export enum ButtonColor {
  Gray,
  LightGray,
  Red,
  White,
}
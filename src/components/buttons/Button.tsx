import styled from 'styled-components';
import { color, padding, px } from '../../styles/theme';

export interface IButtonColors {
  background: string;
  hover: string;
  text: string;
  border?: string;
}

export interface IButtonTheme {
  colors: IButtonColors;
  fontSize?: string;
  lowercase?: boolean;
  fontWeight?: 'lighter' | 'normal' | 'bold';
}

export type IButtonThemes = {
  [name in ButtonFlavor]: IButtonTheme;
};

export enum ButtonFlavor {
  GRAY = 'Gray',
  LIGHT_GRAY = 'LightGray',
  RED = 'Red',
  WHITE = 'White',
  WHITE_RED = 'WhiteRed',
}

export const ButtonThemes: IButtonThemes = {
  [ButtonFlavor.RED]: {
    colors: {
      background: color.button.red,
      hover: color.button.redLight,
      text: color.text.light,
    },
  },
  [ButtonFlavor.WHITE_RED]: {
    colors: {
      background: color.button.white,
      hover: color.button.white,
      text: color.text.red,
      border: color.button.red,
    },
  },
  [ButtonFlavor.WHITE]: {
    colors: {
      background: color.button.white,
      hover: color.button.white,
      text: color.text.primary,
    },
  },
  [ButtonFlavor.LIGHT_GRAY]: {
    colors: {
      background: color.button.lightGray,
      hover: color.background.lightGray,
      text: color.text.primary,
    },
  },
  [ButtonFlavor.GRAY]: {
    colors: {
      background: color.button.gray,
      hover: color.button.disabled,
      text: color.text.primary,
    },
  },
};

export const Button = styled.button<{ theme: IButtonTheme; disabled?: boolean }>`
  box-sizing: border-box;
  cursor: ${(props) => (props.disabled ? 'default' : 'pointer')};
  color: ${(props) => props.theme.colors.text};
  background-color: ${(props) => props.theme.colors.background};
  border-color: ${(props) => props.theme.colors.border || 'none'};
  border-width: ${(props) => (props.theme.colors.border ? '2px' : '0')};
  padding: ${padding.small} ${padding.normal};
  white-space: nowrap;
  font-weight: ${(props) => (props.theme.fontWeight ? props.theme.fontWeight : 'bold')};
  transition-duration: 0.5s;
  font-size: ${(props) => (props.theme.fontSize ? props.theme.fontSize : px(18))};

  p {
    margin: 0;
  }

  &:hover {
    background-color: ${(props) => props.theme.colors.hover};
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

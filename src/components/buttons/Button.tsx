import styled from 'styled-components';
import { color, padding } from '../../styles/theme';
import { IButtonColor } from '../../styles/button-theme';

export const Button = styled.button<{ theme: IButtonTheme; disabled?: boolean }>`
  box-sizing: border-box;
  cursor: ${(props) => (props.disabled ? 'default' : 'pointer')};
  color: ${(props) => props.theme.color.text};
  background-color: ${(props) => props.theme.color.background};
  border: none;
  padding: ${padding.small} ${padding.normal};
  white-space: nowrap;
  font-weight: bold;
  transition-duration: 0.5s;
  font-size: ${(props) => (props.theme.fontSize ? props.theme.fontSize : '18px')};

  &:hover {
    background-color: ${(props) => props.theme.color.hover};
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

export interface IButtonTheme {
  fontSize?: string;
  color: IButtonColor;
}

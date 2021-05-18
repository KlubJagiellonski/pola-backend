import React from 'react';
import styled from 'styled-components';
import { color, padding } from '../../styles/theme';

const Button = styled.button<{ theme: IButtonTheme }>`
  box-sizing: border-box;
  cursor: pointer;
  color: ${props => props.theme.color.text};
  background-color: ${props => props.theme.color.background};
  border: none;
  padding: ${padding.small} ${padding.normal};
  white-space: nowrap;
  font-weight: bold;
  transition-duration: 0.5s;

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

interface IButtonTheme {
  color: {
    background: string;
    hover: string;
    text: string;
  };
}

const getButtonColor = (buttonColor?: ButtonColor): IButtonTheme => {
  switch (buttonColor) {
    case ButtonColor.Red:
      return {
        color: {
          background: color.red,
          hover: color.redLight,
          text: color.white,
        },
      };
    case ButtonColor.Gray:
    default:
      return {
        color: {
          background: color.dark,
          hover: color.primary,
          text: color.text,
        },
      };
  }
};

export enum ButtonColor {
  Gray,
  Red,
}

export interface IPrimaryButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  color?: ButtonColor;
  className?: string;

  onClick?: () => void;
}

export const PrimaryButton: React.FC<IPrimaryButton> = ({ label, icon, className, disabled, color, onClick }) => {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    !disabled && onClick && onClick();
  };

  const theme = getButtonColor(color);

  return (
    <Button theme={theme} className={className} onClick={handleClick}>
      {icon}
      {label}
    </Button>
  );
};

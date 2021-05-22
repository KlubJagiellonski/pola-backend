import React from 'react';
import styled from 'styled-components';
import {ButtonColor, Button, getButtonColor} from './Button'

const SecButton = styled(Button)`
  border-radius: 20px;
`

export interface ISecondaryButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  color?: ButtonColor;
  fontSize?: string;
  className?: string;

  onClick?: () => void;
}

export const SecondaryButton: React.FC<ISecondaryButton> = ({ label, icon, className, disabled, color, fontSize, onClick }) => {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    !disabled && onClick && onClick();
  };

  const themeColor = getButtonColor(color);

  const theme = {
    color: themeColor,
    fontSize
  }

  return (
    <SecButton theme={theme} className={className} onClick={handleClick}>
      {icon}
      {label}
    </SecButton>
  );
};

import React from 'react';
import {ButtonColor, Button, getButtonColor} from './Button'

export interface IPrimaryButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  color?: ButtonColor;
  fontSize?: string;
  className?: string;

  onClick?: () => void;
}

export const PrimaryButton: React.FC<IPrimaryButton> = ({ label, icon, className, disabled, color, fontSize, onClick }) => {
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
    <Button theme={theme} className={className} onClick={handleClick}>
      {icon}
      {label}
    </Button>
  );
};

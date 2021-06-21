import React from 'react';
import { Button } from './Button';
import { ButtonColor, getButtonColor } from '../../styles/button-theme';

export interface IPrimaryButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  color?: ButtonColor;
  fontSize?: string;
  className?: string;
  children?: React.ReactNode;

  onClick?: () => void;
}

export const PrimaryButton: React.FC<IPrimaryButton> = ({
  label,
  icon,
  className,
  disabled,
  color = ButtonColor.Red,
  fontSize,
  onClick,
  children,
}) => {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    !disabled && onClick && onClick();
  };

  const themeColor = getButtonColor(color);

  const theme = {
    color: themeColor,
    fontSize,
  };

  return (
    <Button theme={theme} className={className} onClick={handleClick}>
      {icon}
      {label}
      {children}
    </Button>
  );
};

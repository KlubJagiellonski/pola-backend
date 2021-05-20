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
  className?: string;

  onClick?: () => void;
}

export const SecondaryButton: React.FC<ISecondaryButton> = ({ label, icon, className, disabled, color, onClick }) => {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    !disabled && onClick && onClick();
  };

  const theme = getButtonColor(color);

  return (
    <SecButton theme={theme} className={className} onClick={handleClick}>
      {icon}
      {label}
    </SecButton>
  );
};
